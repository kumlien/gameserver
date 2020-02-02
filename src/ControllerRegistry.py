from src.controllers.ScoreController import ScoreController
from src.controllers.UsersController import UsersController
from src.controllers.IndexController import IndexController
import logging
'''
    Simple map/dict where (http-) controllers can register themselves to 
    handle different resources. Hardcoded paths for now.
'''


class ControllerRegistry:
    indexController = IndexController()
    usersController = UsersController()
    scoreController = ScoreController(usersController)
    mappings = dict([
        ('login',  usersController), 
        ('score', scoreController),
        ('highscorelist', scoreController),
        ('', indexController)
    ])
    
    def registerController(self, resource, handler):
        ControllerRegistry.mappings[resource]=handler
    
    # Ok, this is somewhat backward. The controllers doesn't serve a 'root' resource in this 
    # scenario but instead they serve a 'tail' resource i.e. they are picked based on the last
    # element in the URL, not the first. 
    # GET /<userid>/login
    # POST /<levelid>/score?sessionkey=<sessionkey>
    # GET /<levelid>/highscorelist
    def getController(self, path):
        logging.info('Looking up handler for path %s', path)
        handler = ControllerRegistry.indexController
        if path in ControllerRegistry.mappings.keys():
            logging.info('We have a handler for %s called %s', path, str(ControllerRegistry.mappings[path]))
            handler = ControllerRegistry.mappings[path]

        return handler

