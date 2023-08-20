import scrapy 

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

                event_time = row1.css('th span.event-cell__start-time::text').get()

                team1_name = row1.css('div.event-cell__name-text::text').get()
                team2_name = row2.css('div.event-cell__name-text::text').get()

                team1_run_line = row1.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get()
                team1_run_line_odds = row1.css('td:nth-child(2) span.sportsbook-odds.american::text').get()

                team2_run_line = row2.css('td:nth-child(2) span.sportsbook-outcome-cell__line::text').get()
                team2_run_line_odds = row2.css('td:nth-child(2) span.sportsbook-odds.american::text').get()

                team1_total_points = row1.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract()
                team1_total_points_odds = row1.css('td:nth-child(3) span.sportsbook-odds.american::text').get()

                team2_total_points = row2.css('td:nth-child(3) div.sportsbook-outcome-cell__label-line-container span::text').extract()
                team2_total_points_odds = row2.css('td:nth-child(3) span.sportsbook-odds.american::text').get()

                team1_money_line = row1.css('td:nth-child(4) span.sportsbook-odds.american::text').get()
                team2_money_line = row2.css('td:nth-child(4) span.sportsbook-odds.american::text').get()

                yield {
                    'team1': team1_name,
                    'team2': team2_name,
                    'event_time': event_time,
                    'event_date': event_date,
                    'team1_run_line': {
                        'run_line': team1_run_line,
                        'odds': team1_run_line_odds
                    },
                    'team2_run_line': {
                        'run_line': team2_run_line,
                        'odds': team2_run_line_odds
                    },
                    'team1_total_points': {
                        'total_points': team1_total_points,
                        'odds': team1_total_points_odds
                    },
                    'team2_total_points': {
                        'total_points': team2_total_points,
                        'odds': team2_total_points_odds
                    },
                    'team1_money_line': team1_money_line,
                    'team2_money_line': team2_money_line,
                }



