from wtforms import Form, StringField, TextAreaField
from wtforms import FileField, StringField

class PostForm(Form):
    title = StringField('Title')
    image = FileField('Image')
    body = TextAreaField('Body')
