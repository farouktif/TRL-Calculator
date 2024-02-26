from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

            
class ProjectForm(FlaskForm):
    title = TextAreaField('Say something', validators=[DataRequired()])
    description = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')
