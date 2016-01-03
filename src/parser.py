#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import codecs
import tool
import config
import logging
from HTMLParser import HTMLParser
import shutil

def parser(input_file, output_path, merge, compress_type):
	#logging.basicConfig(level=logging.INFO)
	root = logging.getLogger()
	root.setLevel(logging.INFO)

	# get file information
	f_name, f_extension = os.path.splitext(input_file)
	f_path = os.path.dirname(f_name)
	f_name = os.path.basename(f_name)
	image_title = tool.fetch_title(tool.string_encode(f_name))

	# find image list
	image_list = find_image_list(input_file)
	if image_list is None:
		return False

	# append path to image list
	image_list[:] = [(f_path + '/' + f_name + '_files/' + item) for item in image_list]

	# filter garbage from image list
	image_list = tool.detect_image(image_list)

	# save image to new path
	state = save_image(image_list, image_title, os.path.splitext(image_list[0])[1], output_path)
	if state is False:
		#logging.info("parse file: " + input_file + " [Fail]")
		return False

	#logging.info("parse file: " + input_file + " [OK]")

	return True

def find_image_list(path):
	text = ''

	try:
		text = codecs.open(path, 'r', 'utf-8').read()
	except IOError:
		#logging.error("can't open source file: " + path)
		return None

	html_parser = HTMLTagParser()
	html_parser.feed(text)

	# get image title and lisgt.
	image_list = html_parser.get_image_list()

	# split path.
	image_list[:] = [(os.path.basename(item)) for item in image_list]

	return  image_list

def save_image(image_list, image_title, image_extension, output_path):
	path = output_path + '/' + tool.string_decode(image_title)

	if not os.path.exists(path):
		os.makedirs(path)
	else:
		#logging.error("folder exist. name: " + path)
		return False

	for count in range(0, len(image_list)):
		shutil.copyfile(image_list[count], path + '/' + ("%.3d" % (count + 1)) + image_extension)

class HTMLTagParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.image_list = []
		self.image_title = ''
		self.flag_title = 0
		#self.flag_image = 0

	def handle_starttag(self, tag, attrs):
		if tag.lower() == 'title':
			self.flag_title += 1

		if tag.lower() == 'img':
			for item in attrs:
				if item[0].lower() == 'src':
					img_src = item[1]  # get image path
					ext = os.path.splitext(img_src)[1]
					if ext.lower() in (".jpeg", ".jpg", ".png", ".bmp"):
						self.image_list.append(img_src)
						break

	def handle_data(self, data):
		if self.flag_title:
			self.image_title = data

	def handle_endtag(self, tag):
		if tag == 'title' and self.flag_title:
			self.flag_title -= 1

	def get_title(self):
		return self.image_title

	def get_image_list(self):
		return self.image_list
