#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
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
		opts, args = getopt.getopt(argv[1:], 'f:p:o:h', ['testing', 'merge', 'compress='])
	except getopt.GetoptError as err:
		logging.error(err)
		return None

	if len(args) > 0:
		#logging.error("option sets not correct.")
		return None

	return opts

def select_module(para_set):
	# get parameters.
	input_path = '';
	input_file = '';
	output_path = './';
	testing = False;
	compress = '';
	merge = False;

	for o, a in para_set:
		if o == '-p':
			input_path = a
		elif o == '-f':
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

	# check parameters state
	# only allow user use -p or -f at same time.
	if (bool(len(input_path)) != bool(len(input_file))) is False:
		return False

	if testing:
		# go to test module.
		return True

	if len(input_path) > 0:
		# parse all html files in folder.
		for file in os.listdir(input_path):
			if os.path.isfile(input_path + '/' + file):
				state = parser.parser(input_path + '/' + file, output_path, merge, compress)
				if state is False:
					continue
				else:
					print '[ok]' + file
	else:
		# parse html file.
		state = parser.parser(input_file, output_path, merge, compress)
		if state is False:
			return False
		print '[ok]' + input_file

	return True

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')
	process(sys.argv)
