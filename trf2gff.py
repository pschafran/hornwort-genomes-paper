#!/usr/bin/env python
import sys
fname = sys.argv[1]
min_period_size = sys.argv[2]
with open(fname) as fh:
	for line in fh:
		ele = line.strip().split(" ")
		if line.startswith('@'):
			seq_name = ele[0][1:]
		else:
			[start, stop, period, copies, 
			 consensus_size, perc_match, perc_indels, 
			 align_score, perc_A, perc_C, perc_G, perc_T, 
			 entropy, cons_seq, repeat_seq, left_flank, right_flank] = ele
			gff_line = [seq_name, 'TRF', cons_seq + '_' + copies + '_copies',
						start, stop, '.', '.', '.', 'Name='+ cons_seq + '_' + copies + '_copies']
			if int(period) > int(min_period_size):
				print '\t'.join(gff_line)
