#! /usr/bin/python
#
# 2020 January 15. Peter Schafran ps997@cornell.edu

# Usage: convertFastqToFasta.py File.fastq

from Bio import SeqIO
import sys

filename = sys.argv[1]
try:
	if (filename.split(".")[-1]) != "fastq" and (filename.split(".")[-1]) != "fq":
		print("ERROR: NOT A FASTQ FILE")
		exit(1)
	else:
		fileprefix = ".".join(filename.split(".")[0:-1])
		SeqIO.convert(filename,"fastq","%s.fasta" %(fileprefix),"fasta")
except:
	print("ERROR: Something went wrong...this shouldn't happen")
	exit(1)

