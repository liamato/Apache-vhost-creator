import util
import db
import paths

p = paths.paths()

class host:

	def __init__(self, host):
		self.host = host
		self.__ip = '127.0.0.1'
		self.__db = db.db('hosts')
		
	def exist(self):
		if self.__db.exist(self.host):
			return True
		return False

	def add(self):
		if not self.exist():
			f = open(p.get('hosts')+'hosts', 'a')
			f.write(self.__ip+' '+self.host)
			f.close()
			self.__db.set(self.host, self.__ip)
		else:
			util.error('The host is allready set')

	def remove(self):
		if self.exist():
			f = open(p.get('hosts')+'hosts', 'r+')
			l = [line for line in f.readlines() if line != self.__ip+' '+self.host+'\n']
			f.seek(0)
			f.writelines(l)
			f.truncate()
			f.close()
			self.__db.remove(self.host)
		else:
			util.error('The host isn\'t set')
