#!/usr/bin/env python
#encoding:utf-8
from __future__ import print_function, unicode_literals

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
        r = Request(url_addr)
        response = urlopen(URL + '?key=' + KEY + '&w=' + words)
    except Exception:
        logger.error('哎哟,好像出错了')
        return
    return response, r



def parse_xml(xml):
    import xml.etree.cElementTree as ET
    tree = ET.fromstring(xml)
    for elem in tree.iter():
        if elem.tag == 'acceptation':
            print (elem.tag)
            print (elem.attrib)
            print (elem.text)



if __name__ == '__main__':
    res, r =  get_response(sys.argv[1])
    parse_xml(res.read())
