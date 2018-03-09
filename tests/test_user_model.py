#密码散列化测试
import unittest
from app.models import User

#保证u.password_hash实例存在
class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = '123456')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = '123456')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verify(self):
        u = User(password = '123456')
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('12345678'))

    def test_password_salts_are_random(self):
        u1 = User(password = '123456')
        u2 = User(password = '123456')
        self.assertFalse(u1.password_hash == u2.password_hash)