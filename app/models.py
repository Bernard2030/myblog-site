from . import db 
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager
from sqlalchemy import func











class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(128),index = True)
    email = db.Column(db.String(128),unique = True,index = True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.Date(timezone = True), default = func.now())
    posts = db.relationship('post', backref= 'user', passive_deletes=True)
    

    
   


    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # @staticmethod
    # def get_user_by_username(username):
    #     return User.query.filter_by(username=username).first()
    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  
            

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.text, nullable=False)
    date_created = db.Column(db.Date(timezone = True), default = func.now())
    author = db.Column(db.Integer, db.foreignKey('user.id', ondelete="CASCADE"), nullable=False) 

class Comment(db.Model): 
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.text, nullable=False)
    date_created = db.Column(db.Date(timezone = True), default = func.now())
    author = db.Column(db.Integer, db.foreignKey('user.id', ondelete="CASCADE"), nullable=False) 
    post_id = db.Column(db.Integer, db.Foreighnkey('post_id', ondelete = "CASCADE"), nullable=False)