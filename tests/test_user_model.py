#单元测试
import unittest
import time
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    #创建测试环境，确保能在测试中使用current_app，生成一个全新的数据库以备不时之需
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    #删除创建的数据库的程序上下文
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #确保u.password_hash实例存在    
    def test_password_setter(self):
        u = User(password = '123456')
        self.assertTrue(u.password_hash is not None)

    #确保password是只写属性
    def test_no_password_getter(self):
        u = User(password = '123456')
        with self.assertRaises(AttributeError):
            u.password

    #测试verify函数
    def test_password_verification(self):
        u = User(password = '123456')
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('12345678'))

    #测试同一密码生成的不同序列是否一样（也就是看salts是不是随机的）
    def test_password_salts_are_random(self):
        u1 = User(password = '123456')
        u2 = User(password = '123456')
        self.assertFalse(u1.password_hash == u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='123456')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='123456')
        u2 = User(password='12345')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='123456')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='123456')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, '960101'))
        self.assertTrue(u.verify_password('960101'))

    def test_invalid_reset_token(self):
        u = User(password='123456')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'a', '960101'))
        self.assertTrue(u.verify_password('123456'))