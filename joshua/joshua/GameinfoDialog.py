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

from gi.repository import Gtk # pylint: disable=E0611

from joshua_lib.helpers import get_builder

import locale
from locale import gettext as _
locale.textdomain('joshua')
from joshua.Game import Game

class GameinfoDialog(Gtk.Dialog):
    __gtype_name__ = "GameinfoDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated GameinfoDialog object.
        """
        builder = get_builder('GameinfoDialog')
        new_object = builder.get_object('gameinfo_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a GameinfoDialog object with it in order to
        finish initializing the start of the new GameinfoDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        pass
    
    def get_game_object(self):
        data = {
            'title':self.ui.title.get_text() or "No title", #Set value to "No title" if box is left empty
            'maker':self.ui.maker.get_text(),
            'year':self.ui.year.get_text(),
            'genre':self.ui.genre.get_text(),
            'path':self.ui.path.get_filename(),
            'thumbnail':self.ui.thumbnail.get_filename(),
            'platform':self.ui.platform.get_active_text()
        }
        return Game(data)
    
    def set_emulator_list(self, emulators):
        for item in emulators:
            self.ui.platform.append_text(item)
    
    def fill_from_game(self, game):
        self.ui.title.set_text(game.getTitle())
        self.ui.title.set_sensitive(False) #Lock it down, as it's the index
        #set platform to correct option
        
        def get_iter(model, data):
            #If the GTK devs would just implement a proper search function in TreeModel...
            i = model.get_iter_first()
            while i:
                if model.get_value(i, 0) == data:
                    return i
                i = model.iter_next(i)
                
        i = get_iter(self.ui.platform.get_model(), game.getPlatform())
        self.ui.platform.set_active_iter(i)
        self.ui.platform.set_sensitive(False) #Can't change this either, it's the page we're on
        self.ui.maker.set_text(game.getMaker())
        self.ui.genre.set_text(game.getGenre())
        self.ui.year.set_text(game.getYear())
        if game.getPath():
            self.ui.path.set_filename(game.getPath())
        if game.getThumbnail():
            self.ui.thumbnail.set_filename(game.getThumbnail())


if __name__ == "__main__":
    dialog = GameinfoDialog()
    dialog.show()
    Gtk.main()
