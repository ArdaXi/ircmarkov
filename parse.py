import sys
import re
import cPickle as pickle
f = open(sys.argv[1])
nicks = set()
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
	nicks.add(nick)
	if ignore.count(nick) > 0:
		continue
	msg = match.group(2)
	words = [x for x in msg.split() if not x.strip(':,<>()@+_*').lower() in nicks and not x.startswith("http")]
	if len(words) < 4:
		continue
	for i in range(len(words) - 3):
		key = (words[i].lower(), words[i+1].lower(), words[i+2].lower())
		if key in data:
			data[key].append(words[i+3])
		else:
			data[key] = [words[i+3]]
print '\nStoring dictionary...',
f.close()
pkl = open(sys.argv[1]+'.pkl', 'wb')
pickle.dump(data, pkl)
pkl.close()
