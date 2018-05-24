from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
''' From lotsofmenus.py '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session, connect it to DB

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # start html
                output = ""
                output += "<html><body>"
                output += "<h5><a href='/restaurants/new'>Crete New Restaurant</a></h3>"
                # add a list of all restaurants from restaurants table with links
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<h2>" + restaurant.name + "</h2>"
                    output += "<a href='/edit'>Edit</a>" + " " + "<a href='/delete'>Delete</a>"
                    output += "<br /><br /><br />"
                # close out the html file
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # start html
                output = ""
                output += "<html><body>"
                output += "<h2> Create New Restaurant </h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>Enter name:</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "<a href='/restaurants'>Go Back</a>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Create New Restaurant </h2>"
            output += "<h1> %s added</h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter name:</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "<a href='/restaurants'>Go Back</a>"
            output += "</body></html>"
            self.wfile.write(output)
            newrestaurant = Restaurant(name="%s" % messagecontent[0])
            session.add(newrestaurant)
            session.commit()
            print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()