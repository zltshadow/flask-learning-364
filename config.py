import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #自动提交事务
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #主题，发件人，从环境变量导入管理员邮箱地址
    FLASKLEARNING_MAIL_SUBJECT_PREFIX = '[FLASKLEARNING]'
    FLASKLEARNING_MAIL_SENDER = 'FLASKLEARNING ADMIN <zlt_shadow@163.com>'
    FLASKLEARNING_ADMIN = os.environ.get('FLASKLEARNING_ADMIN')

    @staticmethod
    def init_app(app):
        pass

#开发环境配置类
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

#测试环境配置类
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

#生产环境配置类
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#生成配置对象
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}