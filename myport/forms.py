from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional, URL
from flask_wtf.file import FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Post')
