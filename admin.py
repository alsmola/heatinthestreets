#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from django.utils import simplejson as json
from google.appengine.api import urlfetch 
from gheatae.point import DataPoint
import urllib2
import oauth2
import logging
import time
import tile
import data
import datetime
import categories
import neighborhoods
import metros
import gmerc
import math
import gheatae.tile

yelp_apiv1_key = "piKGKH80o2c9pkXIsXaBmg"

consumer_key = "RPOw3zFwkJZlxyEWf-oozA"
consumer_secret = "zMOd-b6Pu4BGxlxkartDXJphbS8="
token = "nD8eT17aqYqnCrFSUeuRODR7JktmrwBu"
token_secret = "kUygrJkZkFoBbRIgqKYWyBc91Gg="

class ImageHandler(webapp.RequestHandler):
    def get(self):
        zoom = self.request.get('zoom')
        x = self.request.get('x')
        y = self.request.get('y')
        result = db.GqlQuery("SELECT * FROM TileImage WHERE zoom = :1 AND x = :2 AND y = :3 AND categories = :4 LIMIT 1" , zoom, x, y, categories).fetch(1)
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(result[0].picture)
        
class GenTilesHandler(webapp.RequestHandler):   
    def get(self):
        for metro_id, metro in metros.metro_list.items():
            s = metro['lat']['start'] - .1
            w = metro['lng']['start'] - .1
            n = metro['lat']['end'] + .1
            e = metro['lng']['end'] + .1       
            for zoom in [13, 14]:
                x1, y1 = gmerc.ll2px(n, w, zoom)
                x2, y2 = gmerc.ll2px(s, e, zoom)
                startx = int(math.ceil(x1 / 256.0))
                starty = int(math.ceil(y1 / 256.0))
                endx = int(math.ceil(x2 / 256.0))
                endy = int(math.ceil(y2 / 256.0))
                for x in [startx, endx]:
                    for y in [starty, endy]:
                        genTile(zoom, x, y, metro_id)
        self.response.out.write('Starting at: %d, %d, ending at: %d, %d for zoom: %d\n' % (startx, starty, endx, endy, zoom))
 
def genTile(zoom, x, y, metro_id):
    for key, value in categories.category_list.items():
        gheatae.tile.Tile(0, zoom, x, y, key, metro_id).image_out()


class DeleteHandler(webapp.RequestHandler):
    def get(self):
        if (self.request.get('points')):
            q = db.GqlQuery("SELECT * FROM DataPoint")
            results = q.fetch(10000)
            for result in results:
                result.delete()
        if (self.request.get('tiles')):
            q = db.GqlQuery("SELECT * FROM TileImage")
            results = q.fetch(1000)
            for result in results:
                result.delete()    

class GatherHandler(webapp.RequestHandler):
    def get(self):
        offset = int(self.request.get('start'))
        finish = int(self.request.get('finish'))
        metro_index = int(self.request.get('metro'))
#        category_index = int(self.request.get('category'))
        total = 0
        while (finish > offset):
            response = getBars(offset, metro_index) #, category_index)
            if 'total' in response:
                bars =  response['businesses']
                total = response['total']
            else:
                self.response.out.write(response)
                break
            for bar in bars:
                #bar_categories = map(lambda value:value[0], bar['categories'])       
                #if (not getCategory(category_index) in bar_categories):
                #    logging.info(bar['name'] + ':' + getMetro(metro_index) + ' is not a ' + getCategory(category_index))
                createPlace(bar, metro_index)
            offset += 20
            time.sleep(2)
        self.response.out.write(total)

def getBars(offset, metro_index):
    global token
    args = { 'location': getMetro(metro_index), 'category_filter': 'nightlife', 'limit': 20, 'offset': offset }
    url = 'http://api.yelp.com/v2/search?'
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, args)
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                           'oauth_timestamp': oauth2.generate_timestamp(),
                           'oauth_token': token,
                           'oauth_consumer_key': consumer_key})

    new_token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, new_token)
    signed_url = oauth_request.to_url()
    # logging.info('Signed URL: %s' % signed_url)
    # Connect
    try:
        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        response = json.loads(error.read())
    return response;
 
 
def createPlace(bar, metro_index):
    if  not 'neighborhoods' in bar['location'] or not 'categories' in bar:
        return   
    lat = bar['location']['coordinate']['latitude']
    lng = bar['location']['coordinate']['longitude']
    neighborhood = bar['location']['neighborhoods'][0]
    bar_categories = map(lambda value:value[0], bar['categories'])
    rating = determineRating(bar['rating_img_url'])
    weight = rating
    the_range = 5.

    if (not neighborhood in neighborhoods.inv_neighborhood_list):
        neighborhood_index = -1
        # logging.warn('Dumping neighborhood: %s' % neighborhood)
        # return
    else:
        neighborhood_index = neighborhoods.inv_neighborhood_list[neighborhood]
    for category in bar_categories:
        if (category in categories.inv_category_list):
            category_index = categories.inv_category_list[category]
            new_data = DataPoint(location=db.GeoPt(float(lat), float(lng)),
                        time=datetime.datetime.now(),
                        weight=weight,
                        range=the_range,
                        category = category_index,
                        neighborhood = neighborhood_index,
                        url = bar['url'],
                        rating = rating,
                        placeName = bar['name'],
                        metro = metro_index)
#            logging.info('Adding name: %s, category: %s, metro: %s' % (bar['name'], getCategory(category_index), getMetro(metro_index)))
            new_data.update_location()
            new_data.put()
 
def determineRating(url):
    if ('stars_5' in url):
        return 5.
    if ('stars_4_half' in url):
        return 4.5
    if ('stars_4' in url):
        return 4.
    if ('stars_3_half' in url):
        return 3.5
    if ('stars_3' in url):
        return 3.
    if ('stars_2_half' in url):
        return 2.5
    if ('stars_2' in url):
        return 2.
    if ('stars_1_half' in url):
        return 1.5
    if ('stars_1' in url):
        return 1.
    if ('stars_0' in url):
        return 0.

def getMetro(metro_index):
    return metros.metro_list[metro_index]['name']

def getCategoryFilter(category_index):
    return categories.category_list[category_index]['filter']

def getCategory(category_index):
    return categories.category_list[category_index]['name']


def main():
    application = webapp.WSGIApplication([ 
        ('/admin/generate/', GenTilesHandler),
        ('/admin/gather/', GatherHandler),
        ('/admin/delete/', DeleteHandler),
        ('/admin/image/', ImageHandler)])
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()


# How is the category filter supposed to work? When I look for all business in San Francisco, CA with category filter "lounges" and no search term, the response states there are 2426 results. However, there are actually only about 150 - most results after that are not in the lounge category. Is this expected behavior?How is the category filter supposed to work? When I look for all business in San Francisco, CA with category filter "lounges" and no search term, the response states there are 2426 results. However, there are actually only about 150 - most results after that are not in the lounge category. Is this expected behavior?