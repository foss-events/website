from datetime import datetime

from helper import get_end_of_day


def extract_cfp(row, today):
    cfp_date_string = row['cfpdate']

    if row['cfplink'].startswith('http'):
        cfp_link = "<a href='" + row['cfplink'] + "'>Take part</a>."
        cfp_raw_link = row['cfplink']
    else:
        cfp_link = row['cfplink']
        cfp_raw_link = None


    if cfp_date_string:
        if row['cfpdate'] == 'open':
            cfp_date = None
            cfp_passed = False
        else:
            try:
                cfp_date = datetime.strptime(row['cfpdate'], '%Y%m%d')
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
