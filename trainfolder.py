#!/usr/bin/python

import os, sys
import readline, glob


def complete(text, state):
    return (glob.glob(text + '*') + [None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def add_files(folder, trainfile, testfile):
	if folder[-1] != '/':
		folder += '/'

	train = open(trainfile, 'w')
	test = open(testfile, 'w')

	for file in os.listdir(folder):
		if os.path.isdir(folder + file):
			path = os.path.abspath(folder + file) + '/'
			list = os.listdir(path)
			l = len(list)
			#l = 50
			t = int(0.7 * l)
			for img in xrange(t):
				spl = list[img].split('.')
				try:
					if spl[-1] in ['jpg', 'jpeg', 'png' ]:
						train.writelines(file + ';' + path + list[img] + '\n')
				except:
					continue
			for img in xrange(t + 1, l):
				spl = list[img].split('.')
				try:
					if spl[-1] in ['jpg', 'jpeg', 'png' ]:
						test.writelines(file + ';' + path + list[img] + '\n')
				except:
					continue
	train.close()
	test.close()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage: $python trainfolder.py folder trainfile testfile"
		sys.exit(1)
	add_files(sys.argv[1], sys.argv[2], sys.argv[3])
