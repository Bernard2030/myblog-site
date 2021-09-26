from app.models import Post
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

# class ReviewForm(FlaskForm):

#     title = StringField('Review title',validators=[Required()])
#     review = TextAreaField('Movie review')
#     submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    post = TextAreaField('Post', validators=[Required()])
    # category = SelectField('Category', choices=[('products', 'products'), ('interviews', 'interviews'), ('business', 'business')],
                        #    validators=[Required()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Post')


class Vote(FlaskForm):
    submit = SelectField('Like')  


