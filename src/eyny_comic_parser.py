#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import logging

def process(argv):
	# get variable from options.
	para_set = get_option(argv)
	if para_set is None:
		sys.exit(1)

	# get source list.
	for o, a in opts:
		if o == '-i':
			pass
		elif o == '-o':
			pass
		elif o == '--testing':
			pass
		elif o == '--compress':
			pass
		elif o == '--merge':
			pass
		else:
			logging.error("unhandled option.")
			sys.exit(1)

	# filter data.

	# save data.

	pass

def get_option(argv):
	## -i: input file path, -o: output file path, --compress: , --merge, --testing
	opts = None
	args = None
	
	try:
		opts, args = getopt.getopt(argv[1:], 'i:o:h', ['testing', 'merge', 'compress='])
	except getopt.GetoptError as err:
		logging.error(err)
		return None
			
	if len(args) > 0:
		logging.error("option sets not correct.")
		return None

	return opts

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')
	process(sys.argv)
