import random

#----------------------------------------------------------------------------
# return a random substring of length n from seq
#----------------------------------------------------------------------------
def random_substr(seq, n):
	if n > len(seq):
		return None
	b = random.randint(0, len(seq)-n)
	return seq[b : b+n]

#----------------------------------------------------------------------------
def random_dna(n, fasta_out = None):
	s = ''.join([ random.choice('ACGT') for i in range(n) ])
	if fasta_out is not None:
		with open(fasta_out, 'w') as f:
			f.write('> Random DNA sequence of length {}\n'.format(n))
			width = 60
			lines = [ s[i : i+width] for i in range(0, len(s), width) ]
			for line in lines:
				f.write('{}\n'.format(line))
	else:
		return s

#----------------------------------------------------------------------------
# Assuming there is only one sequence in the file.  In general, a FASTA file
# may have multiple sequences, separated by ">"
#----------------------------------------------------------------------------
def read_fasta(filename):
	with open(filename, 'r') as f:
		header = f.readline().strip()
		dna = ''.join([ s.strip() for s in f.readlines() ])
		return header, dna

#----------------------------------------------------------------------------
def mutate_one_base(seq, bases):
	options = list(bases)
	i = random.randint(0, len(seq)-1)
	if seq[i] in options:
		options.remove(seq[i])
	s = list(seq)
	s[i] = options[ random.randint(0, len(options)-1) ]
	return ''.join(s)

#----------------------------------------------------------------------------
'''
Create a random DNA sequence of length ref_seq_len
Create n random reads of length read_length
Ref sequence is saved to ref_seq_file
Reads are saved to reads_file
'''
def chop_into_reads(ref_seq_len, n, read_length, ref_seq_file, reads_file):
	seq = random_dna(ref_seq_len)
	with open(ref_seq_file, 'w') as seq_out:
		seq_out.write('> Reference sequence of length {}\n'.format(len(seq)))
		seq_out.write(seq)

	with open(reads_file, 'w') as reads_out:
		for i in range(n):
			j = random.randint(0, len(seq)-read_length)
			reads_out.write('> position: {}, length: {}\n'.format(j,read_length))
			reads_out.write('{}\n'.format(seq[j:j+read_length]))

#----------------------------------------------------------------------------
# return the set of all k-mers of seq:
def all_kmers(seq, k):
	s = set()
	for i in range(0, len(seq)-k+1):
		s.add(seq[i:i+k])
	return s

#----------------------------------------------------------------------------
if __name__ == '__main__':
	# create/save a random DNA sequence of length 10000 and 100 reads of length 50
	# chop_into_reads(10000, 100, 50, 'seq.fasta', 'reads.fasta')
	# print(random_dna(250, "test.fasta"))
	# header, dna = read_fasta('test.fasta')
	# print(header, len(dna))
	# print(dna)
	# for i in range(20):
	# 	print(mutate_one_base('AAAAAAAAAAA', 'ACGT'))
	print(all_kmers('ABCDEFGHI', 4))
