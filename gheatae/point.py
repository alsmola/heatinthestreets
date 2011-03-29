from geo.geomodel import GeoModel
from google.appengine.ext import db

class DataPoint(GeoModel):
  time = db.DateTimeProperty()
  weight = db.FloatProperty()
  range = db.FloatProperty()
  category = db.IntegerProperty()
  neighborhood = db.IntegerProperty()
  placeName = db.StringProperty()
  rating = db.FloatProperty()
  url = db.LinkProperty()
  metro = db.IntegerProperty()
