import sys
import re
import cPickle as pickle
f = open(sys.argv[1])
nicks = []
msgRegex = re.compile(r'[0-9][0-9]:[0-9][0-9] <@?([a-zA-Z0-9]*)> (.*)$')
ignore = ['Hypatia', 'earlbot', 'shardik','*']
data = {}
total = sum(1 for line in f)
f.seek(0)
lc = 0.0
for line in f:
	lc += 1.0
	print '\rParsing logs... {:.0%}'.format(lc/total),
	match = msgRegex.match(line)
	if match is None:
		continue
	nick = match.group(1).lower()
	if nicks.count(nick) == 0:
		nicks.append(nick)
	if ignore.count(nick) > 0:
		continue
	msg = match.group(2)
	words = filter(lambda x: nicks.count(x.strip(':,<>()@+_*').lower()) == 0 and not x.startswith("http"), msg.split()) 
	if len(words) < 4:
		continue
	for i in range(len(words) - 3):
		key = (words[i].lower(), words[i+1].lower(), words[i+2].lower())
		if key in data:
			data[key].append(words[i+3])
		else:
			data[key] = [words[i+3]]
print '\rStoring dictionary...',
f.close()
pkl = open(sys.argv[1]+'.pkl', 'wb')
pickle.dump(data, pkl)
pkl.close()
