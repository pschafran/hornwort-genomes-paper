#! /usr/bin/env python
### Phytozome Version
# This version of the script concatenates the sequence ID with the gene identifier, which is G + a six digit number, with genes at intervals of 100. Numbering restarts on each sequence.
# Usage: renameGTF.py -i file.gtf --contig-table name_table.tsv
# name_table.tsv is a 2-column tab-separated file with the first item in each line as the original contig name, second item is the new contig name
import sys

genePrefix = ""
assemblyID = ""
interval = 100
digits = 6
alternativeLabel = False
badGenes = False

for arg in sys.argv:
	if arg in ["-i","--in"]:
		gtf = sys.argv[sys.argv.index(arg)+1]
	elif arg == "--contig-table":
		renameTable = open(sys.argv[sys.argv.index(arg)+1], "r")
	#elif arg == "--gene-prefix":
	#	genePrefix = sys.argv[sys.argv.index(arg)+1]
	elif arg == "--assembly-id":
		assemblyID = sys.argv[sys.argv.index(arg)+1]
	#elif arg =="--interval":
	#	interval = int(sys.argv[sys.argv.index(arg)+1])
	elif arg =="--digits":
		digits = int(sys.argv[sys.argv.index(arg)+1])
	elif arg =="--alt":
		alternativeLabel = True
	elif arg =="--bad-genes":
		badGenes = True
		bad_genes = open(sys.argv[sys.argv.index(arg)+1], "r")


gtfFilename = ".".join(gtf.split(".")[0:-1])
outfile = open("%s_renamed.gtf" % gtfFilename, "w")
outputConversionTable = open("%s_renamed.gene_conversion.tsv" % gtfFilename, "w")
outputTranscriptConverstion = open("%s_renamed.transcript_conversion.tsv" % gtfFilename, "w")
if len(assemblyID) >= 1:
	outfile.write("#assembly ID = %s\n" % assemblyID)

renameDict = {}
#contigOrderList = []
for line in renameTable:
	oldContig = line.strip("\n").split("\t")[0]
	oldContig = oldContig.split(" ")[0]
	newContig = line.strip("\n").split("\t")[1]
	newContig = newContig.split(" ")[0]
	renameDict[oldContig] = newContig
#	contigOrderList.append(oldContig)

if badGenes == True:
	badGenesList = []
	badTranscriptsList = []
	for line in bad_genes:
		badGenesList.append(".".join(line.split(".")[0:-1]))
		badTranscriptsList.append(line.strip("\n"))

gtfDict = {}
with open(gtf, "r") as ingtf:
	for line in ingtf:
		line = line.strip("\n")
		if not line.startswith("#"):
			contig = line.split("\t")[0]
			if contig not in gtfDict.keys():
				gtfDict.update({contig : {"startPosDict" : {}}})
				gtfDict[contig].update({"startPosList" : []})
				gtfDict[contig].update({"sortedGeneList" : []})
			feature = line.split("\t")[2]
			startPos = int(line.split("\t")[3])
			description = line.strip(";").split("\t")[8]
			if feature != "gene":
				pass
			else:
				gene_id = description
				if startPos not in gtfDict[contig]["startPosList"]:
					gtfDict[contig]["startPosList"].append(startPos)
				try:
					gtfDict[contig]["startPosDict"][startPos].append(gene_id)
				except:
					gtfDict[contig]["startPosDict"].update({startPos : [gene_id]})
		else:
			pass
for contig in gtfDict:
	sortedStartPos = sorted(gtfDict[contig]["startPosList"])
	for item in sortedStartPos:
		if len(gtfDict[contig]["startPosDict"][item]) == 1:
			gtfDict[contig]["sortedGeneList"].append(gtfDict[contig]["startPosDict"][item][0])
		else:
			for subitem in gtfDict[contig]["startPosDict"][item]:
				gtfDict[contig]["sortedGeneList"].append(subitem)
conversionDict = {}
for contig in gtfDict:
	counter = 0
	for sorted_gene in gtfDict[contig]["sortedGeneList"]:
		counter = interval + counter
		if len(str(counter)) > digits:
			print("WARNING: Gene number exceeds number of digits. %s %s" %(contig,counter))
		formattedCounter = '{num:0{width}}'.format(num=counter, width=digits)
		genePrefix = renameDict[contig]
		if alternativeLabel == False:
			newGene = "%sG%s" % (genePrefix, formattedCounter)
		else:
			newGene = "%sREG%s" % (genePrefix, formattedCounter)
		conversionDict.update({sorted_gene : newGene})
with open(gtf, "r") as ingtf:
	for line in ingtf:
		line = line.strip("\n")
		if not line.startswith("#"):
			contig = line.split("\t")[0]
			source = line.split("\t")[1]
			feature = line.split("\t")[2]
			startPos = line.split("\t")[3]
			startPos = startPos.strip(" ")
			endPos = line.split("\t")[4]
			endPos = endPos.strip(" ")
			score = line.split("\t")[5]
			score = score.strip(" ")
			strand = line.split("\t")[6]
			strand = strand.strip(" ")
			frame = line.split("\t")[7]
			frame = frame.strip(" ")
			description = line.strip(";").split("\t")[8]
			newContig = renameDict[contig]
			if feature != "gene":
				if source == "GUSHR" and feature == "transcript":
					transcript_id = description.split(".")[0]
					transcript_number = description.split(".")[1]
					gene_id = transcript_id
				else:
					splitDescription = description.split("; ")
					for item in splitDescription:
						splitSplitDescription = item.split(" ")
						if splitSplitDescription[0] == "transcript_id":
							transcript_id = splitSplitDescription[1].strip('''"''')
							transcript_number = transcript_id.split(".")[1]
						elif splitSplitDescription[1] == "gene_id":
							gene_id = splitSplitDescription[1].strip('''"''')
				newGene = conversionDict[gene_id]
				newTranscript = "%s.%s" % (conversionDict[gene_id], transcript_number)
				outfile.write('''%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\ttranscript_id "%s"; gene_id "%s"\n''' %(newContig, source, feature, startPos, endPos, score, strand, frame, newTranscript, newGene ))
				if badGenes == True and (gene_id in badGenesList or transcript_id in badTranscriptsList):
					outfile.write('''%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\ttranscript_id "%s"; gene_id "%s"; pseudo "true"\n''' %(newContig, source, feature, startPos, endPos, score, strand, frame, newTranscript, newGene ))
				outputTranscriptConverstion.write("%s\t%s\n" % (transcript_id, newTranscript))
			else:
				gene_id = description
				newGene = conversionDict[gene_id]
				if badGenes == True:
					if gene_id in badGenesList:
						newGene = '''%s; pseudo "true"''' % newGene
				outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(newContig, source, feature, startPos, endPos, score, strand, frame, newGene ))
				outputConversionTable.write("%s\t%s\n" % (gene_id, newGene))
		else:
			outfile.write("%s\n" % line)
renameTable.close()
outfile.close()
outputConversionTable.close()
try:
	bad_genes.close()
except:
	pass
