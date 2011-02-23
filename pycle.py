#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import sys
import gnomekeyring as gk

#import lib.objects
import lib.connections

class Pycle:

    glib.set_application_name('pycle')

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        #Setup the primary window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.window.set_border_width(10)
        self.window.set_title('Pycle 0.0')
        self.window.set_size_request(200, 600)

        #Setup the database objects
        #oracle_objects = lib.objects.OracleObject(sys.argv[1])
        connections = lib.connections.ConnectionList()

        #Setup the initial treeview
        self.treestore = gtk.TreeStore(str)
        for connection in connections.get_connections():
            treeleaf = self.treestore.append(None, [connection.name])
#        for object_type in oracle_objects.get_object_types(sys.argv[2]):
#            print object_type[0]
#            treeleaf = self.treestore.append(None, [object_type[0]])
#            if object_type[0] == "TABLE":
#                self.treestore.append(treeleaf, ['Boo!'])
#                print 'boo'
        self.treeview = gtk.TreeView(self.treestore)
        self.tvcolumn = gtk.TreeViewColumn('Connections')
        self.treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.treeview.set_search_column(0)
        self.tvcolumn.set_sort_column_id(0)
        self.treeview.set_reorderable(True)

        connection_box = gtk.VBox(False, 0)
        add_connection_button = gtk.Button(stock=gtk.STOCK_ADD)
        connection_box.pack_start(add_connection_button, False, False, 0)
        add_connection_button.show()
        connection_box.pack_start(self.treeview, False, False, 0)

        self.window.add(connection_box)
        self.window.show_all()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    pycle = Pycle()
    pycle.main()
