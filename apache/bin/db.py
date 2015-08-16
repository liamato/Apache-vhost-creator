import fs
from config import ext
from paths import paths
import util
import json


p = paths()

class db:
	
	def __init__(self, name):
		self.__name = name
		self.__getdb()

	def __getdb(self):
		if fs.exist(p.get('db')+self.__name+ext('db')):
			self.__db = json.loads(fs.getFileContent(p.get('db')+self.__name+ext('db')))
		else:
			util.error('The database \"'+db+'\" dosn\'t exist', None)

	def __setdb(self):
		fs.setFileContent(p.get('db')+self.__name+ext('db'), json.dumps(self.__db))
	
	def get(self, key=None):
		if key is None:
			return self.__db
		elif key in self.__db:
			return self.__db[key]
		else:
			util.error('The key \"'+key+'\" dosn\'t exist in this db')

	def exist(self, key):
		if key in self.__db:
			return True
		return False

	def update(self, key, value):
		self.__db[key] = value
		self.__setdb()
		
	def set(self, key, value):
		if key in self.__db:
			self.update(key, value)
			return True
		return False

	def remove(self, key):
		if key in self.__db:
			del(self.__db[key])
			self.__setdb()
		else:
			util.error('The key \"'+key+'\" dosn\'t exist')
