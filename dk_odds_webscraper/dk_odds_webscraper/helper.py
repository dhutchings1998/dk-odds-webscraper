import re
from dateutil import parser
import datetime


def isValidAmericanOdds(odds_str):
    if odds_str is None:
        return True
    try:
        if odds_str[0] != '+':
            final_str = f'-{odds_str[1:]}'
        else:
            final_str = odds_str
        pattern = r'^[+-]\d+$'
        return re.match(pattern, final_str) is not None
    except:
        return False
        
def isValidSpreadLine(line):
    if line is None:
        return True
    pattern = r'^[+-]\d+(\.\d+)?$'
    return re.match(pattern, line) is not None

def isValidOverUnderLine(line):
    if len(line) == 0 or line is None:
        return True
        
    if len(line) != 3:
        return False
        
    o_u = line[0] == 'O' or line[0] == 'U'
    if not o_u:
        return False
        
    try:
        float(line[2])
        return True
    except ValueError:
        return False
        
def isValidEventDate(event_date):
    if event_date.lower() == 'today':
        return True
    elif event_date.lower() == 'tomorrow':
        return True 
        
    try:
        parser.parse(event_date)
        return True
    except ValueError:
        return False
    
def isValidEventTime(event_time):
    if event_time is None:
        return True
    pattern = r'^[01]?[0-9]:[0-5][0-9][APap][Mm]$'
    return re.match(pattern, event_time) is not None

def isValidInning(inning_str):
    if inning_str is None:
        return True
    pattern = r'^[1-9][0-9]*[stndrh]+$'
    return re.match(pattern, inning_str) is not None

def format_over_under_lines(adapter):
    over_under_fields = ["team1_total_points_over_under", "team2_total_points_over_under"]
    for field in over_under_fields:
        value = adapter.get(field)
        if value['line'] != None and len(value['line']) == 3:
            value['line'] = f'{value["line"][0]} {value["line"][2]}'
        else:
            value['line'] = None
        adapter[field] = value

def format_event_date(adapter):
    event_date = adapter.get('event_date').lower()
        
    if event_date == 'today':
        formatted_date = get_formatted_date(datetime.date.today())
    elif event_date == 'tomorrow':
        formatted_date = get_formatted_date(datetime.date.today() + datetime.timedelta(days=1))
    else:
        try:
            parsed_date = parser.parse(event_date)
            current_date = datetime.datetime.now()
            if parsed_date.month < current_date.month:
                parsed_date = parsed_date.replace(year=parsed_date.year + 1)

            formatted_date = get_formatted_date(parsed_date.date())
        except ValueError:
            formatted_date = None
        
    adapter['event_date'] = formatted_date

def get_formatted_date(date):
    return date.strftime('%Y-%m-%d')

def format_odds_str(adapter):
    nested_odds_fields = ["team1_point_spread", "team2_point_spread", "team1_total_points_over_under", "team2_total_points_over_under"]
    for field in nested_odds_fields:
        value = adapter.get(field)
        if value['odds'] is None:
            continue
        odds_str = value['odds']
        if odds_str[0] != '+':
            formatted_str = f'-{odds_str[1:]}'
        else:
            formatted_str = odds_str
        value['odds'] = formatted_str
        adapter[field] = value
        
    money_line_fields = ['team1_money_line', 'team2_money_line']
    for field in money_line_fields:
        odds_str = adapter.get(field)
        if odds_str is None:
            continue
        if odds_str[0] != '+':
            formatted_str = f'-{odds_str[1:]}'
        else:
            formatted_str = odds_str
        adapter[field] = formatted_str