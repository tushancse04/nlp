from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
import urllib.request as req
import re
import urllib.parse as parser
import PyPDF2
import random
from nltk import PorterStemmer
import os
import sys
from urllib.parse import urlparse
import json


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)





# We only want to consider visible tags
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Get visible text from html
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

#Calculate each word frequency
def get_word_frequency_dict(words):
	for i,word in enumerate(words):
		words[i] = PorterStemmer().stem(word).lower()
	words = list(set(words))
	stop_words = get_stop_words('english.stopwords.txt')
	words = list(set(words).difference(set(stop_words)))
	word_dict = {}
	for word in words:
		if word in word_dict:
			word_dict[word] += 1
		else:
			word_dict[word] = 1
	return word_dict

#get bag of words from a html page
def get_words_from_html(html_url):
	try:
		url = req.urlopen(html_url)
		s = url.read()
		text = text_from_html(s)
		return get_words_from_text(text)
	except:
		return []

# get bag of words from a raw text after filtering
def get_words_from_text(text):
	text = re.findall(r"[\w']+", text)
	words = [word.title() for word in text if word.strip() and not word.isnumeric()]
	words = [word for word in words if word[0].isalpha() and len(word) > 1]
	return words

# get bag of words from a pdf url
def get_words_from_pdf_url(pdf_url):
	try:
		download_pdf_file(pdf_url)
		pdfFileObj = open('document.pdf','rb')     #'rb' for read binary mode
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		page_count = pdfReader.numPages
		text = ''
		for i in range(page_count):
			pageObj = pdfReader.getPage(i)
			text += pageObj.extractText() + '\n'
		return get_words_from_text(text)
	except:
		return ''

#get bag of words from a text url
def get_words_from_txt_url(txt_url):
	try:
		response = req.urlopen(txt_url)
		text = str(response.read())
		return get_words_from_text(text)
	except:
		return ''



# get one level hyperlinks from a html page specially from course page
def get_hyperlinks(course_url):
	url = req.urlopen(course_url)
	html_doc = url.read()
	soup = BeautifulSoup(html_doc,'lxml')
	links = soup.find_all('a')
	hplinks = []
	for link in soup.findAll('a'):
		hplink = link.get('href')
		if not hplink:
			continue
		if 'PageRankFranceschet' in hplink:
			continue
		hplink = hplink.split('#')[0]
		if hplink in hplinks:
			continue

		if not is_valid_url(hplink):
			continue
		if not hplink.startswith('http'):
			hplink = course_url + hplink

		hplinks += [hplink]
	return hplinks

#to filter by valid hyperlinks
def is_valid_url(url):
	try:
		request = req.Request(url)
		response = req.urlopen(request)
		return True
	except:
		return is_pdf(url) or is_txt(url)

def is_pdf(url):
	return url.endswith('.pdf')

def is_txt(url):
	return url.endswith('.txt')

# download pdf file so that we can read it
def download_pdf_file(download_url):
	response = req.urlopen(download_url)
	file = open("document.pdf", 'wb')
	file.write(response.read())
	file.close()


# get word dictionary for frequency of each doc
def get_doc_dict(hplinks):
	doc_dict = {}
	for link in hplinks:
		words = ''
		if link.endswith('.pdf'):
			words = get_words_from_pdf_url(link)
		elif link.endswith('.txt'):
			words = get_words_from_txt_url(link)
		else:
			words = get_words_from_html(link)
		word_dict = get_word_frequency_dict(words)
		doc_dict[link] = word_dict
	return doc_dict

# print TF and DF here
def print_word_each_doc_count(doc_dict):
	count = 'C'
	docs = 'docs'
	out = 'out'
	words = set([])
	for doc in doc_dict:
		words = words | doc_dict[doc].keys()

	word_each_doc = {}
	for word in words:
		word_each_doc[word,count] = 0
		word_each_doc[word,docs] = ''
	for word in words:
		for doc in doc_dict:
			if is_txt(doc) or is_pdf(doc):
				dname = doc.split('/')
				dname = dname[-1]
			else:
				dname = doc
			if word in doc_dict[doc]:
				word_each_doc[word,count] += doc_dict[doc][word]
				word_each_doc[word,docs] += ', ' + dname + ' : ' +  str(doc_dict[doc][word])
	for word in words:
		word_each_doc[word,out] = word.lower() + ' -> ' + str(word_each_doc[word,count]) + word_each_doc[word,docs]
	for word in words:
		print(word_each_doc[word,out] + '\n')

#generate inverted index
def get_inv_index(corpus_dir):
	inv_idx_dic = {}
	files = os.listdir(corpus_dir)
	for f in files:
		fname = corpus_dir + '/' + f
		words = open(fname).read().split(' ')
		for w in words:
			if w not in inv_idx_dic:
				inv_idx_dic[w] = [0,{}]
			if f not in inv_idx_dic[w][1]:
				inv_idx_dic[w][0] += 1
				inv_idx_dic[w][1][f] = 0
			inv_idx_dic[w][1][f] += 1
	return inv_idx_dic

#print inverted index
def print_inv_idx(inv_idx_dic):
	for ti in inv_idx_dic:
		ostr = ti + ' : ' + str(inv_idx_dic[ti][0]) + ' => '
		for dj in inv_idx_dic[ti][1]:
			ostr += dj + ':' + str(inv_idx_dic[ti][1][dj]) + ';'
		ostr += '\n'
		print(ostr)



#get maximum freq
def get_max_freq(inv_idx_dic):
	term_max_freq_dic = {}
	for ti in inv_idx_dic:
		for dj in inv_idx_dic[ti][1]:
			if dj not in term_max_freq_dic:
				term_max_freq_dic[dj] = 0
			if term_max_freq_dic[dj] < inv_idx_dic[ti][1][dj]:
				term_max_freq_dic[dj] = inv_idx_dic[ti][1][dj]
	return term_max_freq_dic


#get all words
def get_terms(corpus_dir,files):
	words = set()
	for f in files:
		ifile = open(corpus_dir + '/' + f)
		ws = ifile.read().split(' ')
		words = words.union(ws)
	return terms


#get DF here
def get_DF(files):
	for doc in docs:
		pass

#Preprocess documents here
def preprocess(crawl_dir,corpus_dir):
	if not os.path.exists(corpus_dir):
		os.makedirs(corpus_dir)
	files = os.listdir(crawl_dir)
	for f in files:
		if not f.startswith('doc'):
			continue
		ifile = open(crawl_dir + f)
		url = ifile.readline()
		words = []
		for l in ifile:
			words += l.strip().split(' ')

		doc_map[f] = url
		words = get_words_after_stemming(words)
		SaveDoc(corpus_dir,f,words)
		ifile.close()

#Ignore stop words and 
def get_words_after_stemming(words):
	stop_words = get_stop_words('english.stopwords.txt')
	for i,word in enumerate(stop_words):
		stop_words[i] = PorterStemmer().stem(word).lower()[1:]
	for i in range(len(words)-1,-1,-1):
		if words[i] in stop_words:
			words.pop(i)
		else:
			words[i] = PorterStemmer().stem(words[i]).lower()
	#print(words)
	return words

def SaveDoc(corpus_dir,fname,words):
	wstr = ''
	for w in words:
		wstr += ' ' + w
	if len(wstr) > 0:
		wstr =wstr[1:]
	ofile = open(corpus_dir  + fname,'w')
	ofile.write(wstr)
	ofile.close()



def get_stop_words(fname):
	return get_words_from_txt_url('http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt')

def get_yahoo_links():
	links_from_yahoo = ['https://www.yahoo.com/news/police-investigations-rehab-new-accusers-latest-harvey-weinstein-saga-171525449.html']
	links_from_yahoo += ['https://www.yahoo.com/news/googles-home-recording-scandal-makes-case-early-adopter-203620207.html']
	links_from_yahoo += ['https://www.yahoo.com/news/pakistan-says-5-western-hostages-held-taliban-freed-121952586.html']
	links_from_yahoo += ['https://finance.yahoo.com/news/ending-nafta-could-cost-u-50-000-auto-133734028.html']
	links_from_yahoo += ['https://www.yahoo.com/news/excruciating-uncertainty-california-wildfires-005459077.html']
	links_from_yahoo += ['https://www.yahoo.com/news/mitch-mcconnell-keeping-senate-rule-165829823.html']
	links_from_yahoo += ['https://www.yahoo.com/news/former-republican-member-congress-apos-093300061.html']
	links_from_yahoo += ['https://www.yahoo.com/news/m/9565e8c1-0a09-3bf3-ac26-ffcb9fe4fa07/ss_why-republicans-are-starting.html']
	links_from_yahoo += ['http://alwaysthere.amicacoverage.com/?utm_source=yahoo&utm_medium=native%20responsive-display&utm_campaign=enterprise17drstandardna&utm_term=st_ros_na%20--%20educated%20consumer%20no%20phone%20number_dbt_25-54%20in%20market%20for%20auto%20home%20life%20insurance_natl_all_nat%20res_oth_ss_cpc_yah&utm_content=204821014_404641132&cm_mmc=Cronin-_-Display-_-Enterprise-_-Native%20Responsive&cm_mmca1=Display']
	links_from_yahoo += ['https://www.yahoo.com/news/california-fire-apos-help-195903029.html']
	return links_from_yahoo


#Save crawled docs here
def save_crawled_doc(crawl_save_dir,link):
	if not os.path.exists(crawl_save_dir):
		os.makedirs(crawl_save_dir)

	if link.endswith('.pdf'):
		words = get_words_from_pdf_url(link)
	elif link.endswith('.txt'):
		words = get_words_from_txt_url(link)
	else:
		words = get_words_from_html(link)
	#print(len(words))
	if len(words) < 50:
		return False
	wstr = link + '\n'
	for w in words:
		wstr += ' ' + w
	c = len(os.listdir(crawl_save_dir)) + 1
	fname = crawl_save_dir + 'doc-' + str(c) + '.txt'
	ofile = open(fname,'w')
	ofile.write(wstr)
	ofile.close()
	return True

def collect_documents(crawl_dir):
	crawled_urls = []
	base_url = 'http://www.memphis.edu/'
	que = Queue()
	que.enqueue(base_url)
	C = 0
	while(que.size() > 0 and C < 10000):
		try:
			url = que.dequeue()
			crawled_urls += [url]
			if not save_crawled_doc(crawl_dir,url):
				continue
			C += 1
			hplinks = get_hyperlinks(url)
			for link in hplinks:
				parsed = urlparse(link)
				if 'memphis.edu' in parsed.netloc and parsed.path not in crawled_urls:
					que.enqueue(link)
		except:
			continue

doc_map = {}
crawl_dir = 'crawl/'
corpus_dir = 'corpus/'
#collect_documents(crawl_dir)
preprocess(crawl_dir,corpus_dir)
inv_idx_dic = get_inv_index(corpus_dir)
print_inv_idx(inv_idx_dic)

print(json.dumps(doc_map))