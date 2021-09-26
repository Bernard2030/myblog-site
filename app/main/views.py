from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm, UpdateProfile
from .forms import PostForm, CommentForm, UpdateProfile
from ..models import Post, Comment, User, Upvote
from flask_login import login_required,current_user
from .. import db,photos
import markdown2  




# Views

@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data

    '''
   


   
    return render_template('index.html')

@main.route('/pitch')
@login_required
def post():
    Post = post.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('post_display.html', Post=Post, likes=likes, user=user)

@main.route('/new_Post', methods=['GET', 'POST'])
@login_required
def new_Post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        user_id = current_user._get_current_object().id
        Post_obj = Post(post=post, title=title,  user_id=user_id)
        Post_obj.save()
        return redirect(url_for('main.index'))
    return render_template('post.html', form=form)

@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    post = Post.query.get(id)
    user = User.query.all()
    comment = Comment.query.filter_by(post_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = id
        user_id = current_user.id
        new_comment = Comment(
            comment=comment,
            post_id=post_id,
            user_id=user_id
        )
        new_comment.save()
        new_comment = [new_comment]
        print(new_comment)
        return redirect(url_for('.comment', id =id))
    return render_template('comment.html', form=form, Post=Post, comment=comment, user=user)



@main.route('/user/<username>', methods = ['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user.id
        Post_obj = Post(pitch=pitch, title=title, category=category, user_id=user_id)
        Post_obj.save()

    return render_template("profile/profile.html", user = user, form = form)


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

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def upvote(id):
    Post = User.query.get(id)
    vote_new = Upvote(Post=Post, upvote=1)
    vote_new.save()
    return redirect(url_for('main.Posts'))








# @main.route('/dislike/<int:id>', methods=['GET', 'POST'])
# @login_required
# def downvote(id):
#     Pitch = User.query.get(id)
#     vote = Downvote(Pitch=Pitch, downvote=1)
#     vote.save()
#     return redirect(url_for('main.Pitchs'))
    





# # Views

# @main.route('/')
# @login_required
# def index():
#     posts = Post.query.all()

#     '''
#     View root page function that returns the index page and its data

#     '''
   


   
#     return render_template('index.html', user = current_user, posts = posts)


# @main.route('/create_post', method=['GET', 'POST'])
# @login_required
# def create_post():
#     if request.method == "POST":
#        text = request.form.get('text')
#     if not text:
#             flash("post cannot be empty", cateqory='error') 
#     else:
#                 Post = post(text = text, author = current_user.id)
#                 db.session.add(Post)
#                 db.session.commit()        
#                 flash("post created", category="success")
#                 return redirect(url_for('main.index'))




#     return render_template('create_post.html', user=current_user) 

# @main.route('delete-post/<id>')
# @login_required
# def delete_post(id):
#     post = Post.query.filter_by(id = id).first()

#     if not post:
#         flash("post does'nt exist", category='error')
#     elif current_user.id != post.id:
#             flash("You do not have permision to delete this post", category='error')
#     else:
#          db.session.delete(post)
#          db.session.commit()
#          flash("post deleted", category='success')

#          return redirect(url_for('main.index'))  


# @main.route('/posts/<username>')
# @login_required
# def posts(username):
#     user= User.query.filter_bu(username = username).first()

#     if not user:
#         flash("No user with that name exist", category='error')
#         return redirect(url_for('index.html'))

#     posts = user.posts
#     return render_template("posts.html", user = current_user, posts=posts, username = username)               
