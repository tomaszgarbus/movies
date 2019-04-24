"""
Splits data/dbpedia_infobox/infobox_properties_mapped_en.tql into multiple files.

Places the resulting files in data/dbpedia_infobox/split/.
"""
import os
import re
from tqdm import tqdm

INPUT_FILE = 'data/dbpedia_infobox/infobox_properties_mapped_en.tql'
LINES = 27525174
SPLIT_PATH = 'data/dbpedia_infobox/split'


def get_filename_for_resource_name(rname: str) -> str:
    rname = re.sub('/', '_', rname)
    path = os.path.join(SPLIT_PATH, rname[0])
    return path + '.tql'


if __name__ == '__main__':
    # Iterates all lines from the gigantic file.
    with open(INPUT_FILE) as infile:
        for line in tqdm(infile, total=LINES):
            # Ignores comments.
            if line.startswith('#'):
                continue
            resource_tag = line.split(' ')[0]
            offset = len('<http://dbpedia.org/resource/')
            resource_name = resource_tag[offset:-1]

            filename = get_filename_for_resource_name(resource_name)
            with open(filename, 'a+') as output_file:
                output_file.write(line)
