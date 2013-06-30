# -*- coding: utf-8 -*-
"""
Function used to process urls
"""
from urlparse import urlsplit, urlunsplit, parse_qsl
from urllib import urlencode
import urlnorm

SINGLE_LINE_COMMENT_TOKEN = '#'

def canonize_url(url):
    """
    Given a url return its normalized form
    """
    try:
        split = urlsplit(urlnorm.norm(url))
        path = split[2].split(' ')[0]

        while path.startswith('/..'):
            path = path[3:]

        while path.endswith('%20'):
            path = path[:-3]

        query_string = urlencode(sorted(parse_qsl(split.query)))
        return urlunsplit((split.scheme, split.netloc, path, query_string, ''))
    except urlnorm.InvalidUrl:
        return ''

def get_start_urls(file_name):
    """
    Return a list of start urls from a file
    """
    try:
        file_handle = open(file_name, 'r')
        start_urls = []
        for line in file_handle:
            if not line.startswith(SINGLE_LINE_COMMENT_TOKEN):
                crt_url = canonize_url(line.strip())
                if crt_url:
                    start_urls.append(crt_url)
        return start_urls
    except IOError:
        return []

def get_allowed_domains(file_name):
    """
    Return a list of allowed domains from a file
    """
    try:
        file_handle = open(file_name, 'r')
        allowed_domains = []
        for line in file_handle:
            if not line.startswith(SINGLE_LINE_COMMENT_TOKEN):
                allowed_domains.append(line.strip())
        return allowed_domains
    except IOError:
        return []

if __name__ == '__main__':
    print "TEST 1"
    URL = 'http://www.mategl.com'
    print 'URL: ', URL
    print 'NORMALIZED: ', canonize_url(URL)
    print '-----------------------------'

    print "TEST 2"
    URL = 'http://stackoverflow.com/questions/10912349/similar-code-detector'
    print 'URL: ', URL
    print 'NORMALIZED: ', canonize_url(URL)
    print '-----------------------------'

    print "TEST 3"
    URL = 'https://www.google.ro/#output=search&sclient=psy-ab&q=linux&oq=linux&gs_l=hp.3..35i39l2j0l8.2617.9060.1.9220.19.13.6.0.0.0.271.1728.7j4j2.13.0...0.0...1c.1.12.hp.YY8bWtsFFI0&psj=1&bav=on.2,or.r_cp.r_qf.&bvm=bv.46471029,d.Yms&fp=825bce13174d093c&biw=1280&bih=632'
    print 'URL: ', URL
    print 'NORMALIZED: ', canonize_url(URL)
    print '-----------------------------'

    print "TEST 4"
    URL = 'http://mategl.com'
    print 'URL: ', URL
    print 'NORMALIZED: ', canonize_url(URL)
    print '-----------------------------'

    print "TEST 5"
    URL = 'www.discovery.com'
    print 'URL: ', URL
    print 'NORMALIZED: ', canonize_url(URL)
    print '-----------------------------'

    print "TEST 6"
    start_seed_file = 'config/seed.txt'
    print get_start_urls(start_seed_file)

    print "TEST 7"
    allowed_domains = 'config/allowed_domains.txt'
    print get_allowed_domains(allowed_domains)
