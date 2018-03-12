from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#定义Role和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #Role与User模型的关系
    users = db.relationship('User', backref='role', lazy='dynamic')

    #返回一个具有可读性的字符串表示模型，可在调试和测试时使用
    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #为了创建迁移脚本，增加school字段
    school = db.Column(db.String(64), unique=True, index=True)
    #在User模型中加入密码散列
    password_hash = db.Column(db.String(128))
    #增加confirmed字段
    confirmed = db.Column(db.Boolean, default=False)

    #设置password为只写属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #password建立修饰器，生成pass_hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #验证密码散列函数
    def verify_password(self, password):
            return check_password_hash(self.password_hash, password)
    
    #生成一个有效期为3600秒的令牌，用于确认账户
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    #检验令牌，若检验通过，将comfirmed属性设为True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    #生成一个有效期为600秒的令牌，用于重设密码
    def generate_reset_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    #检验令牌，若检验通过，则开始重设密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

#用户回调函数，以user_id加载用户，若找到用户，则返回用户对象，否则返回None
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))