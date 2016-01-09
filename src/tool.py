#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import config
from urllib import url2pathname
from urllib import pathname2url
from PIL import Image
import logging

def string_decode(str):
	# use quote()?
	return url2pathname(str.decode('string-escape'))

def string_encode(str):
	return pathname2url(str.decode('string-escape'))

def fetch_title(str):
	str = re.sub(config.GARBAGE_TITLE_STRING1, '', str)
	str = re.sub(config.GARBAGE_TITLE_STRING2, '', str)

	str = re.sub('(^(%20)*)|((%20)*$)', '', str)
	str = re.sub('(-)*$', '', str)
	str = re.sub('(^(%20)*)|((%20)*$)', '', str)
	str = re.sub('(-)*$', '', str)
	str = re.sub('(^(%20)*)|((%20)*$)', '', str)

	#str = re.sub('(%281/2%29$)', '%281%29', str)
	#str = re.sub('(%282/2%29$)', '%282%29', str)

	return str

def detect_sibling(path):
	pass

def detect_image(image_list):
	result_list = []

	if isinstance(image_list, basestring):
		# is string
		pass
	else:
		# is list
		#for index, item in enumerate(image_list):
		for item in image_list:
			if image_rule1(item) is False:
				continue
			if image_rule2(item) is False:
			 	continue
			if image_rule3(item) is False:
				continue

			result_list.append(item)

	return result_list

def image_rule1(item):
	try:
		item = string_decode(item)
		im = Image.open(item)
	except:
		#logging.warning("can't detect image information")
		return False

	width = im.size[0]
	heigh = im.size[1]

	# avatar image
	if heigh < 400 and width < 400:
		return False

	# big size image
	if heigh > 900:
		return True
	else:
		# use ratio filte very-long type images.
		# ratio should small than 0.5.
		if ((heigh * 1.0) / (width * 1.0)) < 0.45:
			return True
		else:
			return False

	return False

def image_rule2(item):
	for a in config.GARBAGE_IMAGE_LIST:
		if a in os.path.basename(item):
			return False
	return True

def image_rule3(item):
	if len(os.path.basename(item)) < config.IMAGE_MIN_LENGTH: # file name + file extension.
		return False
	return True
