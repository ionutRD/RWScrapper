import json
import threading
from scrapy.exceptions import DropItem

from rwscrapper.settings import *
from rwscrapper.crawl.textutil import *

normalized_lock = threading.Lock()

TEXT_NORM_FUNC = normalize_text

class NormalizeTextPipeline(object):
    """
    Normalize the raw text
    """
    def __init__(self):
        """
        Set the text normalizator
        """
        self.text_normalizator = TEXT_NORM_FUNC

    def process_item(self, item, spider):
        """
        Normalize the raw text
        """
        item['normalized_text'] = self.text_normalizator(item['raw_text'])
        if not item['normalized_text']:
            raise DropItem(NORMALIZED_TEXT_VOID)
        normalized_lock.acquire()
        try:
            item['normalized_pages'] += 1
        except KeyError:
            item['normalized_pages'] = 0
        finally:
            normalized_lock.release();
        return item

class RomanianTextPipeline(object):
    """
    Validate only Romanian texts
    """
    def process_item(self, item, spider):
        raise DropItem(FOREIGN_LANGUAGE_TEXT)

class JSONTestPipeline(object):
    """
    Write some item fields in JSON format. Used for testing purposes.
    """
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        json_data = {}
        json_data['url'] = item['url']
        json_data['canonical_url'] = item['canonical_url']
        json_data['timestamp'] = str(item['timestamp'])
        json_data['total_pages'] = item['total_pages']
        json_data['normalized_pages'] = item['normalized_pages']
        line = json.dumps(json_data) + '\n'
        self.file.write(line)
        return item

