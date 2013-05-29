# Scrapy settings for rwscrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'rwscrapper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['rwscrapper.spiders']
NEWSPIDER_MODULE = 'rwscrapper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

RWSPIDER_NAME = 'rw_spider'
START_SEED_FILE = 'rwscrapper/config/seed.txt'
ALLOWED_DOMAINS_FILE = 'rwscrapper/config/allowed_domains.txt'
ITEM_PIPELINES = ['rwscrapper.pipelines.RomanianTextFilterPipeline']
