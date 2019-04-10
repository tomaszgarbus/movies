"""
Provides an abstraction level over DBPedia infoboxes properties dataset.
"""
import re
import os
from tqdm import tqdm


class DBPediaHelper:
    INPUT_FILE = 'data/dbpedia_infobox/infobox_properties_mapped_en.tql'
    LINES = 27525174
    SPLIT_PATH = 'data/dbpedia_infobox/split'

    def __init__(self):
        pass

    @staticmethod
    def get_filename_for_resource_name(rname: str) -> str:
        """
        Gets the filename and path for the file containing the resource named |rname|.

        :param rname: resource name
        :return: string - a relative path to the file containing the resource of name |rname|
        """
        rname = re.sub('/', '_', rname)
        path = os.path.join(DBPediaHelper.SPLIT_PATH, rname[0])
        return path + '.tql'

    @staticmethod
    def perform_split():
        """
        Splits the original .tql file into parts.

        Each part is identified by the first character of resource name. In other words, resources are grouped by the
        first character of the name and split into files accordingly.
        """
        # Iterates all lines from the gigantic file.
        with open(DBPediaHelper.INPUT_FILE) as infile:
            for line in tqdm(infile, total=DBPediaHelper.LINES):
                # Ignores comments.
                if line.startswith('#'):
                    continue
                resource_tag = line.split(' ')[0]
                offset = len('<http://dbpedia.org/resource/')
                resource_name = resource_tag[offset:-1]

                filename = DBPediaHelper.get_filename_for_resource_name(resource_name)
                with open(filename, 'a+') as output_file:
                    output_file.write(line)
