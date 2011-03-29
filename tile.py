from gheatae import color_scheme, dot, tile, cache, provider
from gheatae.tile import Tile
from gheatae import consts
from os import environ
import logging
import time
import handler

log = logging.getLogger('tile')

tile.cache = cache.Cache()
tile.provider = provider.DBProvider()

class GetTile(handler.Handler):

  def get(self):
    log.info("Running GetTile:GET...")
    st = time.clock()
    path = environ['PATH_INFO']

    log.debug("Path:" + path)
    if path.endswith('.png'):
      raw = path[:-4] # strip extension
      try:
          assert raw.count('/') == 6, "%d /'s" % raw.count('/')
          foo, bar, layer, zoom, xy, category, metro = raw.split('/')
          assert xy.count(',') == 1, "%d /'s" % xy.count(',')
          x, y = xy.split(',')
          assert zoom.isdigit() and x.isdigit() and y.isdigit() and category.isdigit() and metro.isdigit(), "not digits"
          zoom = int(zoom)
          x = int(x)
          y = int(y)
          category = int(category)
          metro = int(metro)
          assert 0 <= zoom <= (consts.MAX_ZOOM - 1), "bad zoom: %d" % zoom
      except AssertionError, err:
          log.error(err.args[0])
          self.respondError(err)
          return
    else:
      self.respondError("Invalid path")
      return

    tile = Tile(layer, zoom, x, y, category, metro)
    log.info("Start-B1: %2.2f" % (time.clock() - st))

    self.response.headers['Content-Type'] = "image/png"
    #log.info("Building image...")
    img_data = tile.image_out()
    log.info("Start-B2: %2.2f" % (time.clock() - st))
    
    #log.info("Writing out image...")
    self.response.out.write(img_data)
    log.info("Start-End: %2.2f" % (time.clock() - st))
