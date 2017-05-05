#! /usr/bin/env python2.7
## Names:       Chris Giuffrida, Thomas Krill, Michael Farren, Pedro SauneroMariaca
## Class:       Data Structures CSE-20312
## Description: Create server to run on localhost:8888 for web client to connect to python scripts.

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from tornado import template
import CityEmotionAnalyzer
import RealTimeEmotionAnalyzer
import json


PORT = 8888
city_count = 0
query = ''

# Handle requests to the main page
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        global query
        query = self.get_argument('query', None)
        # Only get queries that are five words or less
        if query == None or len(query.split()) > 5:
            # Render the homepage if no query present
            self.render('../Website/homepage.html')
        else:
            # Initializr the twitter stream with the query
            RealTimeEmotionAnalyzer.initialize(query)
            # Render the results page with the given query
            self.render('../Website/results.html', query=query)

# Handle requests to the RealTimeEmotionalAnalyzer.py script
class RealTimeHandler(tornado.web.RequestHandler):

    def get(self):
        updated_data = RealTimeEmotionAnalyzer.getStreamData()
        print(json.dumps(updated_data))
        self.write(updated_data)

# Handle requests to the CityEmotionalAnalyzer.py script
class CityHandler(tornado.web.RequestHandler):

    def get(self):
        # Use a count to keep track of the city number that has been processed
        if city_count < 20:
            global city_count
            city_data = CityEmotionAnalyzer.getCityData(query, city_count)
            city_count += 1
            print city_data
            self.write(city_data)

# Create an application class than calls the correct handler for the given request
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler),\
        (r"/Website/(.*)", tornado.web.StaticFileHandler, {'path': r"../Website"}), \
        (r"/realtime", RealTimeHandler), \
        (r"/cities", CityHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)

# Main body of program
if __name__ == "__main__":

    # Instantiate an Application object and start the tornado server
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(PORT)

    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.current().start()
