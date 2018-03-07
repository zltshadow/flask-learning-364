from flask import Flask, render_template
#初始化，创建Flask类对象，也就是程序实例
app = Flask(__name__)

from flask.ext.bootstrap import Bootstrap
#从flask.ext命名空间导入Flask-Bootstrap，然后将程序实例传入构造方法进行初始化
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

if __name__=='__main__':
	app.run()