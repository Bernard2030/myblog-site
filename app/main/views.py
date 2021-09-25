from flask import render_template,request,redirect,url_for,flash, func
from . import main
from .forms import Post, post
from ..models import   User, Post
from flask_login import login_required,current_user
from .. import db, images
import markdown2 





# Views

@main.route('/')
@login_required
def index():
    posts = Post.query.all()

    '''
    View root page function that returns the index page and its data

    '''
   


   
    return render_template('index.html', user = current_user, posts = posts)


@main.route('/create_post', method=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
       text = request.form.get('text')
    if not text:
            flash("post cannot be empty", cateqory='error') 
    else:
                Post = post(text = text, author = current_user.id)
                db.session.add(Post)
                db.session.commit()        
                flash("post created", category="success")
                return redirect(url_for('main.index'))




    return render_template('create_post.html', user=current_user) 

@main.route('delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("post does'nt exist", category='error')
    elif current_user.id != post.id:
            flash("You do not have permision to delete this post", category='error')
    else:
         db.session.delete(post)
         db.session.commit()
         flash("post deleted", category='success')

         return redirect(url_for('main.index'))  


@main.route('/posts/<username>')
@login_required
def posts(username):
    user= User.query.filter_bu(username = username).first()

    if not user:
        flash("No user with that name exist", category='error')
        return redirect(url_for('index.html'))

    posts = Post.query.filter_by(username = username).all()
    return render_template("posts.html", user = current_user, posts=posts, username = username)               
