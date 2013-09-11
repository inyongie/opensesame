import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import uuid
import logging
import re
import json

#JSONification of Messages
def createJSONMsg(idval, typeval, message, source):
  retVal =  { "id" : idval, "type" : typeval , "message" : message , "source" : source }
  return json.dumps(retVal)
#json.loads is decoder

class WSHandler(tornado.websocket.WebSocketHandler):
  clients = {}

  def removeKey(d, key):
    r = dict(d)
    del r[key]
    return r

  def open(self):
    self.write_message("OpenSesame Server Initiated")
    self.id = uuid.uuid4()
    self.write_message("You are Client "+self.id.hex)
    for key in self.clients:
      self.clients[key].write_message("A new client has entered the server")
    self.clients[self.id.hex] = self
    print 'Connection '+self.id.hex+' was opened'
    logging.info('Connection '+self.id.hex+' was opened')

  def on_message(self, message):
    global target
    print 'Incoming message:', message
    logging.info('Incoming message:' +  message)

    # for identifying the raspi client
    targ_p = re.compile('iamtheraspi')
    targ_m = targ_p.match(message)
    if(targ_m):
      target = self
      print "Found the target, Client "+target.id.hex
      logging.info("Found the target, Client "+target.id.hex)

    for key in self.clients:
      if not target == None and self.clients[key].id.hex == target.id.hex:
	continue
      elif not target == None and self.id.hex == target.id.hex:
	continue
      else:
	self.clients[key].write_message(self.id.hex + " says: " + message)

    # if a message is sent by the target and it's not the initialization message, it's a
    # message acknowledgement message that contains the id of the client that sent the request
    ping_p = re.compile('raspiping')
    ping_m = ping_p.match(message)
    if (not target == None and not targ_m and self.id.hex == target.id.hex and not ping_m):
      logging.info('Client ' + self.id.hex + ' has achieved interaction with the Target')
      self.clients[message].write_message("The target has received your message")
    if (ping_m and self.id.hex == target.id.hex):
      self.clients[target.id.hex].write_message("Response ping from OpenSesame Server")

    # for identifying the open signal
    open_p = re.compile('open')
    open_m = open_p.match(message)
    if(open_m):
      target.write_message('Open Request:'+self.id.hex)

  def on_close(self):
    print 'Connection '+self.id.hex+' was closed...'
    logging.info('Connection '+self.id.hex+' was closed...')
    del self.clients[self.id.hex]
    for key in self.clients:
      self.clients[key].write_message("A client has left the server")

application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  global target
  target = None
  logging.basicConfig(filename='pysocketLog.log', filemode='w', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
