import scrapy 
import time
from dk_odds_webscraper.items import NFLGameItem

class NFLOddsSpider(scrapy.Spider):
    name = 'nfloddsspider'
    start_urls = ['https://sportsbook.draftkings.com/leagues/football/nfl?category=game-lines&subcategory=game']

    def parse(self, response):

        table_categories = response.css('table.sportsbook-table')

        for category in table_categories:
            event_date = category.css('thead > tr > th:first-child div.sportsbook-table-header__title span::text').get()

            num_team_lines = len(category.css('tbody > tr'))

            ## loop through each game and extract odds
            for i in range(1, num_team_lines, 2):
                row1 = category.css(f'tbody > tr:nth-child({i})')
                row2 = category.css(f'tbody > tr:nth-child({i+1})')

                nfl_game_item = NFLGameItem()

                nfl_game_item['team1_name'] = row1.css('div.event-cell__name-text::text').get()
                nfl_game_item['team2_name'] = row2.css('div.event-cell__name-text::text').get()
                
                nfl_game_item['event_date'] = event_date
                nfl_game_item['last_updated_utc'] = int(time.time())

                nfl_game_item['team1_point_spread'] = {
                    'line': row1.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get(),
                    'odds': row1.css('td:nth-child(2) span.sportsbook-odds.american::text').get()
                }
                nfl_game_item['team2_point_spread'] = {
                    'line': row2.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get(),
                    'odds': row2.css('td:nth-child(2) span.sportsbook-odds.american::text').get()
                }

                nfl_game_item['team1_total_points_over_under'] = {
                    'line': row1.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract(),
                    'odds': row1.css('td:nth-child(3) span.sportsbook-odds.american::text').get()
                }
                nfl_game_item['team2_total_points_over_under'] = {
                    'line': row2.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract(),
                    'odds': row2.css('td:nth-child(3) span.sportsbook-odds.american::text').get()
                }

                nfl_game_item['team1_money_line'] = row1.css('td:nth-child(4) span.sportsbook-odds.american::text').get()
                nfl_game_item['team2_money_line'] = row2.css('td:nth-child(4) span.sportsbook-odds.american::text').get()

                event_time = row1.css('th span.event-cell__start-time::text').get()
                if event_time: # event is not live
                    nfl_game_item['event_time'] = event_time
                    nfl_game_item['live'] = False
                    nfl_game_item['quarter'] = None
                    nfl_game_item['team1_score'] = 0
                    nfl_game_item['team2_score'] = 0
                else: # event is live
                    nfl_game_item['event_time'] = None
                    nfl_game_item['live'] = True
                    nfl_game_item['quarter'] = row1.css('span.event-cell__period::text').get()
                    nfl_game_item['team1_score'] = row1.css('span.event-cell__score::text').get()
                    nfl_game_item['team2_score'] = row2.css('span.event-cell__score::text').get()

                yield nfl_game_item
