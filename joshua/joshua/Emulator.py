#!/usr/bin/env python
import os

class Emulator(object):
    """
    Represents an emulator.
    command: the shell command to run the emulator
    """

    def __init__(self, platform, command):
        self._platform = platform
        self._command = command
    
    def __str__(self):
        return "%s: %s" % (self._platform, self._command)
    
    def getCommand(self):
        return self._command
        
    def setCommand(self, command):
        self._command = command

    def run(self, game):
        """
        Runs the given game
        game must be a Game object
        """
        os.system('%s "%s"' % (self._command, game.getPath()))
