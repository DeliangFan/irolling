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

from matplotlib import pyplot
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
    for variety, spot_symbol in constants.VARIETY_SYMBOL_MAP.items():
        # get spot price
        spot = api.get_stock_index_spot_daily(symbol=spot_symbol)
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


def get_contract_basis_by_realtime():
    """get contract basis by realtime"""
    today = datetime.datetime.now().date()

    # symbol_expire_map
    symbol_expire_map = api.get_symbol_expire_map(
        today.strftime("%Y%m%d"),
    )

    basis_list = []
    for _, index_symbol in constants.VARIETY_SYMBOL_MAP.items():
        # get spot price
        spot_price = api.get_stock_index_spot_realtime(symbol=index_symbol)
        # get future contracts
        contracts = api.get_stock_index_futures_realtime(symbol=index_symbol)
        contracts = contracts.sort_values(
            by=["symbol"],
            ascending=True,
        )

        # calculate the basis for symbols
        for _, row in contracts.iterrows():
            # prepare the price and days
            future_price = row["price"]
            symbol = row["symbol"]
            expire = symbol_expire_map[symbol]
            days = calendar.delta_days(today, expire)

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

    if calendar.is_after_open_and_before_close(now):
        fmt = "%Y%m%d %H:%M:%S"
        strftime = now.strftime(fmt)
        print(f"Compute basis with realtime {strftime}")
        return get_contract_basis_by_realtime()

    # 1. if today is not a trading date, use the latest trading day
    # 2. if today is a trading day and the market has not open, use
    #    the last trading day data
    # 3. if today is a trading day and the market has closed, use
    #    today's data
    trading_date = calendar.last_trading_day(today)
    if calendar.is_trading_day(today) and calendar.is_after_close(now):
        trading_date = today

    strftime = trading_date.strftime("%Y%m%d")
    print(f"Compute basis with daily {strftime}")
    return get_contract_basis_by_date(trading_date)


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


def get_variety_by_contract(symbol):
    """get variety by contract"""
    if symbol.startswith(constants.IH):
        return constants.IH

    if symbol.startswith(constants.IF):
        return constants.IF

    if symbol.startswith(constants.IC):
        return constants.IC

    if symbol.startswith(constants.IM):
        return constants.IM

    raise NotImplementedError


def get_expire_date(symbol, df):
    """get expire date"""
    today = datetime.date.today()
    symbol_expire_map = api.get_symbol_expire_map(
        today.strftime("%Y%m%d"),
    )

    if symbol in symbol_expire_map:
        return symbol_expire_map[symbol]

    return df.index[-1]


def do_plot(df):
    """plot the figure for symbol dataframe"""

    _, axs = pyplot.subplots(3, 1)

    # figure0, plot the price
    axs[0].plot(df.index, df.spot_close, color="red", label="spot")
    axs[0].plot(df.index, df.future_close, color="blue", label="future")
    axs[0].set_title("Spot & Future Price")
    axs[0].legend(loc='upper right')

    # figure1, plot the basis
    axs[1].plot(df.index, df.basis, color="red", label="basis")
    axs[1].set_title("Basis")
    axs[1].legend(loc='upper right')

    # figure2, plot the basis ratio and basis ratio by year
    axs[2].plot(df.index, df.basis_ratio, color="red", label="basis ratio")
    axs[2].plot(df.index,
                df.basis_ratio_by_year,
                color="blue",
                label="basis ratio by year")
    axs[2].set_title("Basis Ratio")
    axs[2].legend(loc='upper right')

    pyplot.show()


def do_show_basis(args):
    """show basis details for specified contract"""
    symbol = args.symbol
    variety = get_variety_by_contract(symbol)

    # get the spot data
    spot_symbol = constants.VARIETY_SYMBOL_MAP[variety]
    spot = api.get_stock_index_spot_daily(symbol=spot_symbol)

    # get the future data
    future = api.get_future_daily_by_symbol(symbol)

    # format spot dataframe with close price
    spot_close = spot[["close"]]
    spot_close = spot_close.rename(columns={"close": "spot_close"})

    # format future dataframe with close price
    future_close = future[["close"]]
    future_close = future_close.rename(columns={"close": "future_close"})

    # get he expire date to compute basis ratio
    expire_date = get_expire_date(symbol, future)

    # join spot and future dataframe
    df = future_close.join(spot_close, how="inner")

    # add basis column
    for date, row in df.iterrows():
        days = calendar.delta_days(date, expire_date)
        b = basis.Basis(symbol, row["future_close"], row["spot_close"], days)
        df.loc[date, "basis"] = b.basis()
        df.loc[date, "basis_ratio"] = round(b.basis_ratio() * 100, 2)
        df.loc[date, "basis_ratio_by_year"] = \
            round(b.basis_ratio_by_year() * 100, 2)

    # plot the figure
    do_plot(df)
