#!/usr/bin/python

import re
import sys

segment_mod = False
segment_data = []
remove_count = 0

# set io files
file_input = sys.argv[1]
file_output = re.sub('.gcode$', '.mmu-fix.gcode', file_input)
if (file_output == file_input):
	file_output = "{}.mmu-fix".format(file_input)


def segment_check():
	global remove_count
	global segment_data
	global output
	
	# search from end of segment
	output_data = []
	segment_data.reverse()
	found_move = False
	
	# remove all non-extrusion lines up to "last" extrusion
	for line in segment_data:
		m = re.search('^G1\s+[X|Y]', line)
		if (m  and  'E' in line):
			found_move = True
		if (m  and  not found_move):
			remove_count = remove_count + 1
			print "Remove WIPE: {}".format(line)
			continue
		output_data.append(line)
	
	# output entire segment
	output_data.reverse()
	for line in output_data:
		print >> output, line



with open(file_input) as input:
	with open(file_output, 'w') as output:
		for line in input:
			line = line.strip()
			
			# switch on segment
			if (re.search('CP TOOLCHANGE WIPE', line)  or  re.search('CP EMPTY GRID START', line)  or  re.search('CP WIPE TOWER FIRST LAYER BRIM START', line)):
				segment_mod = True
			
			# switch off segment
			if (re.search('CP TOOLCHANGE END', line)  or  re.search('CP EMPTY GRID END', line)  or  re.search('CP WIPE TOWER FIRST LAYER BRIM END', line)):
				segment_mod = False
				segment_check()
				segment_data = []
			
			# don't output if inside segment to modify
			if (segment_mod):
				segment_data.append(line)
				continue
			
			# normal output; copy to new file
			print >> output, line



print "Removed {} extra move lines from {}".format(remove_count, file_output)
