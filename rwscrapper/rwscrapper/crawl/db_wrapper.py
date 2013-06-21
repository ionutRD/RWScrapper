# -*- coding: utf-8 -*-

from sqlalchemy import *

USER_NAME = 'scrapper'
USER_PASSWD = 'scrapper'
HOSTNAME = 'localhost'
DEX_DB = 'DEX'
RWSCRAPPER_DB = 'rwscrapper'

class DbManager(object):
    """
    Manage database connections
    """
    def __init__(user_name, user_passwd, hostname, db_name):
        """
        Create a database connection
        """
        self.user_name = user_name
        self.user_passwd = user_passwd
        self.hostname = hostname
        self.db_name = db_name
        self.db = create_engine('{0}:{1}@{2}/{3}'.\
                  format(user_name, user_passwd, hostname, db_name))
        self.metadata = BoundMetaData(db)

    def db_insert(table_name, values):
        """
        Insert values into a database
        """
        table_obj = Table(table_name, self.metadata, autoload = True)
        ins = table_obj.insert()
        ins.execute(values)

    
