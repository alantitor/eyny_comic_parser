#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import logging
import parser

def process(argv):
	# get variable from options.
	para_set = get_option(argv)
	if para_set is None:
		sys.exit(1)

	# select module.
	state = select_module(para_set)
	if state is False:
		sys.exit(1)

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
		#logging.error("option sets not correct.")
		return None

	return opts

def select_module(para_set):
	# get parameters.
	input_file = '';
	output_path = '';
	testing = False;
	compress = '';
	merge = False;

	for o, a in para_set:
		if o == '-i':
			input_file = a
		elif o == '-o':
			output_path = a
		elif o == '--testing':
			testing = True
		elif o == '--compress':
			compress = a
		elif o == '--merge':
			merge = True
		else:
			#logging.error("unhandled option.")
			return False

	if testing:
		pass
	else:
		state = parser.parser(input_file, output_path, merge, compress)
		if state is False:
			#logging.error("can't not parse file.")
			return False

	return True

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')
	process(sys.argv)
