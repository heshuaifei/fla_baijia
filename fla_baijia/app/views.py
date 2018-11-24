# from manage import app
from flask import Blueprint

blue = Blueprint('app', __name__)


@blue.route('/')
def gello_world():
    return 'Hello World 00000'


