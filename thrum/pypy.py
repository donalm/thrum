#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

"""
Provide implementations of pypy3's BytesBuilder and newlist_hint for pypy2
and cpython
"""

try:
    try:
        from __pypy__.builders import BytesBuilder
    except Exception:
        from __pypy__.builders import StringBuilder as BytesBuilder
except:
    class BytesBuilder(object):
        suboptimal = True  # To help identify which version we're using

        def __init__(self, *args):
            self.buffer = []
            self.append = self.buffer.append

        def build(self):
            return b"".join(self.buffer)

        def append_slice(self, value, start, end):
            self.append(value[start:end])

        def __len__(self):
            return(sum(len(x) for x in self.buffer))

try:
    from __pypy__ import newlist_hint
except ImportError:
    def newlist_hint(x):
        return []
