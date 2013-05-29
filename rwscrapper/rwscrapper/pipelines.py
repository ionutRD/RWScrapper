from scrapy.exceptions import DropItem

class RomanianTextFilterPipeline(object):
    """
    Validate only Romanian texts
    """
    def process_item(self, item, spider):
        raise DropItem("Romanian filter not implemented")


class CouchDBPipeline(object):
    pass
