#! /usr/bin/env python

# Usage: addFastaMetadata.py file.fasta metadata
#		addFastaMetadata.py genome.fasta id=6cde96438c2e713efa5c285e4fe3a62d date=2022-11-01
# Appends the given string(s) as metadata to the end of each sequence header line in the provided fasta file.
# If multiple metadata items of provided, they will be separated by a space in the resulting file.

import sys

metadataList = []
fastaFile = sys.argv[1]
fastaFilename = ".".join(fastaFile.split(".")[0:-1])
for arg in sys.argv[2:]:
	metadataList.append(arg)
metadataString=" ".join(metadataList)
with open(fastaFile, "r") as infile, open("%s_renamed.fasta" % fastaFilename ,"w") as outfile:
	for line in infile:
		if line.startswith(">"):
			newLine = "%s %s\n" %(line.strip("\n"), metadataString)
			outfile.write(newLine)
		else:
			outfile.write(line)
