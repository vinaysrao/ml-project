import sys

n, correct = 0, 0

for l in open(sys.argv[1]):
    cat, pred = l.strip().split(':')
    cat, pred = cat.strip(), pred.strip()
    if cat == pred:
        correct += 1
    n += 1
print (float(correct) / float(n)) * 100