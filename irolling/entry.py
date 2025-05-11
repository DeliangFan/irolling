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

from irolling.analyzer import basis
from irolling import calendar
from irolling.data import api
from irolling.data import constants


def get_contract_basis():
    """show current basis"""

    # check the trading time
    now = datetime.datetime.now()
    trading_date = calendar.last_trading_day(now.date())
    if calendar.is_trading_time(now):
        # NOTE(fixme, support the real time and today)
        raise NotImplementedError

    # symbol_expire_map
    symbol_expire_map = api.get_symbol_expire_map(
        trading_date.strftime("%Y%m%d"),
    )

    basis_list = []
    for variety, index_symbol in constants.VARIETY_SYMBOL_MAP.items():
        # get spot price
        spot = api.get_stock_index_daily(symbol=index_symbol)
        spot_price = spot.loc[trading_date]["close"]

        # get future price
        future = api.get_stock_index_futures_daily(trading_date, trading_date)
        future = future[future["variety"].isin([variety])]
        future = future.sort_values(by=["symbol"], ascending=True)

        # calculate the basis for symbols
        for _, row in future.iterrows():
            # prepare the price and days
            future_price = row["close"]
            symbol = row["symbol"]
            expire = symbol_expire_map[symbol]
            days = calendar.delta_days(trading_date, expire)

            # initiate the basis class for different symbol
            b = basis.Basis(symbol, future_price, spot_price, days)
            basis_list.append(b)

    return basis_list


def do_list_basis(_):
    """list basis for current contracts"""
    basis_list = get_contract_basis()
    for b in basis_list:
        print(b.symbol, b.basis_ratio(), b.basis_ratio_by_year())


def do_show_basis(args):
    """show basis details for specified contract"""
    raise NotImplementedError
