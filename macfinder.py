#!python
from __future__ import print_function
import requests
import clipboard
from make_colors import make_colors
#from pydebugger.debug import debug
#import traceback
import sys
import json
import argparse
import random

class macfinder(object):
	def __init__(self):
		super(macfinder, self)
		self.URL1 = "https://macvendors.co/api/{0}/json"
		self.URL2 = "https://api.macvendors.com/{0}"
		
	def method_1(self, mac):
		data = {}
		a = requests.get(self.URL1.format(mac))
		if a.status_code == 200:
			data = json.loads(a.content)
		return data
	
	def method_2(self, mac):
		data = ""
		a = requests.get(self.URL2.format(mac))
		if a.status_code == 200:
			data = str(a.content)
		return data
		
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("MAC", action='store', help="Mac Address format: 11:22:33:44:55:66")
		parser.add_argument("-m", "--method", action='store', help="Method 1 or 2, default=1", type=int, default=1)
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			colors = ['lightmagenta', 'lightred', 'lightgreen', 'blue']
			if args.MAC == 'c':
				args.MAC = clipboard.paste()
				if not len(str(args.MAC).split(":")) == 6:
					print(make_colors("INVALID MAC ADDRESS !", "lightwhite", "lightred", attrs=['blink']))
					sys.exit(0)
			if not len(str(args.MAC).split(":")) == 6:
				print(make_colors("INVALID MAC ADDRESS !", "lightwhite", "lightred", attrs=['blink']))
				sys.exit(0)
			if args.method == 1:
				data = self.method_1(args.MAC)
				if data and data.get('result'):
					for i in data.get('result'):
						print(make_colors(i, 'lightcyan') + " " * (13 - len(i))  + ":" + make_colors(data.get('result').get(i), 'lightwhite', random.choice(colors)))
				else:
					print(make_colors('NO DATA FOUND, TRY METHOD 2 !', 'lightwhite', 'lightred', attrs=['blink']))
			elif args.method == 2:
				data = self.method_2(args.MAC)
				if data:
					print(make_colors("VENDOR IS:", 'lightwhite', 'blue') + " " + make_colors(data, 'lightwhite', random.choice(colors)))
				else:
					print(make_colors('NO DATA FOUND, SORRY IT NOT IN DATABASE !', 'lightwhite', 'lightred', attrs=['blink']))
			
if __name__ == '__main__':
	c = macfinder()
	c.usage()