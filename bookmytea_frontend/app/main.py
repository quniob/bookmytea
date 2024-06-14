from flask import Flask, render_template, redirect, url_for, session, jsonify, request, flash
import os
import app.rpc as rpc
from app.forms import RegisterForm, LoginForm, BookingForm
from functools import wraps
from uuid import uuid4
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__, template_folder=os.path.relpath('../templates'))
load_dotenv(find_dotenv())
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        try:
            auth_response = rpc.auth("verify_user", {"token": session['token']})
            user_id = auth_response['user_id']
            admin = auth_response['admin']
        except Exception as e:
            session.pop('token', None)
            flash("Сессия устарела либо вы не вошли в аккаунт", "error")
            return redirect(url_for('login'))
        return f(user_id, admin == 'true', *args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'token' in session:
        try:
            user_id = rpc.auth("verify_user", {"token": session['token']})
        except Exception as e:
            session.pop('token', None)
            flash("Сессия устарела либо вы не вошли в аккаунт", "error")
            return redirect(url_for('login'))
        return redirect(url_for('me'))
    if form.validate_on_submit():
        params = {
            "email": form.email.data,
            "password": form.password.data
        }
        try:
            token = rpc.auth('login_user', params)["token"]
        except Exception:
            flash("Неправильная почта или пароль", "error")
            return redirect(url_for('login'))
        session['token'] = token
        return redirect(url_for('me'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout(user_id: str, admin: bool):
    session.pop('token', None)
    return redirect(url_for('login'))


@app.route('/me')
@login_required
def me(user_id: str, admin: bool):
    telegram = rpc.core_client('check_telegram_user', {"user_id": user_id})
    if telegram == "False":
        telegram = False
    return render_template('me.html', user=rpc.core_client('get_user', {"user_id": user_id}), telegram=telegram)


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
            flash("Пользователь с такой почтой уже существует", "error")
            return redirect(url_for('register'))
        user = {
            "email": form.email.data,
            "uuid": uuid
        }
        rpc.core_client("add_user", user)
        session['token'] = token
        flash("Вы успешно зарегистрировались", "success")
        return redirect(url_for('me'))
    return render_template('register.html', form=form)


@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms(user_id: str, admin: bool):
    rooms = rpc.core_client('get_rooms', {})
    user = rpc.core_client('get_user', {"user_id": user_id})
    return render_template('rooms.html', user=user, rooms=rooms)


@app.route('/tables', methods=['POST', 'GET'])
@login_required
def tables(user_id: str, admin: bool):
    telegram = rpc.core_client('check_telegram_user', {"user_id": user_id})
    if telegram == "False":
        telegram = False
    if not telegram:
        flash("Пожалуйста, привяжите аккаунт Telegram для возможности бронировать столы", "error")
        return redirect(url_for('me'))
    room_id = request.args["room_id"]
    user = rpc.core_client('get_user', {"user_id": user_id})
    form = BookingForm()
    tables = []
    if form.validate_on_submit():
        date = form.date.data
        start_time = form.start_time.data
        duration = form.duration.data
        params = {
            "room_id": int(room_id),
            "date": date.strftime("%Y-%m-%d"),
            "start_time": start_time.strftime("%H:%M:%S"),
            "duration": int(duration)
        }
        tables = rpc.core_client('get_available_tables', params)
        return render_template('tables.html', user=user, tables=tables, form=form)
    return render_template('tables.html', user=user, form=form, tables=tables)


@app.route('/book', methods=['POST'])
@login_required
def book(user_id: str, admin: bool):
    telegram = rpc.core_client('check_telegram_user', {"user_id": user_id})
    if telegram == "False":
        telegram = False
    if not telegram:
        flash("Пожалуйста, привяжите аккаунт Telegram для возможности бронировать столы", "error")
    params = {
        "tables": [
            {
                "room_id": request.args["room_id"],
                "table_id": request.args["table_id"],
                "user_id": request.args["user_id"],
                "teaType": request.args["teaType"],
                "additionalInfo": request.args["additionalInfo"],
                "time": request.args["date"] + " " + request.args["time"],
                "duration": request.args["duration"]
            }
        ]
    }

    result = rpc.core_client('book_tables', params)
    if result[0]["result"]:
        flash("Успешно", "success")
        return redirect(url_for('me'))
    else:
        flash("Ошибка бронирования", "error")
        return redirect(url_for('me'))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
