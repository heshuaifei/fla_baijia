from flask import Flask
from flask_script import Manager
from app.views import blue
from user.views import user


app = Flask(__name__)


app.register_blueprint(blueprint=blue, url_prefix='/app')
app.register_blueprint(blueprint=user, url_prefix='/user')

manager = Manager(app=app)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()  # python hello.py runserver -p 8080 -h 0.0.0.0 启动命令
