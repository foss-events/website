#!/usr/bin/env python3

from datetime import datetime
import sys

from .helper import create_jinja_env
from .parser import parse_events, parse_all_events

if len(sys.argv) != 3:
    print("generator must be called with two arguments year and target, e.g. index.py 2021 build/2020/index.html")
    sys.exit(1)

year = int(sys.argv[1])
target = sys.argv[2]

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
all_events = parse_all_events()
events = parse_events(f"data/{year}_events_db.csv", today)

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
with open(target, 'w') as f:
    f.write(result)
