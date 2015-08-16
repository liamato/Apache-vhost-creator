import os
import util


def getFileContent(file):
	if exist(file):
		f = open(file)
		c = f.read()
		f.close()
		return c
	util.error('File \"'+file+'\" doesn\'t exist')

def setFileContent(file, content):
	if exist(file):
		f = open(file, 'w')
		f.write(content)
		f.truncate()
		f.close()
		return
	util.error('File \"'+file+'\" doesn\'t exist')

def exist(path):
	if os.path.exists(path):
		return True
	return False

def getDir(path):
	if exist(path):
		return os.path.dirname(os.path.abspath(path))
	util.error('Path doesn\'t exist')

def getParentDir(path):
	return os.path.dirname(getDir(path))

def ls(path):
    if exist(path):
        return os.listdir(path)
    return None

def isdir(path):
	if exist(path):
		if os.path.isdir(path):
			return True
		return False
	util.error('Path dosn\'t exist')

def isfile(path):
        if exist(path):
                if os.path.isfile(path):
                        return True
                return False
        util.error('Path dosn\'t exist')

def touch(path):
	if not exist(path):
		a = open(path, 'w')
		a.close()
		return True
	return False

def rm(path):
	if exist(path):
		if isfile(path):
			os.remove(path)
		else:
			util.error('Path isn\'t a file')
	else:
		util.error('Path dosn\'t exist')
	
def mkdir(path):
	if not exist(path):
		os.makedirs(path)
		return True
	return False

def rmdir(path):
	if exist(path):
		if isdir(path):
			os.rmdir(path)
		else:
			util.error('Path isn\'t a directory')
	else:
		util.error('Path dosn\'t exist')
