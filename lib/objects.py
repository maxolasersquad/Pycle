#!/usr/bin/evn python

#   This file is part of Git-Notifier.
#
#   Git-Notifier is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License.
#
#   Git-Notifier is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Pycle.  If not, see <http://www.gnu.org/licenses/>.

#import cx_Oracle
import MySQLdb

class MysqlObject(object):
    """Gets MySQL objects from the database"""
    import MySQLdb

    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.connect(host = host, user = user, passwd = password, db = db)

class OracleObject(object):
    """Gets Oracle objects from the database"""

    def __init__(self, con_string):
        self.connection = cx_Oracle.connect(con_string)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_object_types(self, schema):
        query = "\
SELECT DISTINCT(object_type)\
    FROM all_objects"
        if schema != '':
            query += "\
    WHERE owner = :q_schema"
        self.cursor.execute(query, q_schema=schema)
        return self.cursor.fetchall()

    def get_object(self, object_type, schema=''):
        query = "\
SELECT object_name\
    FROM all_objects\
    WHERE object_type = :q_object_type"
        if schema != '':
            query += "\
      AND owner = :q_schema \
            "
        query += "\
    ORDER BY object_name\
        "
        self.cursor.execute(query, q_schema=schema, q_object_type=object_type)
        return self.cursor.fetchall()

    def get_tables(self, schema=''):
        return self.get_object('TABLE', schema)

    def get_views(self, schema=''):
        return self.get_object('VIEW', schema)

    def get_indexes(self, schema=''):
        return self.get_object('INDEX', schema)

    def get_package_specs(self, schema=''):
        return self.get_object('PACKAGE', schema)

    def get_package_bodies(self, schema=''):
        return self.get_object('PACKAGE BODY', schema)

    def get_procedures(self, schema=''):
        return self.get_object('PROCEDURE', schema)

    def get_functions(self, schema=''):
        return self.get_object('FUNCTION', schema)
