"""
Represent a downloaded content
"""
from scrapy.item import Item, Field



class RWScrapperItem(Item):
    """
    Page raw text
    """

    # Initial raw text
    raw_text = Field()

    # Normalized text
    normalized_text = Field()

    # Processed text
    processed_text = Field()

    # Specifies if lacks diacritics
    diacritics_lack = Field()

    # Original url
    url = Field()

    # Canonical url
    canonical_url = Field()

    # Timestamp
    timestamp = Field()

    # Total pages
    total_pages = Field()

    # Normalized pages
    normalized_pages = Field()

    # Trigram error
    tri_err = Field()

    # Bigram error
    bi_err = Field()

    # Unigram error
    uni_err = Field()

    # Most frequent words error
    freq_err = Field()

    # Words length error
    avglen_err = Field()

    # Total romanian language score
    rou_score = Field()

    # Text phrases
    phrases = Field()

