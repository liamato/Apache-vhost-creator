import inspect

def error(msg, func='false', module='false'):
	if func == 'false':
		func = inspect.stack()[1][3]
	if module == 'false':
		module = inspect.getmodule(inspect.stack()[1][0]).__name__
	full = module
	if func != None:
		full = full+'.'+func
	else:
		full = ' '+full+' '
	#print(inspect.stack())
	print('\n<<'+full+'>>\n  Error: '+msg+'\n')
	exit()
