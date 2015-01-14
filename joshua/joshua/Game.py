#!/usr/bin/env python
class Game(object):
    """
    Holds all information related to the game
    """
    def __init__(self, data):
        """
        Create a game object.
        data is a dictionary of attributes.
        """
        self._title = data.get("title", "No title")
        self._path = data.get("path", None)
        self._platform = data.get("platform", None)
        self._thumbnail = data.get("thumbnail", None)
        self._maker = data.get("maker", "Unknown")
        self._year = data.get("year", "Unknown")
        self._genre = data.get("genre", "Unknown")
    
    def __str__(self):
        return self._title
    
    def getTitle(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
        
    def getPath(self):
        return self._path
    
    def setPath(self, path):
        self._path = path
    
    def getPlatform(self):
        return self._platform
    
    def setPlatform(self, platform):
        self._platform = platform
    
    def getThumbnail(self):
        return self._thumbnail
    
    def setThumbnail(self, thumbnail):
        self._thumbnail = thumbnail
    
    def getMaker(self):
        return self._maker
    
    def setMaker(self, maker):
        self._maker = maker
    
    def getGenre(self):
        return self._genre
    
    def setGenre(self, genre):
        self._genre = genre
    
    def getYear(self):
        return self._year
    
    def setYear(self, year):
        self._year = year
