import tornado.ioloop
import tornado.web

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from twisted.python import log

import os, sys

root = os.path.join(os.path.dirname(__file__), ".")
lookup = TemplateLookup(directories=[os.path.join(root, 'views')], 
		input_encoding='utf-8',
		output_encoding='utf-8',
		default_filters=['decode.utf8'],
		module_directory=os.path.join(root, 'tmp/mako'))

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")
		#self.write(renderTemplate("myfile.html"))

def renderTemplate(templateName, **kwargs):
	template = lookup.get_template(templateName)
	args = []
	try: 
		return template.render(*args, **kwargs)
	except Exception, e:	
		print e

if __name__ == "__main__":

	log.startLogging(sys.stdout)

	app = tornado.web.Application([
		(r"/", MainHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	])

	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()