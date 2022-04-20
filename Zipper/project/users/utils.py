from PIL import Image
import os
from flask import current_app, url_for, render_template
from flask_mail import Message
import secrets
from project import mail,app
from threading import Thread

def pic_saver(file,username):
    filename = secrets.token_hex(4)+username+'.'+file.filename.split('.')[-1]
    saving_path = os.path.join(current_app.root_path,'static/profile_pics',filename)
    pic = Image.open(file)
    new_image = pic.resize((120,120))
    new_image.save(saving_path)
    return filename

email_data = {
        'email_confirmation' :{
                'link' : 'users.email_verification',
                'template' : 'email_confirm.html'
            },
        'password_reset' : {
                'link' : 'users.password_reset',
                'template' : 'password_reset_token.html'
            }
    }

def send_async_mail(msg):
    with app.app_context():
        mail.send(msg)


def send_mail(user, message_type):
    token = user.get_token()
    data = email_data[message_type]
    msg = Message(f'{message_type}',
            sender='########@gmail.com',
            recipients=[user.email])
    link = url_for(data['link'],token=token, _external=True)
    msg.html = render_template(data['template'], link=link)
    Thread(target=send_async_mail, args=(msg,)).start()
