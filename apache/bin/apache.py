import os
import fs
import util
from paths import paths
from config import ext
import re

p = paths()

class apache:
	
	def __init__(self):
		self.__getapachectl()
		if not self.__checkvhmod():
			util.error('vhost_alias_module required Apache Module isn\'t enabled')

	def __getapachectl(self):
		p = os.popen('sudo find /bin /sbin /usr -name "apachectl" -print')
		l = [line[:len(line)-1] for line in p.readlines()]
		if len(l) > 0:
			self.__ctl = l[0]
	
	def __getconffile(self):
		p = os.popen('sudo find /etc /usr -name "httpd.conf" -print')
		l = [line[:len(line)-1] for line in p.readlines()]
		if len(l) > 0:
			self.__httpd = l[0]
	
	def __checkvhmod(self):
		p = os.popen('sudo '+self.__ctl+' -M')
		l = re.search(r'^\s(vhost_alias_module).*', p.read(), re.I|re.M)
		if l:
			#l = l.string[l.start():l.end()]
			#l.group()
			return True
		return False
	
	def restart(self):
                os.system('sudo '+self.__ctl+' restart')

	def isenabled(self, site):
		if fs.exist(p.get('esites')+site+ext('load')):
			return True
		return False

	def ensite(self, site):
		if not self.isenabled(site):
			fs.touch(p.get('esites')+site+ext('load'))
			fs.setFileContent(p.get('esites')+site+ext('load'), 'Include \"'+p.get('asites')+site+ext('apache')+'\"')
		else:
			util.error('Site is already enabled')
	
	def disite(self, site):
		if self.isenabled(site):
			fs.rm(p.get('esites')+site+ext('load'))
		else:
			util.error('Site is already disabled ( Is the correct TLD? )')
