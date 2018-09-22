#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import isdir
from shutil import rmtree
from apng import APNG
import requests, re

class LineStickersDownloader:
    #CONSTs
    NORMAL_STICKER_TEMPLATE_URL = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{0}/ANDROID/sticker.png;compress=true"
    ANIMATED_STICKER_TEMPLATE_URL = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{0}/IOS/sticker_animation@2x.png;compress=true"
    STICKER_EXTENSION = '.png'
    CHUCK_SIZE = 1024
    REGEX_PRODUCT_ID  = r'product\/([0-9]+)\/'
    REGEX_IS_ANIMATED = r'type: "animation"' 
    REGEX_STICKERS_ID = r'ids: \[(.*)\]'

    def __init__(self):
        pass

    def get(self, url):
        if not self.is_correct_url_format(url):
            return ('Your link probably in the wrong format :(\nCorrect format => https://store.line.me/stickershop/product/3680530/en?from=sticker')
        html = self.get_raw_html(url)
        self.is_animated = self.check_is_animated(html)
        stickers = self.generate_stickers_data(self.get_stickers_id(html))
        self.product_id = self.parse_product_id(url)
        self.create_folder(self.product_id)
        for sticker in stickers:
            downloaded_sticker = self.download_sticker(sticker)
            print('> Downloaded {0}'.format(downloaded_sticker))
        return ('Stickers downloaded in folder "{0}"!'.format(self.product_id))

    def check_is_animated(self, html):
        if re.search(self.REGEX_IS_ANIMATED, html):
            return True
        else:
            return False

    def is_correct_url_format(self, url):
        if not re.search(self.REGEX_PRODUCT_ID, url):
            return False
        else:
            return True

    def create_folder(self, folder):
        if isdir(folder):
            rmtree(folder)
            makedirs(folder)
        else:
            makedirs(folder)
        return

    def parse_product_id(self, url):
        return re.search(self.REGEX_PRODUCT_ID, url).group(1)

    def get_raw_html(self, url):
        page = requests.get(url)
        html = page.content.decode('utf-8')
        return html

    def get_stickers_id(self, html):
        ids = re.search(self.REGEX_STICKERS_ID, html).group(1)
        return ids.split(',')

    def generate_stickers_data(self, ids):
        data = []
        for sticker_id in ids:
            if self.is_animated:
                data.append(
                    {"id": sticker_id, 
                     "url": self.ANIMATED_STICKER_TEMPLATE_URL.format(sticker_id)})
            else:
                data.append(
                    {"id": sticker_id, 
                     "url": self.NORMAL_STICKER_TEMPLATE_URL.format(sticker_id)})
        return data
            
    def download_sticker(self, sticker):
        sticker_name = sticker['id'] + self.STICKER_EXTENSION
        download_destination = '{0}/{1}'.format(self.product_id, sticker_name)
        load = requests.get(sticker['url'], stream=True)
        
        with open(download_destination, 'wb') as sticker_file:
            for chunk in load.iter_content(chunk_size=self.CHUCK_SIZE): 
                if chunk: 
                    sticker_file.write(chunk)
        return download_destination