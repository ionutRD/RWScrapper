import json
import threading

from sqlalchemy import *
from scrapy.exceptions import DropItem

from rwscrapper.settings import *
from rwscrapper.crawl.textutil import *
from rwscrapper.romanian_filter import *
from rwscrapper.tokenizer import *
from rwscrapper.sentence_processor import *
from rwscrapper.word_processor import *
from rwscrapper.word_cache import *

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
    Phase #4: Generate suggestions
    """
    item['words'] = []
    idx = 0
    for phrase in item['phrases']:
        words += word_tokenizer(phrase)
        for word in words:
            word.set_phrase(idx)
        if len(words) > 0:
            item['words'] += words
        
    if not item['words']:
        raise DropItem(NO_ROMANIAN_WORDS)

    return item

class DbCommunicatorPipeline(object):
    def __init__(self):
    """
    Check if words exists in the database
    Insert new words in db
    """
    self.cache = WordCache(CACHE_CAPACITY)
    self.db_dex = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, DEX_DB))
    self.db_rws = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, SCRAPPER_DB))
    self.meta_dex = MetaData(self.db_dex)
    self.meta_rws = MetaData(self.db_rws)

    def has_diacritics(self, word):
        """
        Check if a word has diacritics
        """
        return all(map(lambda x : 65 <= ord(x) <= 90 or 97 <= ord(x) <= 122 or x == u'-', word))

    def check_word(self, word, item):
        """
        Check if a word is in DEX or scrapper database
        If the word is found in scrapper database 
        Update the timestamp and the number of appearances
        """
        # Step 1: Search the word in cache
        if not word.is_proper() and self.cache.find(word):
            return True
                
        # Step 2: Search the word in DEX
        if not word.is_proper():
            infl_form = Table('InflectedForm', meta_dex, autoload = True)
            stmt = select([infl_form.c.formNoAccent], infl_form.c.formNoAccent == word)
            rs = stmt.execute()
            sel_words = [x[0] for x in rs]
            dret = self.has_diacritics(word)
            if (not dret and len(sel_words) > 0) or (dret and word in sel_words):
                self.cache.add(word)
                return True

        # Step 3: Search the word in scrapper database
        infl_form = Table('InflectedForms', meta_rws, autoload = True)
        stmt = select([infl_form.c.form], infl_form.c.form == word)
        rs = stmt.execute()
        sel_words = [x[0] for x in rs]
        if word in sel_words:    
            return True
                
        return False


    def process_item(self, item, spider):
        updated_phrases = []
        updated_texts = []
        for word in item['words']:
            if not self.check_word(word, item):
                self.
        


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
