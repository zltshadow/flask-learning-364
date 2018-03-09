from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


#异步发送电子邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKLEARNING_MAIL_SUBJECT_PREFIX'] +' ' + subject, 
                  sender = app.config['FLASKLEARNING_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    #开始异步发送电邮线程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr