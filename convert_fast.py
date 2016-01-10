#!/bin/python
# This tiny script converts a JSON file to a CSV
import json


# The first time this is run, records will be initialized as an empty array.
# As it traverses each line, it accumulates records. When done, it returns them.

def unpack_json(json_line, reports=[], cells=[], device_details=[]):
    
    if (type(json_line) is list):
	for item in json_line:
	    unpack_json(item)
    
    if (type(json_line) is dict):
	for key, value in  json_line.iteritems():
	    if (key == 'DeviceId'):
		device_id = value   
		json_line['DeviceInfo']['device_id']  = device_id
	    if (key == 'Reports'): 
		# Add the device id and the cell id to records.
		# This will be important in the new flattened schema.
		for report in json_line[key]:
		    report['c_id']  = report['Cell']['CellId']
		    report['device_id']  = device_id
		    reports.append(report)
	    if (key == 'Cell'): # Collect cells for separate table. 
		cells.append(value)
	    if (key == 'DeviceInfo'): # Collect for separate table. 
		device_details.append(value)
	    if (type(value) is dict):
		for sub_key in json_line[key].keys():
		    unpack_json(value)
	    if (type(value) is list):
		for item in json_line[key]:
		    unpack_json(value)
    
    return (reports,cells,device_details)
    
def store_cells(cells):
    unique_cells = {v['CellId']:v for v in cells}.values() # uniquify them
    print "I would store %r unique cells." % len(unique_cells)	

def store_devices(device_details):
    unique_devices = {v['device_id']:v for v in device_details}.values()#uniquem
    print "I would store %r unique devices." % len(unique_devices)	

def store_reports(reports):
    print "I would store %r reports." % len(reports)	


def main():
    f = open('../ia_coverage_sample.json', 'r')
    parsed_data = []

    for line in f.readlines(): # This will start from the bottom of the input file.
     parsed_data.append(json.loads(line))

    for line in parsed_data:
	result_tuple = unpack_json(line)

    reports, cells, devices = result_tuple

    store_reports(reports)
    store_cells(cells)
    store_devices(devices)
    #for report in reports:
#	print report

if __name__ == "__main__":
            main()
