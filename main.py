from flask import Blueprint


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return 'Home Page'


@main.route('/version')
def version():
    return '1.0'
