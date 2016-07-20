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
actionQueue = LifoQueue()

root = os.path.join(os.path.dirname(__file__), ".")
lookup = TemplateLookup(directories=[os.path.join(root, 'views')], 
		input_encoding='utf-8',
		output_encoding='utf-8',
		default_filters=['decode.utf8'],
		module_directory=os.path.join(root, 'tmp/mako'))

def initNetwork():
	network = MnistNetwork()
	# log. "WEEEWOOOO"

def train():
	network.train()
	print "Done yay"

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")
		#self.write(renderTemplate("myfile.html"))
 
class StartHandler(tornado.web.RequestHandler): 
	@gen.coroutine
	def get(self):
		print "Initializing Neural Network"
		starttime = time.time() 
		from mnistManaged import MnistNetwork
		print initNetwork
		print actionQueue.qsize()
		yield actionQueue.put(initNetwork)
		print actionQueue.qsize()
		print "wowe"
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

def renderTemplate(templateName, **kwargs):
	template = lookup.get_template(templateName)
	args = []
	try: 
		return template.render(*args, **kwargs)
	except Exception, e:	
		print e

# @gen.coroutine
# def consumer():
# 	while True:
# 		item = yield actionQueue.get()
# 		try:
# 			print 'Doing work on'
# 			item()
# 			yield gen.sleep(0.01)
# 		finally:
# 			q.task_done()


if __name__ == "__main__":

	log.startLogging(sys.stdout)

	app = tornado.web.Application([
		(r"/", MainHandler),
		(r"/start", StartHandler),
		(r"/train", TrainHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	], autoreload=True)

	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
	# IOLoop.current().spawn_callback(consumer)
