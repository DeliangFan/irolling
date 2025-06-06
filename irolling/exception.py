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

"""irolling exception handling"""


class IrollingBaseException(Exception):

    """Green turtle base exception."""

    msg_fmt = "greenturtle base exception."

    def __init__(self, message=None):
        if not message:
            message = self.msg_fmt
        else:
            message = str(message)

        super().__init__(message)


class ValidateTradingDayError(IrollingBaseException):
    """Validate trading day error"""
    msg_fmt = "Validate trading day error."


class TradingDayNotFoundError(IrollingBaseException):
    """Trading day not found error"""
    msg_fmt = "Trading day not found error."
