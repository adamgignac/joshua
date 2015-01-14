# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Adam Gignac <gignac.adam@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from gi.repository import Gtk

class GridPage(Gtk.ScrolledWindow):
    """
    A page in a gtk.Notebook containing a gtk.ListView
    in a gtk.ScrolledWindow
    """
    def __init__(self, dataList):
        """
        dataList is a list containing the entries
        to place in the grid
        """
        Gtk.ScrolledWindow.__init__(self)
        self.vbox = Gtk.VBox()
        self.add_with_viewport(self.vbox)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.store = Gtk.ListStore(str)
        for item in dataList:
            self.store.append([item])
        self.treeview = Gtk.TreeView(self.store)
        self.column = Gtk.TreeViewColumn("Game", Gtk.CellRendererText(), text=0)
        self.column.set_sort_column_id(0)
        self.treeview.append_column(self.column)
        self.vbox.add(self.treeview)
        
        self.show_all()
    
    def get_selected_val(self):
        """
        Returns the value from the currently selected cell
        Used for the edit and remove functions
        """
        sel, target = self.treeview.get_selection().get_selected()
        return sel.get_value(target, 0)
    
    def add_item(self, item):
        self.store.append((item,))
    
    def remove_item(self, item):
        #If the GTK devs would just implement a proper search function in TreeModel...
        i = self.store.get_iter_first()
        while i:
            if self.store.get_value(i, 0) == item:
                self.store.remove(i)
                return
            i = self.store.iter_next(i)
    
if __name__ == "__main__":
    w = Gtk.Window()
    w.set_default_size(400, 400)
    n = Gtk.Notebook()
    
    data = ['one', 'two', 'three']
    
    n.set_tab_pos(Gtk.PositionType.LEFT)
    w.add(n)
    page = GridPage(data)
    n.append_page(page, tab_label=Gtk.Label("Tab"))
    w.connect('destroy', lambda w:Gtk.main_quit())
    w.show_all()
    Gtk.main()
