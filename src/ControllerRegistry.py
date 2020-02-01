from src.controllers.HighscoreController import HighscoreController
from src.controllers.UsersController import UsersController
from src.controllers.IndexController import IndexController
'''
    Simple map/dict where (http-) controllers can register themselves to 
    handle different resources. Hardcoded paths for now.
'''


class ControllerRegistry:
    indexController = IndexController()
    mappings = dict([('users',  UsersController()), ('highscores', HighscoreController())])
    
    def registerController(self, resource, handler):
        ControllerRegistry.mappings[resource]=handler
    
    def getController(self, path):
        print('Looking up handler for path', path)
        handler = ControllerRegistry.indexController
        if path in ControllerRegistry.mappings.keys():
            print('We actually have a handler for', path, 'called', ControllerRegistry.mappings[path])
            handler = ControllerRegistry.mappings[path]
        else:
            print('No mapping found for', path, ', fallback to index controller')

        return handler

