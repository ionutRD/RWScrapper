# -*- coding: utf-8 -*-

import re
import sys
import time
from sqlalchemy import *
from sqlalchemy.orm import *

USER_NAME = 'scrapper'
USER_PASSWD = 'scrapper'
HOSTNAME = 'localhost'

DEX_DB = 'DEX'
RWSCRAPPER_DB = 'rwscrapper'

if __name__ == "__main__":
    db = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, RWSCRAPPER_DB))
    meta_dex = MetaData(db)
    words_tbl = Table('InflectedForms', meta_dex, autoload=True)
    stmt = select([words_tbl.c.form, words_tbl.c.noApp], (words_tbl.c.form == sys.argv[1]) | (words_tbl.c.formUtf8General == sys.argv[1]))
    rs = stmt.execute()
    l1 = []
    l2 = []
    for x in rs:
        l1.append(x[0])
        l2.append(x[1])
    print l1
    print l2
    #ins = words_tbl.insert(
    #    values=dict(url='www.google.com',\
    #                  canonicalUrl = 'www.google.com', \
    #                  contentFile = u'Ești aici? Ana are mere roșii.', \
    #                  trigramError = 3.2, \
    #                  bigramError = 1.4, \
    #                  unigramError = 0.455, \
    #                  freqError = 0.12345, \
    #                  averageWordLength = 4.33, \
    #                  romanianScore = 1.33, \
    #                  sourceType = 0, \
    #                  createDate = time.time())
    #)
    #result = db.execute(ins)
    #stmt = select([func.max(words_tbl.c.id)])
    #rs = stmt.execute()
    #print [x[0] for x in rs][0]

