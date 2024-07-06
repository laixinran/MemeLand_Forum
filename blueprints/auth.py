from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("User not found")
                return redirect(url_for("auth.register"))
            if check_password_hash(user.password, password):

                # cookie: 不适合存储太多数据，只适合存储少量数据；一般用来存放登录授权的东西
                # session: flask中的session是经过加密后存在cookie中的
                session["user_id"] = user.id
                return redirect("/")

            else:
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            # 验证成功，将用户信息存储到数据库中
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login")) # 将视图函数转化成url
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 把cookie中的session信息清掉
@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get('email')

    # generate random verification code
    source = string.digits*4
    captcha = random.sample(source,4)

    s = ''.join(captcha)
    message = Message(subject="MemeLand Verification Code", recipients=[email], body=f"Your verification code is {s}")
    mail.send(message)

    # store verification code - use database
    email_captcha = EmailCaptchaModel(email=email, captcha=s)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="Test Message", recipients=["1716734606@qq.com"], body="testtest")
    mail.send(message)
    return "OK"





