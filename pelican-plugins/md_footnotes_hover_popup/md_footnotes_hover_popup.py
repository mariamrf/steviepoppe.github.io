from __future__ import unicode_literals
from os import path, access, R_OK
import os

from pelican import signals

from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        if 'sup' in content:
            footnotes = soup.find(class_="footnote").find_all('p')
            footnoteref = soup.find_all(class_="footnote-ref")

            for index, item in enumerate(footnotes):
                footnoteref[index].parent['class'] = 'popup_footnote'
                tag = soup.new_tag('span')
                tag.append(BeautifulSoup(item.decode_contents(), 'html.parser'))
                #logger.error('Footnotes: %s', tag)
                footnoteref[index].insert_after(tag)

        instance._content = soup.decode()

def register():
    signals.content_object_init.connect(content_object_init)
