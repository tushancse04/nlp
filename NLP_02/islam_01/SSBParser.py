special_chars = ".''``,:$"
class SSBParser:
	
	def __init__(self):
		pass

	def gen_clean_file(self,input_file,out_file):
		self.input_file = input_file
		self.out_file = out_file
		self.parse()

	def get_one_line_sentence(self,input_sentence):
		if len(input_sentence) <= 3:
			return ''
		parts = input_sentence.split('(',1)
		if len(parts) <2:
			return ''

		parts = parts[1].split(' ',1)
		if len(parts) < 2:
			return ''

		tag = parts[0].strip()
		w = parts[1].strip()

		if 'END_OF_TEXT_UNIT' in w:
			return ''

		if '(' not in w:
			if tag in special_chars:
				return ''

			if '-NONE-' == tag:
				return ''

			if '-LRB-' in tag:
				return ''
			if '-RRB-' in tag:
				return ''

			w = w.split(')',1)[0].strip()
			if len(w) == 0:
				return ''
			return tag + ' ' + w + ' '

		w = w.split(')',1)[0]
		return self.get_one_line_sentence(w)


	def parse(self):
		ifile = open(self.input_file)
		S = ''
		for l in ifile:
			l = l.strip()
			S += self.get_one_line_sentence(l)
			if '(TOP' in l:
				S += '\n'

		ifile.close()

		ofile = open(self.out_file,'w')
		ofile.write(S)
		ofile.close()


