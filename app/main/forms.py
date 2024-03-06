from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

            
class ProjectForm(FlaskForm):
    title = TextAreaField('Say something', validators=[DataRequired()])
    lead_pi = TextAreaField('Say something', validators=[DataRequired()])
    description = TextAreaField('Say something', validators=[DataRequired()])
    grant_title = SelectField('Grant', choices=[('TRG', 'TRG')])
    starting_trl = SelectField('TRL', choices=[('TRL1', 'TRL-1'), ('TRL2', 'TRL-2'), 
                                               ('TRL3', 'TRL-3'), ('TRL4', 'TRL-4'), 
                                               ('TRL5', 'TRL-5'), ('TRL6', 'TRL-6'), 
                                               ('TRL7', 'TRL-7'), ('TRL8', 'TRL-8'),
                                               ('TRL9', 'TRL-9')])
    anticipated_ending_trl = SelectField('TRL', choices=[('TRL1', 'TRL-1'), ('TRL2', 'TRL-2'), 
                                               ('TRL3', 'TRL-3'), ('TRL4', 'TRL-4'), 
                                               ('TRL5', 'TRL-5'), ('TRL6', 'TRL-6'), 
                                               ('TRL7', 'TRL-7'), ('TRL8', 'TRL-8'),
                                               ('TRL9', 'TRL-9')])

    submit = SubmitField('Submit')
