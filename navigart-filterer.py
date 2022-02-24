#!/usr/bin/env python3
import argparse
import json
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_args():
    parser = argparse.ArgumentParser(description='Filters a Navigart JSON file of its elements whose field matches with the content passed in parameter.')
    parser.add_argument('-f', '--filename', type=str, required=True, help='Specify the JSON file you want to work with (without the .json extension).')
    parser.add_argument('-c', '--field', nargs='?', default='object_type', type=str, required=True, help='Specify the field to be filtered it empty or null.')
    parser.add_argument('-s', '--search', nargs='?', default='peinture', type=str, required=True, help='Specify the search string (peinture, sculpture, picasso, etc.).')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    return parser.parse_args()

def main():
    # Parameters
    args = parse_args()
    param_file = args.filename
    param_field = args.field
    param_search = args.search

    # Set up the storage directory
    try:
        os.path.isfile(param_file + '.json')
    except OSError:
        print ("I can't find the file " % input_file)

    input_file = open(param_file + '.json')
    json_inputfile = json.load(input_file)

    # Let's go!
    # First, we filter on the department name
    print('Total of elements before the search: {} rows.'.format(len(json_inputfile)))
    filtered_file = [elem for elem in json_inputfile if elem[param_field] in param_search]

    print('Total of elements after the search: {} rows.'.format(len(filtered_file)))
    output_file = param_file + '-' + param_search.lower() + '-filtered.json'
    with open(output_file, 'a+') as json_outputfile:
        json_outputfile.write(json.dumps(filtered_file, indent = 4))
        
    # Finished!
    # We close the opened files
    json_outputfile.close()
    input_file.close()

if __name__ == '__main__':
    main()
