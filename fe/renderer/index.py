from datetime import datetime

from generator.parser import parse_all_events
from generator.parser import parse_events
from generator.helper import create_jinja_env


def render_index(year=None):
    if not year:
        year = datetime.today().year

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    all_events = parse_all_events()
    events = parse_events("data/events.csv", today, year)

    env = create_jinja_env()
    template = env.get_template('index.html')
    result = template.render(
        upcoming=events['upcoming'],
        has_upcoming=events['has_upcoming'],
        prev=events['prev'],
        has_prev=events['has_prev'],
        all_events=all_events,
        year=year
    )

    return result
