#!/usr/bin/python3

import os
import shutil
import sys

from pprint import pprint



filetypes_to_read = ['.php']
files_to_avoid = []



def parse_file(f):

	input = open(f, 'r')
	""" Not using try yet to learn about possible exceptions
	try:
		input = open(f, 'r')
	except Exception as e:
		pass

		IOError: [Errno 2] No such file or directory: 'index']
		Thrown when trying to parse file that does not exits ('index' instead of '.git/index')

	"""

	for l in input:
		if '_GET' in l:
			print("\n%s" % (f,))
			print("Found _GET!")
			print(l)

	input.close()

	return True



def main(files_to_avoid, filetypes_to_read):

	for rootDir, dirs, files in os.walk(os.getcwd()):
		for f in files:
			if not f in files_to_avoid and any(f.endswith(x) for x in filetypes_to_read):
				parse_file(os.path.join(rootDir, f))

	return True



if __name__ == '__main__':
	main(files_to_avoid, filetypes_to_read)
