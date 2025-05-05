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

"""constants for data"""

# stock index symbol constant
SSE50_SYMBOL = "000016"
CSI300_SYMBOL = "000300"
CSI500_SYMBOL = "000905"
CSI1000_SYMBOL = "000852"

# exchange name
CFFEX = "CFFEX"

# stock index variety
IH = "IH"
IF = "IF"
IC = "IC"
IM = "IM"
STOCK_INDEX_VARIETIES = (IF, IC, IM, IH)

# variety index symbol map
VARIETY_SYMBOL_MAP = {
    IH: SSE50_SYMBOL,
    IF: CSI300_SYMBOL,
    IC: CSI500_SYMBOL,
    IM: CSI1000_SYMBOL,
}
