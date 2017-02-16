#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

"""
test_thrum
----------------------------------

Tests for `binary` module.
"""

from __future__ import division, absolute_import

import sys
from twisted.trial import unittest
from thrum import pypy

try:
    from exceptions import AttributeError
except ImportError:
    pass


class BytesBuilderTests(unittest.TestCase):
    def test_len(self):
        bb = pypy.BytesBuilder(10)
        bb.append(b"one ")
        bb.append(b"two ")
        self.assertEqual(len(bb), 8)

    def test_append_slice(self):
        bb = pypy.BytesBuilder(10)
        bb.append(b"one ")
        bb.append(b"two ")
        bb.append_slice(b"garbage three garbage", 8, 13)
        self.assertEqual(bb.build(), b"one two three")

    def test_build(self):
        bb = pypy.BytesBuilder(10)
        bb.append(b"one ")
        bb.append(b"two")
        self.assertEqual(bb.build(), b"one two")

    def test_type(self):
        if hasattr(sys, 'pypy_version_info'):
            # We're in a pypy interpreter
            with self.assertRaises(AttributeError):
                # So our BytesBuilder should not have the 'suboptimal' attr
                pypy.BytesBuilder.suboptimal

    def test_newlist_hint(self):
        # newlist_hint should behave just like a list
        l = pypy.newlist_hint(20)
        for i in range(3):
            l.append(i)
        self.assertEqual(len(l), 3)

        for i in range(17):
            l.append(i)
        self.assertEqual(len(l), 20)

        for i in range(3):
            l.append(i)
        self.assertEqual(len(l), 23)
