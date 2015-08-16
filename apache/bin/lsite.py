#!/usr/bin/python3

import fs
import argparse
import util
#import xml.etree.ElementTree as ET
#import json
from paths import paths
from config import ext

p = paths()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tld', metavar='TLD', help='List the sites ordered by Top Level Domain', nargs='?', const=True)
parser.add_argument('-e', '--enabled', help='List the enabled sites', action='store_true')
parser.add_argument('-d', '--disabled', help='List the disabled sites', action='store_true')
parser.add_argument('-a', '--all', help='List all available sites (Default action)', action='store_true')
parser.add_argument('-f', '--full', help='Alias of: lsite -t -e -d -a', action='store_true')
#parser.add_argument('-j', '--json', help='Prints the output as JSON', action='store_true')
#parser.add_argument('-x', '--xml', help='Prints the output as XML', action='store_true')
#parser.add_argument('-o', '--out', metavar='file', help='Prints the output in the file', nargs=1)

a = parser.parse_args()

tld		= a.tld
enabled		= a.enabled
disabled	= a.disabled
al		= a.all
#ojson		= a.json
#oxml		= a.xml

if a.full:
	tld		= True
	a.tld		= None
	enabled		= True
	disabled	= True
	al		= True
    
if type(a.tld) is str:
	if tld[0] != '.':
		tld = '.'+tld

if not enabled and not disabled and not tld:
	al = True


'''
if a.out:
	out = a.out[0]

if ojson and oxm:
	util.error('Can\'t request XML and JSON in the same call (lsite -j -x)')
'''


# List site
asi = [p[:len(p)-len(ext('apache'))] for p in fs.ls(p.get('asites')) if p[len(p)-len(ext('apache')):] == ext('apache')]
esi = [p[:len(p)-len(ext('load'))] for p in fs.ls(p.get('esites')) if p[len(p)-len(ext('load')):] == ext('load')]
dsi = list(set(asi)-set(esi))
tsi = {}

for s in asi:
	t = s[s.find('.'):]
	if not t in tsi:
		tsi[t] = []
	tsi[t].append(s)

print()

if al:
	print('All Sites:')
	for s in asi:
		print('   + {site}'.format(site=s))
	print()

if enabled:
	print('Sites Enabled:')
	for s in esi:
		print('   + {site}'.format(site=s))
	print()

if disabled:
	print('Sites Disabled:')
	for s in dsi:
		print('   + {site}'.format(site=s))
	print()

if tld is True:
	print('Sites Grouped by TLD:')
	for tl in tsi:
		print('   - {tld}'.format(tld=tl))
		for s in tsi[tl]:
			print('        + {site}'.format(site=s))

if type(a.tld) is str:
	print('Sites with TLD \"{tld}\":'.format(tld=tld))
	for s in tsi[tld]:
		print('   + {site}'.format(site=s))
	print()

'''
print(asi)
print(esi)
print(dsi)
print(tsi)
'''
#parser.parse_args('-h'.split())
