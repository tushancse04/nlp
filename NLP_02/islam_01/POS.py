import operator

class POS:
	
	def __init__(self,training_clean_file,test_clear_file):
		self.training_hash = self.get_hash_of_hash(training_clean_file)
		self.test_hash = self.get_hash_of_hash(test_clear_file)
		self.calculate_performance()


	def calculate_performance(self):
		test_hash = self.test_hash
		training_hash = self.training_hash
		total_words = 0
		correct_words = 0
		for w in test_hash:
			for tag in test_hash[w]:
				total_words += test_hash[w][tag]
			if w in training_hash:
				mft = self.get_most_freq_tag(training_hash[w])
				if mft in test_hash[w]:
					correct_words += test_hash[w][mft]
				else:
					first_key = list(test_hash[w].keys())[0]
					correct_words += test_hash[w][first_key]

		print("performance : " + str(correct_words*100/total_words) + "%")

	def get_most_freq_tag(self,tag_hash):
		cur_freq = 0
		max_tag = None
		for tag in tag_hash:
			if tag_hash[tag] > cur_freq:
				cur_freq = tag_hash[tag]
				max_tag = tag
		return tag


	def print_most_freq_20_tags(self):
		hash_of_hash = self.hash_of_hash
		tag_freq = {}
		for w in hash_of_hash:
			for tag in hash_of_hash[w]:
				if tag not in tag_freq:
					tag_freq[tag] = 0
				tag_freq[tag] += hash_of_hash[w][tag]

		tag_freq = sorted(tag_freq.items(), key=lambda kv: kv[1], reverse=True)
		self.tag_freq = tag_freq
		c = 0
		for tag,freq in tag_freq:
			if c < 20:
				print(tag + ' : ' + str(freq))
			c += 1
	def get_hash_of_hash(self,file_name):
		ifile = open(file_name)
		hash_of_hash = {}
		for l in ifile:
			parts = l.split(' ')
			for i in range(0,len(parts)-1,2):
				tag = parts[i]
				w = parts[i+1]
				if w not in hash_of_hash:
					hash_of_hash[w] = {}
				inn_hash = hash_of_hash[w]
				if tag not in inn_hash:
					inn_hash[tag] = 0
				inn_hash[tag] += 1

				hash_of_hash[w] = inn_hash
		ifile.close()
		return hash_of_hash

