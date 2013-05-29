"""Extract text from PDF file using PDFMiner with whitespace intact."""

from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO

def pdf_to_string(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str
    except IOError:
        return ''

if __name__ == "__main__":
    print "TEST 1"
    print pdf_to_string("sample.pdf")
