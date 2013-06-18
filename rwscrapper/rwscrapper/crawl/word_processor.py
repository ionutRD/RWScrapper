# -*- coding: utf-8 -*-

from __future__ import division
import re

ALLOWED_CHARSET = u'-\'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĂăÂâȘșȚțÎîÃãẼẽĨĩÕõŨũỸỹÑñǍǎĚěǏǐǑǒǓǔŠšŤťȞȟĽľŇňŽžČčĎďŘřǨǩǙǚÊêÎîÔôÛûŶŷĴĵĈĉĤĥẐẑŜŝĔĕŎŏĬĭŬŭĞğÅåŮůĄąĘęĮįǪǫŲųßĐđŁłÀàÈèÌìÒòÙùỲỳẀẁȦȧĖėİıȮȯẆẇṖṗṘṙṄṅṀṁṪṫḊḋḞḟĠġḢḣȷĿŀḂḃŻżṠṡĊċÁáÉéÍíÓóÚúÝýŃńÇçŔŕŚśŹźḾḿĹĺḰḱǴǵẂẃǗǘŰűŐőÄäËëÏïÖöÜüŸÿẄẅẌẍŖŗŞşŢţḐḑĢģĻļÇçŅņȨȩḨḩ'

SEP = ur'\s|!|\?|;|,|\.|\(|\)|\[|\]|\{|\}|\^|~|#|\*|\+|/|<|>|:|"|”|„|§|©'

MIN_WLEN = 3
DIA_MIN_WLEN = 5

PREFIXES = [
        u'an', \
        u'ab', \
        u'ambi', \
        u'ante', \
        u'anti', \
        u'anto', \
        u'antre', \
        u'antropo', \
        u'arhi', \
        u'atot', \
        u'auto', \
        u'avan', \
        u'bine', \
        u'bio', \
        u'centri', \
        u'co', \
        u'contra', \
        u'crono', \
        u'cvasi', \
        u'dez', \
        u'dis', \
        u'diz', \
        u'des', \
        u'de', \
        u'di', \
        u'demo', \
        u'dia', \
        u'echi', \
        u'endo', \
        u'exo', \
        u'extra', \
        u'entero', \
        u'entomo', \
        u'epi', \
        u'eso', \
        u'eu', \
        u'euro', \
        u'filo', \
        u'fito', \
        u'geronto', \
        u'heli', \
        u'hemi', \
        u'semi', \
        u'helio', \
        u'hemo', \
        u'hetero', \
        u'etero', \
        u'hidro', \
        u'higro', \
        u'hiper', \
        u'hipo', \
        u'holo', \
        u'homo', \
        u'homeo', \
        u'omo', \
        u'homi', \
        u'infra', \
        u'ultra', \
        u'inter', \
        u'între', \
        u'intra', \
        u'intro', \
        u'extra', \
        u'extro', \
        u'izo', \
        u'iso', \
        u'mega', \
        u'melo', \
        u'meta', \
        u'micro', \
        u'multi', \
        u'poli', \
        u'pluri', \
        u'nano', \
        u'ne', \
        u'non', \
        u'neo', \
        u'paleo', \
        u'novo', \
        u'oligo', \
        u'omni', \
        u'orto', \
        u'para', \
        u'pan', \
        u'pato', \
        u'peri', \
        u'petro', \
        u'post', \
        u'pre', \
        u'prea', \
        u'pro', \
        u'proto', \
        u'pseudo', \
        u'psiho', \
        u'psihro', \
        u'quasi', \
        u'radio', \
        u'rău', \
        u'răs', \
        u'răz', \
        u're', \
        u'retro', \
        u'sin', \
        u'sim', \
        u'sine', \
        u'sino', \
        u'supra', \
        u'sub', \
        u'super', \
        u'stră', \
        u'trans', \
        u'mono', \
        u'uni', \
        u'bi', \
        u'di', \
        u'tri', \
        u'cvadri', \
        u'tetra', \
        u'penta', \
        u'hexa', \
        u'sexa', \
        u'septen', \
        u'octo', \
        u'deca', \
        u'miria', \
]

ACRONYM_SUFFIXES = [
        u'-ul',
        u'-uri',
        u'-ului',
        u'-urile',
        u'-urilor',
]

def word_filter(word):
    """
    Filter void words, words that contain other characters
    from set ALLOWRD_CHARSET
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
    words = re.split(SEP, sentence)
    words = filter(word_filter, words)
    
    # Correct misspelled â/î
    words = map(spellchecker, words)

    return words

if __name__ == "__main__":
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
