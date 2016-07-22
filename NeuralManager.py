import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.queues import Queue

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from concurrent.futures import ThreadPoolExecutor
from twisted.python import log
from tornado.concurrent import return_future
from tornado.concurrent import run_on_executor

import os, sys, time
import signal
import json
from datetime import timedelta
import time
network = ''
initialized = False
actionQueue = Queue()
ourSecretPassword = "password"
ourSecretUsername = "guinness"
name = "digitRecognizer"

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

@gen.coroutine
def initNetwork(callback=None):
	print "doing the thing"
	from mnistManaged import MnistNetwork
	app.network = MnistNetwork()
	app.initialized = True

@gen.coroutine
def train(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	app.train_err = app.network.train()

@gen.coroutine
def validation(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	app.val_acc = app.network.val_acc()

@gen.coroutine
def snapshot(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	print sys.getsizeof(app.network)
	app.snapshot = app.network.snapshot()

@gen.coroutine
def idle(callback=None):
	gen.sleep(0.01)


@return_future
def save(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	if not os.path.exists(name):
		os.makedirs(name)

	savedParams = {}
	for i in range(0, len(app.network.params)):
		savedParams[i] = app.network.params[i].get_value().tolist()

	with open('./'+name+'/parameters.json', 'w') as fp:
		json.dump(savedParams, fp)

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

# @return_future
# @gen.engine
class Tasks():
	executor = ThreadPoolExecutor(max_workers=4)

	@run_on_executor
	def futureCreator(self, func):
		result = func()
		# callback(result)
		# gen.Return(func())

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

class SaveParameterHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Saving current network parameters..."
			starttime = time.time()
			yield actionQueue.put(save)
			self.write("time taken: " + str(time.time() - starttime))

class StopHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Stopping Neural Network and Backing up"

			# tornado.ioloop.IOLoop.current().stop()
			# print "here?"
			app.stopState = True

			# tornado.ioloop.IOLoop.current().close()
			# tornado.ioloop.IOLoop.current().spawn_callback(consumer)
			# tornado.ioloop.IOLoop.current().start()
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
	runner = Tasks()
	while True:
		item = yield actionQueue.get()
		print item
		future = runner.futureCreator(item)
		while True:
			if app.stopState == True:
				for item in range(actionQueue.qsize()):
					actionQueue.get()
					actionQueue.task_done()
				future = runner.futureCreator(idle)
				print "queue supposedly emptied, ",actionQueue.qsize()
				app.stopState = False
				break

			try:
				result = yield gen.with_timeout(time.time() + 1, future)
				# print result
				actionQueue.task_done()
				print "ding fries are done"
				# yield gen.sleep(0.01)
				break
			except gen.TimeoutError:
				print('tick')




		# try:
		# 	print 'Doing work on'
		# 	item()
		# 	print "item completed"
		# 	yield gen.sleep(0.01)
		# finally:
		# 	actionQueue.task_done()

app = ''

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
	(r"/save", SaveParameterHandler),
	(r"/snapshot", SnapshotHandler),
	(r"/login", LoginHandler),
	(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
], autoreload=True, cookie_secret="fe444a5c-4edf-11e6-beb8-9e71128cae77")
app.initialized = False
app.stopState = False
app.snapshot = 'No Snapshot'


@gen.coroutine
def main():
	app.listen(8888)
	tornado.ioloop.IOLoop.current().spawn_callback(consumer)
	# future = futureCreator(consumer)
	# gen.with_timeout(time.time() + 100, future)
	while True:
		print "Starting continuation loop"
		tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
	main()
