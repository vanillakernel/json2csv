#!/bin/python
# This tiny script converts a JSON file to a CSV
import json


f = open('../ia_coverage_sample.json', 'r')
parsed_data = []
device_id = None
cell_id = None
for line in f.readlines():
    parsed_data.append(json.loads(line))
for key, value in  parsed_data[1].iteritems():
    print "%s \n " % key
    if (key == 'DeviceId'):
	device_id =value
    if (isinstance(parsed_data[1][key],dict)):
        for sub_key in parsed_data[1][key].keys():
		print "\t %s" % sub_key  
for key in  parsed_data[1]['Reports'][0].keys():
    parsed_data[1]['Reports'][0]['device_id'] = device_id
    print "\t %s " % key
    if key == 'Cell':
	for key in  parsed_data[1]['Reports'][0]['Cell'].keys():
	    cell_id = parsed_data[1]['Reports'][0]['Cell']['CellId']
	    parsed_data[1]['Reports'][0]['c_id'] = cell_id
	    print "\t\t %s " % key
print parsed_data[1]
print parsed_data[1]['Reports'][0]
