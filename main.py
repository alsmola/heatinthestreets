#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from django.utils import simplejson

import os
import categories
import metros
import tile
import data
import logging

class NeighborhoodsHandler(webapp.RequestHandler):
    def get(self):
        category = int(self.request.get('category_id'))
        result = get_neighborhood_stats(category)
        self.response.out.write(simplejson.dumps(result))

def get_neighborhood_stats(category):
    cache_result = memcache.get('category%d' % category)
    if (cache_result):
        logging.warn('Cache hit: category%d' % category)
        return cache_result
    logging.warn('Cache miss: category%d' % category)
    neighborhood_stats = []
    max_count = 0.
    for key, value in neighborhoods.neighborhood_list.items():
        query = db.GqlQuery("SELECT * FROM DataPoint WHERE neighborhood = :1 AND category = :2", key, category)
        count = 0.
        for record in query:
            count = count + 1
        if max_count < count:
            max_count = count
        if count > 0:
            neighborhood_stats.append([key, value, count])
    for stat in neighborhood_stats:
        stat[2] = stat[2] / max_count
    sorted_neighborhood_stats = sorted(neighborhood_stats, key=lambda neighborhood: neighborhood[2], reverse=True)
    sorted_neighborhood_stats
    store_neighborhood_stats(category, sorted_neighborhood_stats)
    return sorted_neighborhood_stats

def store_neighborhood_stats(category, neighborhood_stats):
    logging.warn('Cache store: category%d' % category)
    memcache.add('category%d' % category, neighborhood_stats)

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {'category_list':  categories.category_list, 'metro_list': metros.metro_list}))

def main():
    application = webapp.WSGIApplication([('/', MainHandler), 
        ('/neighborhoods/.*', NeighborhoodsHandler), 
        ('/tile/.*', tile.GetTile), 
        ('/data/.*', data.Data)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
