from flask import Flask, render_template, flash, request, send_file
from wtforms import Form, TextField, TextAreaField, RadioField, validators, StringField, SubmitField
import logging
import time
# import image
import db
import os
from flask import send_file
from flask_mail import Mail, Message
import threading
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.mail.yahoo.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'YOUR_EMAIL',
	MAIL_PASSWORD = 'YOUR_PASSWORD'
	)
mail = Mail(app)

ii = {1234:['prashantsengar5@gmail.com','abc@ptg.com']}

def get_my_ip():
    return request.remote_addr

def maill(sender, receiver, ip):
    try:
        msg = Message(f"{receiver} has opened the email",
          sender="prashantsgig@yahoo.com",
          recipients=[sender])
        msg.body = f"{receiver} opened the email just now from IP: {ip}\n\n'Sent by mTrack'"           
        mail.send(msg)
        app.logger.warning('Mail sent!')
    except Exception as e:
        app.logger.warning(e)

@app.route("/image", methods=["GET"])
def render_image():
    app.logger.warning('Called')
    mailID = int(request.args.get('type'))
    app.logger.warning(mailID)
    if mailID in ii:
        ip = get_my_ip()
        app.logger.warning(ip)
##        t=threading.Thread(target=maill, args=(ii[mailID][0], 'a',))
##        t.start()
        maill(ii[mailID][0], ii[mailID][1], ip)
    return send_file('pi.png', mimetype='image/gif')




def create_id():
    return str(int(time.time()%99999))


class ReusableForm(Form):
    def validate_amazon(form, field):
        logging.warning(field.data)
        
    sender = TextField('Sender\'s email:', validators=[validators.required()])
    receiver = TextField('Receiver\'s email:', validators=[validators.Email('Please enter a valid email address')])
    # url = TextField('URL:', validators=[validators.required(), validators.URL('Enter URL with http:// or https://'), validate_amazon])
    # label = RadioField('Label', choices=[('PayPal','PayPal'),('Amazon','Amazon Gift Card'),('ptm', 'PayTM')])

    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
        print (form.errors)
        if request.method == 'POST':
            sender=str(request.form['sender'])
            receiver=str(request.form['receiver'])
#             email=request.form['email']
#             choice = request.form['label']
#             print('-------')
#             print(str(choice))
#             print('------')
# ##            print (name, " ", email, " ", urll, choice)
    
            if form.validate():
            # Save the comment here.
                mail_id = create_id()
                flash('SUCCESS: Thanks for registration ')
                logging.warning(f'{sender}, {receiver}')
                
                flash(f'Paste this HTML code in the email: ')

                url = request.url_root
                html_code = f'<img src={url}image?type={mail_id}></img>'
                flash(f'{html_code}')
                db.write_data(sender, receiver, mail_id)
                ii[int(mail_id)]=[sender, receiver]
                app.logger.warning(ii)
                
            else:
                msg=''
                ers = form.errors
                for key in ers.keys():
                    for l in ers[key]:
                        msg+=l
                        msg+='. '
                print(msg)

                flash(f'Error: {msg}')

        
        return render_template('hello.html', form=form)

if __name__ == "__main__":
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='localhost', port=port)
    except:
        logging.exception('error')
