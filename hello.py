import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread

#数据库文件地址
basedir = os.path.abspath(os.path.dirname(__file__))

#初始化程序实例
app = Flask(__name__)

#config字典，存储密钥（CSRF保护）,数据库URL，自动提交事务
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#设置发件人smtp服务器地址，端口，加密方式以及用户，密码
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = '1393609636@qq.com'
#app.config['MAIL_PASSWORD'] = '授权码'
#set MAIL_USERNAME=1393609636@qq.com(作用于当前cmd)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#设置Flask learning 邮件主题，发件人，发件邮箱（通过set命令，利用环境变量导入）
app.config['FLASKLEARNING_MAIL_SUBJECT_PREFIX'] = '[FLASKLEARNING]'
app.config['FLASKLEARNING_MAIL_SENDER'] = '1393609636@qq.com'
#app.config['FLASKLEARNING_ADMIN'] = 'zlt_shadow@163.com'
app.config['FLASKLEARNING_ADMIN'] = os.environ.get('FLASKLEARNING_ADMIN')

#将程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

#定义Role和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #Role与User模型的关系
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

#异步发送电子邮件邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_eamil(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKLEARNING_MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['FLASKLEARNING_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


#定义表单类，包含一个文本字段和一个提交按钮
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        #使用filter_by()查询过滤器从数据库中查找提交的名字
        user = User.query.filter_by(username=form.name.data).first()
        if user == None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKLEARNING_ADMIN']:
                send_eamil(app.config['FLASKLEARNING_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    #变量known被写入用户对话中，可以将数据传给模板，从而实现显示自定义的欢迎消息的功能
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

if __name__ == '__main__':
    app.run()