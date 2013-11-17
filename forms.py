from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, SelectField, FileField 
#from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import Form
from models import *


 
class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
  


class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  phone = TextField('Phone Number', [validators.Required('Please enter your mobile number'),  validators.length(min=11, max=15)])
  country_id = SelectField(u'Country', choices=[('1', 'NG - Nigeria'), (('2', 'FO - Foreigner'))])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  confirm = PasswordField('Repeat Password', [validators.Required("Please re-enter your password to confirm"), validators.EqualTo('password', message='Passwords must match')])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True
      
class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    userpass = User.query.filter_by(pwdhash = self.password.data.lower()).first()
        
    if user and userpass:
      user = User.query.filter_by(email = self.email.data.lower()).one()
      userpass = User.query.filter_by(pwdhash = self.password.data.lower()).one()
      
      if user == userpass:
        return True
      else:
        self.email.errors.append("Invalid e-mail or password")
        return False
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
      


class WalletForm(Form):
  squestion = SelectField(u'Security Question', choices=[('What is the name of your first city', 'What is the name of your first city'), ('The Name of your Best Movie', 'The Name of your Best Movie'), ('The Name of your Best Book', 'The Name of your Best Book'), ('When You made your First Money', 'When You made your First Money')])
  sanswer = TextField("Security Answer",  [validators.Required("Please enter your security answer")])
  amount = TextField("Amount")
  submit = SubmitField("Create Wallet")
   
  
  

class PostForm(Form):
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  body = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  propics = FileField(u'Product Picture', [validators.Required("Please select a picture.")])
  submit = SubmitField("Comment")
   
