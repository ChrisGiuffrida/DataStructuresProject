#! /usr/bin/env python2.7

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

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        global query
        query = self.get_argument('query', None)
        if query == None:
            self.render('../Website/homepage.html')
        else:
            RealTimeEmotionAnalyzer.initialize(query)
            self.render('../Website/results.html', query=query)

class RealTimeHandler(tornado.web.RequestHandler):

    def get(self):
        updated_data = RealTimeEmotionAnalyzer.getStreamData()
        print(json.dumps(updated_data))
        self.write(updated_data)

class CityHandler(tornado.web.RequestHandler):

    def get(self):
        if city_count < 15:
            global city_count
            city_data = CityEmotionAnalyzer.getCityData(query, city_count)
            city_count += 1
            print city_data
            self.write(city_data)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler),\
        (r"/Website/(.*)", tornado.web.StaticFileHandler, {'path': r"../Website"}), \
        (r"/realtime", RealTimeHandler), \
        (r"/cities", CityHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":

    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(PORT)

    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.current().start()
