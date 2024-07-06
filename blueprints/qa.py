from flask import Blueprint, request, render_template, g, redirect, url_for
from .forms import PostForm, CommentForm
from models import PostModel, CommentModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/") #根路径做前缀

@bp.route("/")
def index():
    posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    return render_template("index.html", posts=posts)

@bp.route("/qa/publish", methods=["GET", "POST"])
@login_required
def publish_question():
    if request.method == "GET":
        return render_template("publish_question.html")
    else:
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            post = PostModel(title=title, content=content, author=g.user)
            db.session.add(post)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.publish_question"))

@bp.route("/qa/detail/<post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    comments_count = len(post.comments)
    return render_template("detail.html", post=post, comments_count=comments_count)

@bp.route("/comment/publish", methods=["POST"])
@login_required
def publish_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        comment = CommentModel(content=content, post_id=post_id, author=g.user)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("qa.post_detail", post_id=post_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.post_detail", post_id=request.form.get("post_id")))


@bp.route("/search")
def search():
    p = request.args.get("p")
    if not p:
        posts = PostModel.query.all()
    else:
        posts = PostModel.query.filter(PostModel.title.contains(p)).all()
    return render_template("index.html", posts=posts)









