#! /usr/bin/env python

# Usage: renameFasta.py seqs.fasta names.table

# Name table is 2-column TSV with old name in col 1 and new name in col 2

import sys


fasta = sys.argv[1]
names = sys.argv[2]

filename = ".".join(fasta.split(".")[:-1])
fileext = fasta.split(".")[-1]

seqNameDict = {}

with open(names, "r") as inNames:
	for line in inNames:
		oldName = line.strip("\n").split("\t")[0]
		if oldName.startswith(">"):
			oldName = oldName.strip(">")
		newName = line.strip("\n").split("\t")[1]
		if newName.startswith(">"):
			newName = newName.strip(">")
		seqNameDict[oldName] = newName
outfile = open("%s_renamed.%s" % (filename, fileext), "w")
with open(fasta, "r") as inSeqs:
	for line in inSeqs:
		if line.startswith(">"):
			oldName = line.strip(">\n")
			try:
				outfile.write(">%s\n" % seqNameDict[oldName])
			except KeyError:
				print("Name missing from conversion table: %s" % oldName)
				exit(1)
		else:
			outfile.write(line)
outfile.close()
