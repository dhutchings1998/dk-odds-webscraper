import os

BOT_NAME = "dk_odds_webscraper"

SPIDER_MODULES = ["dk_odds_webscraper.spiders"]
NEWSPIDER_MODULE = "dk_odds_webscraper.spiders"

ROBOTSTXT_OBEY = False


# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'  # Set the desired log level
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Configure log file
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'scrapy.log')

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False


#SPIDER_MIDDLEWARES = {
#    "dk_odds_webscraper.middlewares.DkOddsWebscraperSpiderMiddleware": 543,
#}


#DOWNLOADER_MIDDLEWARES = {
#    "dk_odds_webscraper.middlewares.DkOddsWebscraperDownloaderMiddleware": 543,
#}


ITEM_PIPELINES = {
    "dk_odds_webscraper.pipelines.ValidationPipeline": 200,
    "dk_odds_webscraper.pipelines.ManipulationPipeline": 300,
    # "dk_odds_webscraper.pipelines.NFLDatabaseWriter": 400,
}


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
