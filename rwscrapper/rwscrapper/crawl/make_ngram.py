from __future__ import division
import codecs
import re
import sys

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

def make_ngram_from_file(fname, n):
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
        if not total:
            return dict()
        for ngram in ndict:
            ndict[ngram] /= total
        return ndict
    except IOError:
        return dict()


def make_freq_words_from_file(fname, n):
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
                wdict[words] = 1
            total += 1
        fh.close()
        if not total:
            return dict()
        for word in ndict:
            wdict[word] /= total
        return wdict
    except IOError:
        return dict()

def make_ngram_from_text(utext, n):
    """
    Make ngram frequency from an input text
    """
    total = 0
    ndict = {}
    utext = utext.lower()
    words = re.sub(ur'[^\wu\u0103\u0219\u021b\xe2\xee-]', u'\n', utext).split()
    for word in words:
        word = u'#' + word + u'#'
        ngrams = [word[i:i+n] for i in range(len(word) - n + 1)]
        for ngram in ngrams:
            try:
                ndict[ngram] += 1
            except KeyError:
                ndict[ngram] = 1
            total += 1
    if not total:
        return dict()
    for ngram in ndict:
        ndict[ngram] /= total
    return ndict

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
        ndict = make_ngram_from_text(u'A fost odata ca-n povesti a fost ca niciodata din rude mari imparatesti', 3)
        print ndict
        #print read_ngram(sys.argv[1])
