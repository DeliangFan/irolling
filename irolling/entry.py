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

"""entry module for irolling"""

import datetime

import prettytable

from irolling.analyzer import basis
from irolling import calendar
from irolling.data import api
from irolling.data import constants


def get_contract_basis_by_date(date):
    """get contract basis by date"""
    # symbol_expire_map
    symbol_expire_map = api.get_symbol_expire_map(
        date.strftime("%Y%m%d"),
    )

    # get future price
    futures = api.get_stock_index_futures_daily(date, date)

    basis_list = []
    for variety, index_symbol in constants.VARIETY_SYMBOL_MAP.items():
        # get spot price
        spot = api.get_stock_index_daily(symbol=index_symbol)
        spot_price = spot.loc[date]["close"]

        # filter the contracts by variety
        contracts = futures[futures["variety"].isin([variety])]
        contracts = contracts.sort_values(
            by=["symbol"],
            ascending=True,
        )

        # calculate the basis for symbols
        for _, row in contracts.iterrows():
            # prepare the price and days
            future_price = row["close"]
            symbol = row["symbol"]
            expire = symbol_expire_map[symbol]
            days = calendar.delta_days(date, expire)

            # initiate the basis class for different symbol
            basis_list.append(
                basis.Basis(symbol, future_price, spot_price, days),
            )

    return basis_list


def get_contract_basis():
    """show current basis"""

    # check the trading time
    now = datetime.datetime.now()
    today = now.date()

    if calendar.is_trading_day(today):
        # if today is a trading day and the market has not open, use
        # the last trading day data
        if calendar.is_before_open(now):
            last_trading_date = calendar.last_trading_day(today)
            return get_contract_basis_by_date(last_trading_date)

        # if today is a trading day and the market has closed, use
        # today's data
        if calendar.is_after_close(now):
            return get_contract_basis_by_date(today)

        # if today is a trading day and is on trading time, use the realtime
        # data
        if calendar.is_trading_time(now):
            # NOTE(fixme, support the real time and today)
            raise NotImplementedError

        # if today is a trading day and is in the breaking time for noon
        raise NotImplementedError

    # if today is not a trading date, use the latest trading day
    last_trading_date = calendar.last_trading_day(today)
    return get_contract_basis_by_date(last_trading_date)


def do_list_basis(_):
    """list basis for current contracts"""

    table = prettytable.PrettyTable()
    table.field_names = [
        "Symbol",
        "Contract Price",
        "Spot Price",
        "Basis",
        "Basis Ratio(%)",
        "Basis Ratio By Year(%)",
        "Residual Maturity(days)",
    ]

    basis_list = get_contract_basis()
    for b in basis_list:
        table.add_row([
            b.symbol,
            b.future_price,
            b.spot_price,
            round(b.basis(), 2),
            round(b.basis_ratio() * 100, 2),
            round(b.basis_ratio_by_year() * 100, 2),
            b.days,
        ])

    print(table)


def do_show_basis(args):
    """show basis details for specified contract"""
    raise NotImplementedError
