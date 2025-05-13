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

"""command module for irolling"""

import argparse

from irolling import entry

# pylint: disable=R0801
parser = argparse.ArgumentParser(
    prog="irolling",
    description="irolling is a tiny tool for analyzing stock index future.",
)

# create sub parser
subparsers = parser.add_subparsers(
    required=True,
    help="subcommand for irolling",
)

# add list parser to list the basis of current contracts
parser_list = subparsers.add_parser(
    "list",
    help="list the contract",
)
parser_list.set_defaults(func=entry.do_list_basis)

# add show parser to show the details basis for a specified contract
parser_show = subparsers.add_parser(
    "show",
    help="show the contract",
)
parser_show.add_argument(
    "symbol",
    type=str,
    help="the future contract symbol to show, for example, IC2503",
)
parser_show.set_defaults(func=entry.do_show_basis)


def main():
    """main function"""
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
