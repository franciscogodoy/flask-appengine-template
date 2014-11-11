"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users, urlfetch, images
from google.appengine.ext import db
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, Response, make_response

from flask_cache import Cache
#from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
from flask import send_from_directory

from application import app
from decorators import login_required, admin_required
from forms import LoginForm, ImageUploadForm, ProductUploadForm
from models import ExampleArticle, Article
#from models import ExampleModel
import os

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)
#images = UploadSet('images', IMAGES)
#configure_uploads(app, (images,))

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def buy():
  allproducts = getAllArticles()
  #allproducts = getPicture("mesa")
  #allproducts = [dict({"product_name": allproducts.product_name, "picture_count": allproducts.picture_count})]
  #return "%s" % allproducts[0].product_name
  return render_template("articles_test.html", allproducts=allproducts)

def rent():
  return render_template("articles_test.html")

def other_example():
  return redirect(url_for(''))

def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

def login():
  form = LoginForm(request.form)
  #if request.method == "POST" and form.validate_on_submit()
  # TODO still need to manage the submit part of the form
  return render_template("load_product.html", title="Load Product", form=form)

def allowed_file(filename):
  return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def photo(filename):
  """This function is used to test if an image was loaded."""
  # change so that it can upload multiple images. First test with one image
  # then go to multiple
  # may have to change Models database to have just link to images and not all in one Entity 
  picture = getPicture(filename)
  return render_template("show.html", filename=filename, ids=picture.picture_count)

def show(filename, ids=0):
  picture = getPicture(filename)
  if picture:
    response = None
    if int(ids) == 0 and picture.picture1:
      response = make_response(picture.picture1)
      response.headers["Content-Type"] = "image_jpeg"
    elif int(ids) == 1 and picture.picture2:
      response = make_response(picture.picture2)
      response.headers["Content-Type"] = "image_jpeg"
    elif picture.picture3:
      response = make_response(picture.picture3)
      response.headers["Content-Type"] = "image_jpeg"
    #return "this was saved %s" % picture.message
      #return Response(picture.picture, mimetype='image_jpeg')
    return response
  else:
    return None
  #return '<img src=' + url_for('static',filename= os.path.join('img',filename)) + '>'
    
def getPicture(articlename):
   # add memcache later to not do so many requests
  result = db.GqlQuery("SELECT * FROM Article WHERE product_name = :1 LIMIT 1",
                    articlename).fetch(1)
  if (len(result) > 0):
    return result[0]
  else:
    return None

def getAllArticles():
   # add memcache later to not do so many requests
  result = db.GqlQuery("SELECT product_name, picture_count FROM Article").run()
  return result
  resultlist = []
  for item in result:
    resultlist.append(item)
  return resultlist

def warmup():
  return ""

def upload_product():
  form = ProductUploadForm(request.form)
  if request.method == 'POST':
    picture_count = 0
    file1 = request.files["picture1"] # request.files is a dictionary with the name matching
                                    # the input name

    # only one picture is required the others can be skipped
    file2 = request.files["picture2"]
    file3 = request.files["picture3"]
    keywords = request.form["keywords"]
    product_name = request.form["product_name"]
    # email is temporary now. Later it will be replaced with open id or other method
    #condition = request.form["condition"]
    #return "%s" % (request.form.keys())
    if file1 and allowed_file(file1.filename):
      filename1 = secure_filename(file1.filename)
      # switching to Google Datastore model - previous way used to store files in server
      article = Article(product_name=product_name, keywords = keywords, condition="needs fixing")
      image1 = file1.getvalue()
      #imagerz1 = images.resize(image1, 1024, 768) # only on production
      imagerz1 = image1
      article.picture1 = db.Blob(imagerz1)
      picture_count += 1
      if file2 and allowed_file(file2.filename):
        image2 = file2.getvalue()
        #imagerz2 = images.resize(image2, 1024, 768) # only on production
        imagerz2 = image2
        article.picture2 = db.Blob(imagerz2)
        picture_count += 1
      if file3 and allowed_file(file3.filename):
        image3 = file3.getvalue()
        #imagerz3 = images.resize(image3, 1024, 768) # only on production
        imagerz3 = image3
        article.picture3 = db.Blob(imagerz3)
        picture_count += 1
      article.picture_count = picture_count
      article.put()
      #return "this are the values %s" % str(file_.keys())
      return redirect(url_for('buy'))
      #return render_template('show.html', filename=product_name)
  return render_template('upload_flask.html', form = form)

def test_upload():
  form = ImageUploadForm(request.form)
  #if request.method == "POST" and form.validate_on_submit():
  #if request.method == "POST" and form.validate(): #wtforms
  if request.method == "POST":
    #name = form.name.data
    #if form.validate():
    #  name = form.name.data
    #  image = form.picture.data
    file_ = request.files["picture"] # request.files is a dictionary with the name matching
    if file_ and allowed_file(file_.filename):
      name = request.form["name"]
      image = file_.getvalue()
      article = ExampleArticle(name=name)
      article.picture = db.Blob(image)
      article.put()
      return redirect(url_for('show', filename=name))
  return render_template('test_upload.html', form=form)
