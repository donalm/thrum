#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.


class ThrumError(Exception):
    pass


class PostgresError(Exception):
    """
    Parse the fields that Postgres returns in its error messages into a Python
    Exception with the attributes listed in 'keys'

    More info on the Postgres fields can be found here:
    https://www.postgresql.org/docs/9.6/static/protocol-error-fields.html
    """
    keys = {'S': 'severity_local',
            'V': 'severity',
            'C': 'sqlstate_code',
            'M': 'message',
            'D': 'detail',
            'H': 'hint',
            'P': 'position',
            'p': 'position_internal',
            'q': 'query_internal',
            'W': 'where',
            's': 'schema',
            't': 'table',
            'c': 'column',
            'd': 'data_type',
            'n': 'constraint',
            'F': 'file',
            'L': 'line',
            'R': 'routine'}

    def __init__(self, error_data):
        for key, value in self.keys.items():
            setattr(self, value, error_data.get(key))

    def __str__(self):
        r = "PostgresError: %s" % (self.message,)
        return r
