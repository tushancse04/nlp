ifile = open('BROWN-clean.pos_milu.txt')
hash_of_hash_milu = {}
for l in ifile:
	words = l.split(' ')
	for i in range(0,len(words)-1,2):
		tag = words[i]
		w = words[i+1]
		if (w,tag) not in hash_of_hash_milu:
			hash_of_hash_milu[w,tag] = 0

		hash_of_hash_milu[w,tag] += 1


ifile = open('BROWN-clean.pos.txt')
hash_of_hash = {}
c = 0
for l in ifile:
	words = l.split(' ')
	for i in range(0,len(words)-1,2):
		tag = words[i]
		w = words[i+1]
		if (w,tag) not in hash_of_hash:
			hash_of_hash[w,tag] = 0

		hash_of_hash[w,tag] += 1
		c += 1

print(c)

for w,tag in hash_of_hash:
	w,tag = w.strip(),tag.strip()
	if (w,tag) not in hash_of_hash_milu:
		print(tag,w)