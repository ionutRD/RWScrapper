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
        romanian_score(item['processed_text'], NO_DIA)

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
        idx += 1

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
        self.clitic_tokens_tbl = Table('CliticTokens', \
                                       meta_rws, \
                                       autoload = True)
        stmt = select([self.clitic_tokens_tbl.c.form, \
                       self.clitic_tokens_tbl.c.formNoDia])
        rs = stmt.execute()
        self.cliticTokens = [x[0] for x in rs]
        self.cliticTokensNoDia = [x[1] for x in rs]
        self.clitics_tbl = Table('Clitics', meta_rws, autoload = True)
        stmt = select([self.clitics_tbl.c.form, \
                       self.clitics_tbl.c.formNoHyphen, \
                       self.clitics_tbl.c.formNoDia])
        rs = stmt.execute()
        self.clitics = [x[0] for x in rs]
        self.cliticsNoHyphen = [x[1] for x in rs]
        self.cliticsNoDia = [x[2] for x in rs]

        self.texts_tbl = Table('Texts', meta_rws, autoload = True)
        self.phrases_tbl = Table('Phrases', meta_rws, autoload = True)
        self.words_tbl = Table('Words', meta_rws, autoload = True)
        self.inflected_forms_tbl = Table('Words', meta_rws, autoload = True)

    def has_diacritics(self, word):
        """
        Check if a word has diacritics
        """
        return all(map(lambda x : 65 <= ord(x) <= 90 \
                       or 97 <= ord(x) <= 122 or x == u'-', word))

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
            stmt = select([infl_form.c.formNoAccent], \
                           infl_form.c.formNoAccent == word)
            rs = stmt.execute()
            sel_words = [x[0] for x in rs]
            dret = self.has_diacritics(word)
            if (not dret and len(sel_words) > 0) or (dret and word in sel_words):
                self.cache.add(word)
                return True

        # Step 3: Search the word in scrapper database
        stmt = select([self.inflected_forms_tbl.c.form, \
                       self.inflected_forms_tbl.c.noApp], \
                       self.inflected_forms_tbl.c.form == word)
        rs = stmt.execute()
        sel_words = [(x[0], x[1]) for x in rs]
        if word, nr_app in sel_words:
            # Update the number of appearances

            return True

        return False

    def check_clitic(self, word, item):
        """
        Check if a word is a clitic
        """
        # Step 1: Check if the word is a clitic itself
        if word in self.clitics or \
           word in self.cliticsNoHyphen or \
           word in self.cliticsNoDia:
            return True

        # Step 2: Check if the word contains clitic tokens
        word_tokens = word.split('-')
        for token in word_tokens:
            if token in self.cliticTokens or \
               token in self.cliticTokensNoDia:
            return True

        return False

    def process_item(self, item, spider):
        # Find the last text id
        stmt = select([func.max(self.texts_tbl.c.id)])
        rs = stmt.execute()
        last_txt_id = [x[0] for x in rs][0]

        # Find the last phrase id
        stmt = select([func.max(self.phrases_tbl.c.id)])
        rs = stmt.execute()
        last_phrase_id = [x[0] for x in rs][0]

        # Find the last word id
        stmt = select([func.max(self.words_tbl.c.id)])
        rs = stmt.execute()
        last_word_id = [x[0] for x in rs][0]

        tbi_words = []
        tbi_phrases = set()

        for word in item['words']:
            if not self.check_word(word, item) and not self.check_clitic(word, item):
                tbi_phrases.add(word.get_phrase())
                tbi_words.append(word)

        if not tbi_words:
            raise DropItem(NO_NEW_WORD)

        # Insert the text in the database
        item['timestamp'] = time.time()
        ins = self.texts_tbl.insert(
            values = dict(url = item['url'],\
                          canonicalUrl = item['canonical_url'], \
                          contentFile = item['normalized_text'], \
                          trigramError = item['tri_err'], \
                          bigramError = item['bi_err'], \
                          unigramError = item['uni_err'], \
                          freqError = item['freq_err'], \
                          averageWordLength = item['avglen_err'], \
                          romanianScore = item['rou_score'], \
                          sourceType = item['file_type'], \
                          createDate = item['timestamp'],
                          noDia = item['diacritics_lack'])
        )
        result = db_rws.execute(ins)

        text_id = last_txt_id + 1
        crt_phrase_id = last_phrase_id + 1
        phrases_ids = {}
        for idx in tbi_phrases:
            # Insert the phrases in the database
            ins = self.phrases_tbl.insert(
                values = dict(textId = text_id, \
                              phraseContent = item['phrases'][idx], \
                              romanianScore = item['rou_score'])
            )
            result = self.db_rws.execute(ins)
            phrases[idx] = crt_phrase_id
            crt_phrase_id += 1

        crt_word_id = last_word_id + 1
        for word in tbi_words:
            # Insert the new words in the databse
            ins = self.words_tbl.insert(
                values = dict(phraseId = phrases_ids[word.get_phrase], \
                              form = word.get_word(), \
                              formUtf8General = word.get_word(), \
                              reverse = word.get_word()[::-1]
                              charLength = len(word.get_word())
                              createDate = time.time())
                )
            result = self.db_rws.execute(ins)
            ins = self.inflected_forms_tbl(
                values = dict(wordId = crt_word_id, \
                              form = word.get_word(), \
                              formUtf8General = word.get_word(), \
                              inflectionId = 102)
            )
            result = self.db_rws.execute(ins)
            crt_word_id += 1

        return item
