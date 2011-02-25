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


import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import lib.connections

class AddConnection:
    def __init__(self):
        self.gladefile = 'add_connection.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('main_window')
        self.username_entry = self.wTree.get_widget('username_entry')
        self.password_entry = self.wTree.get_widget('password_entry')
        self.sid_entry = self.wTree.get_widget('sid_entry')
        self.hostname_entry = self.wTree.get_widget('hostname_entry')
        self.port_entry = self.wTree.get_widget('port_entry')

        dic = {
            'on_cancel_button_clicked': self.cancel_button_clicked,
            'on_ok_button_clicked': self.ok_button_clicked,
            'destroy': gtk.main_quit
        }
        self.wTree.signal_autoconnect(dic)

        #self.window.connect('destroy', gtk.main_quit)
        self.window.show()

    def ok_button_clicked(self, widget):
        connection = lib.connections.ConnectionList()
        connection.create_connection(self.username_entry.get_text(), self.password_entry.get_text(), self.sid_entry.get_text(), self.hostname_entry.get_text(), self.port_entry.get_text())
        self.window.destroy()

    def cancel_button_clicked(self, widget):
        self.window.destroy()

if __name__ == "__main__":
    add_connection = AddConnection()
    gtk.main()
