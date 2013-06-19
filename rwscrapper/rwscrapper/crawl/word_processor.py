# -*- coding: utf-8 -*-

from __future__ import division
import re

ALLOWED_CHARSET = u' -\'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĂăÂâȘșȚțÎîÃãẼẽĨĩÕõŨũỸỹÑñǍǎĚěǏǐǑǒǓǔŠšŤťȞȟĽľŇňŽžČčĎďŘřǨǩǙǚÊêÎîÔôÛûŶŷĴĵĈĉĤĥẐẑŜŝĔĕŎŏĬĭŬŭĞğÅåŮůĄąĘęĮįǪǫŲųßĐđŁłÀàÈèÌìÒòÙùỲỳẀẁȦȧĖėİıȮȯẆẇṖṗṘṙṄṅṀṁṪṫḊḋḞḟĠġḢḣȷĿŀḂḃŻżṠṡĊċÁáÉéÍíÓóÚúÝýŃńÇçŔŕŚśŹźḾḿĹĺḰḱǴǵẂẃǗǘŰűŐőÄäËëÏïÖöÜüŸÿẄẅẌẍŖŗŞşŢţḐḑĢģĻļÇçŅņȨȩḨḩ'

SEP = ur'\s|!|\?|;|,|\.|\(|\)|\[|\]|\{|\}|\^|~|#|\*|\+|/|<|>|:|"|”|„|§|©|€'

MIN_WLEN = 3
DIA_MIN_WLEN = 5
SUFFIX_LEN = 2
PREFIX_LEN = 2

ROU_CHARS = u'șțăîâȘȚĂÎÂ'
LOAN_CHARS = u'ÃãǍǎÅåĄąÀàȦȧÁáÄäḂḃČčĈĉĊċĆćÇçĐđĎďḊḋḐḑẼẽĚěÊêĔĕĘęÈèĖėÉéËëȨȩḞḟĜĝǦǧĞğĠġǴǵĢģĤĥȞȟḢḣḦḧḨḩĨĩǏǐÎîĬĭĮįÌìİıÍíÏïĴĵǨǩḰḱĶķŁłĽľĿŀĹĺĻļṀṁḾḿÑñŇňǸǹṄṅŃńŅņÕõǑǒÔôŎŏǪǫÒòȮȯÓóŐőÖöṖṗṔṕẪầŘřṘṙŔŕŖŗŠšŜŝṠṡŚśŞşŤťṪṫŢţŨũǓǔÛûŬŭŮůŲųÙùÚúŰűÜüṼṽǙǚǛǜǗǘŴŵẀẁẆẇẂẃẄẅẊẋẌẍỸỹŶŷỲỳẎẏÝýŸÿŽžẐẑŻżŹźß'

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
        u'-ul', \
        u'-uri', \
        u'-ului', \
        u'-urile', \
        u'-urilor', \
]

SUFFIXES = [
    u'agiu', \
    u'egiu', \
    u'ugiu', \
    u'aj', \
    u'ej', \
    u'iune', \
    u'ie', \
    u'iciu', \
    u'uri', \
    u'abil', \
    u'ibil', \
    u'ubil', \
    u'bil', \
    u'ace', \
    u'aie', \
    u'țial', \
    u'țional', \
    u'ean', \
    u'andru', \
    u'ian', \
    u'an', \
    u'ant', \
    u'ent', \
    u'anță', \
    u'ență', \
    u'ință', \
    u'ar', \
    u'al', \
    u'ard', \
    u'are', \
    u'ire', \
    u'ere', \
    u'arh', \
    u'arhie', \
    u'at', \
    u'et', \
    u'it', \
    u'ut', \
    u'atru', \
    u'ație', \
    u'autică', \
    u'eutică', \
    u'ază', \
    u'eză', \
    u'iză', \
    u'bilitate', \
    u'cefal', \
    u'ces', \
    u'cid', \
    u'crat', \
    u'crație', \
    u'cron', \
    u'cul', \
    u'culă', \
    u'dinte', \
    u'ea', \
    u'eag', \
    u'iag', \
    u'og', \
    u'eală', \
    u'ean', \
    u'ee', \
    u'enie', \
    u'esc', \
    u'ește', \
    u'estru', \
    u'et', \
    u'ime', \
    u'tate', \
    u'tură', \
    u'at', \
    u'etă', \
    u'et', \
    u'ețe', \
    u'eu', \
    u'fag', \
    u'vor', \
    u'fer', \
    u'fil', \
    u'filie', \
    u'fob', \
    u'fon', \
    u'fonie', \
    u'form', \
    u'fug', \
    u'gen', \
    u'genie', \
    u'graf', \
    u'grafie', \
    u'scopie', \
    u'ibilitate', \
    u'ic', \
    u'ier', \
    u'ieră', \
    u'il', \
    u'im', \
    u'in', \
    u'iot', \
    u'ire', \
    u'ism', \
    u'ist', \
    u'lniță', \
    u'rniță', \
    u'iș', \
    u'iște', \
    u'itudine', \
    u'iță', \
    u'uță', \
    u'iv', \
    u'log', \
    u'gie', \
    u'mânt', \
    u'morf', \
    u'nic', \
    u'nim', \
    u'onim', \
    u'oar', \
    u'uar', \
    u'oare', \
    u'oriu', \
    u'or', \
    u'os', \
    u'țional', \
    u'țial', \
    u'tură', \
    u'ui', \
    u'ual', \
    u'uu', \


]

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

    def __str__(self):
        return repr(self._word)

    def __len__(self):
        return len(self._word)

    def get_word(self):
        return self._word

    def get_nr_app(self):
        return _nr_app

    def get_prefix(self):
        return self._prefix

    def get_suffix(self):
        return self._suffix

    def is_hyphenized(self):
        return self._hyphen_word

    def is_loan(self):
        return self._is_loan

    def is_proper(self):
        return self._is_proper

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

    return word_list

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
