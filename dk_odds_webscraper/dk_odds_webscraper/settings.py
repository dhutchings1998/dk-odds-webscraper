import os

BOT_NAME = "dk_odds_webscraper"

SPIDER_MODULES = ["dk_odds_webscraper.spiders"]
NEWSPIDER_MODULE = "dk_odds_webscraper.spiders"

ROBOTSTXT_OBEY = False

SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")


EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

SCRAPEOPS_SETTINGS_EXCLUSION_LIST = [
    'API_KEY', 'APIKEY', 'SECRET_KEY', 'SECRETKEY'
]

LOG_LEVEL = 'ERROR'

# LOG_ENABLED = True
# LOG_LEVEL = 'DEBUG'  # Set the desired log level
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# # Configure log file
# LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
# LOG_FILE = os.path.join(LOG_DIR, 'scrapy.log')

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
