"""Extract text from PDF file using PDFMiner with whitespace intact."""
import sys

from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO
import textutil

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

if __name__ == "__main__":
    print "TEST 1"
    txt = pdf_to_string(sys.argv[1])
    ntext = textutil.normalize_text(txt)
    print ntext
