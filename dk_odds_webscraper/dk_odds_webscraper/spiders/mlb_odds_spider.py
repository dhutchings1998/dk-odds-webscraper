import scrapy 

class MLBOddsSpider(scrapy.Spider):
    name = 'mlboddsspider'
    start_urls = ['https://sportsbook.draftkings.com/leagues/baseball/mlb?category=game-lines&subcategory=game']

    def parse(self, response):
        game_links = response.css('a.event-cell-link::attr(href)').extract()
        game_links = list(set(game_links))

        base_url = 'https://sportsbook.draftkings.com'
        for rel_link in game_links:
            yield scrapy.Request(
                url=f'{base_url}{rel_link}',
                callback=self.parse_game_page
            )
    
    def parse_game_page(self, response):
        team_name_1 = response.css('table.sportsbook-table > tbody.sportsbook-table__body > tr:first-child div.event-cell__name-text::text').get()
        team_name_2 = response.css('table.sportsbook-table > tbody.sportsbook-table__body > tr:nth-child(2) div.event-cell__name-text::text').get()
        
        run_line_1 = response.xpath('//table[@class="sportsbook-table"]/tbody[@class="sportsbook-table__body"]/tr[1]/td[1]//span[@class="sportsbook-outcome-cell__line"]/text()').get()
        run_line_1_odds = response.xpath('//table[@class="sportsbook-table"]/tbody[@class="sportsbook-table__body"]/tr[1]/td[1]//span[contains(@class, "sportsbook-odds") and contains(@class, "american")]/text()').get()
        
        run_line_2 = response.xpath('//table[@class="sportsbook-table"]/tbody[@class="sportsbook-table__body"]/tr[2]/td[1]//span[@class="sportsbook-outcome-cell__line"]/text()').get()
        run_line_2_odds = response.xpath('//table[@class="sportsbook-table"]/tbody[@class="sportsbook-table__body"]/tr[2]/td[1]//span[contains(@class, "sportsbook-odds") and contains(@class, "american")]/text()').get()

        yield {
            'team1': team_name_1,
            'team2': team_name_2,
            'run_line_1': run_line_1,
            'run_line_1_odds': run_line_1_odds,
            'run_line_2': run_line_2,
            'run_line_2_odds': run_line_2_odds
        }