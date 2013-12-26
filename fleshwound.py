#!/usr/bin/python3

"""

Python script for finding PHP vulnerabilities and coding errors.


TODO


KNOWN ISSUES

Only supports variable assignment on a single line.
Only supports function declaration on a single line.
Does not support code outside functions after function declarations start.
Does not support variables defined in include()ed or require()ed files.


@author     Dotan Cohen
@version    2013-12-26

"""

import os
import re
import shutil
import sys

from pprint import pprint



filetypes_to_read = ['.php']
files_to_avoid = []



def parse_file(filename):

	variable_match = re.compile('(\$[\w]+\s*={0,3})')
	original_defined_variables = ['$_GET', '$_POST', '$_REQUEST', '$_SERVER', '$argv']
	defined_variables = original_defined_variables[:]
	defined_variables_stack = []
	line_number = 0
	printedFilename = False

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
		line_number +=1

		inFunctionDeclaration = False

		#if re.search('\s*(static)?\s*(public)?\s*(static)?\s*function\s*[\w]*\s*\(', line):
		if re.search('\s*function\s*[\w]*\s*\(', line):
			inFunctionDeclaration = True
			defined_variables = original_defined_variables[:]

		try:
			matches = variable_match.search(line)
			for found_var in matches.groups():

				if inFunctionDeclaration:
					defined_variables.append(found_var.strip('=\t '))
					continue

				if re.search('^\s*global\s*', line):
					defined_variables.append(found_var.strip('=\t '))
					continue

				if found_var.strip('=\t ') in defined_variables:
					continue

				if found_var.endswith('=='):
					printedFilename = print_error_line(found_var, line, line_number, filename, printedFilename)
					continue

				if found_var.endswith('='):
					defined_variables.append(found_var[:-1].strip())
					continue

				printedFilename = print_error_line(found_var, line, line_number, filename, printedFilename)

		except AttributeError as e:
			# AttributeError: 'NoneType' object has no attribute 'groups'
			pass

	"""
		Add: Find multiple variables per line
		Add: Create a new stack when going into a function declaration

	"""

	input.close()

	return True



def print_error_line(found_var, line, line_number, filename, printedFilename):

	found_var = found_var.strip('=\t ')

	if not printedFilename:
		print("\n\n - File:   %s\n\n" % (filename,))

	print("Use of undefined var: %s on line %i" % (found_var, line_number,))
	print(line)

	return True



def main(files_to_avoid, filetypes_to_read):

	for rootDir, dirs, files in os.walk(os.getcwd()):
		for f in files:
			if not f in files_to_avoid and any(f.endswith(x) for x in filetypes_to_read):
				parse_file(os.path.join(rootDir, f))

	return True



if __name__ == '__main__':
	main(files_to_avoid, filetypes_to_read)
