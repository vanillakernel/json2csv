#!/bin/python
# This tiny script converts a JSON file to a CSV
import json
import numpy as np
import csv

# The first time this is run, records will be initialized as an empty array.
# As it traverses each line, it accumulates records. When done, it returns them.

def unpack_json(json_lines, reports=[], cells=[], device_details=[]):
    reports = np.array([np.array(d['Reports']) for d in json_lines])
    device_details = np.array([d["DeviceInfo"] for d in json_lines])
    cells = np.zeros(sum([len(report) for report in reports]), dtype='object')
    tot_cells = 0
    for idx, line in enumerate(json_lines):
        device_id = line["DeviceId"]
        for report in reports[idx]:
            report['c_id'] = report['Cell']['CellId']
            report['device_id'] = device_id
            cells[tot_cells] = report['Cell']
            report.pop("Cell", None)
            tot_cells += 1
        device_details[idx]['device_id'] = device_id    
    reports = np.hstack(reports[:])
    return (reports,cells,device_details)
    
def store_cells(cells, basename, outpath):
    unique_cells = {v['CellId']:v for v in cells if v != 0}.values() # uniquify them
    f = open(path.join(outpath, basename + '_cells.csv'), 'w')
    #f.write(unique_cells[0].keys()) #Get the csv headers
    i = 0
    try:
	writer = csv.writer(f)
	# Use first row to get headers. Likely just for debug.
	print ','.join('"{}"'.format(key) for key, val in unique_cells[0].items() )
	#writer.writerow( unique_cells[0].keys() )
	for record in unique_cells :
	    
	    writer.writerow ([i+1] + [str(val) for key, val in record.items()])
	    i+=1

	    #print ', '.join(value for key, value in record.iteritems())
	    #writer.writerow( (i+1)
    finally:
	    f.close()
    print "Wrote %r unique cells to Cells.json" % len(unique_cells)	
 
def store_devices(device_details, basename, outpath):
    unique_devices = {v['device_id']:v for v in device_details}.values()#uniquem
    f = open(path.join(outpath, basename + '_devices.csv'), 'w')
    #f.write(unique_cells[0].keys()) #Get the csv headers
    i = 0
    try:
	writer = csv.writer(f)
	# Use first row to get headers. Likely just for debug.
	print ','.join('"{}"'.format(key) for key, val in unique_devices[0].items() )
	#writer.writerow( unique_cells[0].keys() )
	for record in unique_devices :
	    
	    writer.writerow ([i+1] + [str(val) for key, val in record.items()])
	    i+=1

	    #print ', '.join(value for key, value in record.iteritems())
	    #writer.writerow( (i+1)
    finally:
	    f.close()
 
    print "I would store %r unique devices." % len(unique_devices)	

def store_reports(reports, basename, outpath):
    f = open(path.join(outpath, basename + '_reports.csv'), 'w')
    #f.write(unique_cells[0].keys()) #Get the csv headers
    i = 0
    try:
	writer = csv.writer(f)
	# Use first row to get headers. Likely just for debug.
	print ','.join('"{}"'.format(key) for key, val in reports[0].items() )
	#writer.writerow( unique_cells[0].keys() )
	for record in reports:
	    
	    writer.writerow ([i+1] + [str(val) for key, val in record.items()])
	    i+=1

	    #print ', '.join(value for key, value in record.iteritems())
	    #writer.writerow( (i+1)
    finally:
	    f.close()
 
    print "I would store %r reports." % len(reports)	


def main(filename, outpath):
    f = open(filename, 'r')
    basename = path.basename(path.splitext(filename)[0])
    parsed_data = []
    loads = json.loads
    parsed_data = np.array([loads(line) for line in f])
    reports, cells, devices = unpack_json(parsed_data)
    store_reports(reports, basename, outpath)
    store_cells(cells, basename, outpath)
    store_devices(devices, basename, outpath)
    #for report in reports:
#	print report

if __name__ == "__main__":
    from optparse import OptionParser
    from os import path, listdir
    parser = OptionParser()
    parser.add_option('-f', '--filename')
    parser.add_option('-d', '--dirname')
    parser.add_option('-o', '--outpath')
    options, args = parser.parse_args()
    if options.dirname:
        for file in listdir(path.abspath(options.dirname)):
            main(path.abspath(path.join(options.dirname, file)),path.abspath(options.outpath))
    else:
        main(path.abspath(options.filename), path.abspath(options.outpath))
