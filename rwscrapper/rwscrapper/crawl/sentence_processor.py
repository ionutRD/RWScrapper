# -*- coding: utf-8 -*-

from __future__ import division
import re

from romanian_filter import *

LOWER_PERCENT = 0.5
K1 = 5
K2 = 2.5
K3 = -20
K4 = 10
K5 = 15
K6 = 10
K7 = 10

def lowercase_filter(text):
    """
    Calculate the percent of lower case characters
    """
    n1 = len(filter(lambda x : x.islower(), text))
    n2 = len(text)

    if n1 / n2 > LOWER_PERCENT:
        return True
    return False

def romanian_language_filter(text):
    """
    Decide whether the phrase is in romanian or not
    """
    rtext = prepare_text(text)

    # Diacritics score
    n1 = len(filter(lambda x : x in u'șțăîâ', rtext))
    diacritics_score = n1 / len(rtext)

    # Rare characters
    n2 = len(filter(lambda x : x in u'kqyw', rtext))
    rare_char_score = n2 / len(rtext)

    # Double consonant score
    n3 = 0
    for idx in range(len(rtext) - 1):
        if rtext[idx] == rtext[idx + 1] and rtext[idx] in u'bcdfghjklmnopqrstuvwxyza':
            n3 += 1
    double_consonant = n3 / len(rtext)

    # Quote frequency
    n4 = 0
    n4 = len(filter(lambda x : x in '\'', rtext))
    quote_freq = n4 / len(text)

    bi_dict = ngram_from_text(rtext, 2)
    tri_dict = ngram_from_text(rtext, 3)
    freq_words = freq_words_from_text(rtext)

    if  diacritics_score == 0:
        bi_err = relative_ngram_error(bi_dict, BIGRAM_DICT_NO_DIA)
        tri_err = relative_ngram_error(tri_dict, TRIGRAM_DICT_NO_DIA)
        freq_err = relative_ngram_error(RO_FREQ_DICT, freq_words)
    else:
        bi_err = relative_ngram_error(bi_dict, BIGRAM_DICT)
        tri_err = relative_ngram_error(tri_dict, TRIGRAM_DICT)
        freq_err = relative_ngram_error(RO_FREQ_DICT_NO_DIA, freq_words)

    print 'freq_err: ', freq_err, 'bi_err: ', bi_err, 'tri_err: ', tri_err, 'dia_score: ', diacritics_score, 'rare_score: ', rare_char_score, 'dc: ', double_consonant, 'quote_freq', quote_freq

    score = (tri_err * K1 + bi_err * K2 + diacritics_score * K3 + rare_char_score * K4 + freq_err * K5 + double_consonant * K6 + quote_freq * K7) / \
            (K1 + K2 + K3 + K4 + K5 + K6 + K7)
    print 'score: ', score
    return score

def sentence_normalization(text):
    """
    Normalize a sentence
    """
    if not lowercase_filter(text):
        return UNICODE_VOID
    ntext = re.sub(u'\s|^[a-zA-Z0-9]\)\s|$', UNICODE_WSPACE, text)
    ntext = re.sub(u'[\(\)\[\]\{\}]', UNICODE_WSPACE, ntext)
    ntext = re.sub(u'\s+', UNICODE_WSPACE, ntext)
    ntext = ntext.strip()
    return ntext


if __name__ == '__main__':
    print "RO1: "
    txt = u'Notă: (1) Se completează în situația în care lichidatorul solicită acoperirea cheltuielilor din fondul de lichidare constituit în baza Legii nr. întrucât nu există disponibilități în averea debitorului'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO2: "
    txt = u'2013 și va fi organizată de inspectoratele'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO3: "
    txt = u'de 500 de lei'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO4: "
    txt = u'toate întâmplările din basmul primei zile de școală'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO5: "
    txt = u'Teste de admitere în clasa a V-a'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO6: "
    txt = u'Subiectele de la Concursul Cristian S'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO7: "
    txt = u'început școala, Ionuț a început școala'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO8: "
    txt = u'întrebă ea'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO9: "
    txt = u'Nume și prenume: str.nr. bloc'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO10: "
    txt = u'str Cartea Funciară nr. a localității'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO11: "
    txt = u'Multe s-au pastrat numai ca nume de familie: Anastasiu, Anastasescu, Nastac, Nastase, Nasta, Naste s. a.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "IT1: "
    txt = u"Il livello medio marino era di circa 120 metri inferiore a quello attuale, e la zona dove sorge attualmente la Manica era una distesa di tundra attraversata da un fiume che drenava le acque del Reno e del Tamigi nell'oceano Atlantico"
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "EN1: "
    txt = u'Example: The sound of her voice was sweet'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "EN2: "
    txt = u'language, imagery can apply to any component of a poem that evoke sensory experience and emotional'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "EN3: "
    txt = u'n the stanzas following the first stanza, the first and third lines of the first stanza'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "EN4: "
    txt = u'The House on the Hill'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)
