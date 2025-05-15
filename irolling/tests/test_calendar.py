# Copyright (c) 2025 irolling
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

"""unittest for calendar module"""

import datetime
import unittest

from irolling import calendar
from irolling import exception


class TestCalendar(unittest.TestCase):
    """unittest for calendar.py"""

    def test_validate_cn_date_success(self):
        """test validate_cn_date success"""
        calendar.validate_cn_date(datetime.date(2010, 1, 1))
        calendar.validate_cn_date(datetime.date(2025, 12, 31))

    def test_validate_cn_date_failed(self):
        """test validate_cn_date failed"""
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.validate_cn_date,
            datetime.date(2003, 12, 31),
        )
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.validate_cn_date,
            datetime.date(2026, 1, 1),
        )

    def test_is_cn_trading_day(self):
        """test is_trading_day"""
        self.assertTrue(calendar.is_trading_day(
            datetime.date(2019, 1, 2)))
        self.assertTrue(calendar.is_trading_day(
            datetime.date(2025, 1, 27)))
        self.assertTrue(calendar.is_trading_day(
            datetime.date(2025, 2, 28)))

        self.assertFalse(calendar.is_trading_day(
            datetime.date(2025, 1, 26)))
        self.assertFalse(calendar.is_trading_day(
            datetime.date(2025, 1, 28)))

        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.is_trading_day,
            datetime.date(2003, 12, 31),
        )
        self.assertRaises(
            exception.ValidateTradingDayError,
            calendar.is_trading_day,
            datetime.date(2026, 1, 1),
        )

    def test_last_trading_day(self):
        """test last_trading_day"""
        date = datetime.date(2025, 5, 15)
        actual = calendar.last_trading_day(date)
        expect = datetime.date(2025, 5, 14)
        self.assertEqual(expect, actual)

    def test_next_trading_day(self):
        """test next_trading_day"""
        date = datetime.date(2025, 5, 15)
        actual = calendar.next_trading_day(date)
        expect = datetime.date(2025, 5, 16)
        self.assertEqual(expect, actual)

    def test_delta_days(self):
        """test delta_days"""
        start = datetime.date(2025, 5, 15)
        end = datetime.date(2025, 5, 16)
        actual = calendar.delta_days(start, end)
        self.assertEqual(2, actual)

    def test_is_trading_time(self):
        """test is_trading_time"""
        time = datetime.datetime(2025, 5, 15, 10, 30, 0)
        self.assertTrue(calendar.is_trading_time(time))

        time = datetime.datetime(2025, 5, 15, 12, 30, 0)
        self.assertFalse(calendar.is_trading_time(time))

        time = datetime.datetime(2025, 5, 15, 20, 30, 0)
        self.assertFalse(calendar.is_trading_time(time))

    def test_is_after_open_and_before_close(self):
        """test is_after_open_and_before_close"""
        time = datetime.datetime(2025, 5, 15, 10, 30, 0)
        self.assertTrue(calendar.is_after_open_and_before_close(time))

        time = datetime.datetime(2025, 5, 15, 12, 30, 0)
        self.assertTrue(calendar.is_after_open_and_before_close(time))

        time = datetime.datetime(2025, 5, 15, 20, 30, 0)
        self.assertFalse(calendar.is_after_open_and_before_close(time))

    def test_is_before_open(self):
        """test is_before_open"""
        time = datetime.datetime(2025, 5, 15, 8, 30, 0)
        self.assertTrue(calendar.is_before_open(time))

        time = datetime.datetime(2025, 5, 15, 10, 30, 0)
        self.assertFalse(calendar.is_before_open(time))

    def test_is_after_close(self):
        """test is_after_close"""
        time = datetime.datetime(2025, 5, 15, 20, 30, 0)
        self.assertTrue(calendar.is_after_close(time))

        time = datetime.datetime(2025, 5, 15, 10, 30, 0)
        self.assertFalse(calendar.is_after_close(time))
