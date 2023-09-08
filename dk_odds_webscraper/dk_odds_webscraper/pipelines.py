from itemadapter import ItemAdapter
import requests
from scrapy.exceptions import DropItem
from .helper import isValidAmericanOdds, isValidSpreadLine, isValidOverUnderLine, isValidEventDate, isValidEventTime, isValidInning, format_over_under_lines, format_event_date, get_formatted_date, format_odds_str


class ValidationPipeline:
    def process_item(self, item, spider):

        ## validate that team names exist
        team_name_fields = ['team1_name', 'team2_name']
        for field in team_name_fields:
            if not item[field]:
                raise DropItem('Missing team name value')
        
        ## validate event date
        if not isValidEventDate(item['event_date']):
            raise DropItem(f'Invalid event date {item["event_date"]}')
        
        ## validate point spreads
        point_spread_fields = ['team1_point_spread', 'team2_point_spread']
        for field in point_spread_fields:
            value = item[field]
            if not isValidSpreadLine(value['line']):
                raise DropItem(f'Invalid spread line {value["line"]}')
            if not isValidAmericanOdds(value['odds']):
                raise DropItem(f'Invalid spread odds {value["odds"]}')
        
        ## validate over under
        over_under_fields = ['team1_total_points_over_under', 'team2_total_points_over_under']
        for field in over_under_fields:
            value = item[field]
            if not isValidOverUnderLine(value['line']):
                raise DropItem(f'Invalid over under line {value["line"]}')
            if not isValidAmericanOdds(value['odds']):
                raise DropItem(f'Invalid over under odds {value["odds"]}')
        
        ## validate money lines
        money_line_fields = ['team1_money_line', 'team2_money_line']
        for field in money_line_fields:
            if not isValidAmericanOdds(item[field]):
                raise DropItem(f'Invalid money line odds {item[field]}')
        
        ## validate event time
        if not isValidEventTime(item['event_time']):
            raise DropItem(f'Invalid event time {item["event_time"]}')
        
        ## validate inning
        if spider.name == 'mlboddsspider':
            if not isValidInning(item['inning']):
                raise DropItem(f'Invalid inning {item["inning"]}')
            
        return item
    


class ManipulationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        format_over_under_lines(adapter)
        format_event_date(adapter)
        format_odds_str(adapter)
        
        return item
    


class NFLDatabaseWriterPipeline:
    def process_item(self, item, spider):
        url = 'https://z8jt2djc6i.us-east-1.awsapprunner.com/api/v1/nfl/games'
        response = requests.post(url, json=dict(item))

        if response.status_code == 200:
            print('successful write')
        else:
            print(f'{response.status_code}: {response.text}')

        return item





