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
    u'PhD', \
    u'dipl', \
    u'v', \
    u'vulg', \
    u'zool', \
    u'art', \
    u'nr', \
    u'pct', \
    u'urm', \
    u'Ed', \
    u'Vol', \

]

def sentence_tokenizer(text):
    """
    Split the text into sentences
    """

