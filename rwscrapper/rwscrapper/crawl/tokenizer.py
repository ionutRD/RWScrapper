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
]

UNCOMMON_ENDS = [
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
        print idx, search_idx
        if idx == -1:
            tokens.append(text[last_idx:])
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
            tokens.append(text[last_idx:idx])
            last_idx = idx
        search_idx = idx + 1
    return tokens

if __name__ == "__main__":
    TEXT = u'ana are mere , \n roșii și \n Verzi'
    tokens = sentence_tokenizer(TEXT)
    print len(tokens)
    for sentence in tokens:
        print sentence
