import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.queues import Queue

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from twisted.python import log

import os, sys, time

network = ''
initialized = False
actionQueue = Queue()

root = os.path.join(os.path.dirname(__file__), ".")
lookup = TemplateLookup(directories=[os.path.join(root, 'views')],
		input_encoding='utf-8',
		output_encoding='utf-8',
		default_filters=['decode.utf8'],
		module_directory=os.path.join(root, 'tmp/mako'))


#############################
#
#	Network Functions
#
#############################

def initNetwork():
	from mnistManaged import MnistNetwork
	app.network = MnistNetwork()
	app.initialized = True

def train():
	if app.initialized == False:
		print "network not yet initialized"
		return
	app.network.train()

def validation():
	if app.initialized == False:
		print "network not yet initialized"
		return
	app.val_acc = app.network.val_acc()

def snapshot():
	if app.initialized == False:
		print "network not yet initialized"
		return
	print sys.getsizeof(app.network)
	app.snapshot = app.network.snapshot()


#############################
#
#	Request Endpoints
#
#############################

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("views/index.html")

class StartHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Initializing Neural Network"
		starttime = time.time()
		yield actionQueue.put(initNetwork)
		self.write("time taken: " + str(time.time() - starttime))


class TrainHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Training Neural Network"
		starttime = time.time()
		yield actionQueue.put(train)
		self.write("time taken: " + str(time.time() - starttime))

class SnapshotHandler(tornado.web.RequestHandler):
	def get(self):
		print "Getting a snapshot"
		print sys.getsizeof(app.network)
		print app.network
		self.write("Network Snapshot: " + str(app.snapshot))

class StopHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		print "Training Neural Network"
		starttime = time.time()
		yield actionQueue.put(train)
		self.write("time taken: " + str(time.time() - starttime))

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
		(r"/snapshot", SnapshotHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	], autoreload=True)

	app.initialized = False
	app.snapshot = 'No Snapshot'
	app.listen(8888)
	tornado.ioloop.IOLoop.current().spawn_callback(consumer)
	tornado.ioloop.IOLoop.current().start()
