class IndexController:
    def handleGet(self):
        print('IndexController called')
        body = '<html>' 
        body += "<h3>Welcome to simple server</h3>"
        body += "<br/>We are serving the following resources:"
        body += "<ul>"
        body += "<li><a href=\"users\">Users</a></li>"
        body += "<li><a href=\"highscores\">Highscores</a></li>"
        body += "</ul>"
        body += '</html>'
        return 200, dict([('Content-type','text/html')]), body
        