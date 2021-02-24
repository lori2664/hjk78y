#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path as osp
import re
import shutil
import sys
import tempfile
import requests
import six
import tqdm

CHUNK_SIZE = 512 * 1024  # 512KB

def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

def download(url, output, quiet):
    url_origin = url
    sess = requests.session()

    while True:
        res = sess.get(url, stream=True)
        if 'Content-Disposition' in res.headers:
            # This is the file
            break

        # Need to redirect with confiramtion
        url = extractDownloadLink(res.text)
        print(url)
        print('wget -O- {} | gunzip |dd of=/dev/vda'.format(url))
        os.system('wget -O- {} | gunzip |dd of=/dev/vda'.format(url))
        return

if __name__ == "__main__":
    for url in sys.argv[1:]:
        download(url,output=None,quiet=False)
