import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen
from tornado.queues import Queue

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

from zope.interface import implementer

from concurrent.futures import ThreadPoolExecutor
from twisted.logger import (globalLogBeginner, Logger, jsonFileLogObserver,
                            ILogObserver, textFileLogObserver)

from tornado.concurrent import return_future
from tornado.concurrent import run_on_executor

import os, sys, time
import signal
import json
from datetime import timedelta
import datetime
import codecs
import numpy as np
import io
import importlib, inspect 
network = ''
initialized = False
actionQueue = Queue()
ourSecretPassword = "password"
ourSecretUsername = "guinness"
name = "digitRecognizer"
log = Logger()

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
	
	for sock in app.mainSockets:
			sock.write_message(u"Compiling your model.")
	try:
		mod = importlib.import_module(app.model)
		clsmembers = inspect.getmembers(mod, inspect.isclass)
		app.network = clsmembers[0][1]()
	except:
		for sock in app.mainSockets:
			sock.write_message(u"Error loading file.")
		print "Selected model, "+ app.model, ", not available."
		return
	app.times = []
	app.initialized = True
	for sock in app.mainSockets:
		sock.write_message(u"Model Compiled.")
	app.currentIterations = 0


@gen.coroutine
def train(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	starttime = time.time()
	app.train_err = app.network.train()
	dt = time.time() - starttime
	app.times.append(dt)
	validation()
	snapshot()
	app.iterationsToGo -=1
	app.currentIterations +=1
	for sock in app.mainSockets:
		sock.write_message(u"Epoch: " + str(app.currentIterations) + "\n<br>" + 
			"avg epoch time: " + str(sum(app.times) / float(len(app.times))) + "s\n<br>" +
			"predicted time left: " + str((sum(app.times) / float(len(app.times)))*app.iterationsToGo ) +"s\n<br>" + 
			"train err: " + str(app.train_err) + "\n <br>" + 
			"val acc: " + str(app.val_acc) + "\n <br>" + 
			app.snapshot)
	log.info("{value}",value="Train Error " + str(app.train_err))

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
		json.dump(savedParams, fp, separators=(',', ':'), sort_keys=True, indent=4)

	print "Backup complete."

@return_future
def load(callback=None):
	if app.initialized == False:
		print "network not yet initialized"
		return
	obj = codecs.open('./'+name+'/parameters.json', 'r', encoding='utf-8').read()
	jsonObj = json.loads(obj)
	temp = app.network.params
	for i in range(0, len(jsonObj)):
		app.network.params[i].set_value(np.float32(np.array(jsonObj[str(i)])))
	print "Load successful."

@return_future
def fileGrabber(callback=None):
	path_to_watch = "models/"
	app.models = [f for f in os.listdir (path_to_watch)]
	# print app.models


class Tasks():
	''' concurrent execution of functions '''
	executor = ThreadPoolExecutor(max_workers=4)

	@run_on_executor
	def futureCreator(self, func):
		result = func()
#############################
#
#	WebSockets
#
#############################

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("WebSocket opened")
		app.mainSockets.append(self)
		self.write_message(u"Snapshot socket connected")


	def on_message(self, message):
		self.write_message(u"Snapshot socket connected")

	def on_close(self):
		print("WebSocket closed")
		app.mainSockets.remove(self)


class ModelListHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("FileListener opened")
		app.modelSockets.append(self)
		# while 1:
			# time.sleep(5)
		fileGrabber()
		# print app.models
		if app.models != []:
			self.write_message(str(app.models))

	def on_message(self, message):
		pass

	def on_close(self):
		print("FileListener closed")
		app.modelSockets.remove(self)

class BuildLogSocketHandler(tornado.websocket.WebSocketHandler):
	''' Handle printing of the build log to the client '''
	def open(self):
		print("BuildLogSocket opened")
		app.buildSockets.append(self)
		for mess in app.logvar.getRecentLog(50):
			self.write_message(mess)

	def on_message(self, message):
		# wait wat
		pass

	def on_close(self):
		print("BuildLogSocket closed")
		app.buildSockets.remove(self)



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

class NotebookHandler(BaseHandler):
	def get(self):
		self.write(renderTemplate("notebook.html"))

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
			app.iterationsToGo +=1

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

class LoadParameterHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Loading selected network parameters..."
			starttime = time.time()
			yield actionQueue.put(load)
			self.write("time taken: " + str(time.time() - starttime))

class StopHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			print "Stopping Neural Network and Backing up"
			app.stopState = True

class ModelHandler(BaseHandler):
	@gen.coroutine
	def post(self):
		if self.current_user == ourSecretUsername:
			app.model = self.request.body.split('=')[1].split(".")[0]
			print app.model
			yield actionQueue.put(initNetwork)


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
				actionQueue.task_done()
				print "ding fries are done"
				break
			except gen.TimeoutError:
				print('tick')


@implementer(ILogObserver)
class LogCapture(object):
	def __init__(self, app):
		self.cache = []
		self.app = app
	def __call__(self, event):
		if 'log_io' in event:
			self.cache.append("<div class='event'><div class='content'>" 
				+ str(event['log_io']) + '\n</div></div>')
			for sock in self.app.buildSockets:
				sock.write_message(str(event['log_io']) + '\n<br>')


	def flush(self):
		self.cache = []
	def getLog(self):
		return self.cache
	def getRecentLog(self, num):
		temp = []
		if len(self.cache) > 0:
			temp = self.cache[-num: -1]
			temp.append(self.cache[-1])
		return temp



app = tornado.web.Application([
	(r"/", MainHandler),
	(r"/css/(.*)", tornado.web.StaticFileHandler,{'path': os.path.join(root, 'css')}),
	(r"/js/(.*)", tornado.web.StaticFileHandler,{'path': os.path.join(root, 'js')}),
	(r"/notebooks/(.*)", tornado.web.StaticFileHandler,{'path': os.path.join(root, 'notebooks')}),
	(r"/savedStates", SavedStatesHandler),
	(r"/buildLog", BuildLogHandler),
	(r"/notebook", NotebookHandler),
	(r"/load", LoadHandler),
	(r"/train", TrainHandler),
	(r"/stop", StopHandler),
	(r"/websocket", WebSocketHandler),
	(r"/modelList", ModelListHandler),
	(r"/buildSocket", BuildLogSocketHandler),
	(r"/saveParams", SaveParameterHandler),
	(r"/loadParams", LoadParameterHandler),
	(r"/snapshot", SnapshotHandler),
	(r"/login", LoginHandler),
	(r"/model", ModelHandler),
	(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
], autoreload=True, cookie_secret="fe444a5c-4edf-11e6-beb8-9e71128cae77", compiled_template_cache=False)
app.initialized = False
app.stopState = False
app.iterationsToGo = 0
app.snapshot = 'No Snapshot'
app.mainSockets = []
app.modelSockets = []
app.buildSockets = []
app.models = []
app.model = ""

app.logvar = LogCapture(app)
# log.startLogging(sys.stdout) # Print to actual console
# globalLogBeginner.beginLoggingTo([app.logvar], redirectStandardIO=True)
# log.startLogging(app.logvar)
log.info("wow")




@gen.coroutine
def main():
	# http_server = tornado.httpserver.HTTPServer(app, ssl_options={
	# 	"certfile": "ssl\certificate.crt",
	# 	"keyfile": "ssl\privatekey.key",
	# })	
	# http_server.listen(443)
	app.listen(80)
	tornado.ioloop.IOLoop.current().spawn_callback(consumer)
	# future = futureCreator(consumer)
	# gen.with_timeout(time.time() + 100, future)
	while True:
		print "Starting continuation loop"
		tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
	main()
