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

import locale
from locale import gettext as _
locale.textdomain('joshua')

import os
import pickle

from gi.repository import Gtk, GdkPixbuf # pylint: disable=E0611
import logging
logger = logging.getLogger('joshua')

from joshua_lib import Window
from joshua.AboutJoshuaDialog import AboutJoshuaDialog
from joshua.GameinfoDialog import GameinfoDialog
from joshua.EnhancedNotebook import EnhancedNotebook
from joshua.JoshuaGridPage import GridPage
from joshua.Game import Game
from joshua.Emulator import Emulator

from quickly import prompts

# See joshua_lib.Window.py for more details about how this class works
class JoshuaWindow(Window):
    __gtype_name__ = "JoshuaWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JoshuaWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJoshuaDialog

        # Code for other initialization actions should be added here.
        
        self.ui.mnu_add.connect('activate', self.on_addButton_clicked)
        self.ui.mnu_edit.connect('activate', self.on_editButton_clicked)
        self.ui.mnu_remove.connect('activate', self.on_removeButton_clicked)
        self.ui.mnu_addEmulator.connect('activate', self.on_addEmulator_clicked)
        
        self.JOSHUA_DIR = os.path.expanduser("~/.config/joshua/")
        if not os.path.isdir(self.JOSHUA_DIR):
            logger.info("Creating config directory in ~/.config/joshua")
            os.mkdir(self.JOSHUA_DIR)
        
        if os.path.exists(self.JOSHUA_DIR + "games"):
            logger.info("Found games pickle")
            f = open(self.JOSHUA_DIR + "games")
            self.games = pickle.load(f)
            f.close()
        else:
            self.games = {}
        if os.path.exists(self.JOSHUA_DIR + "emulators"):
            logger.info("Found emulators pickle")
            f = open(self.JOSHUA_DIR + "emulators")
            self.emulators = pickle.load(f)
            f.close()
        else:
            self.emulators = {}
        self.pages = {}
        
        self.tabs = EnhancedNotebook({"Edit":self.edit_emulator, "Remove":self.remove_emulator})
        self.tabs.set_tab_pos(Gtk.PositionType.LEFT)
        self.ui.vbox1.add(self.tabs)
        self.ui.vbox1.reorder_child(self.tabs, 2)
        if self.emulators == {}:
            self.on_addEmulator_clicked() #Add new emulator on first run
        else:
            for emulator in self.emulators:
                logger.info("Adding emulator %s" % emulator)
                games = self._findGames(emulator)
                games.sort()
                page = GridPage(games)
                page.treeview.connect('row-activated', self.run_game)
                page.treeview.connect('cursor-changed', self.update_panel)
                self.pages[emulator] = page
                self.tabs.append_page(page, Gtk.Label(emulator))
        
        self.show_all()
    
    def _findGames(self, platform):
        return [game for game in self.games if self.games[game].getPlatform() == platform]
    
    def edit_emulator(self, menu, emulator, data=None):
        resp, command = prompts.string("Edit Emulator", "Command for %s emulator" % emulator, self.emulators[emulator].getCommand())
        if resp == Gtk.ResponseType.OK:
            logger.info("Updating emulator %s" % emulator)
            self.emulators[emulator].setCommand(command)
    
    def remove_emulator(self, menu, emulator, data=None):
        games = self._findGames(emulator)
        resp = prompts.warning("Warning", "This will remove %d games" % len(games)) if len(games) > 0 else Gtk.ResponseType.OK
        if resp == Gtk.ResponseType.OK:
            logger.info("Removing emulator %s" % emulator)
            self.tabs.remove_page(self.tabs.page_num(self.pages[emulator]))
            self.pages.pop(emulator)
            self.emulators.pop(emulator)
            #TODO: Remove games for platform?
    
    def on_destroy(self, *args):
        f = open(self.JOSHUA_DIR + "games", 'w')
        logger.info("Saving games...")
        pickle.dump(self.games, f)
        f.close()
        logger.info("Games saved")
        f = open(self.JOSHUA_DIR + "emulators", 'w')
        logger.info("Saving emulators...")
        pickle.dump(self.emulators, f)
        f.close()
        logger.info("Emulators saved")
        Gtk.main_quit()
    
    def run_game(self, *args):
        game = self.get_selected_game()
        self.emulators[game.getPlatform()].run(game)
    
    def update_panel(self, treeview, data=None):
        game = self.get_selected_game()
        if game:
            self.ui.gameTitle.set_text(game.getTitle())
            self.ui.gameMaker.set_text(game.getMaker())
            self.ui.gameYear.set_text(game.getYear())
            self.ui.gameGenre.set_text(game.getGenre())
            if game.getThumbnail() is not None:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(game.getThumbnail())
                self.ui.thumbnail.set_from_pixbuf(pixbuf.scale_simple(100, 75, GdkPixbuf.InterpType.BILINEAR))
            else:
                self.ui.thumbnail.set_from_file("")
    
    def on_addButton_clicked(self, *args):
        d = GameinfoDialog()
        d.set_emulator_list(self.emulators)
        resp = d.run()
        if resp == Gtk.ResponseType.OK:
            game = d.get_game_object()
            self.games[game.getTitle()] = game
            self.pages[game.getPlatform()].add_item(game.getTitle())
        d.destroy()
    
    def on_editButton_clicked(self, *args):
        game = self.get_selected_game()
        if game:
            d = GameinfoDialog()
            d.set_emulator_list(self.emulators)
            d.fill_from_game(game)
            resp = d.run()
            if resp == Gtk.ResponseType.OK:
                game = d.get_game_object()
                self.games[game.getTitle()] = game
            d.destroy()
    
    def on_removeButton_clicked(self, *args):
        game = self.get_selected_game()
        if game:
            self.games.pop(game.getTitle())
            self.pages[game.getPlatform()].remove_item(game.getTitle())
    
    def on_aboutButton_clicked(self, widget, data=None):
        d = self.AboutDialog()
        d.run()
        d.destroy()
        
    def on_addEmulator_clicked(self, *args):
        resp, name = prompts.string("Add Emulator", "Name of platform:")
        if resp == Gtk.ResponseType.OK and name not in self.emulators:
            resp2, command = prompts.string("Add Emulator", "Command for %s emulator" % name)
            if resp2 == Gtk.ResponseType.OK:
                logger.info("Adding emulator %s" % name)
                self.emulators[name] = Emulator(name, command)
                newPage = GridPage([])
                newPage.treeview.connect('row-activated', self.run_game)
                newPage.treeview.connect('cursor-changed', self.update_panel)
                self.pages[name] = newPage
                self.tabs.append_page(newPage, Gtk.Label(name))
    
    def get_selected_game(self):
        current_page = self.tabs.get_nth_page(self.tabs.get_current_page())
        try:
            sel, target = current_page.treeview.get_selection().get_selected()
        except:
            sel = target = None
        if target:
            title = sel.get_value(target, 0)
            return self.games[title]
        return None
    
    """Leaving this here for future reference.
    This function could be passed to the EnhancedNotebook constructor as the second argument
    to add a "New tab" button at the bottom. This would be called when that button is clicked.
    In this case, it turns out to be redundant with the toolbar item but it may be useful later.
    def add_emulator(self):
        resp, name = prompts.string("Add Emulator", "Name of platform:")
        if resp == Gtk.ResponseType.OK and name not in self.emulators:
            resp2, command = prompts.string("Add Emulator", "Command for %s emulator" % name)
            if resp2 == Gtk.ResponseType.OK:
                logger.info("Adding emulator %s" % name)
                self.emulators[name] = Emulator(name, command)
                newPage = GridPage([])
                newPage.treeview.connect('row-activated', self.run_game)
                newPage.treeview.connect('cursor-changed', self.update_panel)
                self.pages[name] = newPage
                return newPage, Gtk.Label(name)
        return None
    """
