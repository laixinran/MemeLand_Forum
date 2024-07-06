from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate



app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# before_request 钩子函数hook，拦截器，拿出用户id，供视图函数使用
# 请求到达视图函数之前
# g: global
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

# 上下文处理器: 返回的数据在所有模版均可以被使用
@app.context_processor
def my_context_processor():
    return {'user': g.user}

if __name__ == '__main__':
    app.run()
