from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

            
class ProjectForm(FlaskForm):
    title = TextAreaField('Proposal Title', validators=[DataRequired()])
    lead_pi = TextAreaField('Lead PI', validators=[DataRequired()])
    description = TextAreaField('Proposal Description', validators=[DataRequired()])
    grant_title = SelectField('Grant Type', choices=[('TRG', 'TRG')], validators=[DataRequired()])
    starting_trl = SelectField('Starting TRL', choices=[('TRL1', 'TRL-1'), ('TRL2', 'TRL-2'), 
                                               ('TRL3', 'TRL-3'), ('TRL4', 'TRL-4'), 
                                               ('TRL5', 'TRL-5'), ('TRL6', 'TRL-6'), 
                                               ('TRL7', 'TRL-7'), ('TRL8', 'TRL-8'),
                                               ('TRL9', 'TRL-9')], validators=[DataRequired()])
    anticipated_ending_trl = SelectField('Anticipated Ending TRL', choices=[('TRL1', 'TRL-1'), ('TRL2', 'TRL-2'), 
                                               ('TRL3', 'TRL-3'), ('TRL4', 'TRL-4'), 
                                               ('TRL5', 'TRL-5'), ('TRL6', 'TRL-6'), 
                                               ('TRL7', 'TRL-7'), ('TRL8', 'TRL-8'),
                                               ('TRL9', 'TRL-9')], validators=[DataRequired()])

    submit = SubmitField('Submit')
