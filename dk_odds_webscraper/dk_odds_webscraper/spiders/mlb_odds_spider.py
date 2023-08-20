import scrapy 
import time
from dk_odds_webscraper.items import MLBGameItem

class MLBOddsSpider(scrapy.Spider):
    name = 'mlboddsspider'
    start_urls = ['https://sportsbook.draftkings.com/leagues/baseball/mlb?category=game-lines&subcategory=game']

    def parse(self, response):

        table_categories = response.css('table.sportsbook-table')

        for category in table_categories:
            event_date = category.css('thead > tr > th:first-child div.sportsbook-table-header__title span::text').get()

            num_team_lines = len(category.css('tbody > tr'))

            ## loop through each game and extract odds
            for i in range(1, num_team_lines, 2):
                row1 = category.css(f'tbody > tr:nth-child({i})')
                row2 = category.css(f'tbody > tr:nth-child({i+1})')

                mlb_game_item = MLBGameItem()

                mlb_game_item['team1_name'] = row1.css('div.event-cell__name-text::text').get()
                mlb_game_item['team2_name'] = row2.css('div.event-cell__name-text::text').get()
                
                mlb_game_item['event_date'] = event_date
                mlb_game_item['last_updated_utc'] = int(time.time())

                mlb_game_item['team1_point_spread'] = {
                    'line': row1.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get(),
                    'odds': row1.css('td:nth-child(2) span.sportsbook-odds.american::text').get()
                }
                mlb_game_item['team2_point_spread'] = {
                    'line': row2.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get(),
                    'odds': row2.css('td:nth-child(2) span.sportsbook-odds.american::text').get()
                }

                mlb_game_item['team1_total_points_over_under'] = {
                    'line': row1.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract(),
                    'odds': row1.css('td:nth-child(3) span.sportsbook-odds.american::text').get()
                }
                mlb_game_item['team2_total_points_over_under'] = {
                    'line': row2.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract(),
                    'odds': row2.css('td:nth-child(3) span.sportsbook-odds.american::text').get()
                }

                mlb_game_item['team1_money_line'] = row1.css('td:nth-child(4) span.sportsbook-odds.american::text').get()
                mlb_game_item['team2_money_line'] = row2.css('td:nth-child(4) span.sportsbook-odds.american::text').get()

                event_time = row1.css('th span.event-cell__start-time::text').get()
                if event_time: # event is not live
                    mlb_game_item['event_time'] = event_time
                    mlb_game_item['live'] = False
                    mlb_game_item['inning'] = None
                    mlb_game_item['team1_score'] = 0
                    mlb_game_item['team2_score'] = 0
                else: # event is live
                    mlb_game_item['event_time'] = None
                    mlb_game_item['live'] = True
                    mlb_game_item['inning'] = row1.css('span.event-cell__period::text').get()
                    mlb_game_item['team1_score'] = row1.css('span.event-cell__score::text').get()
                    mlb_game_item['team2_score'] = row2.css('span.event-cell__score::text').get()

                yield mlb_game_item
