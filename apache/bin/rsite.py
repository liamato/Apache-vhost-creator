#!/usr/bin/python3

import fs
import argparse
import config as conf
from paths import paths
import util
import ports
import hosts as dns
import apache


defaults = conf.config('defaults').get()
p = paths()
apache = apache.apache()

parser = argparse.ArgumentParser()
parser.add_argument('site', metavar='Site', help='Name of the site', nargs=1)
parser.add_argument('-p', '--port', metavar='Port', default=defaults['port'], help='Port for the site', nargs=1)
parser.add_argument('-t', '--tld', metavar='TLD', default=defaults['tld'], help='Top Level Domain', nargs=1)
parser.add_argument('-r', '--no-restart', dest='restart', help='Prevent the restart httpd action', action='store_false')
parser.add_argument('-l', '--log', '--preserve-log', help='Preserves the log', action='store_true')
parser.add_argument('-e', '--error', '--preserve-errors', help='Preserves the error log', action='store_true')
parser.add_argument('-d', '--docs', '--preserve-docs', help='Preserves the htdoc files of the sites', action='store_false')
parser.add_argument('-w', '--hosts', help='Creates a DNS in the server: site.tld->127.0.0.1', action='store_true')

a = parser.parse_args()

site 	= a.site[0]
port 	= a.port[0]
tld  	= a.tld[0]
restart = a.restart
log 	= a.log
error	= a.error
docs	= a.docs
hosts	= a.hosts

if tld[0] is not '.':
	tld = '.'+tld

domain=site+tld


# Remove site
if fs.exist(p.get('asites')+domain+conf.ext('apache')):
	# sites_available
	fs.rm(p.get('asites')+domain+conf.ext('apache'))
	# sites_enabled
	if apache.isenabled(domain):
		apache.disite(domain)
	# ports
	ports.ports(port).substract()
    
    
	# error
	if not error:
		fs.rm(p.get('error')+domain+conf.ext('error'))
	# log
	if not log:
		fs.rm(p.get('log')+domain+conf.ext('log'))
	# sites/{site}/
	fs.rmdir(p.get('sites')+domain)
	# apache
	if restart:
		apache.restart()
	# hosts
	if hosts:
		h = dns.host(domain)
		if h.exist():
			h.remove()

else:
	util.error('Site \"'+site+'\" dosn\'t exist', None, 'rsite')
