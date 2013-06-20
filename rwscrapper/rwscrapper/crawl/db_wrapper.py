# -*- coding: utf-8 -*-

import re
import sqlalchemy

USER_NAME = 'scrapper'
USER_PASSWD = 'scrapper'
HOSTNAME = 'localhost'

class Db_Connector:
    """
    Handle database operations
    """
    def __init__(self, user_name, user_passwd, hostname):
        self.engine = \
        sqlalchemy.create_engine('mysql://{0}:{1}@{2}'.format(user_name, \
                                                              user_passwd, \
                                                              hostname));
        self.connection = self.engine.connect()

    def use_db(self, db_name):
        """
        Select new database
        """
        self.engine.execute("use {0}".format(db_name))


if __name__ == "__main__":
    conn = Db_Connector(USER_NAME, USER_PASSWD, HOSTNAME)
    conn.use_db('DEX')
