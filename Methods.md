# Hornwort Genomes Paper

## Methods
1. Sampling and Cultivation
2. DNA and RNA Sequencing
3. Genome Assembly and Scaffolding
4. Annotation
 	4a. Gene Models
	4b. Repetitive Elements
	4c. Methylation
5. Orthogroups
6. Gene Family Expansion/Contraction
7. Synteny
	7a. Within hornworts
	7b. Within bryophytes
	7c. Chromosome evolution
8. Pangenome
9. WGD
10. Horizontal Gene Transfer
11. Stomatal Gene Expression
12. Cyanobacterial Symbiosis
13. GID1-DELLA
14. Anthocyanin pathway
15. Pyrenoid genes
16. LTR taxonomy, distributions, ages

### Sampling and Cultivation
Sporophytes were collected from the wild (Table 1). Depending on size, one to three sporophytes were macerated with forceps in 1.5 mL centrifuge tubes containing 1 mL of 0.1% Tween in sterile water, vortexed for 30 seconds, then centrifuged at 5000 RPM for 5 minutes to pull down spores. Sporophyte debris was removed, then the supernatant pipetted off. One mL of sterile water was added to the spore pellet, vortexed for 30 seconds, then centrifuged as above and the water removed. This washing was repeated three times. Spores were resuspended in 30 uL of sterile water and split into 10 uL aliquots. Aliquots were added to 50 uL of 2.5%, 5%, and 10% dilutions of commercial bleach, vortexed for five seconds, and let sit for one minute. After one minute, 50 uL of sterile 0.1 M sodium thiosulfate was added and immediately vortexed for five seconds to quench the reaction.

### DNA and RNA Sequencing

### Genome Assembly and Scaffolding
ONT reads less than 5 kbp were removed and the remainder were assembled with Flye v2.9. Contigs were corrected with Illumina DNA sequence data using Pilon v1.24. HiC libraries were prepared, sequenced, and scaffolded by Phase Genomics (Seattle, WA). TGS-Gapcloser was used to fill gaps between scaffolds with ONT reads and polish filled gaps with Illumina data. 
