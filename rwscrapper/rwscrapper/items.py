from scrapy.item import Item, Field

class RWScrapperItem(Item):
    """
    Page raw text
    """
    text = Field()
    url = Field()
    canonical_url = Field()
    pass
