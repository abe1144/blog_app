from flask_wtf import FlaskForm
from wtforms import FileField, StringField


class newProject(FlaskForm):
    project_name = StringField('Project Name')
    image = FileField('Image')
    project_url = StringField('Project URL')
    info_url = StringField('Project Info URL')
