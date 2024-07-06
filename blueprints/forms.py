import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db


# 主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Invalid email')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='Captcha Invalid')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='Username Invalid')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password Invalid')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='Passwords do not match')])


    # 自定义验证：1. 邮箱是否已经被注册 2. 验证码是否正确
    def validate_email(self, field):
        user = UserModel.query.filter_by(email=field.data).first()
        if user:
            raise wtforms.ValidationError('Email already registered')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data

        # 根据两个条件进行查找
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError('Captcha invalid')
        else:
            db.session.delete(captcha_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Invalid email')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password Invalid')])

class PostForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message='Title Invalid')])
    content = wtforms.StringField(validators=[Length(min=3, max=500, message='Content Invalid')])

class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, max=500, message='Content Invalid')])
    post_id = wtforms.StringField(validators=[InputRequired(message='Post ID Invalid')])







