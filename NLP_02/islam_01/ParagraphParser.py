import string
from operator import itemgetter

punctuations = string.punctuation + '",-"'

class ParaParser:
	
	def __init__(self,p):
		self.paragraph = p
		self.words = self.get_words()
		self.word_counts = self.get_word_counts()

	def get_words(self):
		self.separate_punctuations()
		words = self.paragraph.split(' ')
		for i,word in enumerate(words):
			words[i] = word.strip()
		words = [word for word in words if len(word) > 0]
		return words


	def separate_punctuations(self):
		punc_sep_para = ''
		for i,c in enumerate(self.paragraph):
			if c in punctuations:
				punc_sep_para += ' ' + c + ' '
			else:
				punc_sep_para += c
		self.paragraph = punc_sep_para

	def get_word_counts(self):
		word_counts = {}
		for word in self.words:
			if word not in word_counts:
				word_counts[word] = 0
			word_counts[word] += 1
		return word_counts
	def print_most_freq_words(self):
		dic = sorted(self.word_counts.items(), key=itemgetter(1), reverse=True)
		i = 1
		for word,fred in dic:
			if i > 10: 
				break
			print(word + " : " + str(fred) + '\n')
			i += 1