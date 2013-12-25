#!/usr/bin/python3

import os
import shutil
import sys



def parse_file(f):

	print(f)

	return True



def main():

	for rootDir, folders, files in os.walk(os.getcwd()):
		for f in files:
			parse_file(f)

	return True



if __name__ == '__main__':
	main()
