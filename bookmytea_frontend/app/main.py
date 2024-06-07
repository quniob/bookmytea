from flask import Flask, render_template, redirect, url_for, session
import os
import rpc
from forms import RegisterForm, LoginForm
from functools import wraps
from uuid import uuid4

app = Flask(__name__, template_folder=os.path.relpath('../templates'))
app.config['SECRET_KEY'] = 'test'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        try:
            user_id = rpc.auth("verify_user", {"token": session['token']})
        except Exception as e:
            return redirect(url_for('login'))
        return f(user_id['user_id'], *args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'token' in session:
        return redirect(url_for('me'))
    if form.validate_on_submit():
        params = {
            "email": form.email.data,
            "password": form.password.data
        }
        try:
            token = rpc.auth('login_user', params)["token"]
        except Exception:
            return redirect(url_for('login'))
        session['token'] = token
        return redirect(url_for('me'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout(user_id: str):
    session.pop('token', None)
    return redirect(url_for('login'))


@app.route('/me')
@login_required
def me(user_id: str):
    return render_template('me.html', user=rpc.core_client('get_user', {"user_id": user_id}))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'token' in session:
        return redirect(url_for('me'))
    form = RegisterForm()
    if form.validate_on_submit():
        uuid = str(uuid4())
        params = {
            "email": form.email.data,
            "password": form.password.data,
            "uuid": uuid
        }
        try:
            token = rpc.auth('register_user', params)["token"]
        except Exception:
            return redirect(url_for('register'))
        user = {
            "email": form.email.data,
            "uuid": uuid
        }
        rpc.core_client("add_user", user)
        session['token'] = token
        return redirect(url_for('me'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
