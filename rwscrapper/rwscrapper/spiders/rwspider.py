"""
Module responsible for downloading the html content
"""
import os
import tempfile
import threading
import time

from rwscrapper.settings import *
from rwscrapper.crawl.urlutil import *
from rwscrapper.items import RWScrapperItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

HTML_TO_TEXT_XPATH = "//text()[not(ancestor::script)][not(ancestor::style)][not(ancestor::noscript)][not(ancestor::form)]"

class RWSpider(CrawlSpider):
    """
    Class responsible for downloading the html content
    """
    name = RWSPIDER_NAME
    start_urls = get_start_urls(START_SEED_FILE)
    allowed_domains = get_allowed_domains(ALLOWED_DOMAINS_FILE)
    rules = (Rule(SgmlLinkExtractor(allow=('.*\.html', \
                                           '.*\.htm', \
                                           '.*\.shtml', \
                                           '.*\.cgi', \
                                           '.*\.pl', \
                                           '.*\.asp', \
                                           '.*\.aspx', \
                                           '.*\.php', )), \
             callback='parse_html', follow=True), \
             Rule(SgmlLinkExtractor(allow=('.*\.pdf', )), \
             callback='parse_pdf', follow=False), \
             Rule(SgmlLinkExtractor(allow=('.*\.txt', )), \
             callback='parse_txt', follow=False))

    def parse_html(self, response):
        """
        Extract the text from a html/php file and return a corresponding item
        """
        hxs = HtmlXPathSelector(response)
        items = []
        item = RWScrapperItem()
        item['raw_text'] = ''.join(hxs.select(HTML_TO_TEXT_XPATH).extract())
        item['url'] = str(response.url)
        item['canonical_url'] = canonize_url(item['url'])
        item['timestamp'] = time.time()
        item['file_type'] = 0
        items.append(item)
        return items

    def parse_pdf(self, response):
        """
        Extract the text from a pdf file and return a corresponding item
        """
        try:
            hxs = HtmlXPathSelector(response)
            items = []
            item = RWScrapperItem()
            file_handle = tempfile.NamedTemporaryFile(delete=False)
            file_handle.write(response.body)
            file_handle.close()
            item['raw_text'] = pdf_to_string(file_handle.name)
            if not item['raw_text']:
                os.unlink(file_handle.name)
                return []
            item['url'] = str(response.url)
            item['canonical_url'] = canonize_url(item['url'])
            item['timestamp'] = time.time()
            item['file_type'] = 1
            os.unlink(file_handle.name)
            return items
        except IOError:
            return []

    def parse_txt(self, response):
        """
        Extract the text from a txt file and return a corresponding item
        """
        items = []
        item = RWScrapperItem()
        item['raw_text'] = response.body
        item['url'] = str(respose.url)
        item['canonical_url'] = canonize_url(item['url'])
        item['timestamp'] = time.time()
        item['file_type'] = 2
        item.append(item)
        return items
