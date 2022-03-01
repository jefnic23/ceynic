from flask_mail import Message
from threading import Thread
from flask import render_template
from app import mail, app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[TraceyNicholasArt] Reset your password',
        sender='info@traceynicholas.com',
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', token=token),
        html_body=render_template('email/reset_password.html', token=token))

def send_contact_email(form):
    send_email(f'[TraceyNicholasArt] Message from {form.name.data}',
        sender=(form.name.data, form.email.data),
        recipients=['info@traceynicholas.com'],
        text_body=render_template('email/contact_me.txt', msg=form.msg.data),
        html_body=render_template('email/contact_me.html', msg=form.msg.data))
