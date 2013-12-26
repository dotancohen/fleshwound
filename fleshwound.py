#!/usr/bin/python3

import os
import re
import shutil
import sys

from pprint import pprint



filetypes_to_read = ['.php']
files_to_avoid = []



def parse_file(filename):

	defined_variables = ['$_GET', '$_POST', '$_REQUEST', '$_SERVER', '$argv']
	variable_match = re.compile('(\$[\w]+\s*={0,3})')

	try:
		input = open(filename, 'r')
	except Exception as e:
		print("\nFile could not be opened: %s\n%s" % (filename, e))
		"""
		IOError: [Errno 2] No such file or directory: 'index']
		Thrown when trying to parse file that does not exits ('index' instead of '.git/index')

		Got some utf8 error when parsing a binary file
		"""



	for line in input:
		print(line.strip())
		try:
			matches = variable_match.search(line)
			#pprint(matches.groups())
			for found_var in matches.groups():

				if found_var.strip('=\t ') in defined_variables:
					continue

				if found_var.endswith('=='):
					print("!!!!!!!!!!!!!!!!!! Use of undefined var: %s" % (found_var.strip('=\t '),))
					continue

				if found_var.endswith('='):
					defined_variables.append(found_var[:-1].strip())
					continue

				print("!!!!!!!!!!!!!!!!!! Use of undefined var: %s" % (found_var,))

		except AttributeError as e:
			# AttributeError: 'NoneType' object has no attribute 'groups'
			pass

	"""
		Add: Find variables defined in function parameters
		Add: Find multiple variables per line
		Add: Create a new stack when going into a function declaration

	"""

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
