# -*- coding: utf-8 -*-

from __future__ import division
import re

from textconstants import *

ABBREVIATIONS = [
    u'dl', \
    u'dle', \
    u'dlui', \
    u'dlor', \
    u'dnă', \
    u'dna', \
    u'dnei', \
    u'dnelor', \
    u'prof', \
    u'dr', \
    u'arh', \
    u'pr', \
    u'ing', \
    u'înv', \
    u'inv', \
    u'av', \
    u'vol', \
    u'fig', \
    u'mr', \
    u'mrs', \
    u'pt', \
    u'etc', \
    u'lt', \
    u'mat', \
    u'fiz', \
    u'agr', \
    u'amer', \
    u'anat', \
    u'aprox', \
    u'cca', \
    u'arheol', \
    u'arhit', \
    u'aritm', \
    u'alim', \
    u'astron', \
    u'astrol', \
    u'bibl', \
    u'biol', \
    u'bl', \
    u'ap', \
    u'cf', \
    u'constr', \
    u'chir', \
    u'dial', \
    u'ex', \
    u'etnogr', \
    u'etnom', \
    u'euf', \
    u'etc', \
    u'ec', \
    u'electr', \
    u'fr', \
    u'fot', \
    u'fiziol', \
    u'fam', \
    u'ferov', \
    u'geogr', \
    u'germ', \
    u'geod', \
    u'gastr', \
    u'hidr', \
    u'ind', \
    u'ital', \
    u'iht', \
    u'ist', \
    u'lit', \
    u'lingv', \
    u'log', \
    u'lat', \
    u'muz', \
    u'metr', \
    u'mitol', \
    u'mec', \
    u'mar', \
    u'numism', \
    u'ornit', \
    u'pag', \
    u'psih', \
    u'peior', \
    u'paleogr', \
    u'paleont', \
    u'pict', \
    u'pl', \
    u'pers', \
    u'part', \
    u'parl', \
    u'perf', \
    u'poligr', \
    u'prez', \
    u'spl', \
    u'reg', \
    u'rel', \
    u'sg', \
    u'subj', \
    u'smth', \
    u'smb', \
    u'sl', \
    u'sg', \
    u'silv', \
    u'superl', \
    u'tipogr', \
    u'tehn', \
    u'univ', \
    u'phd', \
    u'dipl', \
    u'v', \
    u'vb', \
    u'vulg', \
    u'zool', \
    u'art', \
    u'nr', \
    u'pct', \
    u'urm', \
    u'ed', \
    u'vol', \
    u'str', \
    u'tel', \
    u'fax', \
    u'adr', \
    u'alin', \
]

UNCOMMON_ENDS = [
    u'u', \
    u'în', \
    u'in', \
    u'despre', \
    u'între', \
    u'intre', \
    u'printre', \
    u'dintre', \
    u'cu', \
    u'la', \
    u'până', \
    u'pînă', \
    u'pina', \
    u'pentru', \
    u'din', \
    u'către', \
    u'catre', \
    u'pe', \
    u'aidoma', \
    u'datorită', \
    u'datorita', \
    u'grație', \
    u'dedesubtul', \
    u'deasupra', \
    u'înspre', \
    u'inspre', \
    u'lângă', \
    u'langa', \
    u'lîngă', \
    u'și', \
    u'si', \
    u'sau', \
    u'ori', \
    u'niciun', \
    u'nicio', \
    u'niciunui', \
    u'niciunei', \
    u'un', \
    u'o', \
    u'de', \
    u'unui', \
    u'unei', \
    u'unor', \
    u'niște', \
    u'niste', \
    u'acest', \
    u'acești', \
    u'acesti', \
    u'aceste', \
    u'acei', \
    u'acele', \
    u'acelor', \
    u'acelui', \
    u'acestui', \
    u'acestei', \
    u'acestor', \
    u'alt', \
    u'altui', \
    u'altor', \
    u'altă', \
    u'altei', \
]

PUNCTUATION = [
    u'.', \
    u',', \
    u':', \
    u'?', \
    u'!', \
    u';', \
]

SEP = [
    u'.', \
    u'!', \
    u'?', \
    u';', \
]

STRIPS = [
    u'.', \
    u',', \
    u':', \
    u';', \
    u'-', \
    u'?', \
    u'!', \
    u' ', \
    u'\n', \
]

NUM_WORDS_PER_PHRASE = 2

def find_first_of(text, sep, search_idx):
    """
    Find the first appearance of a separator
    from 'sep' after search_idx
    """
    if search_idx < 0 or search_idx >= len(text):
        return -1
    idx = search_idx
    for ch in text[search_idx:]:
        if ch in sep:
            return idx
        idx +=1
    return -1

def generalized_strip(text, punctuation):
    """
    Strip a text by a set of punctuation characters
    """
    if not punctuation:
        return text

    start_idx = 0
    for ch in text:
        if ch not in punctuation:
            break
        start_idx += 1

    end_idx = len(text)
    for idx in range(len(text) - 1, -1, -1):
        if text[idx] not in punctuation:
            end_idx = idx + 1
            break

    return text[start_idx:end_idx]

def process_text(text):
    """
    Normalize each phrase
    """
    processed_text = re.sub(ur'\n[\(\)\[\]\{\}]', UNICODE_WSPACE, text)
    processed_text = re.sub(ur'^[a-z0-9]\)\s', UNICODE_WSPACE, processed_text)
    processed_text = re.sub(ur'\s+', UNICODE_WSPACE, processed_text)

    return processed_text



def sentence_tokenizer(text):
    """
    Split the text into sentences
    """
    tokenized = False
    tokens = []
    search_idx = 0
    last_idx = 0

    # Phase 1: End of line tokenizing
    while True:
        idx = text.find(u'\n', search_idx)
        if idx == -1:
            tokens.append(process_text(text[last_idx:]))
            break
        slice_txt = text[:idx].lower().strip()
        not_end = False
        for abbr in ABBREVIATIONS:
            if slice_txt.endswith(u'{0}.'.format(abbr)) or \
               slice_txt.endswith(abbr):
               not_end = True
               break
        for uncommon in UNCOMMON_ENDS:
            if slice_txt.endswith(uncommon):
                not_end = True
                break
        if idx < len(text) - 1:
            next_slice = text[idx + 1:].strip()[0]
            for punct in PUNCTUATION:
                if slice_txt.endswith(punct) and next_slice.islower():
                    not_end = True
                    break
        if not not_end:
            tokens.append(process_text(text[last_idx:idx]))
            last_idx = idx
        search_idx = idx + 1

    sentence_tokens = []
    # Phase 2: Punctuation tokenizing
    for token in tokens:
        search_idx = 0
        last_idx = 0
        while True:
            idx = find_first_of(token, SEP, search_idx)
            if idx == -1:
                sentence_tokens.append(process_text(token[last_idx:]))
                break
            slice_txt = token[:idx].lower().strip()
            not_end = False
            for abbr in ABBREVIATIONS:
                if slice_txt.endswith(u'{0}.'.format(abbr)) or \
                   slice_txt.endswith(abbr):
                    not_end = True
                    break
            if not not_end:
                sentence_tokens.append(process_text(token[last_idx:idx]))
                last_idx = idx
            search_idx = idx + 1

    # Phase 3: Phrase filtering
    sentence_tokens = filter(lambda x : x != UNICODE_VOID, sentence_tokens)
    sentence_tokens = filter(lambda x : len(x.split()) > NUM_WORDS_PER_PHRASE, sentence_tokens)

    for idx in range(len(sentence_tokens)):
        sentence_tokens[idx] = generalized_strip(sentence_tokens[idx], STRIPS)


    return sentence_tokens

if __name__ == "__main__":
    TEXT = u'Ana are mere. Merele sunt roșii'
    tokens = sentence_tokenizer(TEXT)
    print len(tokens)
    for sentence in tokens:
        print sentence
