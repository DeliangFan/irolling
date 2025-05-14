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

"""module to compute the basis of stock index contracts"""


class Basis:
    """basis class"""
    def __init__(self, symbol, future_price, spot_price, days):
        """
        :param symbol: name of the stock index contract
        :param future_price: the price of the future contract
        :param spot_price: the price of the spot
        :param days: the number of days to expire for the contract
        """
        self.symbol = symbol
        self.future_price = future_price
        self.spot_price = spot_price
        self.days = days

    def basis(self):
        """basis between contract and index"""
        return self.future_price - self.spot_price

    def basis_ratio(self):
        """basis ratio between contract and index"""
        return self.basis() / self.spot_price

    def basis_ratio_by_year(self):
        """basis ratio between contract and index by year"""
        if self.days == 0:
            return 0

        return self.basis_ratio() * 365 / self.days
