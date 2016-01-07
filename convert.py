#!/bin/python
# This tiny script converts a JSON file to a CSV
import json


f = open('../ia_coverage_sample.json', 'r')
parsed_data = []
for line in f.readlines():
    parsed_data.append(json.loads(line))
for key, value in  parsed_data[1].iteritems():
    print "%s \n " % key
    if (isinstance(parsed_data[1][key],dict)):
        for sub_key in parsed_data[1][key].keys():
		print "\t %s" % sub_key  
for key in  parsed_data[1]['Reports'][0].keys():
    print "\t %s " % key
    if key == 'Cell':
	for key in  parsed_data[1]['Reports'][0]['Cell'].keys():
	    print "\t\t %s " % key
print parsed_data[1]['Reports'][0]
