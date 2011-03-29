#!/usr/bin/env python
# encoding: utf-8

metro_list = {
    2: { 'name': 'San Francisco, CA', 'lat': {'start': 37.72, 'end': 37.83}, 'lng': {'start': -122.51, 'end': -122.385} },
    0: { 'name': 'New York, NY', 'lat': {'start': 40.6, 'end': 40.8}, 'lng': {'start': -74, 'end': -73.85} },
    1: { 'name': 'Los Angeles, CA', 'lat': {'start': 34, 'end': 34.13}, 'lng': {'start': -118.5, 'end': -118.2} }, 
    3: { 'name': 'Chicago, IL', 'lat': {'start': 41.8, 'end': 41.99}, 'lng': {'start': -87.74, 'end': -87.6} },
    4: { 'name': 'San Diego, CA', 'lat': {'start': 32.68, 'end': 32.76}, 'lng': {'start': -117.255, 'end': -117.05} },
    #5: { 'name': 'Orange County, CA', 'lat': {'start': 33.5, 'end': 33.925}, 'lng': {'start': -118.1, 'end': -117.56} },
    #6: { 'name': 'East Bay, CA', 'lat': {'start': 37.72, 'end': 37.92}, 'lng': {'start': -122.34, 'end': -122.04} },
    7: { 'name': 'Seattle, WA', 'lat': {'start': 47.6475, 'end': 47.6}, 'lng': {'start': -122.27, 'end': -122.33} },
    8: { 'name': 'Boston, MA', 'lat': {'start': 42.347, 'end': 42.377}, 'lng': {'start': -71.02, 'end': -71.11} },
    9: { 'name': 'Portland, OR', 'lat': {'start': 45.5, 'end': 45.54}, 'lng': {'start': -122.7, 'end': -122.634} },
    10: { 'name': 'Washington D.C', 'lat': {'start': 38.87, 'end': 38.917}, 'lng': {'start': -77.06, 'end': -76.97} },
    11: { 'name': 'Las Vegas, NV', 'lat': {'start': 36.05, 'end': 36.158}, 'lng': {'start': -115.22, 'end': -115.07} },
    12: { 'name': 'Austin, TX', 'lat': {'start': 30.25, 'end': 30.3}, 'lng': {'start': -97.77, 'end': -97.7} },
    13: { 'name': 'Philadelphia, PA', 'lat': {'start': 39.92, 'end': 40}, 'lng': {'start': -75.22, 'end': -75.105} },
    14: { 'name': 'Denver, CO', 'lat': {'start': 39.71, 'end': 39.777}, 'lng': {'start': -105.02, 'end': -104.92} },
    15: { 'name': 'New Orleans, LA', 'lat': {'start': 29.92, 'end': 30.035}, 'lng': {'start': -90.12, 'end': -90} }
}



inv_metros_list = dict((v['name'],k) for k, v in metro_list.iteritems())
