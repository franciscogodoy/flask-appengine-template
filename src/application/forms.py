"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""
"""
from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import ExampleModel
"""
from wtforms import Form
from flaskext.uploads import UploadSet, IMAGES
from wtforms import SelectField, TextField, BooleanField, PasswordField, FileField, validators
from wtforms.validators import Required
from flask_wtf.file import FileAllowed, FileRequired


images = UploadSet("images", IMAGES)

class LoginForm(Form):
  #username = TextField('Username', [validators.Length(min=4, max=25)])
  #name = TextField('Sellers Name', [validators.Length(min=6, max=35)])
  #email = TextField('Email Address', [validators.Length(min=6, max=35)])
  openid = TextField('openid', validators = [Required()])
  keywords = TextField('Related Keywords', [validators.Length(min=6, max=35)])
  #password = PasswordField('New Password', [
  #   validators.Required(),
  #   validators.EqualTo('confirm', message='Passwords must match')
  #])
  #confirm = PasswordField('Repeat Password')
  accept_tos = BooleanField('I accept the TOS', [validators.Required()])
  remember_me = BooleanField('remember_me', default = False)

class ImageUploadForm(Form):
  name = TextField("Picture Name", [validators.Length(min=4, max=25)])
  #picture = FileField("image", validators=[FileRequired(), FileAllowed(images, "Images Only!")])
  picture = FileField("image", validators=[validators.InputRequired(), FileAllowed(images, "Images Only!")])

class ProductUploadForm(Form):
  product_name = TextField("Product Name", [validators.Length(min=4, max=25)])
  keywords = TextField("Keywords", [validators.Length(min=4, max=25)])
  condition = SelectField("Product Condtion", choices=[("like new", "Like New"), ("very good", "Very Good"), ("some wear and tear", "Some Wear and Tear"), ("needs fixing", "Needs Fixing")])
  picture1 = FileField("image1", validators=[validators.InputRequired(), FileAllowed(images, "Images Only!")])
  picture2 = FileField("image2", validators=[FileAllowed(images, "Images Only!")])
  picture3 = FileField("image3", validators=[FileAllowed(images, "Images Only!")])

