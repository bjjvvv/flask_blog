from datetime import datetime
from flask import render_template, current_app, session, redirect, url_for

from . import main
from app.email import send_email
from .forms import NameForm
from .. import db
from ..models import User

# 修饰器由蓝本提供
@main.route('/')
def index():
    return render_template('index.html')