import sys
import random
import cPickle as pickle
f = open(sys.argv[1], 'rb')
data = pickle.load(f)
f.close()
seed = random.choice(data.keys())
w1, w2, w3 = seed[0], seed[1], seed[2]
genwords = []
for i in xrange(int(sys.argv[2])):
	genwords.append(w1)
	genwords.append(w2)
	try:
		nw = random.choice(data[(w1.lower(), w2.lower(), w3.lower())])
		data[(w1, w2, w3)].remove(nw)
		w1, w2, w3 = w2, w3, nw
	except (KeyError, IndexError):
		seed = random.choice(data.keys())
		w1, w2, w3 = seed[0], seed[1], seed[2]
	genwords.append(w3)
print ' '.join(genwords)
