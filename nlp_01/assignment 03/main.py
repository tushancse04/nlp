from SSBParser import SSBParser
from POS import POS
from unknown_word_handler import unknown_word_handler



parser = SSBParser()
train_clean_file = 'BROWN-clean.pos.txt'
test_clean_file = 'SnapshotBROWN-clean.pos.txt'
parser.gen_clean_file('BROWN.pos.all',train_clean_file)
parser.gen_clean_file('SnapshotBROWN.pos.all.txt',test_clean_file)

print('1(i) : Baseline statistical tagger implemented for entire Brown corpus.')
print('***********************************************************************')

print('1(ii) : Calculating performance for snapshot')
pos = POS(train_clean_file,test_clean_file)
print('***********************************************************************')


print('1(iii) : Calculating performance for news collected from web. please see news.txt to see the input file')
uwh = unknown_word_handler('news.txt','news-clean.txt',pos)
test_clean_file = 'news-clean.txt'
pos = POS(train_clean_file,test_clean_file)
