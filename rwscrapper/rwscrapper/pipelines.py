import json
import threading
from scrapy.exceptions import DropItem

from rwscrapper.settings import *
from rwscrapper.crawl.textutil import *
from rwscrapper.romanian_filter import *
from rwscrapper.tokenizer import *
from rwscrapper.sentence_processor import *
from rwscrapper.word_processor import *

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
        item['processed_text'] = prepare_text(item['normalized_text'])

        if  not item['processed_text']:
            raise DropItem(PROCESSED_TEXT_VOID)

        (dia_lack, tri_err, bi_err, uni_err, freq_err, avg_err, total_err) = \
        romanian_score(item['processed_text'])

        if total_err > ROMANIAN_THRESHOLD:
            raise DropItem(FOREIGN_LANGUAGE_TEXT)

        item['diacritics_lack'] = dia_lack
        item['tri_err'] = tri_err
        item['bi_err'] = bi_err
        item['uni_err'] = uni_err
        item['freq_err'] = freq_err
        item['avglen_err'] = avg_err
        item['rou_score'] = total_error

        return item

class PhraseSplitterPipeline(object):
    """
    Splits the text into phrases
    """
    def process_item(self, item, spider):
        item['phrases'] = sentence_tokenizer(item['normalized_text'])
        if not item
            raise DropItem(TEXT_CANNOT_BE_SPLITTED)

        return item

class SentenceLevelProcessingPipeline(object):
    """
    Phase #1: Normalize every phrase
    Phase #2: Filter only Romanian phrases
    """
    for idx in range(len(item['phrases'])):
        item['phrases'][idx] = sentence_normalization(item['phrases'][idx])
    if item['rou_score'] < ROMANIAN_THRESHOLD_NO_PHRASE_CHECK:
        item['phrases'] = filter(romanian_language_filter, item['phrases'])

    if not item['phrases']:
        raise DropItem(NO_ROMANIAN_PHRASE)

    return item

class WordLevelProcessingPipeline(object):
    """
    Phase #1: Tokenize each phrase
    Phase #2: Error checking
    Phase #3: Database lookup
    Phase #4: Generate suggestions
    """
    item['words'] = []
    for phrase in item['phrases']:
        words += word_tokenizer(phrase)
        if len(words) > 0:
            item['words'] += words

    if not item['words']:
        raise DropItem(NO_ROMANIAN_WORDS)

    return item

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

