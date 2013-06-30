# -*- coding: utf-8 -*-

from __future__ import division
import re
from sqlalchemy import *

from textconstants import *

USER_NAME = 'scrapper'
USER_PASSWD = 'scrapper'
DEX_DB = 'DEX'
SCRAPPER_DB = 'rwscrapper'
HOSTNAME = 'localhost'

# RWscrapper database engine
DB_ENGINE = create_engine('mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(USER_NAME, USER_PASSWD, HOSTNAME, SCRAPPER_DB))
META = MetaData(DB_ENGINE)

def get_all_entries(table_name):
    """
    Retrieve all prefixes from database
    """
    tbl = Table(table_name, META, autoload=True)
    stmt = select([tbl.c.form])
    rs = stmt.execute()
    return [x[0] for x in rs]

# All prefixes
PREFIXES = get_all_entries('Prefixes')

# All suffixes
SUFFIXES = get_all_entries('Suffixes')

MIN_WLEN = 3
DIA_MIN_WLEN = 5
SUFFIX_LEN = 2
PREFIX_LEN = 2

class Word:
    """
    Denote a single word
    """
    def __init__(self, word, nr_app = 1, is_proper = False):
        self._word = word
        self._nr_app = nr_app
        self._is_proper = is_proper
        self._prefix = u''
        self._suffix = u''
        self._hyphen_word = False
        self._is_loan = False
        self._rou_chars = False
        self._phrase_id = -1
        self._reverse = word[::-1]

    def __str__(self):
        return repr(self._word)

    def __len__(self):
        return len(self._word)

    def __eq__(self, other):
        return self._word == other._word

    def __hash__(self):
        return hash(self._word)

    def get_word(self):
        return self._word

    def get_nr_app(self):
        return self._nr_app

    def get_prefix(self):
        return self._prefix

    def get_suffix(self):
        return self._suffix

    def get_phrase(self):
        return self._phrase_id

    def is_hyphenized(self):
        return self._hyphen_word

    def is_loan(self):
        return self._is_loan

    def is_proper(self):
        return self._is_proper

    def set_phrase(self, id):
        self._phrase_id = id

    def set_prefix(self, prefix):
        self._prefix = prefix

    def set_suffix(self, suffix):
        self._suffix = suffix

    def set_hyphenized(self):
        self._hyphen_word = True

    def set_rou_chars(self):
        self._rou_chars = True

    def set_loan(self):
        self._is_loan = True

def is_space_between(sentence, w1, w2):
    """
    Check if between w1 and w2 in the sentence
    there are only spaces
    """
    i = sentence.find(w1)
    if i == -1:
        return False
    start_idx = i + len(w1)
    end_idx = sentence.find(w2)

    if end_idx == -1:
        return False

    return sentence[start_idx:end_idx].isspace()

def word_filter(word):
    """
    Filter void words, words that contain other characters
    from set ALLOWED_CHARSET
    """
    if len(word) < MIN_WLEN:
        return False
    if word.isupper():
        return False
    for acronym in ACRONYM_SUFFIXES:
        if word.endswith(acronym) and word[:-len(acronym)].isupper():
            return False
    for ch in word:
        if ch not in ALLOWED_CHARSET:
            return False

    return True

def post_word_filter(word):
    """
    Perform a final filter on words
    """
    if word.get_word().startswith('\'') or word.get_word().startswith('-') or \
       word.get_word().endswith('\'') or word.get_word().endswith('-'):
        return False

    wtokens = word.get_word().split()
    if len(wtokens) > 4:
        return False
    for wtoken in wtokens:
        caps = [x for x in wtoken if x.isupper()]
        if len(caps) > 1 and word.is_proper():
            return False
        elif len(caps) > 0 and not word.is_proper():
            return False
        elif wtoken.endswith('-lea') or \
             wtoken.endswith('-a'):
            return False

    if not word.is_proper():
        for bigram in STRANGE_NGRAMS:
            if bigram in word.get_word():
                return False

    return True

def spellchecker(word):
    """
    Correct misspelled â/î
    Valid only for common nouns
    """
    if word[0].isupper() or len(word) < DIA_MIN_WLEN:
        return word
    pref = u''
    start = u''
    end = u''
    rest = word
    for prefix in PREFIXES:
        if word.startswith(prefix):
            rest = word[len(prefix):]
            pref = prefix

    if len(rest) == 0:
        return word

    if rest[0] == u'â':
        start = u'î'
    else:
        start = rest[0]

    if rest[-1] == u'â':
        end = u'î'
    else:
        end = rest[-1]

    middle = rest[1:-1]
    middle = re.sub(u'î', u'â', middle)

    word = pref + start + middle + end

    # Strip final suffix for loan words
    for suffix in ACRONYM_SUFFIXES:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break

    return word

def word_tokenizer(sentence):
    """
    Tokenize the sentence to obtain a list of words
    """
    words = re.split(WORD_SEP, sentence)
    words = filter(lambda x : x != u'', words)

    if not words:
        return []

    # Eliminate starting capital letter words
    idx = 0
    for w in words:
        if not w[0].isupper():
            break
        idx += 1

    words = words[idx:]

    proper_words = []
    pword = u''

    for i in range(len(words) - 1):
        if words[i] and words[i][0].isupper() and words[i + 1] and words[i + 1][0].isupper() \
           and is_space_between(sentence, words[i], words[i + 1]):
           pword += words[i] + u' '
        elif words[i] and words[i][0].isupper():
            pword += words[i] + u' '
            proper_words.append(pword.strip())
        else:
            pword = u''

    proper_words = filter(word_filter, proper_words)

    words = filter(lambda x : x and not x[0].isupper(), words)
    words = filter(word_filter, words)

    # Correct misspelled â/î
    words = map(spellchecker, words)

    # Concatenate with proper words
    words += proper_words

    # Count the number of appearances of each word in the sentence
    words = list(set([(w, words.count(w)) for w in words]))

    word_list = []
    # Create the word list
    for word, nr_app in words:
        is_proper = False
        if word[0].isupper():
            is_proper = True
        new_word = Word(word, nr_app, is_proper)
        for suffix in SUFFIXES:
            if word.endswith(suffix) and len(word[:len(suffix)]) > SUFFIX_LEN \
                                     and not is_proper:
                new_word.set_suffix(suffix)
                break
        for prefix in PREFIXES:
            if word.startswith(prefix) and len(word[len(prefix):]) > PREFIX_LEN \
                                       and not is_proper:
                new_word.set_prefix(prefix)
        for suffix in ACRONYM_SUFFIXES:
            pass
        else:
            if u'-' in word:
                new_word.set_hyphenized()

        for ch in LOAN_CHARS:
            if ch in word:
                new_word.set_loan()

        for ch in ROU_CHARS:
            if ch in word:
                new_word.set_rou_chars()

        word_list.append(new_word)

    word_list = filter(post_word_filter, word_list)

    return word_list

if __name__ == "__main__":
    '''
    txt = u'În principiu un NAP este o sală plină cu rutere, cel puțin unul pentru fiecare backbone conectat. O rețea locală conectează toate aceste rutere astfel încât pachetele să poată fi retransmise rapid din orice coloană în orice alta. În afară de conectarea în NAP-uri, backbone-urile de dimensiuni mari au numeroase conexiuni directe între ruterele lor, tehnică numită conectare privată (private peering).'
    words = word_tokenizer(txt)
    for word in words:
        print word

    print '--------------------------------------------------'

    txt = u'Termenul Internet provine din împreunarea artificială și parțială a două cuvinte englezești: interconnected = interconectat și network = rețea.'
    words = word_tokenizer(txt)
    for word in words:
        print word


    print '--------------------------------------------------'

    txt = u'Deși mai multe țări din Uniunea Europeană au testat diferite proiecte de vot electronic, Estonia este în prezent (2011) singurul membru UE care folosește această procedură pe scară largă.'
    words = word_tokenizer(txt)
    for word in words:
        print word


    print '--------------------------------------------------'

    txt = u'Societatea gălăţeană a reprezentat companiile europene la forumul anual al constructorilor şi echipamentelor navale * Rolls-Royce, Mitsubishi, Samsung s-au aflat printre greii alături de care s-a discutat despre viitorul industriei navale mondiale * Navele specializate, culoarul de producţie pentru constructorii gălăţeni'
    words = word_tokenizer(txt)
    for word in words:
        print word


    print '--------------------------------------------------'

    txt = u'Aici se adăpostește mormântul lui Ștefan cel Mare'
    words = word_tokenizer(txt)
    for word in words:
        print word
    '''

    txt = u'Aici este \'Gologan II-lea cine'
    words = word_tokenizer(txt)
    for word in words:
        print word
