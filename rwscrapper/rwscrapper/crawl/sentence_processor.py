# -*- coding: utf-8 -*-

from __future__ import division
import re

from romanian_filter import *

LOWER_PERCENT = 0.5
ROMANIAN_SCORE = -0.5
K1 = 14
K2 = 4.5
K3 = 65
K4 = -65
K5 = 20
K6 = -45.5
K7 = -10

def lowercase_filter(text):
    """
    Calculate the percent of lower case characters
    """
    n1 = len(filter(lambda x : x.islower(), text))
    n2 = len(text)

    if n1 / n2 > LOWER_PERCENT:
        return True
    return False

def ngram_score(d1, d2, bonus = 0):
    """
    Calculate the ngram score between two dictionaries
    """
    score = 0
    for ngram in d1:
        if ngram in d2:
            score += d1[ngram]
        else:
            score += bonus

    return score

def romanian_language_filter(text):
    """
    Decide whether the phrase is in romanian or not
    """

    if len(text) == 0:
        return False

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
        bi_err = ngram_score(bi_dict, BIGRAM_DICT_NO_DIA, 0)
        tri_err = ngram_score(tri_dict, TRIGRAM_DICT_NO_DIA, 0)
        freq_err = ngram_score(freq_words, RO_FREQ_DICT, 0)
    else:
        bi_err = ngram_score(bi_dict, BIGRAM_DICT)
        tri_err = ngram_score(tri_dict, TRIGRAM_DICT)
        freq_err = ngram_score(freq_words, RO_FREQ_DICT_NO_DIA)

    #print 'freq_err: ', freq_err, 'bi_err: ', bi_err, 'tri_err: ', tri_err, 'dia_score: ', diacritics_score, 'rare_score: ', rare_char_score, 'dc: ', double_consonant, 'quote_freq', quote_freq

    score = (tri_err * K1 + diacritics_score * K3 + rare_char_score * K4 + freq_err * K5 + double_consonant * K6 + quote_freq * K7)
    #print 'score: ', score
    return score > ROMANIAN_SCORE

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

    print "RO12: "
    txt = u'Presaram marar proaspat, tocat.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO13: "
    txt = u'Turnam laptele intr-o farfuriuta adanca si inmuiem feliile de paine, apoi le inmuiem in ou si le prajim in uleiul incins, timp de - minute, pe ambele parti.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO14: "
    txt = u'Amestecam faina, zaharul, sucul de rosii, sarea si nucsoara, adaugam peste mazare si continuam fierbearea inca 10 minute.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO15: "
    txt = u'Anastasia -  Pe 22 decembrie este pomenita Sf. Mare Mucenita Anastasia, martirizata pentru Hristos la 25 decembrie 304.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO16: "
    txt = u'Termenul "Liturghie"este de origine greaca. La inceput, cuvantul "Liturghie" desemna orice actiune sau lucrare in interes public sau comun. In Antichitatea greaca, termenul.Liturghie. avea o intrebuintare nereligioasa.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "RO17: "
    txt = u'Sarbatoarea numita Izvorul Tamaduirii s-a generalizat in Biserica Ortodoxa inca din secolul al V-lea. In toate bisericile si manastirile ortodoxe, dupa savarsirea Sfintei Liturghii, se savarseste slujba de sfintire a apei, dupa o randuiala adecvata Saptamanii Luminate.'
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "IT1: "
    txt = u"Il livello medio marino era di circa 120 metri inferiore a quello attuale, e la zona dove sorge attualmente la Manica era una distesa di tundra attraversata da un fiume che drenava le acque del Reno e del Tamigi nell'oceano Atlantico"
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "IT2: "
    txt = u"Dal 1994, inoltre, è attivo l'eurotunnel, un tunnel stradale e ferroviario che collega le due sponde."
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "IT3: "
    txt = u"La situazione cambiò drasticamente quando a capo degli Unni salì Attila nel 445"
    ntxt = sentence_normalization(txt)
    romanian_language_filter(ntxt)

    print "IT4: "
    txt = u"Il nuovo imperatore, reclutati forti contingenti di mercenari barbari, riuscì, con la forza del suo esercito, ad ottenere il riconoscimento di Visigoti, Burgundi e proprietari terrieri gallici, recuperando per l'Impero la Gallia e la Hispania."
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
