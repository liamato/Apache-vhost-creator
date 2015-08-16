#!/usr/bin/python3

import fs
import argparse
import config as conf
from paths import paths as p
import util
import ports
import hosts as dns
import apache


defaults = conf.config('defaults').get()
p = p()
apache = apache.apache()

parser = argparse.ArgumentParser()
parser.add_argument('site', metavar='Site', help='Name of the site', nargs=1)
parser.add_argument('-p', '--port', metavar='Port', default=defaults['port'], help='Port for the site', nargs=1)
parser.add_argument('-t', '--tld', metavar='TLD', default=defaults['tld'], help='Top Level Domain', nargs=1)
parser.add_argument('-r', '--no-restart', dest='restart', help='Prevent the restart httpd action', action='store_false')
parser.add_argument('-d', '--disable', help='Disables the site after her creation (-r implicit)', action='store_true')
parser.add_argument('-w', '--hosts', help='Creates a DNS in the server: site.tld->127.0.0.1', action='store_true')

a = parser.parse_args()

site 	= a.site[0]
port 	= a.port[0]
tld  	= a.tld[0]
restart = a.restart
disable = a.disable
hosts	= a.hosts

if tld[0] is not '.':
	tld = '.'+tld

if disable:
	restart = False

domain=site+tld

# Create site
if fs.touch(p.get('asites')+domain+conf.ext('apache')):
	# sites_available
	tpl = fs.getFileContent(p.get('config')+'tpl.conf').format(port=port, sites=p.get('sites'), domain=domain, error=p.get('error'), exterror=conf.ext('error'), log=p.get('log'), extlog=conf.ext('log'))
	fs.setFileContent(p.get('asites')+domain+conf.ext('apache'), tpl)
	# error
	fs.touch(p.get('error')+domain+conf.ext('error'))
	# log
	fs.touch(p.get('log')+domain+conf.ext('log'))
	# sites/{site}/
	fs.mkdir(p.get('sites')+domain)
	# ports
	ports.ports(port).add()
	

	# apache
	if restart:
		apache.restart()
	# enable
	if not disable:
		apache.ensite(domain)	
	# hosts
	if hosts:
		h = dns.host(domain)
		if not h.exist():
			h.add()

else:
	util.error('Site \"'+site+'\" already exist', None, 'csite')
