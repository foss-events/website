import re

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

TAG_RE = re.compile(r'<[^>]+>')


def get_start_of_month(date):
    return datetime(date.year, date.month, 1, 0, 0, 0)


def get_end_of_day(date):
    return datetime(date.year, date.month, date.day, 23, 59, 59)


def generate_event_details_path(event):
    event_path = event['start_year'] + '/'

    if event['start_month']:
        event_path += event['start_month'] + '-'

    if event['start_day']:
        event_path += event['start_day'] + '-'

    return event_path + slugify(event['label']) + '.html'


def url_mixed_filter(value):

    if not value:
        return '?'
    elif value.startswith('http'):
        return "<a href='" + value + "'>yes</a>"
    else:
        return value


def create_jinja_env():
    file_loader = FileSystemLoader('src/templates')
    env = Environment(loader=file_loader)
    env.filters['url_mixed'] = url_mixed_filter
    return env


def generate_event_ical_path(event):
    event_path = event['start_year'] + '/'

    if event['start_month']:
        event_path += event['start_month'] + '-'

    if event['start_day']:
        event_path += event['start_day'] + '-'

    return event_path + slugify(event['label']) + '.ics'


def remove_tags(text):
    text = text.replace('<br>', '\n')
    text = text.replace('</p>', '\n\n')
    return TAG_RE.sub('', text)
