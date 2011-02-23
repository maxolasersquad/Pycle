#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class AddConnection:
    def __init__(self):
        self.gladefile = 'add_connection.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('main_window')
        self.window.show()

if __name__ == "__main__":
    add_connection = AddConnection()
    gtk.main()
