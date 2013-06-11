"""
Represent a downloaded content
"""
from scrapy.item import Item, Field



class RWScrapperItem(Item):
    """
    Page raw text
    """
    raw_text = Field()
    normalized_text = Field()
    processed_text = Field()
    diacritics_lack = Field()
    url = Field()
    canonical_url = Field()
    timestamp = Field()
    total_pages = Field()
    normalized_pages = Field()
