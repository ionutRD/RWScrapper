"""
Class used to process raw text
"""
import re
from textconstants import *

def normalize_text(raw_text):
    """
    Normalize the text
    """
    try:
        # Strip white space characters
        ntext = raw_text.strip().translate(TRANSTAB)

        # Strip multiple spaces
        ntext = re.sub(ur' +', UNICODE_WSPACE, ntext)

        # Delete multiple dots
        ntext = re.sub(ur'\.+', u'.', ntext)

        # Delete multiple commas
        ntext = re.sub(ur',+', u',', ntext)

        # Delete multiple colons
        ntext = re.sub(ur':+', u':', ntext)

        # Delete multiple semicolons
        ntext = re.sub(ur';+', u';', ntext)

        # Delete multiple question signs
        ntext = re.sub(ur'\?+', u'?', ntext)

        # Delete multiple exclamation signs
        ntext = re.sub(ur'!+', u'!', ntext)

        # Delete spaces before and after newlines
        ntext = re.sub(ur' ?\n ?', UNICODE_CR, ntext)

        # Delete non-alphanumeric lines
        ntext = re.sub(ur'\n[^\w]+\n', UNICODE_CR, ntext)

        # Delete digit lines
        ntext = re.sub(ur'\n[\d]+\n', UNICODE_CR, ntext)

        # Strip multiple new lines
        ntext = re.sub(ur'\n+', UNICODE_CR, ntext)

        return ntext

    except Exception:
        return UNICODE_VOID

if __name__ == "__main__":
    print "TEST 1"
    txt = u' Sunt \u015fi aici \u015fi acolo \n             Ce vrei??!   \r\n\n Hahaha'
    print normalize_text(txt)
