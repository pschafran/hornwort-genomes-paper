#! /usr/bin/python
# Script used in genomeMaker.sh pipeline to rename and reorder assemblies from longest to shortest contig. Uses col 2 in names.table as the sort order
# Usage: renameFastaAndSort.py seqs.fasta names.table

# Name table is 2-column TSV with old name in col 1 and new name in col 2

import sys
from Bio import SeqIO

fasta = sys.argv[1]
names = sys.argv[2]

def wrapLine(string, width = 80):
	return [string[i:i+width] for i in range(0, len(string), width)]

filename = ".".join(fasta.split(".")[:-1])
fileext = fasta.split(".")[-1]

record_dict = SeqIO.to_dict(SeqIO.parse(fasta, "fasta"))

with open(names, "r") as inNames:
	with open("%s_renamed.%s" % (filename, fileext), "w") as outfile:
		for line in inNames:
			oldName = line.strip("\n").split("\t")[0]
			newName = line.strip("\n").split("\t")[1]
			outfile.write(">%s\n" % newName)
			wrappedline = wrapLine(record_dict[oldName].seq)
			for j in wrappedline:
				outfile.write("%s\n" % j)
