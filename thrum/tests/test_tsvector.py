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

from twisted.trial import unittest

from thrum import tsvector


class TsVectorTests(unittest.TestCase):

    def test_accumulate_duplicates(self):
        data = """Bridging up is harder than bridging down"""

        tsv = tsvector.TsVector()
        tsv.load_words_file()
        tsv.normalize_and_add_document(data)
        self.assertEqual(len(tsv.entries), 6)
        self.assertEqual(tsv[0].text, 'bridge')
        self.assertEqual(len(tsv[0].positions), 2)
        self.assertEqual(tsv[5].text, 'down')

    def test_normalize_and_add(self):
        data = """Bridging up is harder than bridging down"""

        tsv = tsvector.TsVector()
        tsv.load_words_file()
        tsv.normalize_and_add("bridging")
        tsv.normalize_and_add("up")
        tsv.normalize_and_add("is")
        tsv.normalize_and_add("harder")
        tsv.normalize_and_add("than")
        tsv.normalize_and_add("bridging")
        tsv.normalize_and_add("down")

        self.assertEqual(len(tsv.entries), 6)
        self.assertEqual(tsv[0].text, 'bridge')
        self.assertEqual(tsv[5].text, 'down')

    def test_add_entry(self):
        data = """Bridging up is harder than bridging down"""

        tsv = tsvector.TsVector()
        tsv.load_words_file()
        tsv.add_entry("bridge", 1)
        tsv.add_entry("up", 2)
        tsv.add_entry("is", 3)
        tsv.add_entry("hard", 4)
        tsv.add_entry("than", 5)
        tsv.add_entry("bridge", 6)
        tsv.add_entry("down", 7)

        self.assertEqual(len(tsv.entries), 6)
        self.assertEqual(tsv[0].text, 'bridge')
        self.assertEqual(tsv[5].text, 'down')

    def test_normalize_tried(self):
        word = "tried"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'try')

    def test_normalize_stabber(self):
        word = "stabber"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'stab')

    def test_normalize_unfortunately(self):
        word = "unfortunately"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'unfortunate')

    def test_normalize_automatically(self):
        word = "automatically"
        tsv = tsvector.TsVector()
        self.assertEqual(tsv.normalize(word), 'automatic')

    def test_normalize_confirmation(self):
        word = "confirmation"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'confirm')

    def test_normalize_sullied(self):
        word = "sullied"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'sully')

    def test_normalize_partier(self):
        word = "partier"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'party')

    def test_normalize_upping(self):
        word = "upping"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'up')

    def test_normalize_strides(self):
        word = "Strides"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'stride')

    def test_normalize_bridging(self):
        word = "Bridging"
        tsv = tsvector.TsVector()
        tsv.load_words_file()
        self.assertEqual(tsv.normalize(word), 'bridge')

    def test_vector_entry_position(self):
        tse = tsvector.TsVectorEntry("hoop", 1, 'A')
        self.assertEqual(tse.positions, set([(1,'A')]))
        tse.positions 

    def test_vector_entry_bad_weight(self):
        with self.assertRaises(Exception):
            tse = tsvector.TsVectorEntry("hoop", 1, 'X')

    def test_vector_entry_summarize(self):
        tse = tsvector.TsVectorEntry("hoop", 1, 'A')
        self.assertEqual(tse.summarize(), "hoop:1A")

    def test_vector_entry_repr(self):
        tse = tsvector.TsVectorEntry("hoop", 1, 'A')
        self.assertEqual(str(tse), "<TsVectorEntry (hoop:1A)>")
