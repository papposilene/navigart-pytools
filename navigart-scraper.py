#!/usr/bin/env python3
import argparse
import json
import requests
import time

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
    parser = argparse.ArgumentParser(description='Scrape the Navigart internal API for retrieving all public data into an output file.')
    parser.add_argument('-m', '--museum', nargs='?', default='museum', type=str, required=False, help='Choose a name of the museum for the output file name (default: museum).')
    parser.add_argument('-s', '--start', nargs='?', default=0, type=int, required=False, help='choose a start page (default: 0).')
    parser.add_argument('-l', '--limit', nargs='?', default=1000, type=int, required=False, help='choose a limit by page (default: 1000).')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    return parser.parse_args()

def create_entry():
    return {
        "id": None,
        #"index": None,
        "department": None, # collection_department
        # Artist: array() authors
        "artist_id": None, # authors.*._id
        "artist_type": None, # authors.*.type
        "artist_name": None, # authors.*.notice
        "artist_date": None, # authors_birth_death ("1866, Moscou (Russie, Empire Russe) - 1944, Neuilly-sur-Seine (Seine, France)")
        "artist_gender": None, # authors.*.gender
        # Object
        "object_inventory": None, # inventory
        "object_title": None, # title_notice
        "object_date": None, # date_creation
        "object_type": None, # domain
        "object_technique": None, # domain_description_mst
        "object_height": None, # dimensions ("92 x 73 cm")
        "object_width": None,
        "object_depth": None,
        "object_weight": None,
        "object_copyright": None, # copyright
        # Metadata
        "art_movement": None, # key_words_movement
        "acquisition_type": None, # acquisition_mode
        "acquisition_date": None, # acquisition_year
    }

def main():
    # Initialization

    fieldnames = [
        'id', 'department',
        'artist_id', 'artist_type', 'artist_name', 'artist_date', 'artist_gender',
        'object_inventory', 'object_title', 'object_date', 'object_type', 'object_technique',
        'object_height', 'object_width', 'object_depth', 'object_weight', 'object_copyright',
        'art_movement', 'acquisition_type', 'acquisition_date'
    ]

    args = parse_args()
    num_rows = 0

    # https://api.navigart.fr/15/artworks?sort=by_inv&size=1000&from=0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    api_limit = args.limit
    api_start = args.start
    api_infos = requests.get('https://api.navigart.fr/15/artworks?sort=by_inv&size=1&from=0', headers=headers)
    navigart_info = api_infos.json()
    print(f"{bcolors.HEADER}Total of available objects:", navigart_info['filteredCount'], f"{bcolors.ENDC}")

    for num_rows in range(num_rows, navigart_info['filteredCount'], 1):
        navigart = requests.get('https://api.navigart.fr/15/artworks?sort=by_inv&size=' + str(api_limit) + '&from=' + str(api_start), headers=headers)
        print(f"{bcolors.WARNING}HTTP Status:", navigart.status_code, f"{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Page number:", api_start, f"{bcolors.ENDC}")
        navigart_json = navigart.json()

        for navigart_data in navigart_json['results']:
            print(f"{bcolors.OKGREEN}Retrieving row #", num_rows, f"{bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}Retrieving data for object #", navigart_data['_source']['ua']['artwork']['_id'], "(", navigart_data['_source']['ua']['artwork']['title_notice'], f").{bcolors.ENDC}")

            entry = create_entry()

            entry['id'] = navigart_data['_source']['ua']['artwork']['_id']
            if 'collection_department' in navigart_data['_source']['ua']['artwork']:
                entry['department'] = navigart_data['_source']['ua']['artwork']['collection_department']
            else:
                entry['department'] = 'Inconnu'

            # Artist
            for author in navigart_data['_source']['ua']['authors']:
                if '_id' in author: entry['artist_id'] = author['_id']
                if 'type' in author: entry['artist_type'] = author['type']
                if 'name' in author: entry['artist_name'] = author['name']['notice']
                if 'gender' in author: entry['artist_gender'] = author['gender']

            # Object
            if 'inventory' in navigart_data['_source']['ua']['artwork']:
                entry['object_inventory'] = navigart_data['_source']['ua']['artwork']['inventory']
            if 'title_notice' in navigart_data['_source']['ua']['artwork']:
                entry['object_title'] = navigart_data['_source']['ua']['artwork']['title_notice']
            if 'date_creation' in navigart_data['_source']['ua']['artwork']:
                entry['object_date'] = navigart_data['_source']['ua']['artwork']['date_creation']
            if 'domain' in navigart_data['_source']['ua']['artwork']:
                entry['object_type'] = navigart_data['_source']['ua']['artwork']['domain']
            if 'domain_description_mst' in navigart_data['_source']['ua']['artwork']:
                entry['object_technique'] = navigart_data['_source']['ua']['artwork']['domain_description_mst']
            if 'dimensions' in navigart_data['_source']['ua']['artwork']:
                entry['object_height'] = navigart_data['_source']['ua']['artwork']['dimensions']
            if 'dimensions' in navigart_data['_source']['ua']['artwork']:
                entry['object_width'] = navigart_data['_source']['ua']['artwork']['dimensions']
            if 'dimensions' in navigart_data['_source']['ua']['artwork']:
                entry['object_depth'] = navigart_data['_source']['ua']['artwork']['dimensions']
            if 'dimensions' in navigart_data['_source']['ua']['artwork']:
                entry['object_weight'] = navigart_data['_source']['ua']['artwork']['dimensions']
            if 'copyright' in navigart_data['_source']['ua']['artwork']:
                entry['object_copyright'] = navigart_data['_source']['ua']['artwork']['copyright']

            # Metadata
            if 'key_words_movement' in navigart_data['_source']['ua']['artwork']:
                entry['art_movement'] = navigart_data['_source']['ua']['artwork']['key_words_movement']
            if 'acquisition_mode' in navigart_data['_source']['ua']['artwork']:
                entry['acquisition_type'] = navigart_data['_source']['ua']['artwork']['acquisition_mode']
            if 'acquisition_year' in navigart_data['_source']['ua']['artwork']:
                entry['acquisition_date'] = navigart_data['_source']['ua']['artwork']['acquisition_year']


            output_file = './data/' + args.museum + '-' + api_start + '.json'
            with open(output_file, 'a+') as json_outputfile:
                json_outputfile.write(json.dumps(entry, indent = 4))
                json_outputfile.close()

            num_rows += 1

        api_start = api_start + api_limit
        print('Just wrote {} rows.'.format(num_rows))
        print('Waiting for next round, starting at {}.'.format(api_start))
        time.sleep(5)

    print('Wrote a total of {} rows.'.format(num_rows))

if __name__ == '__main__':
    main()
