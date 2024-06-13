#! /usr/bin/python

import sys
from Bio import SeqIO

fasta = sys.argv[1]

outfile = open("%s_sequence_lengths.tmp" %fasta, "w")

seqIndex = SeqIO.index(fasta, "fasta")
for key in seqIndex:
	record = seqIndex[key]
	outfile.write("%s\t%s\n" %(record.id, len(record.seq)))	
outfile.close()
outputfilename = "%s_sequence_lengths.tmp" %fasta
print("sort -k2,2nr %s > %s.sorted.tmp " %(outputfilename, outputfilename))
print(r'''awk -F"\t" -v i="1" '{ print $1"\tcontig_"i++ }' %s.sorted.tmp > %s.new_contig_names.tsv''' %(outputfilename, outputfilename))
