#!/usr/bin/python

import sys
import helpers


def recognize_routine(recognize_file, training_folder):
    if training_folder[-1] != '/':
        training_folder += '/'

    print helpers.loadObject(training_folder + 'ids.txt')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: $python svm_recognize.py recognize_file training_folder"
        sys.exit(1)

    recognize_routine(sys.argv[1], sys.argv[2])
