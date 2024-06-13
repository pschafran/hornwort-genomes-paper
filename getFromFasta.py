#! /usr/bin/env python
'''Command Line:
getFromFasta.py [--inverse] sourceFile.fasta seqID[.txt]
OR
pipeline | getFromFasta.py [--inverse] sourceFile.fasta - [ > outfile.fasta ]

--inverse option returns fasta with all sequences EXCEPT the one(s) specified

FASTA formatted sequences output to STDOUT
Names of any missing sequences are output to STDERR
'''
import sys
import os.path

if "--inverse" in sys.argv:
	mode = "inverse"
	scaffoldFile = sys.argv[2]
	scaffoldID = sys.argv[3]
	inverseList = []
else:
	mode = "normal"
	scaffoldFile = sys.argv[1]
	scaffoldID = sys.argv[2]
openInFile = open(scaffoldFile, "r")

sourceDict = {}

for line in openInFile:
	if line.startswith(">"):
		lineName = line.strip(">\n").split(" ")[0]
		sourceDict.update({lineName : []})
		try:
			seq = "".join(sourceDict[previousLineName])
			sourceDict[previousLineName] = seq
		except:
			pass
	else:
		previousLineName = lineName
		sourceDict[lineName].append(line.strip("\n"))
seq = "".join(sourceDict[previousLineName])
sourceDict[previousLineName] = seq
missingList = []
if os.path.isfile(scaffoldID):
	infile = open(scaffoldID, "r")
	for line in infile:
		if line.startswith("#"):
			pass
		else:
			name = line.strip(">\n").split(" ")[0]
			if mode == "inverse":
				inverseList.append(name)
			else:
				try:
					print(">" + name + "\n" + sourceDict[name])
					#print(sourceDict[name])
				except:
					missingList.append(name)
elif scaffoldID != "-":
	name = scaffoldID.strip(">\n").split(" ")[0]
	if mode == "inverse":
		inverseList.append(name)
	else:
		try:
			print(">" + name + "\n" + sourceDict[name])
			#print(sourceDict[name])
		except:
			missingList.append(name)
elif scaffoldID == "-":
	for line in sys.stdin:
		if line.startswith("#"):
			pass
		else:
			name = line.strip(">\n").split(" ")[0]
			if mode == "inverse":
				inverseList.append(name)
			else:
				try:
					print(">" + name + "\n" + sourceDict[name])
	#				print(sourceDict[name])
				except:
					missingList.append(name)
if mode == "inverse":
	for seq in sourceDict:
		if seq not in inverseList:
			try:
				print(">" + seq + "\n" + sourceDict[seq])
#				print(sourceDict[name])
			except:
				missingList.append(name)

if len(missingList) >= 1:
	print("Missing in source FASTA:", file=sys.stderr)
	print(missingList, file=sys.stderr)

openInFile.close()
