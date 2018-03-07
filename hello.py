from flask import Flask, render_template
#初始化，创建Flask类对象，也就是程序实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

from flask.ext.bootstrap import Bootstrap
#从flask.ext命名空间导入Flask-Bootstrap，然后将程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)

from flask_moment import Moment
#从flask_moment命名空间导入Flask-Moment，3.6.4版本用flask.ext会有警告，将程序实例传入构造方法进行初始化
moment = Moment(app)

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('submit')

from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template("index.html", form=form, name=name)

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__=='__main__':
	app.run()