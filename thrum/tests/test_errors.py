#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

from __future__ import division, absolute_import

from twisted.trial import unittest
from thrum import errors


class PostgresErrorTests(unittest.TestCase):

    def test_attributes(self):
        test_data = {'C': 'some sqlstate_code',
                     'D': 'some detail',
                     'F': 'some file',
                     'H': 'some hint',
                     'L': 'some line',
                     'M': 'some message',
                     'P': 'some position',
                     'R': 'some routine',
                     'S': 'some severity_local',
                     'V': 'some severity',
                     'W': 'some where',
                     'c': 'some column',
                     'd': 'some data_type',
                     'n': 'some constraint',
                     'p': 'some position_internal',
                     'q': 'some query_internal',
                     's': 'some schema',
                     't': 'some table'}

        e = errors.PostgresError(test_data)

        for key in test_data:
            attribute_name = errors.PostgresError.keys[key]
            self.assertEqual(test_data[key], getattr(e, attribute_name))

    def test_attribute(self):
        e = errors.PostgresError({'H': 'some hint'})
        self.assertEqual('some hint', e.hint)

    def test_tautological(self):
        e = errors.PostgresError({})
        with self.assertRaises(errors.PostgresError):
            raise e
