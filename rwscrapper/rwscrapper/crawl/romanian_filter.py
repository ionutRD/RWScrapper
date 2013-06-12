# -*- coding: utf-8 -*-

from __future__ import division
import codecs
import re
import sys
from textconstants import *

# Global constants
RO_BASE = '../corpora/ro_base'
RO_BASE_NO_DIA = '../corpora/ro_base_no_diacritics'
TRIGRAM_FILE = '../corpora/ro_tri'
TRIGRAM_NO_DIA_FILE = '../corpora/ro_tri_no_diacritics'
BIGRAM_FILE = '../corpora/ro_bi'
BIGRAM_NO_DIA_FILE = '../corpora/ro_bi_no_diacritics'
UNIGRAM_FILE = '../corpora/ro_uni'
UNIGRAM_NO_DIA_FILE = '../corpora/ro_uni_no_diacritics'
RO_FREQ = '../corpora/ro_freq'
RO_FREQ_NO_DIA = '../corpora/ro_freq_no_diacritics'
ROMANIAN_BASE = '../corpora/ro_base'
ROMANIAN_BASE_NO_DIACRITICS = '../corpora/ro_base_no_diacritics'


# Helper functions

def make_char_list():
    """
    Make a list of all romanian unigram
    characters including the hyphen
    """
    chr_ords = range(ord(u'a'), ord(u'z') + 1)
    ro_chrs = map(lambda ch : unicode(chr(ch)), chr_ords)
    ro_chrs.append(u'\u021b')
    ro_chrs.append(u'\u0219')
    ro_chrs.append(u'\u0103')
    ro_chrs.append(u'\xee')
    ro_chrs.append(u'\xe2')
    ro_chrs.append(u'-')
    return ro_chrs


def unigram_from_file(fname):
    """
    Make unigram dictionary from an input file
    """
    try:
        fh = codecs.open(fname, 'r', 'utf-8')
        total = 0
        ndict = {}
        for char in RO_CHRS:
            ndict[char] = 0

        for line in fh:
            line = line[:-1]
            for char in line:
                if char in ndict:
                    ndict[char] += 1
                    total += 1
        fh.close()
        for ngram in ndict:
            ndict[ngram] /= total
        return ndict
    except IOError:
        return dict()
    except ZeroDivisionError:
        return dict()


def ngram_from_file(fname, n):
    """
    Calculate ngram frequency from a list of words
    """
    try:
        fh = codecs.open(fname, 'r', 'utf-8')
        total = 0
        ndict = {}
        for line in fh:
            line = u'#' + line[:-1] + u'#'
            ngrams = [line[i:i+n] for i in range(len(line) - n + 1)]
            for ngram in ngrams:
                try:
                    ndict[ngram] += 1
                except KeyError:
                    ndict[ngram] = 1
                total += 1
        fh.close()
        for ngram in ndict:
            ndict[ngram] /= total
        return ndict
    except IOError:
        return dict()
    except ZeroDivisionError:
        return dict()


def freq_words_from_file(fname):
    """
    Make a list of words along with its frequency
    from an input file
    """
    try:
        fh = codecs.open(fname, 'r', 'utf-8')
        total = 0
        wdict = {}
        for line in fh:
            word = line[:-1]
            try:
                wdict[word] += 1
            except KeyError:
                wdict[word] = 1
            total += 1
        fh.close()
        for word in wdict:
            wdict[word] /= total
        return wdict
    except IOError:
        return dict()
    except ZeroDivisionError:
        return dict()

def avg_words_len_from_file(fname):
    """
    Return the average words length from an
    input file
    """
    try:
        fh = codecs.open(fname, 'r', 'utf-8')
        sumtotal = 0
        numwords = 0
        for line in fh:
            sumtotal += len(line[:-1])
            numwords += 1
        return sumtotal / numwords
    except IOError:
        return 0
    except ZeroDivisionError:
        return 0


def read_ngram(fname):
    """
    Read an ngram along with its frequency
    from an input file
    """
    try:
        fh = codecs.open(fname, 'r', 'utf-8')
        ndict = {}
        for line in fh:
            line_list = line.split()
            ngram = line_list[0]
            freq = float(line_list[1])
            ndict[ngram] = freq
        fh.close()
        return ndict
    except IOError:
        return dict()

def most_frequent_dict(max_words, no_dia = False):
    """
    A dictionary of max_words most frenquent
    words
    """
    if not no_dia:
        ro_freq_dict = read_ngram(RO_FREQ)
    else:
        ro_freq_dict = read_ngram(RO_FREQ_NO_DIA)
    ro_freq_items = ro_freq_dict.items()
    ro_freq_items.sort(key = lambda x : x[1], reverse = True)
    ro_freq_items_most = ro_freq_items[:max_words]
    return dict(ro_freq_items_most)


# Romanian character list
MAX_WORDS = 10
RO_CHRS = make_char_list()
UNIGRAM_DICT = read_ngram(UNIGRAM_FILE)
BIGRAM_DICT = read_ngram(BIGRAM_FILE)
TRIGRAM_DICT = read_ngram(TRIGRAM_FILE)
UNIGRAM_DICT_NO_DIA = read_ngram(UNIGRAM_NO_DIA_FILE)
BIGRAM_DICT_NO_DIA = read_ngram(BIGRAM_NO_DIA_FILE)
TRIGRAM_DICT_NO_DIA = read_ngram(TRIGRAM_NO_DIA_FILE)
RO_FREQ_DICT = most_frequent_dict(MAX_WORDS)
RO_FREQ_DICT_NO_DIA = most_frequent_dict(MAX_WORDS, True)
RO_AVG_LEN = 4.96245408368
NO_DIA_FACT = 100
COEFF_TRI = 30
COEFF_BI = 10
COEFF_UNI = 5
COEFF_FREQ = 10
COEFF_AVG = 1
BONUS = 0.05


def prepare_text(text):
    """
    Prepare text for romanian filter
    """

    # Lower case all text
    text = text.lower()
    text = re.sub(ur'[,\.:!\?/\(\)\[\]\{\}]', u' ', text)
    text = re.sub(ur'[^\w\s\u021b\u0219\u0103\xee\xe2-]', UNICODE_VOID, text)
    text = re.sub(ur'[\d]', UNICODE_VOID, text)
    text = re.sub(ur'\s[bcdfghjklmnpqrstvwxyzu\u021b\u0219\u0103]\s', UNICODE_VOID, text)
    text = re.sub(ur'\n', u' ', text)
    text = re.sub(ur'\s+', u' ', text)
    text = text.strip()
    text = text + ' '

    return text

def unigram_from_text(text):
    """
    Return unigram statistics dictionary
    """
    try:
        txt_no_space = filter(lambda x : not x.isspace(), text)
        len_no_space = len(txt_no_space)

        ndict = {}

        for char in RO_CHRS:
            ndict[char] = \
            len([c for c in txt_no_space if c == char]) / len_no_space
        return ndict
    except ZeroDivisionError:
        return dict()


def ngram_from_text(utext, n):
    """
    Make ngram frequency from an input text
    """
    try:
        total = 0
        ndict = {}
        utext = utext.lower()
        words = \
        re.sub(ur'[^\wu\u0103\u0219\u021b\xe2\xee-]', u'\n', utext).split()
        for word in words:
            word = u'#' + word + u'#'
            ngrams = [word[i:i+n] for i in range(len(word) - n + 1)]
            for ngram in ngrams:
                try:
                    ndict[ngram] += 1
                except KeyError:
                    ndict[ngram] = 1
                total += 1
        for ngram in ndict:
            ndict[ngram] /= total
        return ndict
    except ZeroDivisionError:
        return dict()

def freq_words_from_text(text):
    """
    Return the words frequency from a text
    """
    try:
        words = text.split(' ')
        nwords = len(words)
        wdict = {}
        for word in words:
            try:
                wdict[word] += 1
            except KeyError:
                wdict[word] = 1

        for word in wdict:
            wdict[word] /= nwords

        return wdict
    except ZeroDivisionError:
        return dict()

def avg_words_len(text):
    """
    Return the average length of the words in a text
    """
    try:
        words = text.split(' ')
        nwords = len(words)
        avg = 0
        for word in words:
            avg += len(word) / nwords

        return avg
    except ZeroDivisionError:
        return 0


def relative_ngram_error(d1, d2):
    """
    Given two dictionaries of ngrams,
    calculate the sum of absolute differences between
    the two ngram frequencies
    """
    sumtotal = 0
    for ngram in d1:
        if ngram in d2:
            sumtotal += abs(d1[ngram] - d2[ngram])
        else:
            sumtotal += abs(d1[ngram])

    return sumtotal


def romanian_score(text):
    """
    Calculate the romanian language score for an input text
    """

    is_no_dia = False
    bonus = 0
    uni_dict = unigram_from_text(text)

    if uni_dict[u'ă'] == 0 or \
       uni_dict[u'ș'] == 0 or \
       uni_dict[u'ț'] == 0:
        text = text.replace(u',â', u'a')
        text = text.replace(u'ă', u'a')
        text = text.replace(u'î', u'i')
        text = text.replace(u'ș', u's')
        text = text.replace(u'ț', u't')
        is_no_dia = True

    tri_dict = ngram_from_text(text, 3)
    bi_dict = ngram_from_text(text, 2)
    uni_dict = unigram_from_text(text)
    freq_words = freq_words_from_text(text)
    avg_wlen = avg_words_len(text)
    avg_err = abs(avg_wlen - RO_AVG_LEN)

    if not is_no_dia:
        uni_err = relative_ngram_error(uni_dict, UNIGRAM_DICT)
        bi_err = relative_ngram_error(bi_dict, BIGRAM_DICT)
        tri_err = relative_ngram_error(tri_dict, TRIGRAM_DICT)
        freq_err = relative_ngram_error(RO_FREQ_DICT, freq_words)
        bonus = BONUS

    else:
        uni_err = relative_ngram_error(uni_dict, UNIGRAM_DICT_NO_DIA)
        bi_err = relative_ngram_error(bi_dict, BIGRAM_DICT_NO_DIA)
        tri_err = relative_ngram_error(tri_dict, TRIGRAM_DICT_NO_DIA)
        freq_err = relative_ngram_error(RO_FREQ_DICT_NO_DIA, freq_words)
        bonus = -BONUS

    total_error = (COEFF_TRI * tri_err + COEFF_BI * bi_err + COEFF_UNI * uni_err + COEFF_FREQ * freq_err + COEFF_AVG * avg_wlen) / \
                  (COEFF_TRI + COEFF_BI + COEFF_UNI + COEFF_FREQ + COEFF_AVG) - bonus

    return (is_no_dia, tri_err, bi_err, uni_err, freq_err, avg_err, total_error)

if __name__ == "__main__":
        """
        ndict = make_ngram(sys.argv[1], 2)
        pdict = ndict.items()
        pdict.sort(key = lambda x : x[1])

        fh = codecs.open('unigrams', 'w', 'utf-8')
        for ngram, freq in pdict:
                print >>fh, ngram, ' ', freq
        fh.close()
        """

        #ndict = freq_words_from_file('../corpora/ro_base_no_diacritics')
        #fh = codecs.open('ro_tri', 'w', 'utf-8')
        #for ngram in ndict:
        #    print >>fh, ngram, ' ', ndict[ngram]
        #fh.close
        print avg_words_len_from_file(RO_BASE_NO_DIA)
        #ndict1 = make_ngram_from_text(u'A fost odata ca-n pove\u0219ti a fost ca niciodata din rude mari imparatesti', 3)
        #ndict2 = make_ngram_from_text(u'Once upon a time my name was John', 3)
        #print relative_ngram_error(ndict1, ndict2)
        #ndict = unigram_from_text(u'A fost odata ca-n pove\u0219ti a fost ca niciodata din rude mari imparatesti')
        #print avg_words_len(u'A fost odata ca-n pove\u0219ti a fost ca niciodata din rude mari imparatesti')

        #print ndict
        #print read_ngram(sys.argv[1])
