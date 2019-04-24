"""
Provides an abstraction level over DBPedia infoboxes properties dataset.
"""
import os
import re
from tqdm import tqdm
from typing import Dict


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

    def load_resource_string(self, rname: str) -> str:
        """
        Gets the resource by resource name and returns raw string - lines from this resource.

        :param rname: Resource name.
        :return: String containing lines for resource |rname|.
        """
        rpath: str = DBPediaHelper.get_filename_for_resource_name(rname)
        if not os.path.exists(rpath):
            raise FileNotFoundError
        with open(rpath, 'r') as rfile:
            content = rfile.read()
        content_filtered = list(filter(lambda line: line.startswith('<http://dbpedia.org/resource/{0}>'.format(rname)),
                                       content.split('\n')))
        return '\n'.join(content_filtered)

    def load_resourse_as_flat_json(self, rname: str) -> Dict:
        """
        Gets the resource by resource name and produces a flat Json out of it.

        :param rname: Resource name.
        :return: A dict object - a Python representation of a Json.
        """
        rstr = self.load_resource_string(rname)

        flat_json = {}
        # Every predicate starts with this prefix string.
        pred_pref = 'http://dbpedia.org/property/'

        for line in rstr.split('\n'):
            subj = '<http://dbpedia.org/resource/{0}>'.format(rname)
            line = line[len(subj):]
            pred_long = line[line.find('<')+1:line.find('>')]
            pred_short = pred_long[len(pred_pref):]
            line = line[line.find('>')+1:]
            obj = line[:line.find('<')]
            flat_json[pred_short] = obj.strip(' ^"')
        return flat_json
