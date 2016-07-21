import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.queues import Queue

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from twisted.python import log

import os, sys, time
import signal
import json

network = ''
initialized = False
actionQueue = Queue()
ourSecretPassword = "password"
ourSecretUsername = "guinness"

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
	app.train_err = app.network.train()

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

# def save():



#############################
#
#	Request Endpoints
#
#############################

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
	def get(self):
		self.write(renderTemplate("main.html"))

class SavedStatesHandler(BaseHandler):
	def get(self):
		self.write(renderTemplate("savedStates.html"))

class BuildLogHandler(BaseHandler):
	def get(self):
		self.write(renderTemplate("buildLog.html"))
	def post(self):
		print self.request.body

class LoadHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Initializing Neural Network"
			starttime = time.time()
			yield actionQueue.put(initNetwork)
			self.write("time taken: " + str(time.time() - starttime))

class LoadHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Initializing Neural Network"
			starttime = time.time()
			yield actionQueue.put(initNetwork)
			self.write("time taken: " + str(time.time() - starttime))


class TrainHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Training Neural Network"
			starttime = time.time()
			yield actionQueue.put(train)
			self.write("time taken: " + str(time.time() - starttime))

class SnapshotHandler(BaseHandler):
	def get(self):
		if self.current_user == ourSecretUsername:
			print "Getting a snapshot"
			print sys.getsizeof(app.network)
			print app.network
			self.write("Network Snapshot: " + str(app.snapshot))

class StopHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Stopping Neural Network and Backing up"
			tornado.ioloop.IOLoop.current().set_blocking_signal_threshold(0.05, signal.CTRL_BREAK_EVENT)
		# tornado.ioloop.IOLoop.current().spawn_callback(tester)
		#TODO

def wowhandler():
	print "wow"

class LoginHandler(BaseHandler):
	def post(self):
		print self.request.body
		args = convertRequestArgs(self.request.body)

		print "Send the ajax login data here for verification"

		if args["password"] == ourSecretPassword:
			self.set_secure_cookie("user", ourSecretUsername)
			print "authenticated user"


def renderTemplate(templateName, **kwargs):
	template = lookup.get_template(templateName)
	args = []
	try:
		return template.render(*args, **kwargs)
	except Exception, e:
		print e

def convertRequestArgs(args):
	return json.loads(args)

@gen.coroutine
def tester():
	print "tester here"

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
		(r"/savedStates", SavedStatesHandler),
		(r"/buildLog", BuildLogHandler),
		(r"/load", LoadHandler),
		(r"/train", TrainHandler),
		(r"/stop", StopHandler),
		(r"/snapshot", SnapshotHandler),
		(r"/login", LoginHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	], autoreload=True, cookie_secret="fe444a5c-4edf-11e6-beb8-9e71128cae77")

	app.initialized = False
	app.snapshot = 'No Snapshot'
	app.listen(8888)
	tornado.ioloop.IOLoop.current().spawn_callback(consumer)
	tornado.ioloop.IOLoop.current().start()
