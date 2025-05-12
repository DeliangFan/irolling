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

"""api for access stock index data."""

import datetime

import akshare as ak

from irolling.data import constants


def get_stock_index_daily(symbol):
    """get_stock_index return index with dataframe format"""
    df = ak.index_zh_a_hist(symbol=symbol,
                            period="daily",
                            start_date="19700101")
    name_mapping = {
        "日期": "date",
        "最高": "high",
        "最低": "low",
        "开盘": "open",
        "收盘": "close",
    }

    # rename columns
    df = df.rename(columns=name_mapping)
    # filter desired columns
    filter_columns = ["date", "high", "low", "open", "close"]
    df = df[filter_columns]
    # set the index to datetime.date format
    df["date"] = df["date"].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
    )
    # set index
    df.set_index("date", inplace=True)

    return df


def get_sse50_daily():
    """get sse50 index"""
    return get_stock_index_daily(constants.SSE50_SYMBOL)


def get_csi300_daily():
    """get csi300 index"""
    return get_stock_index_daily(constants.CSI300_SYMBOL)


def get_csi500_daily():
    """get csi500 index"""
    return get_stock_index_daily(constants.CSI500_SYMBOL)


def get_csi1000_daily():
    """get csi1000 index"""
    return get_stock_index_daily(constants.CSI1000_SYMBOL)


def get_cffex_futures_daily(start_date, end_date):
    """get cffex futures contract daily"""
    df = ak.get_futures_daily(
        start_date=start_date,
        end_date=end_date,
        market=constants.CFFEX)

    filter_columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "symbol",
        "variety",
    ]

    df = df[filter_columns]

    # set the date to datetime.date format
    df["date"] = df["date"].apply(
        lambda x: datetime.datetime.strptime(x, "%Y%m%d").date(),
    )

    df.set_index("date", inplace=True)

    return df


def get_stock_index_futures_daily(start_date, end_date):
    """get stock index futures contract daily"""
    df = get_cffex_futures_daily(start_date, end_date)
    # filter the stock index
    df = df[df["variety"].isin(constants.STOCK_INDEX_VARIETIES)]
    return df


def get_ih_futures_daily(df):
    """get if(sse50) future contracts daily"""
    df = df[df["variety"].isin([constants.IH])]
    return df


def get_if_futures_daily(df):
    """get if(csi300) future contracts daily"""
    df = df[df["variety"].isin([constants.IF])]
    return df


def get_ic_futures_daily(df):
    """get ic(csi500) future contracts daily"""
    df = df[df["variety"].isin([constants.IC])]
    return df


def get_im_futures_daily(df):
    """get im(csi1000) future contracts daily"""
    df = df[df["variety"].isin([constants.IM])]
    return df


def get_stock_index_realtime(symbol):
    """get realtime stock index price"""
    df = ak.stock_zh_index_spot_em(symbol="上证系列指数")
    if symbol == constants.SSE50_SYMBOL:
        df = df[df["名称"].isin(["上证50"])]
    elif symbol == constants.CSI300_SYMBOL:
        df = df[df["名称"].isin(["沪深300"])]
    elif symbol == constants.CSI500_SYMBOL:
        df = df[df["名称"].isin(["中证500"])]
    elif symbol == constants.CSI1000_SYMBOL:
        df = df[df["名称"].isin(["中证1000"])]
    else:
        raise NotImplementedError

    return df.iloc[0]["最新价"]


def get_cffex_contract_info(date):
    """get cffex current contract info"""
    df = ak.futures_contract_info_cffex(date)

    name_mapping = {
        "合约代码": "symbol",
        "最后交易日": "expire",
        "品种": "variety",
    }

    # rename columns
    df = df.rename(columns=name_mapping)
    # filter desired columns
    filter_columns = ["symbol", "expire", "variety"]
    df = df[filter_columns]

    return df


def get_stock_index_contract_info(date):
    """get stock index contract info"""
    df = get_cffex_contract_info(date)
    df = df[df["variety"].isin(constants.STOCK_INDEX_VARIETIES)]
    return df


def get_symbol_expire_map(date):
    """get symbol expire map"""

    df = get_stock_index_contract_info(date)
    symbol_expire_map = {}
    for _, row in df.iterrows():
        symbol = row["symbol"]
        expire = row["expire"]
        symbol_expire_map[symbol] = expire

    return symbol_expire_map
