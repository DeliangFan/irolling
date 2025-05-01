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

import akshare as ak

from irolling.data import constants


def get_stock_index(symbol):
    """get_stock_index return index with dataframe format"""
    index = ak.index_zh_a_hist(symbol=symbol,
                               period="daily",
                               start_date="19700101")
    return index


def get_sse50():
    """get sse50 index"""
    return get_stock_index(constants.SSE50_SYMBOL)


def get_csi300():
    """get csi300 index"""
    return get_stock_index(constants.CSI300_SYMBOL)


def get_csi500():
    """get csi500 index"""
    return get_stock_index(constants.CSI500_SYMBOL)


def get_csi1000():
    """get csi1000 index"""
    return get_stock_index(constants.CSI1000_SYMBOL)
