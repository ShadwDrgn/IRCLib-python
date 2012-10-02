import eventhook
import socket
import string
import thread
import time

class IRCLib:
 def __init__(self):
  self.onLine = eventhook.EventHook()
  self.onLine += self.hLine
  self.onMessage = eventhook.EventHook()
  self.onNotice = eventhook.EventHook()
  self.onConnect = eventhook.EventHook()

 def connect(self, nick, server, port):
  self.isConnected = True
  self.nick = nick
  self.s = socket.socket()
  self.s.connect((server, port))
  self.s.send("USER IRCLib na na :ShadwDrgn's IRCLib\n")
  self.s.send("NICK " + nick + "\n")
  data = ""
  self.th = thread.start_new_thread(self.readLoop, ())

 def readLoop(self):
  buffer = ""
  self.isConnected = True
  while True:
   data = self.s.recv(4098)
   buffer += data
   lines = string.split(buffer,"\n")
#   if buffer[buffer.__len__() - 1] != "\n":
#    buffer = lines.pop()
   for line in lines:
    self.onLine.fire(line)
   buffer = ""
  self.isConnected = False

 def hPrivmsg(self, msg):
  parts = msg.split()
  orig = parts[0].lstrip(":")
  dest = parts[2]
  if parts[3][0] == ':':
   parts[3] = parts[3][1:]
  content = " ".join(parts[3:])
  self.onMessage.fire(orig, dest, content)

 def hNotice(self, msg):
  parts = msg.split()
  orig = parts[0].lstrip(":")
  dest = parts[2]
  if parts[3][0] == ':':
   parts[3] = parts[3][1:]
  content = " ".join(parts[3:])
  self.onNotice.fire(orig, dest, content)

 def hCommand(self, cmd, msg):
  if cmd == 'PRIVMSG':
   self.hPrivmsg(msg)
  elif cmd == 'NOTICE':
   self.hNotice(msg)
  elif cmd == '001':
   self.onConnect.fire()

 def hLine(self, msg):
  mSplit = msg.split()
  if len(mSplit) == 0:
   return
  if mSplit[0] == "PING":
   self.s.send("PONG " + mSplit[1].lstrip(":") + "\n")
  else:
   if len(mSplit) > 1:
    self.hCommand(mSplit[1], msg)

 def sendMessage(self, t, m):
  self.s.send("PRIVMSG " + t + " :" + m + "\n")

#Example usage:
#def testshit(o, d, c):
# snick = o.split("!")[0]
# bot.sendMessage(snick, c)

#bot = IRCLib()
#bot.connect("IRCLib", "irc.esper.net", 6667)
#bot.onMessage += testshit
#while (bot.isConnected):
# continue
#print "pwnt"
