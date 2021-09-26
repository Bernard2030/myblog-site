from enum import unique
from . import db 
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager





#...




class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique= True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='author', lazy=True)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')

    
   


    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    

     
    def __repr__(self):
        return f'User {self.username} Email:{self.email}, Image: {self.image_file}'

        

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))         


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy = "dynamic")


    def __repr__(self):
        return f'User {self.name}'


        # testing
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post = db.Column(db.String, nullable=False)
    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    up_vote = db.relationship('Upvote', backref='post', lazy='dynamic')
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"post Title: {self.title}, Date Posted: {self.date_created}, post Content: {self.content}"
        

   


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment = db.Column(db.Text())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}'    



class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def upvote(cls, id):
        upvote_post = Upvote(user=current_user, post_id=id)
        upvote_post.save()

    @classmethod
    def query_upvotes(cls, id):
        upvote = Upvote.query.filter_by(post_id=id).all()
        return upvote

    @classmethod
    def all_upvotes(cls):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
       





   


        
             




       


 






# from . import db 
# from datetime import datetime
# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin, current_user
# from . import login_manager
# from sqlalchemy import func, Date











# class User(UserMixin, db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String(128),index = True)
#     email = db.Column(db.String(128),unique = True,index = True)
#     password_hash = db.Column(db.String(128))
#     date_created = db.Column(db.TIMESTAMP(timezone = True), default = func.now())
#     posts = db.relationship('post', backref= 'user', passive_deletes=True)
    

    
   


#     @property
#     def password(self):
#         raise AttributeError('You cannnot read the password attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)


#     def verify_password(self,password):
#         return check_password_hash(self.password_hash,password)

#     # @staticmethod
#     # def get_user_by_username(username):
#     #     return User.query.filter_by(username=username).first()
    

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))  
            

#     def __repr__(self):
#         return f'User {self.username}'


# class Post(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     text = db.Column(db.text, nullable=False)
#     date_created = db.Column(db.TIMESTAMP(timezone = True), default = func.now())
#     author = db.Column(db.Integer, db.foreignKey('user.id', ondelete="CASCADE"), nullable=False) 

# class Comment(db.Model): 
#     id = db.Column(db.Integer,primary_key = True)
#     text = db.Column(db.text, nullable=False)
#     date_created = db.Column(db.TIMESTAMP(timezone = True), default = func.now())
#     author = db.Column(db.Integer, db.foreignKey('user.id', ondelete="CASCADE"), nullable=False) 
#     post_id = db.Column(db.Integer, db.Foreighnkey('post_id', ondelete = "CASCADE"), nullable=False)