from datetime import datetime


def get_start_of_month(date):
    return datetime(date.year, date.month, 1, 0, 0, 0)


def get_end_of_day(date):
    return datetime(date.year, date.month, date.day, 23, 59, 59)
