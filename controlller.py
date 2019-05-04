from flask import render_template, request, abort, redirect, url_for
from  flask_login import current_user, login_required,login_user, logout_user

import crud

from model import app,Customer,login_manager

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)

@app.route('/')
def home():
    return render_template('Shoptobd Login.html')



