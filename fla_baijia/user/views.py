
from flask import Blueprint, redirect, url_for, request, make_response, render_template


user = Blueprint('user', __name__)  # 参数一 蓝图别名


@user.route('/')
def hello_world():
    return 'xiyan 1111'


@user.route('/git_id/<id>/')
def git_id(id):
    return 'id: %s' % id


@user.route('/redirect')
def redirect_hello():
    # 实现跳转
    # return redirect('/user/')
    # 1. 硬编码URl
    # 2. 反向解析redirect(url_for('蓝图别名.跳转函数名'))
    # return redirect(url_for('user.hello_world'))
    return redirect(url_for('user.git_id', id=3))  # 函数有参数,直接在跳转的后面加参数即可


# 请求与相应
@user.route('/request/', methods=['GET', 'POST', 'PUT'])
def get_request():
    # 请求上下文 request
    # 获取GET请求传递的参数: request.args.get(key)/request.args.getlist(key)
    # 获取POST请求传递的参数: request.form.get(key)/request.form.getlist(key)
    # 判断请求方式: request.method

    pass


@user.route('/response/', methods=['GET'])
def get_response():
    # 创建响应
    res = make_response('lalalalalala', 200)
    # 响应绑定cookie, set_cookie(key, value, max_age, expirse)
    # 删除cookie delete_cookie

    res_index = render_template('index.html')
    res = make_response(res_index)
    return res


@user.route('/index/', methods=['GET'])
def index():
    # 返回一个页面
    return render_template('index.html')


@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 获取页面传递的参数
        username = request.form.get('username')
        password = request.form.get('password')
        # 验证用户和密码是否正确
        if username == 'xiyan' and password == '123456':
            return redirect(url_for('user.get_response'))

        else:
            return render_template('login.html')


