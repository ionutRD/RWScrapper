import json
import threading

from sqlalchemy import *
from scrapy.exceptions import DropItem

from rwscrapper.settings import *
from rwscrapper.crawl.textutil import *
from rwscrapper.crawl.romanian_filter import *
from rwscrapper.crawl.tokenizer import *
from rwscrapper.crawl.sentence_processor import *
from rwscrapper.crawl.word_processor import *
from rwscrapper.crawl.word_cache import *

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

        if not item['processed_text']:
            raise DropItem(PROCESSED_TEXT_VOID)

        (dia_lack, tri_err, bi_err, uni_err, freq_err, avg_err, total_err) = \
        romanian_score(item['processed_text'])

        if total_err > ROMANIAN_THRESHOLD:
            raise DropItem(FOREIGN_LANGUAGE_TEXT)

        if dia_lack and not NO_DIA:
            raise DropItem(FOREIGN_LANGUAGE_TEXT)

        item['diacritics_lack'] = dia_lack
        item['tri_err'] = tri_err
        item['bi_err'] = bi_err
        item['uni_err'] = uni_err
        item['freq_err'] = freq_err
        item['avglen_err'] = avg_err
        item['rou_score'] = total_err

        return item

class PhraseSplitterPipeline(object):
    """
    Splits the text into phrases
    """
    def process_item(self, item, spider):
        item['phrases'] = sentence_tokenizer(item['normalized_text'])
        if not item:
            raise DropItem(TEXT_CANNOT_BE_SPLITTED)

        return item

class SentenceLevelProcessingPipeline(object):
    """
    Phase #1: Normalize every phrase
    Phase #2: Filter only Romanian phrases
    """
    def process_item(self, item, spider):
        for idx in range(len(item['phrases'])):
            item['phrases'][idx] = \
            sentence_normalization(item['phrases'][idx])
        if item['rou_score'] < ROMANIAN_THRESHOLD_NO_PHRASE_CHECK:
            item['phrases'] = \
            filter(romanian_language_filter, item['phrases'])

        if not item['phrases']:
            raise DropItem(NO_ROMANIAN_PHRASE)

        return item

class WordLevelProcessingPipeline(object):
    """
    Phase #1: Tokenize each phrase
    Phase #2: Error checking
    Phase #4: Generate suggestions
    """
    def process_item(self, item, spider):
        item['words'] = []
        idx = 0

        for phrase in item['phrases']:
            words = word_tokenizer(phrase)
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
                                       self.meta_rws, \
                                       autoload = True)
        stmt = select([self.clitic_tokens_tbl.c.form, \
                       self.clitic_tokens_tbl.c.formNoDia])
        rs = stmt.execute()
        self.cliticTokens = []
        self.cliticTokensNoDia = []
        for it in rs:
            self.cliticTokens.append(it[0])
            self.cliticTokensNoDia.append(it[1])
        self.clitics_tbl = Table('Clitics', self.meta_rws, autoload = True)
        stmt = select([self.clitics_tbl.c.form, \
                       self.clitics_tbl.c.formNoHyphen, \
                       self.clitics_tbl.c.formNoDia])
        rs = stmt.execute()
        self.clitics = []
        self.cliticsNoHyphen = []
        self.cliticsNoDia = []
        for it in rs:
            self.clitics.append(it[0])
            self.cliticsNoHyphen.append(it[1])
            self.cliticsNoDia.append(it[2])
        self.wdict = {}


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
        if word.is_proper() and not PROPER:
            return True

        # Step 1: If word
        if len(word) <= WLEN:
            return True

        # Step 2: Search the word in cache
        if self.cache.find(word):
            return True

        # Step 3: Search the word in DEX
        wtokens = word.get_word().split()

        for wtoken in wtokens:
            infl_form = Table('InflectedForm', self.meta_dex, autoload = True)
            stmt = select([infl_form.c.formNoAccent], \
                         (infl_form.c.formNoAccent == wtoken) | \
                         (infl_form.c.formUtf8General == wtoken))
            rs = self.conn_dex.execute(stmt)
            sel_words = [x[0] for x in rs]
            if len(sel_words) > 0:
                return True

        # Step 4: Split the word in two, and search each part in dex or cache
        if u'-' not in word.get_word() and \
           u' ' not in word.get_word() and \
           len(word) > WLEN + 2:
            pair_words = [(word.get_word()[:i], word.get_word()[i:]) for i in range(3,len(word) - 2)]
            for pw in pair_words:
                stmt = select([infl_form.c.formNoAccent], \
                             (infl_form.c.formNoAccent == pw[0]) | \
                             (infl_form.c.formUtf8General == pw[0]))
                rs = self.conn_dex.execute(stmt)
                sel_words0 = [x[0] for x in rs]

                stmt = select([infl_form.c.formNoAccent], \
                             (infl_form.c.formNoAccent == pw[1]) | \
                             (infl_form.c.formUtf8General == pw[1]))
                rs = self.conn_dex.execute(stmt)
                sel_words1 = [x[0] for x in rs]

                if len(sel_words0) > 0 and len(sel_words1) > 0:
                    return True


        # Step 5: Search the word in scrapper database
        if  word.get_word() in self.wdict:
            self.wdict[word.get_word()] += word.get_nr_app()

            # Update the number of appearances
            upd = update(self.inflected_forms_tbl,
                         self.inflected_forms_tbl.c.form == word.get_word())
            self.conn_rws.execute(upd, noApp = self.wdict[word.get_word()])
            return True

        stmt = select([self.inflected_forms_tbl.c.form, \
                       self.inflected_forms_tbl.c.noApp],
                       (self.inflected_forms_tbl.c.form == word.get_word()) | \
                       (self.inflected_forms_tbl.c.formUtf8General == word.get_word()))
        rs = self.conn_rws.execute(stmt)
        sel_words = []
        for it in rs:
            sel_words.append((it[0], it[1]))
        for (w, it) in sel_words:
            # Update the number of appearances
            upd = update(self.inflected_forms_tbl,
                         self.inflected_forms_tbl.c.form == w)
            self.conn_rws.execute(upd, noApp = it + word.get_nr_app())
            return True

        return False

    def check_clitic(self, word, item):
        """
        Check if a word is a clitic
        """
        # Step 1: Check if the word is a clitic itself
        if word.get_word() in self.clitics or \
           word.get_word() in self.cliticsNoHyphen or \
           word.get_word() in self.cliticsNoDia:
            return True

        # Step 2: Check if the word contains clitic tokens
        word_tokens = word.get_word().split('-')
        for token in word_tokens:
            if token in self.cliticTokens or \
               token in self.cliticTokensNoDia:
                return True

        return False

    def process_item(self, item, spider):
        self.db_dex = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, DEX_DB))
        self.db_rws = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, SCRAPPER_DB))
        self.meta_dex = MetaData(self.db_dex)
        self.meta_rws = MetaData(self.db_rws)
        self.conn_dex = self.db_dex.connect()
        self.conn_rws = self.db_rws.connect()

        self.texts_tbl = Table('Texts', self.meta_rws, autoload = True)
        self.phrases_tbl = Table('Phrases', self.meta_rws, autoload = True)
        self.words_tbl = Table('Words', self.meta_rws, autoload = True)
        self.inflected_forms_tbl = Table('InflectedForms', self.meta_rws, autoload = True)

        item['words'] = list(set(item['words']))

        # Find the last text id
        stmt = select([func.max(self.texts_tbl.c.id)])
        rs = stmt.execute()
        last_txt_id = [x[0] for x in rs][0]

        if not last_txt_id:
            last_txt_id = -1

        # Find the last phrase id
        stmt = select([func.max(self.phrases_tbl.c.id)])
        rs = stmt.execute()
        last_phrase_id = [x[0] for x in rs][0]

        if not last_phrase_id:
            last_phrase_id = -1

        # Find the last word id
        stmt = select([func.max(self.words_tbl.c.id)])
        rs = stmt.execute()
        last_word_id = [x[0] for x in rs][0]

        if not last_word_id:
            last_word_id = -1

        print last_txt_id, last_phrase_id, last_word_id
        print item['canonical_url']

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
        result = self.conn_rws.execute(ins)

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
            result = self.conn_rws.execute(ins)
            phrases_ids[idx] = crt_phrase_id
            crt_phrase_id += 1

        crt_word_id = last_word_id + 1
        for word in tbi_words:
            if len(self.wdict) < MAX_DICT_CACHE:
                self.wdict[word.get_word()] = 1
            # Insert the new words in the databse
            ins = self.words_tbl.insert(
                values = dict(phraseId = phrases_ids[word.get_phrase()], \
                              form = word.get_word(), \
                              formUtf8General = word.get_word(), \
                              reverse = word.get_word()[::-1], \
                              charLength = len(word.get_word()), \
                              createDate = time.time())
                )
            result = self.conn_rws.execute(ins)
            ins = self.inflected_forms_tbl.insert(
                values = dict(wordId = crt_word_id, \
                              form = word.get_word(), \
                              formUtf8General = word.get_word(), \
                              noApp = word.get_nr_app(), \
                              inflectionId = 102)
            )
            result = self.conn_rws.execute(ins)
            crt_word_id += 1

        self.conn_rws.close()
        self.conn_dex.close()

        return item
