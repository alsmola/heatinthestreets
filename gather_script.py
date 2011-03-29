#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import urllib2
import time
import metros
import categories
def main():
    for metro_index, metro in metros.metro_list.iteritems():
        total = 10000
        start = 0
        finish = 99
        while start < total:
            if (finish > total):
                finish = total
            url = 'http://localhost:8080/admin/gather/?start=%d&finish=%d&metro=%d' % (start, finish, metro_index)
            print url
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            total = int(res.read())
            start = start + 100
            finish = start + 99
            time.sleep(5)
    #url = 'http://localhost:8081/admin/generate'
    #print url
    #req = urllib2.Request(url)
    #res = urllib2.urlopen(req)    
if __name__ == '__main__':
    main()

