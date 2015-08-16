import db
import fs
from config import ext
from paths import paths

p = paths()

class ports:
	
	def __init__(self, port):
		self.__port = port
		self.__getDb()

	def __getDb(self):
		self.__db = db.db('ports')

	def add(self):
		port = str(self.__port)
		if self.__db.exist(port):
			self.__db.update(port, self.__db.get(port)+1)
		else:
			f = open(p.get('config')+'ports'+ext('apache'), 'a')
			f.write('Listen '+port+'\n')
			f.truncate()
			f.close()
			self.__db.set(port, 1)

	def substract(self):
		port = str(self.__port)
		if self.__db.exist(port):
			if  self.__db.get(port) > 1:
				self.__db.set(port, self.__db.get(port)-1)
			else:
				f = open(p.get('config')+'ports'+ext('apache'), 'r+')
				lines = [l for l in f.readlines() if l != 'Listen '+port+'\n']
				f.seek(0)
				f.writelines(lines)
				f.truncate()
				f.close()
				self.__db.remove(port)
		else:
			util.error('Port isn\'t set')
