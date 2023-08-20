import scrapy

class MLBGameItem(scrapy.Item):
    team1_name = scrapy.Field()
    team2_name = scrapy.Field()
    event_time = scrapy.Field()
    event_date = scrapy.Field()
    last_updated_utc = scrapy.Field()
    team1_point_spread = scrapy.Field()
    team2_point_spread = scrapy.Field()
    team1_total_points_over_under = scrapy.Field()
    team2_total_points_over_under = scrapy.Field()
    team1_money_line = scrapy.Field()
    team2_money_line = scrapy.Field()
    live = scrapy.Field()
    inning = scrapy.Field()
    team1_score = scrapy.Field()
    team2_score = scrapy.Field()
