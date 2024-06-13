#! /home/ps997/miniconda3/bin/python
# Needs to run with python 3 on our server!!!
#

from Bio import SeqIO
from collections import OrderedDict
from datetime import datetime
import sys

assemblyfiles = sys.argv[1:]
plotAUNdict = {}

def computeAUN(assemblyfile):
	seqLengthDict = {}
	assemblyLength = 0
	inputFastaDict = SeqIO.index(assemblyfile, "fasta")
	for key in inputFastaDict.keys():
		seqLengthDict[key] = int(len(inputFastaDict[key].seq))
		assemblyLength += int(len(inputFastaDict[key].seq))
	auN = 0
	for key in seqLengthDict.keys():
		percentLength = (float(seqLengthDict[key])/float(assemblyLength))*100
		auN += seqLengthDict[key]*percentLength
	print("%s\t%.3f" %(assemblyfile, auN))
	
def plotAUN(assemblyfile):
	seqLengthDict = {}
	recordCounter = 0
	assemblyLength = 0
	inputFastaDict = SeqIO.index(assemblyfile, "fasta")
	for key in inputFastaDict.keys():
		seqLengthDict[key] = int(len(inputFastaDict[key].seq))
		assemblyLength += int(len(inputFastaDict[key].seq))
	sortedSeqDict = OrderedDict(sorted(seqLengthDict.items(), key = lambda item: item[1], reverse=True))
	xList = []
	yList = []
	yListKbp = []
	plotAUNdict[assemblyfile] = {"xList":[]}
	plotAUNdict[assemblyfile].update({"yList":[]})
	plotAUNdict[assemblyfile].update({"yListKbp":[]})
	percentSum = 0
	sumXCounter = 0.000
	for key in sortedSeqDict.keys():
		xCounter = 0.001
		percentLength = (float(sortedSeqDict[key])/float(assemblyLength))*100
		percentSum += percentLength
		while xCounter < percentLength:
			xList.append("%.3f" % sumXCounter)
			yList.append(sortedSeqDict[key])
			yListKbp.append(float(sortedSeqDict[key])/float(1000))
			plotAUNdict[assemblyfile]["xList"].append("%.3f" % sumXCounter)
			plotAUNdict[assemblyfile]["yList"].append(sortedSeqDict[key])
			plotAUNdict[assemblyfile]["yListKbp"].append(float(sortedSeqDict[key])/float(1000))
			xCounter += 0.001
			sumXCounter += 0.001
	import matplotlib.pyplot as plt
	import matplotlib.ticker as mtick
	fig = plt.figure(1, (7,4))
	ax = fig.add_subplot(1,1,1)
	ax.plot(xList, yListKbp)
	ax.xaxis.set_major_locator(plt.MaxNLocator(12))
	ax.set_xticklabels(['0%','0%', '10%','20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
	plt.ylabel("Contig Length (kbp)")
	plt.title("%s" %(assemblyfile))
	plt.savefig("%s_Nx.pdf" %(assemblyfile), format="pdf")
	plt.close()

for assemblyfile in assemblyfiles:
	computeAUN(assemblyfile)
for assemblyfile in assemblyfiles:
	plotAUN(assemblyfile)

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
fig = plt.figure(1, (7,4))
ax = fig.add_subplot(1,1,1)
for key in plotAUNdict.keys():
	ax.plot(plotAUNdict[key]["xList"], plotAUNdict[key]["yListKbp"], label=key)
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.set_xticklabels(['0%','0%', '10%','20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
plt.ylabel("Contig Length (kbp)")
plt.title("Nx")
ax.legend(loc="upper right", fontsize="x-small")
plt.savefig("grouped_Nx.png", format="png")
plt.savefig("grouped_Nx.pdf", format="pdf")
plt.close()
