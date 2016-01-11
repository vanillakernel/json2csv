#!/bin/python
# This tiny script converts a JSON file to a CSV
import json
import numpy as np

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
            tot_cells += 1
        device_details[idx]['device_id'] = device_id    
    reports = np.hstack(reports[:])
    return (reports,cells,device_details)
    
def store_cells(cells):
    unique_cells = {v['CellId']:v for v in cells if v != 0}.values() # uniquify them
    print "I would store %r unique cells." % len(unique_cells)	

def store_devices(device_details):
    unique_devices = {v['device_id']:v for v in device_details}.values()#uniquem
    print "I would store %r unique devices." % len(unique_devices)	

def store_reports(reports):
    print "I would store %r reports." % len(reports)	


def main():
    f = open('./ia_coverage_sample.json', 'r')
    parsed_data = []
    loads = json.loads
    parsed_data = np.array([loads(line) for line in f])
    reports, cells, devices = unpack_json(parsed_data)
    store_reports(reports)
    store_cells(cells)
    store_devices(devices)
    #for report in reports:
#	print report

if __name__ == "__main__":
            main()
