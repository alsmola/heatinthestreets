from gheatae import color_scheme
from gheatae.dot import dot
from pngcanvas import PNGCanvas
from random import random, Random
from cache import Cache
import logging
import gmerc
import math
import os

log = logging.getLogger('space_level')

# This is the provider of data and interfaced to data interface
provider = None
cache = Cache()

rdm = Random()

LEVEL_MAX = 300

cache_levels = []

for i in range(LEVEL_MAX):
  cache_levels.append(int(((-(pow(float(i) - LEVEL_MAX, 2))/LEVEL_MAX) + LEVEL_MAX) / LEVEL_MAX * 255))

class Tile(object):
  
  def __init__(self, layer, zoom, x, y, category, metro):
    self.layer = layer
    self.zoom = zoom
    self.x = x
    self.y = y
    self.category = category
    self.metro = metro
    self.color_scheme = color_scheme.cyan_red
    self.decay = 0.0
    self.tile_img = None
    # attempt to get a cached object
    self.tile_dump = self.__get_cached_image()
    if not self.tile_dump:
        half_size = (zoom + 1) * 3 / 2
        self.georange = gmerc.px2ll(x * 256 - half_size, y * 256 - half_size, zoom)
        self.georange_next = gmerc.px2ll((x + 1) * 256 + half_size, (y + 1) * 256 + half_size, zoom)
        self.zoom_step = [ self.georange_next[0] - self.georange[0],
        self.georange_next[1] - self.georange[1]]
        # Get the points and start plotting data
        self.tile_img = self.plot_image(
        provider.get_data(self.zoom, self.layer, 
                            self.georange[0], self.georange[1], 
                            self.zoom_step[0], self.zoom_step[1], category, metro))
  
  def plot_image(self, points):
    space_level = self.__create_empty_space()
    for point in points:
      self.__merge_point_in_space(space_level, point) 
    return self.convert_image(space_level)
  
  def __merge_point_in_space(self, space_level, point):
    # By default, multiply per color point
    dot_levels, x_off, y_off = self.get_dot(point)
    half_size = (self.zoom + 1) * 3 / 2
    x_off -= half_size
    y_off -= half_size
    for y in range(y_off, y_off + len(dot_levels)):
      if y < 0 or y >= len(space_level):
        continue
      for x in range(x_off, x_off + len(dot_levels[0])):
        if x < 0 or x >= len(space_level[0]):
          continue
        dot_level = dot_levels[y_off - y][x_off - x]
        if dot_level <= 0.:
          continue
        space_level[y][x] += dot_level

  def convert_image(self, space_level):
    tile = PNGCanvas(len(space_level[0]), len(space_level), bgcolor=[0xff,0xff,0xff,0])
    color_scheme = []
    for i in range(LEVEL_MAX):
      color_scheme.append(self.color_scheme.canvas[cache_levels[i]][0])
    for y in xrange(len(space_level[0])):
      for x in xrange(len(space_level[0])):
        #log.error(space_level[y][x])
        tile.canvas[y][x] = color_scheme[min(LEVEL_MAX - 1, int(space_level[y][x]))]
    return tile

  def get_dot(self, point):
    cur_dot = dot[self.zoom]
    full_size = (self.zoom + 1) * 3
    y_off = int(math.ceil((-1 * self.georange[0] + point.location.lat) / self.zoom_step[0] * (256. + full_size) - len(cur_dot) / 2))
    x_off = int(math.ceil((-1 * self.georange[1] + point.location.lon) / self.zoom_step[1] * (256. + full_size) - len(cur_dot[0]) / 2))
    #log.info("lat, lng  dist_lng, dist_lng  Y_off, X_off: (%6.4f, %6.4f) (%6.4f, %6.4f) (%4d, %4d)" % (point.location.lat, point.location.lon,
    #                                                                                    (-1 * self.georange[0] + point.location.lat) / self.zoom_step[0] * 256, (-1 * self.georange[1] + point.location.lon) / self.zoom_step[1] * 256,
    #                                                                                    y_off, x_off))
    return cur_dot, x_off, y_off

  def __create_empty_space(self):
    space = []
    for i in range(256):
      space.append( [0.] * 256 )
    return space

  def __get_cached_image(self):
    return cache.get_image(self.zoom, self.x, self.y, self.category, self.metro)
  
  def __cache_image(self, tile_dump):
    return cache.store_image(self.zoom, self.x, self.y, self.category, self.metro, tile_dump)

  def image_out(self):
    if self.tile_img:
      self.tile_dump = self.tile_img.dump()
      self.__cache_image(self.tile_dump)

    if self.tile_dump:
      return self.tile_dump
    else:
      raise Exception("Failure in generation of image.")