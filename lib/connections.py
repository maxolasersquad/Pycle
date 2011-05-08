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

try:
    import gnomekeyring as gk
    keyring = 'gk'
except ImportError:
    try:
        import PyKDE4.kdeui.KWallet
        keyring = 'kk'
    except ImportError:
        import PyMacAdmin.Security.Keychain
        keyring = 'xk'
import glib
import objects

glib.set_application_name('gk_text')

if 'pycle' not in gk.list_keyring_names_sync():
    gk.create_sync('pycle', 'pyclepass')

class Connection(object):
    """A database connection"""

    def __init__(self, username, password, **params):
        if 'key' in params:
            self.key = params['key']
        else:
            self.key = None
        if 'sid' in params:
            self.sid = params['sid']
            self.name = username + '@' + self.sid
        elif 'host' in params:
            self.host = params['host']
            self.name = username + '@' + self.host
        else:
            print('Unable to create a connection without a host or sid')
            raise
        self.username = username
        self.password = password

    def save(self):
        if keyring == 'gk':
            try:
                gk.item_create_sync('pycle', gk.ITEM_GENERIC_SECRET, self.name, {'username': self.username, 'sid': self.sid}, self.password, True)
            except AttributeError:
                gk.item_create_sync('pycle', gk.ITEM_GENERIC_SECRET, self.name, {'username': self.username, 'host': self.host}, self.password, True)
        elif keyring == 'kk':
            pass
        elif keyring == 'xk':
            pass

    def delete(self):
        if keyring == 'gk':
            if self.key != None:
                gk.item_delete_sync('pycle', self.key)
        elif keyring == 'kk':
            pass
        elif keyring == 'xk':
            pass

    def connect(self):
        self.connection = objects.OracleObject(self.username, self.password, self.sid)
        #if self.sid != None:
        #    self.connection = objects.OracleObject(self.username + '/' + self.password + '@' + self.sid)
        #else:
        #    self.connection = objects.OracleObject(self.username + '/' + self.password + '@' + self.host)

def get_connections():
    connection_list = []
    keys = gk.list_item_ids_sync('pycle')
    for key in keys:
        item_info = gk.item_get_info_sync('pycle', key)
        attributes = gk.item_get_attributes_sync('pycle', key)
        if 'sid' in attributes:
            connection = Connection(attributes['username'], item_info.get_secret(), sid=attributes['sid'], key=key)
        else:
            connection = Connection(attributes['username'], item_info.get_secret(), host=attributes['host'], key=key)
        connection_list.append(connection)
    return connection_list

if __name__ == '__main__':
    test1 = Connection('suncom_query', 'suncom_query1', sid='nmsdev')
    test1.save()
<<<<<<< HEAD
    test2 = Connection('kim', 'kim_pass', sid='test')
    test2.save()
=======
    #create_connection('david', 'test', host='test_db')
>>>>>>> 976076119b63444a313864e29221b5fb8ec3e7c4
    for conn in get_connections():
        try:
            print(conn.key, conn.name, conn.username, conn.password, conn.host)
        except AttributeError:
            print(conn.key, conn.name, conn.username, conn.password, conn.sid)
        conn.connect()
        print conn.connection.get_object_types('OASIS_BILLING')
