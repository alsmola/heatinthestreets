#!/usr/bin/env python
# encoding: utf-8

category_list = {
        0: { 'name': 'Dive Bars', 'filter': 'divebars' },
        1: { 'name': 'Lounges', 'filter': 'lounges' },
        2: { 'name': 'Gay Bars', 'filter': 'gaybars' },
        3: { 'name': 'Hookah Bars', 'filter': 'hookah_bars' },
        4: { 'name': 'Pubs', 'filter': 'pubs' },
        5: { 'name': 'Sports Bars', 'filter': 'sportsbars' },
        6: { 'name': 'Wine Bars', 'filter': 'wine_bars' },
        7: { 'name': 'Dance Clubs', 'filter': 'danceclubs' },
        8: { 'name': 'Karaoke', 'filter': 'karaoke' },
        9: { 'name': 'Gastropubs', 'filter': 'gastropubs' },
        10: { 'name': 'Comedy Clubs', 'filter': 'comedyclubs' },
        11: { 'name': 'Music Venues', 'filter': 'musicvenues' },
        12: { 'name': 'Jazz & Blues', 'filter': 'jazzandblues' },
        13: { 'name': 'Adult Entertainment', filter:'adultentertainment' },
        14: { 'name': 'Champagne Bars', 'filter': 'champagne_bars' },
        15: { 'name': 'Breweries', 'filter': 'breweries'},
        16: { 'name': 'Pool Halls', 'filter': 'poolhalls'}
        
}

inv_category_list = dict((v['name'],k) for k, v in category_list.iteritems())
