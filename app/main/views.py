from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from .forms import ReviewForm, UpdateProfile
from .forms import Post_Form,PostForm, UpdateProfile
from ..models import Post, Comment, User, Upvote
from flask_login import login_required,current_user
from .. import db,photos
from app.requests import get_Quotes
import markdown2 
import os
import secrets


import app 




# Views

@main.route('/')
@login_required
def index():
    quotes = get_Quotes()
    posts = Post.query.all()
    

    return render_template('index.html', quotes = quotes, posts = posts, current_user = current_user)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)

    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    return picture_fn


# @main.route('/post')
# @login_required
# def post():
#     Post = post.query.all()
#     likes = Upvote.query.all()
#     user = current_user
#     return render_template('post_display.html', Post=Post, likes=likes, user=user)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = Post_Form()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('profile/profile.html', title='Profile', image_file=image_file, form=form)




    


@main.route('/user/<username>/update',methods = ['GET','POST'])
def update_profile(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',username = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<username>/update/pic',methods = ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username = username))




@main.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title='New Post',
                           form=form, legend='New Post')


@main.route("/post/<int:post_id>")
@login_required
def post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    print(comments)
    heading = 'comments'
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post, comments=comments, heading=heading)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.mypost', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title='Update Post',
                           form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))    

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def upvote(id):
    Post = User.query.get(id)
    vote_new = Upvote(Post=Post, upvote=1)
    vote_new.save()
    return redirect(url_for('main.Posts'))


@main.route('/comment/<post_id>', methods=['Post', 'GET'])
@login_required
def comment(post_id):
    comment = request.form.get('newcomment')
    new_comment = Comment(comment=comment, user_id=current_user._get_current_object().id, post_id=post_id)
    new_comment.save()
    return redirect(url_for('main.Posts', post_id=post_id))
