#!/usr/bin/env python

# Modified by PWS 12 May 2020 to accept filename at commandline and work with RepeatModeler 2
# Usage: extract_unknownLTR.py consensis.fa.classified

from Bio import SeqIO
import re
import sys

infile = sys.argv[1]

def parse_fasta(infile):
	AllSeq = SeqIO.parse(infile, 'fasta')
	return [i for i in AllSeq]

input = parse_fasta(infile)
output_unknown = open('%s.LTRlib.unknown.fa' % infile, 'w')
output_known = open('%s.LTRlib.known.fa' % infile, 'w')

for seq in input:
	if str(seq.id).find('nknown') != -1:
		output_unknown.write('>' + str(seq.id) + '\n' + str(seq.seq) + '\n')
	else:
		output_known.write('>' + str(seq.id) + '\n' + str(seq.seq) + '\n')
	
