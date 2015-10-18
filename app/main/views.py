from flask import render_template
from . import main

# 修饰器由蓝本提供
@main.route('/')
def index():
    return render_template('index.html')
