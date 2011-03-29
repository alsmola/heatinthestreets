from google.appengine.api import memcache
from pngcanvas import PNGCanvas
import os.path
from google.appengine.ext import db
import logging

class Cache(object):
  
  def __init__(self):
      pass
   
  def get_image(self, zoom, x, y, category, metro):
      key = '%d/%d,%d/%d/%d' % (zoom, x, y, category, metro)
      image = memcache.get(key)
      if image is not None:
          logging.warn('Hit memcache: Z=%d, X=%d, Y=%d, C=%d, M=%d' % (zoom, x, y, category, metro))
          return image
      else:
          result = db.GqlQuery("SELECT * FROM TileImage WHERE zoom = :1 AND x = :2 AND y = :3 AND category = :4 AND metro = :5 LIMIT 1", zoom, x, y, category, metro).fetch(1)
          if (len(result) > 0):
              logging.warn('Hit dbcache: Z=%d, X=%d, Y=%d, C=%d, M=%d' % (zoom, x, y, category, metro))
              memcache.add(key, result[0].picture)
              return result[0].picture
          else:
              logging.warn('Miss: Z=%d, X=%d, Y=%d, C=%d, M=%d' % (zoom, x, y, category, metro))
              return None
  
  def store_image(self, zoom, x, y, category, metro, image_dump):
      img = TileImage()
      img.zoom = zoom
      img.x = x
      img.y = y
      img.category = category
      img.metro = metro
      img.picture = image_dump
      img.put()
      key = '%d/%d,%d/%d/%d' % (zoom, x, y, category, metro)
      memcache.add(key, image_dump)
      logging.warn('Caching: Z=%d, X=%d, Y=%d, C=%d, M=%d' % (zoom, x, y, category, metro))


class TileImage(db.Model):
    zoom = db.IntegerProperty()
    x = db.IntegerProperty()
    y = db.IntegerProperty()
    category = db.IntegerProperty()
    metro = db.IntegerProperty()
    picture = db.BlobProperty(default=None)
    