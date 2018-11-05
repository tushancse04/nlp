import re
class Parser:
	
	def __init__(self,corpus_file):
		self.count = 0
		self.corpus_file = corpus_file
		sentences = self.get_sentences()
		rules = self.get_rules(sentences)
		self.print_most_freq_rules(rules)
		self.print_tags_with_most_alt_rules(rules)


	def get_sub_parts(self,s_parts):
		if s_parts[0] != '(':
			return []
		sub_parts = []
		c = 0
		for i,p in enumerate(s_parts):
			if p == '(':
				c = c + 1

			if p == ')':
				c = c - 1
			if c == 0:
				sub_parts += [s_parts[0:i+1]]
				sub_parts += self.get_sub_parts(s_parts[i+1:])
				break

		return sub_parts




	def get_rules_by_sentence(self,s_parts,rules):
		if len(s_parts) <= 4:
			if len(s_parts) == 4 and len(s_parts[2]) > 2:
				self.count += 1
			return


		r = s_parts[1]
		sub_parts = self.get_sub_parts(s_parts[2:])
		childs = ''
		for sp in sub_parts:
			if sp[1] == '-NONE-':
				continue
			if len(re.sub('\W+','', sp[1] )) == 0:
				continue
			childs += sp[1]  + ' '
		if r != 'TOP' and len(childs) > 0:
			rules += [r + ' -> ' + childs]
		for sp in sub_parts:
			self.get_rules_by_sentence(sp,rules)


	def get_rules(self,sentences):
		rules = []
		c = 0
		for s in sentences:
			parts = s.split()
			self.get_rules_by_sentence(parts,rules)
		print(self.count)
		return rules


	def get_sentences(self):
		fname = self.corpus_file
		ifile = open(fname)
		sentences = []
		s = ''
		c = 0
		for l in ifile:
			if l.startswith('(TOP END_OF_TEXT_UNIT)'):
				continue
			if len(l.strip()) == 0:
				continue
			if l.startswith('(TOP'):
				sentences += [s]
				s = ''
				c += 1
			l = ' '.join(l.split())
			l = l.replace('(','( ')
			l = l.replace(')',' )')
			s += l + ' '


		return sentences

	def print_tags_with_most_alt_rules(self,rules):
		ltag_dic = {}
		for r in rules:
			ltag = r.split('->')[0]
			rtags = r.split('->')[1]
			if ltag not in ltag_dic:
				ltag_dic[ltag] = []
			if rtags not in ltag_dic[ltag]:
				ltag_dic[ltag] += [rtags]


		sorted_dic = sorted(ltag_dic.items(), key=lambda item: (len(item[1]), item[0]),reverse=True)
		print('Non-terminal with most alternate rules : ')
		for r,t in sorted_dic:
			print(r)
			break


	def print_most_freq_rules(self,rules):
		rule_dic = {}
		for r in rules:
			if r not in rule_dic:
				rule_dic[r] = 0
			rule_dic[r] += 1
		print("Total rules : " + str(len(rule_dic)))
		print('--------------------------------')
		sorted_dic = sorted(rule_dic.items(), key=lambda item: (item[1], item[0]),reverse=True)
		c = 1
		print('10 most frequent rules:')
		for r,t in sorted_dic:
			print(r)
			c += 1
			if c > 10:
				break
		print('--------------------------------')





