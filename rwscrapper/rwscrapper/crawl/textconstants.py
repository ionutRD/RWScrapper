# Global constants
SMALL_S_CEDILLA = u'\u015f'
CAPITAL_S_CEDILLA = u'\u015e'
SMALL_S_COMMA = u'\u0219'
CAPITAL_S_COMMA = u'\u0218'
SMALL_T_CEDILLA = u'\u0163'
CAPITAL_T_CEDILLA = u'\u0162'
SMALL_T_COMMA = u'\u021b'
CAPITAL_T_COMMA = u'\u021a'
QUOTATION_MARK1 = u'\u201c'
QUOTATION_MARK2 = u'\u201d'
QUOTATION_MARK3 = u'\u201e'
QUOTATION_MARK4 = u'\u201f'
QUOTATION_MARK5 = u'\u201a'
QUOTATION_MARK6 = u'\u201b'
APOSTROPHE1 = u'\u2018'
APOSTROPHE2 = u'\u2019'
DAGGER = u'\u2020'
DOUBLE_DAGGER = u'\u2021'
BULLET = u'\u2022'
HYPHEN_BULLET = u'\u2043'
TRIANGULAR_BULLET = u'\u2023'
DOUBLE_EXCL = u'\u203c'
HORIZ_ELLIPSIS = u'\u2026'
TWO_DOT = u'\u2025'
ONE_DOT = u'\u2024'
UNICODE_WSPACE = u' '
UNICODE_CR = u'\n'
UNICODE_VOID = u''

# Translation table
TRANSTAB = {ord(u'\t') : UNICODE_WSPACE, \
            ord(u'\f') : UNICODE_WSPACE, \
            ord(u'\v') : UNICODE_CR, \
            ord(SMALL_S_CEDILLA) : SMALL_S_COMMA, \
            ord(CAPITAL_S_CEDILLA) : CAPITAL_S_COMMA, \
            ord(SMALL_T_CEDILLA) : SMALL_T_COMMA, \
            ord(CAPITAL_T_CEDILLA) : CAPITAL_T_COMMA, \
            ord(QUOTATION_MARK1) : u'"', \
            ord(QUOTATION_MARK2) : u'"', \
            ord(QUOTATION_MARK3) : u'"', \
            ord(QUOTATION_MARK4) : u'"', \
            ord(QUOTATION_MARK5) : u'"', \
            ord(QUOTATION_MARK6) : u'"', \
            ord(APOSTROPHE1) : u'\'', \
            ord(APOSTROPHE2) : u'\'', \
            ord(DOUBLE_EXCL) : u'!', \
            ord(HORIZ_ELLIPSIS) : u'.', \
            ord(ONE_DOT) : u'.', \
            ord(TWO_DOT) : u'.', \
            ord(DAGGER) : None, \
            ord(DOUBLE_DAGGER) : None, \
            ord(BULLET) : None, \
            ord(TRIANGULAR_BULLET) : None, \
            ord(HYPHEN_BULLET) : None, \
            ord(u'\r') : None, \
            ord(u'\a') : None, \
            ord(u'\b') : None}
