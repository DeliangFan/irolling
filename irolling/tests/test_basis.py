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

"""unittest for basis"""

import unittest

from irolling.analyzer import basis


class TestBasis(unittest.TestCase):
    """unittest for basis.py"""

    def setUp(self):
        self.b = basis.Basis("IC2512", 5417.8, 5793.67, 221)

    def test_basis(self):
        """test basis"""
        self.assertEqual(self.b.basis(),  -375.87)

    def test_basis_ratio(self):
        """test basis_ratio"""
        self.assertEqual(self.b.basis_ratio(), -0.0649)

    def test_basis_ratio_by_year(self):
        """test basis_ratio_by_year"""
        self.assertEqual(self.b.basis_ratio_by_year(), -0.1072)
