"""
models.py

App Engine datastore models

"""
import datetime
from google.appengine.ext import db
from google.appengine.ext import webapp

class Article(db.Model):
  """Model for each article on sale"""
  #added_by = db.UserProperty() - find out how to use this.
  product_name = db.StringProperty(required=True)
  keywords = db.StringProperty(required=True, multiline=True)
  condition = db.StringProperty(required=True, choices=set(["like new", "very good", "some wear and tear", "needs fixing"]))
  date = db.DateTimeProperty(auto_now_add=True)
  picture_count = db.IntegerProperty()
  picture1 = db.BlobProperty(default=None)
  picture2 = db.BlobProperty(default=None)
  picture3 = db.BlobProperty(default=None)

class Transaction(db.Model):
  """Model for each transaction buy or rent that takes place."""
  user = db.UserProperty(required=True)
  product = db.StringProperty(required=True)
  action = db.StringProperty(required=True, choices=set(["buy", "rent"]))
  date = db.DateTimeProperty(auto_now_add=True)
  amount = db.FloatProperty()
  seller = db.UserProperty()
  seller_rating = db.IntegerProperty()

class UserRatings(db.Model):
  """Store all the ratings for a given user."""
  user = db.UserProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)
  rating = db.RatingProperty()
  action = db.StringProperty(choices=set(["buyer", "renter", "seller", "rent-owner"]))
  transaction_count = db.IntegerProperty() 
  seller_rating = db.FloatProperty()
  rating_issuer_id = db.UserProperty()
  buyer_rating = db.FloatProperty()
  renter_rating = db.FloatProperty()
  rent_owner_rating = db.FloatProperty()


# This is the test version of the Article model
# will start with just a picture and expand it from there
class ExampleArticle(db.Model):
  name = db.StringProperty(required=True)
  #message = db.StringProperty()
  picture = db.BlobProperty(default=None)
  timestamp = db.DateTimeProperty(auto_now_add=True)
