#!/bin/python
# This tiny script converts a JSON file to a CSV
import json


# The first time this is run, records will be initialized as an empty array.
# As it traverses each line, it accumulates records. When done, it returns them.

def unpack_json(json_line, records=[]):
    if (isinstance(json_line,list)):
	for item in json_line:
	    unpack_json(item)
    
    if (isinstance(json_line,dict)):
	for key, value in  json_line.iteritems():
	    if (key == 'DeviceId'):
		device_id = value   
	    if (key == 'Reports'): 
		# Add the device id and the cell id to records.
		# This will be important in the new flattened schema.
		for report in json_line[key]:
		    report['c_id']  = report['Cell']['CellId']
		    report['device_id']  = device_id
		    records.append(report)
	    if (isinstance(value,dict)):
		for sub_key in json_line[key].keys():
		    unpack_json(value)
	    if (isinstance(value,list)):
		for item in json_line[key]:
		    unpack_json(value)
    return records    
    

f = open('../ia_coverage_sample.json', 'r')
parsed_data = []
for line in f.readlines(): # This will start from the bottom of the input file.
    parsed_data.append(json.loads(line))
records = unpack_json(parsed_data[0])
for record in records:
    print record
