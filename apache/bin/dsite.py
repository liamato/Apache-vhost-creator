#!/usr/bin/python3

import fs
import argparse
import config as conf
from paths import paths as p
import util
import apache


defaults = conf.config('defaults').get()
p = p()
apache = apache.apache()

parser = argparse.ArgumentParser()
parser.add_argument('site', metavar='Site', help='Name of the site', nargs=1)
parser.add_argument('-t', '--tld', metavar='TLD', default=defaults['tld'], help='Top Level Domain', nargs=1)
parser.add_argument('-r', '--no-restart', dest='restart', help='Prevent the restart httpd action', action='store_false')

a = parser.parse_args()

site 	= a.site[0]
tld  	= a.tld[0]
restart = a.restart

if tld[0] is not '.':
	tld = '.'+tld

domain=site+tld

# Enable site
if fs.exist(p.get('asites')+domain+conf.ext('apache')):
	# enable
	if apache.isenabled(domain):
		apache.disite(domain)
	else:
		util.error('Site \"'+site+'\" isn\'t enabled', None, 'dsite')

	# apache
	if restart:
		apache.restart()

else:
	util.error('Site \"'+site+'\" dosn\'t exist', None, 'dsite')
