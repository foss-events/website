import warnings
from datetime import datetime

from iso639 import Lang

from .helper import get_end_of_day

# only print warning message, not path or message code, etc
warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'

def extract_meta_keywords(row):
    meta_keywords = [
        'Free Software',
        'FOSS',
        'FLOSS',
        'Software Libre',
        'Open Source',
        'Events'
    ]

    if row['name']:
        meta_keywords.append(row['name'])

    if row['shortname']:
        meta_keywords.append(row['shortname'])

    if row['hashtag']:
        meta_keywords.append(row['hashtag'])

    if row['city']:
        meta_keywords.append(row['city'])

    if row['country']:
        meta_keywords.append(row['country'])

    if row['tags']:
        meta_keywords += row['tags'].split(',')

    if row['type']:
        meta_keywords.append(row['type'])

    if row.get('Main Organiser', None):
        meta_keywords.append(row['Main Organiser'])

    return meta_keywords


def extract_cfp(row, today):
    cfp_date_string = row['cfp_date']

    if row['cfp_link'].startswith('http'):
        cfp_link = "<a href='" + row['cfp_link'] + "'>Take part</a>."
        cfp_raw_link = row['cfp_link']
    else:
        cfp_link = row['cfp_link']
        cfp_raw_link = None


    if cfp_date_string:
        if row['cfp_date'] == 'open':
            cfp_date = None
            cfp_passed = False
        else:
            try:
                cfp_date = datetime.strptime(row['cfp_date'], '%Y%m%d')
                end_of_today = get_end_of_day(today)

                if cfp_date < end_of_today:
                    cfp_passed = True
                else:
                    cfp_passed = False
            except:
                cfp_date = None
                cfp_link = None
                cfp_passed = None

    else:
        cfp_date = None
        cfp_link = None
        cfp_passed = None

    return {
        'cfp_date': cfp_date,
        'cfp_passed': cfp_passed,
        'cfp_link': cfp_link,
        'cfp_raw_link': cfp_raw_link
    }

def translate_iso639_code2name(code):
    code_clean = code.strip().lower()

    try:
        name = Lang(code_clean).name
    except:
        name = code
        warnings.warn(code + " is not a valid iso 639 code")

    return name
