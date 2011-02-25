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

import gnomekeyring as gk
import glib

class Connection(object):
    """A database connection"""
    name = ''
    username = ''
    password = ''
    sid = ''
    hostname = ''
    port = ''

class ConnectionList(object):
    glib.set_application_name('gk_text')

    if 'pycle' not in gk.list_keyring_names_sync():
        gk.create_sync('pycle', 'pyclepass')

    def get_connections(self):
        connection_list = []
        keys = gk.list_item_ids_sync('pycle')
        for key in keys:
            connection = Connection()
            item_info = gk.item_get_info_sync('pycle', key)
            attributes = gk.item_get_attributes_sync('pycle', key)
            connection.name = item_info.get_display_name()
            connection.username = attributes['username']
            connection.password = item_info.get_secret()
            connection.sid = attributes['sid']
            connection.hostname = attributes['hostname']
            connection.port = attributes['port']
            connection_list.append(connection)
        return connection_list

    def create_connection(self, username='', password='', sid='', hostname='', port=''):
        attributes = {
            'username': username,
            'sid': sid,
            'hostname': hostname,
            'port': port
        }
        gk.item_create_sync('pycle', gk.ITEM_GENERIC_SECRET, username + '@' + sid + ' ' + hostname, attributes, password, True)

    def delete_connection(self, connection):
        items = gk.list_item_ids_sync('pycle')
        for item in items:
            if gk.item_get_info_sync('pycle', item).get_display_name() == connection.username + '@' + connection.sid + ' ' + connection.hostname:
                gk.item_delete_sync('pycle', item)

#foo = ConnectionList()
#foo.create_connection('baucumd', 'baucumpass', 'dev', '', '1532')
#connection = foo.get_connections()
