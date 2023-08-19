

BOT_NAME = "dk_odds_webscraper"

SPIDER_MODULES = ["dk_odds_webscraper.spiders"]
NEWSPIDER_MODULE = "dk_odds_webscraper.spiders"

ROBOTSTXT_OBEY = False


DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


# Disable cookies (enabled by default)
#COOKIES_ENABLED = False


#SPIDER_MIDDLEWARES = {
#    "dk_odds_webscraper.middlewares.DkOddsWebscraperSpiderMiddleware": 543,
#}


#DOWNLOADER_MIDDLEWARES = {
#    "dk_odds_webscraper.middlewares.DkOddsWebscraperDownloaderMiddleware": 543,
#}


#ITEM_PIPELINES = {
#    "dk_odds_webscraper.pipelines.DkOddsWebscraperPipeline": 300,
#}


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
