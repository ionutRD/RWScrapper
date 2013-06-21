# -*- coding: utf-8 -*-

import re
import sys
from sqlalchemy import *

USER_NAME = 'scrapper'
USER_PASSWD = 'scrapper'
HOSTNAME = 'localhost'

DEX_DB = 'DEX'
RWSCRAPPER_DB = 'rwscrapper'

if __name__ == "__main__":
    db = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, DEX_DB))
    meta_dex = MetaData(db)
    update()
    inflected_form = Table('InflectedForm', meta_dex, autoload=True)
    stmt = select([inflected_form.c.formNoAccent], (inflected_form.c.formNoAccent == sys.argv[1]) | (inflected_form.c.formUtf8General == sys.argv[1]))
    rs = stmt.execute()
    for row in rs:
        print row
