import re
import nltk
class unknown_word_handler:
	def __init__(self,input_file,clean_file,pos):
		self.input_file = input_file
		self.clean_file = clean_file
		self.pos = pos
		self.process()
	def process(self):
		ifile = open(self.input_file)
		ofile = open(self.clean_file,'w')
		pos = self.pos
		for l in ifile:
			l = re.sub(r'\W+', ' ', l)
			text = nltk.word_tokenize(l)
			tags = nltk.pos_tag(text)
			s = ''
			for w,tag in tags:
				if w not in pos.training_hash:
					if w.endswith('ed'):
						tag = 'VBD'
					elif w.endswith('ious'):
						tag = 'JJ'
					elif w.endswith('rs'):
						tag = 'NNS'
					elif w.endswith('style'):
						tag = 'JJ'
					else:
						tag = 'NN'
				s += tag + ' ' + w + ' '
			s += '\n'
			ofile.write(s)

		ifile.close()
		ofile.close()


