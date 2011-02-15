#!/usr/bin/python

import cx_Oracle

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

    def get_package_specs(self, schema='')
        return self.get_object('PACKAGE', schema)

    def get_package_bodies(self, schema='')
        return self.get_object('PACKAGE BODY', schema)

    def get_procedures(self, schema='')
        return self.get_object('PROCEDURE', schema)

    def get_functions(self, schema='')
        return self.get_object('FUNCTION', schema)
