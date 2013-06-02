"""Extract text from PDF file using PDFMiner with whitespace intact."""

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
    txt = pdf_to_string("../test/pdftest/sample1.pdf")
    ntext = textutil.normalize_text(txt)
    print ntext

    """
    print "TEST 2"
    print pdf_to_string("../test/pdftest/sample2.pdf")

    print "TEST 3"
    print pdf_to_string("../test/pdftest/sample3.pdf")

    print "TEST 4"
    print pdf_to_string("../test/pdftest/sample4.pdf")

    print "TEST 5"
    print pdf_to_string("../test/pdftest/sample5.pdf")

    print "TEST 7"
    print pdf_to_string("../test/pdftest/sample7.pdf")
    """
