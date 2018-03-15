#导入正在使用的Flask扩展
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config


#创建Flask扩展对象，但是不传入参数
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

#定义工厂函数
def create_app(config_name):
    #创建程序实例
    app = Flask(__name__)
    #使用from_object()方法导入配置，通过参数config_name选择导入的配置文件
    app.config.from_object(config[config_name])
    #初始化程序实例
    config[config_name].init_app(app)
    
    #初始化Flask扩展对象，也就是传入程序实例   
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    #使用蓝本附加路由和自定义错误页面，两步，1.从蓝本命名空间导入蓝本，2.将蓝本注册到程序上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #使用蓝本附加login实现认证功能
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app