#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lsd import LineStickersDownloader

def prompt(question):
    while True:
        answer = input(question)
        if answer.lower() == 'y': return True
        if answer.lower() == 'n': return False
        print('Invailid anwser!') 

downloader = LineStickersDownloader()
while True:
    url = input('Paste (right-click) the stickers pack\'s url: ')
    download_result = downloader.get(url)
    print(download_result)
    continue_ = prompt('Download another pack? (y/n): ')
    if continue_ == False: break;
