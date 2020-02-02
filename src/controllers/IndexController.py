class IndexController:
    def handleGet(self, id=None):
        print('IndexController called')

        if id is None:
            return 404, dict([('Content-type','text/html')]), None

        body = '<html>' 
        body += "<h3>Welcome to simple server</h3>"
        body += "<br/>We are serving the following resources:"
        body += "<ul>"
        body += "<li><a href=\"users\">Users</a></li>"
        body += "<li><a href=\"highscores\">Highscores</a></li>"
        body += "</ul>"
        body += '</html>'
        return 200, dict([('Content-type','text/html')]), body

    
        
        