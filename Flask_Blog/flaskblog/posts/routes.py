from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm


posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET', 'POST']) 
@login_required
def new_post(): 
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # 需要注意作者
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success' ) # 暂时先用这个对付下
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post', 
                           form = form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  
    # 通过id获取用 get()  见Part4    这是个get()的升级版，看名字就知道干嘛的  一会要写404页面的
    return render_template('post.html', title = 'Post', post = post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403)    # this 403 response is the HTTP response for a forbidden route 后面也会重写的
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() 
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', 
                           form = form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
