"""
Class used to process raw text
"""
from __future__ import division
import re
from textconstants import *

LOWER_ALPHA_PERCENT_LIMIT = 0.65
UPPER_PERCENT_LIMIT = 0.5
LOWER_SPACE_PERCENT_LIMIT = 0.1
UPPER_SPACE_PERCENT_LIMIT = 0.8
LEN_LIMIT = 4

def accept_line(line):
    """
    Decide to accept or reject a line based on
    some criteria
    """
    line_len = len(line)
    if line_len < LEN_LIMIT:
        return False

    # Reject line with only capital letter words or digits
    if line.isupper() or line.isdigit():
        return False

    alpha_len = len([ch for ch in line if ch.isalpha()])

    # Reject lines with high percent of non-alpha characters
    alpha_ratio = alpha_len / line_len
    if alpha_ratio < LOWER_ALPHA_PERCENT_LIMIT:
        return False

    # Reject lines that contain a high percent of upper case letter words
    upper_len = len([ch for ch in line if ch.isupper()])
    upper_ratio = upper_len / line_len
    if upper_ratio > UPPER_PERCENT_LIMIT:
        return False

    # Reject lines that contains too much spaces or too few spaces
    space_len = len([ch for ch in line if ch.isspace()])
    space_ratio = space_len / line_len
    if space_ratio < LOWER_SPACE_PERCENT_LIMIT or \
       space_ratio > UPPER_SPACE_PERCENT_LIMIT:
        return False


    return True

def normalize_text(raw_text):
    """
    Normalize the text
    """
    try:
        # Strip white space characters
        ntext = raw_text.strip().translate(TRANSTAB)

        # Delete non-alphanumeric lines between new line characters
        ntext = re.sub(ur'[\n]([^\w]|[\d])+[\n]', UNICODE_CR, ntext)

        # Delete non-alphanumeric sentences
        ntext = re.sub(ur'[\.]([^\w]|[\d])+[\.\n!\?]', u'.', ntext)

        # Strip non-alphanumeric character
        ntext = re.sub(ur'^([^\w]|[\d])+', UNICODE_CR, ntext)

        ntext = re.sub(ur'[\s\.!\?^]([^\w\s\d])+[\s\.!\?$]', UNICODE_CR, ntext)

        # Delete multiple dots
        ntext = re.sub(ur'\.+', u'.', ntext)

        # Delete multiple spaces
        ntext = re.sub(ur' +', UNICODE_WSPACE, ntext)

        # Delete spaces before and after newlines
        ntext = re.sub(ur' ?\n ?', UNICODE_CR, ntext)

        # Strip multiple new lines
        ntext = re.sub(ur'\n+', UNICODE_CR, ntext)

        list_text = ntext.split(UNICODE_CR)

        new_list_text = filter(accept_line, list_text)

        return UNICODE_CR.join(new_list_text)

    except Exception:
        return UNICODE_VOID

if __name__ == "__main__":
    print "TEST 1"
    txt = u' Sunt \u015fi aici \u015fi acolo \n             Ce vrei??!   \r\n\n Hahaha'
    print normalize_text(txt)
