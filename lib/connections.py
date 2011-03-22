#!/usr/bin/env python

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

import gnomekeyring as gk
import glib
import objects

class Connection(object):
    """A database connection"""

    def __init__(self, attributes):
        self.attributes = attributes

    def connect(self):
        if database == 'oracle':
            connection = OracleObject(self.name + '/' + self.password + '@' + self.sid)
        elif database == 'mysql':
            connection = MysqlObject(self.hostname, self.user, self.password, database)

class ConnectionList(object):
    glib.set_application_name('gk_text')

    if 'pycle' not in gk.list_keyring_names_sync():
        gk.create_sync('pycle', 'pyclepass')

    def get_connections(self):
        connection_list = []
        keys = gk.list_item_ids_sync('pycle')
        for key in keys:
            #connection = Connection()
            item_info = gk.item_get_info_sync('pycle', key)
            attributes = gk.item_get_attributes_sync('pycle', key)
            attributes['name'] = item_info.get_display_name()
            connection = Connection(attributes)
            #connection.attributes = attributes
            connection_list.append(connection)
        return connection_list

    def create_connection(self, username, password, db_type, **params):
        attributes = {
            'username': username,
            'type': db_type
        }

        if attributes['type'] == 'oracle':
            connection_name = username + '@'
            if 'sid' in params or 'host' in params:
                if 'sid' in params and 'host' in params:
                    print 'Only a sid or a host may be specified for an oracle connection.'
                    raise
                if 'sid' in params:
                    connection_name += params['sid']
                else:
                    connection_name += params['host']
            else:
                print 'Either a sid or a host must be specified for an oracle connection.'
                raise

        elif attributes['type'] == 'mysql':
            if not 'host' in params:
                print 'A host must be specified for a mysql connection.'
                print params
                raise
            connection_name = username + '@' + params['host']

        for param in params:
            attributes[param] = params[param]
        gk.item_create_sync('pycle', gk.ITEM_GENERIC_SECRET, connection_name, attributes, password, True)

    def delete_connection(self, connection):
        items = gk.list_item_ids_sync('pycle')
        for item in items:
            if gk.item_get_info_sync('pycle', item).get_display_name() == connection.username + '@' + connection.sid + ' ' + connection.hostname:
                gk.item_delete_sync('pycle', item)

foo = ConnectionList()
#foo.create_connection('david', 'test', 'mysql', host='test_db')
for conn in foo.get_connections():
    print conn.attributes
