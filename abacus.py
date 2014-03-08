import socket
import time

Server = "irc.freenode.net"
Channel = "#OfficialWutang"
BotNick = "Abacus_"
BotPassword = "wrapper"
Password = "@#%2325!!"
IRCsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Ping():
	IRCsock.send("PONG :Pong\n")

def SendMsg(message):
	IRCsock.send("PRIVMSG " + Channel + " :" + message + "\n")

def SendUsrMsg(user, message):
	IRCsock.send("PRIVMSG " + user + " :" + message + "\n")

def JoinChan(chan, Pass):
	IRCsock.send("JOIN " + chan + " " + Pass + "\n")

class Count:
	def __init__(self):
		self.btctotal=0.0
		self.starttime=time.time()
		SendMsg("Get ready to count our bitcoin! Reply with !btc plus the number you hold")
	
	def add(self, btc, username):
		self.btctotal+=btc
		SendMsg(username + " added " + str(btc) + " btc")
	def final(self):
		SendMsg("Count is over! Total bitcoin: " + str(self.btctotal))
	
IRCsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRCsock.connect((Server, 6667))
IRCsock.send("USER " + BotNick + " " + BotNick + " " + BotNick + " :This bot is a bot\n")
IRCsock.send("NICK " + BotNick + "\n")
SendUsrMsg("NickServ", "identify " + BotPassword)

IRCsock.send("JOIN " + Channel + " " + Password + "\n")
x = None
while True:
	IRCmsg = IRCsock.recv(2048)
	IRCmsg = IRCmsg.strip("\n\r")

	username = (((IRCmsg.split())[0])[1:]).split("!", 1)[0]

	if (IRCmsg.find(":!COUNT") != -1):
		x = Count()

	if x is not None and (IRCmsg.find(":!END") != -1):
		x.final()
		x = None
	
	if x is not None and (IRCmsg.find(":!btc") != -1):
		split = IRCmsg.split()
		flare = (split[3])[1:]
		print flare
		try:
			num = float(split[4])
		except ValueError:
			pass
		else:
			x.add(num, username)

	if IRCmsg.find("PING :") != -1:
		Ping()
 
