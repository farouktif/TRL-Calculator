from flask import render_template, current_app
from app.email import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[TRL-Calculator] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
    

def send_password_reset_email_success(user):    
    send_email('[TRL-Calculator] Reset Your Password Success',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password_success.txt',
                                         user=user),
               html_body=render_template('email/reset_password_success.html',
                                         user=user))