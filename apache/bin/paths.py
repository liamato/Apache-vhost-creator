import fs
import json
import inspect
import util


class paths:
	__dirs = {}

	def __init__(self):
		self.__dirs['base'] = fs.getParentDir(inspect.getfile(inspect.currentframe()))
		self.__correctPath('base')
		self.__getPaths()
	
	def __getPaths(self):
		obj = json.loads(fs.getFileContent(self.__dirs['base']+'paths.json'))
		for name in sorted(obj):
			self.__addDir(name, obj[name])

	def __correctPath(self, name):
		if name in self.__dirs:
			path = self.__dirs[name]
			if fs.exist(path) and fs.isdir(path):
				if path[len(path)-1] != '/':
					self.__dirs[name] = path+'/'
			else:
				util.error('Directory \"'+path+'\" dosn\'t exist', None)
		else:
			if fs.exist(name) and fs.isdir(name):
				if name[len(name)-1] != '/':
					return name+'/'
				else:
					return name
			else:
				util.error('Directory \"'+name+'\" dosn\'t exist', None)

	def __addDir(self, name, dir):
		dir = dir.format(**self.__dirs)
		if '**' in dir:
			ddir = dir.split('**')
			dir  = self.__correctPath(fs.getDir(ddir[0]))+ddir[1]
		dir = self.__correctPath(dir)
		self.__dirs[name] = dir

	def get(self, name):
		if name in self.__dirs:
			return self.__dirs[name]
		util.error('Directory name \"'+name+'\" dosn\'t exist')

	def list(self):
		print('{\n')
		for name in self.__dirs:
			print('    \"'+name+'\": '+self.__dirs[name]+',')
		print('}')
		
