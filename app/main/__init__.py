from flask import Blueprint

main = Blueprint('main', __name__) # 蓝本(名字，包名or模块名)

from . import views, errors