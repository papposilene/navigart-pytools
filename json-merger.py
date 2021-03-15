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
    parser = argparse.ArgumentParser(description='Merge all JSON files in a given folder.')
    parser.add_argument('-f', '--folder', type=str, required=True, help='Choose a folder.')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    return parser.parse_args()

def main():
    # Initialization
    args = parse_args()
    path = './' + args.folder
    result = []

    print(f"{bcolors.HEADER}Folder:", path, f"{bcolors.ENDC}")

    for file in os.listdir(path):
        if file.endswith('.json'):
            to_merge = os.path.join(path, file)
            print(f"{bcolors.OKCYAN}Found the file", to_merge, f"{bcolors.ENDC}")
            with open(to_merge, "rb") as infile:
                result.extend(json.load(infile))

    with open(path + '/merged_file.json', 'w') as json_outputfile:
        json_outputfile.write(json.dumps(result, indent = 4))
        json_outputfile.close()

    print(f"{bcolors.OKGREEN}Merged all JSON files.{bcolors.ENDC}")

if __name__ == '__main__':
    main()
