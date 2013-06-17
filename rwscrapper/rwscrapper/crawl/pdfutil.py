# -*- coding: utf-8 -*-
"""Extract text from PDF file using PDFMiner with whitespace intact."""
import codecs
import sys

from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO
import textutil
import romanian_filter
import tokenizer

def pdf_to_string(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'unicode-escape'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return unicode(str, 'unicode-escape')
    except Exception:
        return textutil.UNICODE_VOID

def txt_to_string(path):
    try:
        fh = codecs.open(path, 'r', 'utf-8')
        text = textutil.UNICODE_VOID
        for line in fh:
            text += line + u'\n'
        return text
        fh.close()
    except Exception:
        return textutil.UNICODE_VOID

if __name__ == "__main__":
    if sys.argv[1].endswith('.pdf'):
        txt = pdf_to_string(sys.argv[1])
    else:
        txt = txt_to_string(sys.argv[1])
    ntext = textutil.normalize_text(txt)
    phrases = tokenizer.sentence_tokenizer(ntext)

    for phrase in phrases:
        print phrase
        print '---------------------------------------'

    #ntext = romanian_filter.prepare_text(ntext)
    #print ntext
    #ntext = u"A fost odată ca-n povești a fost ca niciodată din rude mari împărătești o prea frumoasă fată"
    #print romanian_filter.romanian_score(ntext)
