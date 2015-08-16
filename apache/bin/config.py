import fs 
from paths import paths as p
import json

def ext(name):
	return json.loads(fs.getFileContent(p().get('config')+'ext.json'))[name]


class config:
	def __init__(self, file):
		self.file = file
		self.__ext = ext('config')

	def get(self):
		return json.loads(fs.getFileContent(p().get('config')+self.file+self.__ext))
