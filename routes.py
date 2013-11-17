from flask import Flask, render_template, request, flash, session, url_for, redirect, g, abort, send_from_directory
from forms import ContactForm, SignupForm, SigninForm, PostForm, WalletForm
from flask.ext.mail import Message, Mail
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
import psycopg2
from sqlalchemy import *
import os
from werkzeug import secure_filename
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from twilio.rest import TwilioRestClient
import twilio.twiml
from datetime import datetime
import time
from sms import *


UPLOAD_FOLDER = 'C:/Users/Princewill/Flaskapp/farmexport/app/static/img/productpics/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

mail = Mail()
 
app = Flask(__name__)
 
app.secret_key = "a_random_Transformer_secret_key_$%#!@"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trans:transformer@localhost/mydatabase'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'Transformingthings@gmail.com'
app.config["MAIL_PASSWORD"] = 'nonmenclature'
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/img/productpics/' #UPLOAD_FOLDER
mail.init_app(app)

from models import User

photos = UploadSet('photos', IMAGES)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



@app.route('/show')
def show_entries():
    form = PostForm()
    import psycopg2
    conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
    cur = conn.cursor()
    #cur2 = conn.cursor()    
    
    cur.execute("""select subject, simage, body, author, timestamp from posts order by uid desc""")
    rows = cur.fetchall()
    
    #cur2.execute("""select simage from stockimage order by picsid asc""")
    #rows2 = cur2.fetchall()
    
    entries = [dict(subject=row[0], simage=row[1], body=row[2], author=row[3], timestamp=row[4]) for row in rows]
    
    #picture = [dict(simage=row[0]) for row in rows2]
    
    #session['subject']= Post.query.order_by(Post.subject.desc())
    #session['body']=Post.query.order_by(Post.body.desc())
    
    return render_template('welcome.html', entries=entries, form=form)



@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))




@app.route('/')
def home():
  import psycopg2
  conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
  cur = conn.cursor()
  cur.execute("""select subject, simage, body, author, timestamp from posts order by uid desc""")
  rows = cur.fetchall()
  entries = [dict(subject=row[0], simage=row[1], body=row[2], author=row[3], timestamp=row[4]) for row in rows]
  return render_template('home.html', entries=entries)
  
@app.route('/about')
def about():
  return render_template('about.html')
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender=form.email.data, recipients=['Transformingthings@yahoo.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
   
  if 'email' in session:
    return redirect(url_for('welcome', form=form)) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      signin = User.query.filter_by(email = session['email']).first()
      if signin:
        signin = db_session.query(User.lastname).filter(User.email == session['email']).first()
        signfirst = db_session.query(User.firstname).filter(User.email == session['email']).first()
        signphone = db_session.query(User.phone).filter(User.email == session['email']).first()
        signcountry_id = db_session.query(User.country_id).filter(User.email == session['email']).first()
      session['lastname'] = signin
      session['firstname'] = signfirst
      session['phone'] = signphone
      session['country_id'] = signcountry_id
      
      
      if session['country_id'] == db_session.query(User.country_id).filter(User.country_id == 1).first():
        session['country_id'] = 'Nigerian'
      else:
        session['country_id'] = 'Foreigner'
      
      return redirect(url_for('welcome', form=form))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      g.newuser = User(form.firstname.data, form.lastname.data, form.phone.data, form.country_id.data, form.email.data, form.password.data)
      db_session.add(g.newuser)
      db_session.commit()
      
      session['lastname'] = g.newuser.lastname
      session['firstname'] = g.newuser.firstname
      session['phone'] = g.newuser.phone
      session['country_id'] = g.newuser.country_id
      if g.newuser.country_id == 1:
        session['country_id'] = 'Nigerian'
      else:
        session['country_id'] = 'Foreigner'
      session['email'] = g.newuser.email
      
      return redirect(url_for('wallet'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  
    
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')
    

@app.route('/welcome')
def welcome():
  form = PostForm()
  
  if request.method == 'POST':
    if form.validate() == False:
      
      return render_template('welcome.html', entries=entries)
    else:
      session['email'] = form.email.data
                          
  elif request.method == 'GET':
    import psycopg2
    conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
    cur = conn.cursor()
    cur.execute("""select subject, simage, body, author, timestamp from posts order by uid desc""")
    rows = cur.fetchall()
    
    entries = [dict(subject=row[0], simage=row[1], body=row[2], author=row[3], timestamp=row[4] )  for row in rows]
    return render_template('welcome.html', entries=entries, form=form)
  


@app.route('/add', methods=['POST'])
def add_entry():
    form = PostForm()
    file = request.files['propics']
    if 'email' not in session:
                   
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('welcome.html', form=form)
        else:
              
            g.post = db_session.query(User.id).filter(session['email'] == User.email).first()
            g.lastname = db_session.query(User.lastname).filter(session['email'] == User.email).first()
            g.firstname = db_session.query(User.firstname).filter(session['email'] == User.email).first()
            g.fullname = g.lastname + g.firstname  
                             
            
            file = request.files['propics']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #open(os.path.join(app.config['UPLOAD_FOLDER'], file), 'w').write(file)
                filename=filename
                
                                
                entries = Post(form.subject.data, filename, form.body.data, user_id=g.post, author=g.fullname)     
                #productimage = Image(form.body.data, filename)
                #db_session.add(productimage)
                db_session.add(entries)
                db_session.commit()
                flash('New entry was successfully posted')
            return redirect(url_for('show_entries'))

    return "It could go with the settings"

def show_pics():
    productpics = db_session.query(Image.simage).filter(Image.simage == Post.body).filter(session['email'] == User.email).first()
    if productpics:
        return send_from_directory(app.config['UPLOAD_FOLDER'], productpics)


        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
  form = WalletForm()
  
  if request.method== 'POST':
    if form.validate() == False:
      return render_template('wallet.html', form=form)
    else:
      g.wallet = User.query.filter_by(email = session['email']).first()
      if g.wallet:
        g.wallet = db_session.query(User.id).filter(User.email == session['email']).one()
        newuser = Wallet(g.wallet, form.squestion.data, form.sanswer.data, amount=1000.0)
        db_session.add(newuser)
        db_session.commit()
        session['squestion'] = newuser.squestion
        session['sanswer'] = newuser.sanswer
        session['amount'] = newuser.amount
     
      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('wallet.html', form=form)


  


@app.route('/contactuser')
def contactuser():
    
    
    querylast = db_session.query(User.lastname).filter(Post.user_id==User.id).filter(Post.author==User.lastname).first()
    queryfirst = db_session.query(User.firstname).filter(Post.user_id==User.id).first()
    queryphone = db_session.query(User.phone).filter(Post.user_id==User.id).first()
    querycountry_id = db_session.query(User.country_id).filter(Post.user_id==User.id).first()
    queryemail = db_session.query(User.email).filter(Post.user_id==User.id).first()
    
    if querylast:
        import psycopg2
        conn = psycopg2.connect("dbname='mydatabase' user='trans' host='localhost' password='transformer'")
        cur = conn.cursor()
        cur.execute("""select lastname, firstname, phone, email from signup """)
        rows = cur.fetchone()
        entries = [dict(lastname=row[0], firstname=row[1], phone=row[2], email=row[3]) for row in rows]
    return render_template('contactuser.html', entries=entries)



  
if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)
  

  
