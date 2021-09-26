from flask_login import current_user
from app.models import Post
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Required
from app.models import User

class ReviewForm(FlaskForm):

    title = StringField('Review title',validators=[Required()])
    review = TextAreaField('Movie review')
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class Post_Form(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')    


class PostForm(FlaskForm):
      title = StringField('Title', validators=[DataRequired()])
      content = TextAreaField('Content', validators=[DataRequired()])
      submit = SubmitField('Post')



class CommentForm(FlaskForm):
      comment = TextAreaField('Comment', validators=[DataRequired()])
      submit = SubmitField('Post')


class Vote(FlaskForm):
    submit = SelectField('Like')  


