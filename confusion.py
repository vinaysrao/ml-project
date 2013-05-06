#!/usr/bin/python

import sys

if __name__ == "__main__":
    infile = sys.argv[1]
    d = {}
    for line in open(infile):
        actual, predicted = line.strip().split(':')
        actual, predicted = actual.strip(), predicted.strip()

        if actual not in d:
            d[actual] = {}

        if predicted not in d[actual]:
            d[actual][predicted] = 0

        d[actual][predicted] += 1

    print d