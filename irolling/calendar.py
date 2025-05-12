# Copyright (c) 2025 GreenTurtle
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
calendar module

The only reason that I create this module is that I could not find a
accurate open source project for china future trading. So I have to
reinvent the calendar wheel and maintain it in the project.
"""

import datetime

import chinese_calendar

from irolling import exception


# the cn stock index starts from 01/Jan/2005
START_DATE = datetime.date(year=2005, month=1, day=1)
END_DATE = datetime.date(year=2025, month=12, day=31)
RETRY = 30

# special days, need to update the special days every year
SPECIAL_DATES = [
    datetime.date(year=2005, month=2, day=7),
    datetime.date(year=2005, month=2, day=8),
    datetime.date(year=2006, month=1, day=26),
    datetime.date(year=2006, month=1, day=27),
    datetime.date(year=2024, month=2, day=9)
]


def validate_cn_date(date):
    """
    validate china date, only support the date between START_DATE and
    END_DATE
    """
    if date < START_DATE or date > END_DATE:
        raise exception.ValidateTradingDayError


def is_trading_day(date):
    """
    check if it is a china trading day, a day is a trading day only if
    - it is a working day
    - it is weekday
    - exclude some special days
    """
    validate_cn_date(date)

    if chinese_calendar.is_holiday(date):
        return False

    if date.isoweekday() >= 6:
        return False

    if date in SPECIAL_DATES:
        return False

    return True


def last_trading_day(date):
    """get cn last trading day before date"""
    # we must find the trading date within 30 days
    retry = RETRY
    date += datetime.timedelta(days=-1)

    while retry > 0:
        validate_cn_date(date)

        if is_trading_day(date):
            return date

        date += datetime.timedelta(days=-1)
        retry = retry - 1

    raise exception.TradingDayNotFoundError


def next_trading_day(date):
    """get cn next trading day after the date"""
    # we must find the trading date within 30 days
    retry = RETRY
    date += datetime.timedelta(days=1)

    while retry > 0:
        validate_cn_date(date)

        if is_trading_day(date):
            return date

        date += datetime.timedelta(days=1)
        retry = retry - 1

    raise exception.TradingDayNotFoundError


def delta_days(start_date, end_date):
    """number of days between two date"""
    delta = end_date - start_date
    return delta.days


def is_trading_time(time):
    """
    check if it is a trading time
    :param time: datetime.datetime format
    """
    date = time.date()
    if not is_trading_day(date):
        return False

    morning_start = datetime.datetime(date.year, date.month, date.day, 9, 30)
    morning_end = datetime.datetime(date.year, date.month, date.day, 11, 30)
    if morning_start <= time <= morning_end:
        return True

    afternoon_start = datetime.datetime(date.year, date.month, date.day, 13, 0)
    afternoon_end = datetime.datetime(date.year, date.month, date.day, 15, 0)
    if afternoon_start <= time <= afternoon_end:
        return True

    return False


def is_after_open_and_before_close(time):
    """
    check if it is after market morning open time and before market close
    afternoon
    :param time:
    """
    date = time.date()
    if not is_trading_day(date):
        return False

    morning_start = datetime.datetime(date.year, date.month, date.day, 9, 30)
    afternoon_end = datetime.datetime(date.year, date.month, date.day, 15, 0)
    if morning_start <= time <= afternoon_end:
        return True

    return False


def is_before_open(time):
    """
    check if it is before market open
    :param time:
    """
    date = time.date()
    morning_start = datetime.datetime(date.year, date.month, date.day, 9, 30)
    if time <= morning_start:
        return True

    return False


def is_after_close(time):
    """
    check if it is after market close
    :param time:
    """
    date = time.date()
    afternoon_end = datetime.datetime(date.year, date.month, date.day, 15, 0)
    if time >= afternoon_end:
        return True

    return False
