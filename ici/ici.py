#!/usr/bin/env python
#encoding:utf-8
from __future__ import print_function, unicode_literals
import json, codecs
from requests import Request
import re
import sys
import getopt
import logging
from xml.dom import minidom
import lxml
from collections import namedtuple
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from termcolor import colored


KEY = 'E0F0D336AF47D3797C68372A869BDBC5'
URL = 'http://dict-co.iciba.com/api/dictionary.php'
TAG = namedtuple('TAG', 'value color')
TAG_DICT = {
    'ps': TAG('[%s]', 'green'),
    'fy': TAG('%s', 'green'),
    'orig': TAG('ex. %s', 'blue'),
    'trans': TAG('    %s', 'cyan'),
    'pos': TAG('%s'.ljust(12), 'green'),
    'acceptation': TAG('%s', 'yellow')
}


logger = logging.getLogger(__name__)


def get_response(words):
    try:
        url_addr = URL + '?key=' + KEY + '&w=' + words
        response = urlopen(URL + '?key=' + KEY + '&w=' + words)
    except Exception:
        logger.error('哎哟,好像出错了')
        return
    return response



def parse_xml(xml):
    import xml.etree.cElementTree as ET
    tree = ET.fromstring(xml)
    chinese = []
    for elem in tree.iter():
        if elem.tag == 'acceptation':
            tmp = re.split(r'[;,；，\s]', elem.text.strip())
            tmp = [item for item in tmp if item.strip()]
            chinese += tmp
    return chinese

def translate(word):
    response = get_response(word)
    chinese = parse_xml(response.read())
    return chinese
    
if __name__ == '__main__':
    for item in translate(u'word'):
        print (item)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ifilename', help='tags input file name', default='image.json')
    parser.add_argument('-o', '--ofilename', help='tag output file name', default='chinese_image.json')
    args = parser.parse_args()
    ifilename = args.ifilename
    ofilename = args.ofilename
    with codecs.open(ifilename, 'r', 'utf-8') as input_file:
        with codecs.open(ofilename, 'w', 'utf-8') as output_file:
            line = input_file.readline()
            while line:
                line = json.loads(line)
                tags = line['img_tags']
                img_url = line['img_url']
                chinese_tags = []
                for tag in tags:
                    if (len(tag.split())>1):
                        continue
                    c_tag = translate(tag)
                    chinese_tags.append(c_tag[0])
                line['img_tags'] = chinese_tags
                line = json.dumps(line, ensure_ascii=False)
                output_file.write(line + '\n')
                line = input_file.readline()
