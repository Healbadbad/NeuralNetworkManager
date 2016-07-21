import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.queues import LifoQueue

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from twisted.python import log

import os, sys, time

network = ''
initialized = False
actionQueue = LifoQueue()

root = os.path.join(os.path.dirname(__file__), ".")
lookup = TemplateLookup(directories=[os.path.join(root, 'views')],
		input_encoding='utf-8',
		output_encoding='utf-8',
		default_filters=['decode.utf8'],
		module_directory=os.path.join(root, 'tmp/mako'))

def initNetwork():
	from mnistManaged import MnistNetwork
	app.network = MnistNetwork()
	print app.network

	app.initialized = True
	# log. "WEEEWOOOO"

def train():
	if app.initialized == False:
		print "network not yet initialized"
		return
	app.network.train()
	print "Done yay"

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("views/index.html")

class StartHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Initializing Neural Network"
		starttime = time.time()
		yield actionQueue.put(initNetwork)
		print "wowe"

		# print self.application
		self.write("time taken: " + str(time.time() - starttime))

		# self.write("Hello, world")


class TrainHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Training Neural Network"
		starttime = time.time()
		yield actionQueue.put(train)
		self.write("time taken: " + str(time.time() - starttime))

		# self.write("Hello, world")

class StopHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Training Neural Network"
		starttime = time.time()
		yield actionQueue.put(train)
		self.write("time taken: " + str(time.time() - starttime))

		# self.write("Hello, world")

def renderTemplate(templateName, **kwargs):
	template = lookup.get_template(templateName)
	args = []
	try:
		return template.render(*args, **kwargs)
	except Exception, e:
		print e

@gen.coroutine
def consumer():
	while True:
		item = yield actionQueue.get()
		try:
			print 'Doing work on'
			item()
			yield gen.sleep(0.01)
		finally:
			actionQueue.task_done()


if __name__ == "__main__":

	log.startLogging(sys.stdout)

	app = tornado.web.Application([
		(r"/", MainHandler),
		(r"/css/(.*)", tornado.web.StaticFileHandler,{'path': os.path.join(root, 'css')}),
		(r"/js/(.*)", tornado.web.StaticFileHandler,{'path': os.path.join(root, 'js')}),
		(r"/start", StartHandler),
		(r"/train", TrainHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	], autoreload=True)

	app.initialized = False
	app.listen(8888)
	tornado.ioloop.IOLoop.current().spawn_callback(consumer)
	tornado.ioloop.IOLoop.current().start()
