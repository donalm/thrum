#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

"""
For most purposes, users will want to use the to_tsvector function within
postgresql. For testing the client encode/decode features I coded up this
TsVector class.

This could conceivably be useful if you were writing (for example) some
code to parse web pages using beautifulsoup and then index their content
with Python/Postgres.
"""
from collections import OrderedDict

import re


class TsVectorEntry(object):
    __slots__ = ('text', 'positions',)
    def __init__(self, text, position=None, weight='D'):
        self.text = text
        self.positions = set()
        self.add_position(position, weight)

    def add_position(self, position, weight='D'):
        """
        Lexemes that have positions can further be labeled with a weight, which
        can be A, B, C, or D. D is the default.
        """
        if position is None:
            return

        if weight not in ('A', 'B', 'C', 'D'):
            msg = "Illegal value '%s' for weight of '%s' at position %s"
            raise Exception(msg % (weight, self.text, position))

        if position < 1:
            msg = "tsvector positions start at 1. Cannot be %s"
            raise Exception(msg % (position,))

        self.positions.add((position, weight))

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if len(self.positions) != len(other.positions):
            return False
        for item in self.positions:
            if not item in other.positions:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def summarize(self):
        rval = []
        if not self.positions:
            rval.append(self.text)
        else:
            rval.append(self.text + ':')
            rval.append(','.join(['%s%s' % pos for pos in self.positions]))

        return ''.join(rval).rstrip()

    def __repr__(self):
        return '<TsVectorEntry (%s)>' % (self.summarize(),)


class TsVector(object):
    __slots__ = ('entries', )
    words = []
    rgx = re.compile("[^\w+]")

    def __init__(self):
        self.entries = OrderedDict()

    def __iter__(self):
        """
        So we can do things like:
        for tsentry in tsvector:
            print(tsentry.text)
        """
        return self.entries.itervalues()

    def __getitem__(self, index):
        if type(index) == int:
            for i, item in enumerate(self.entries.values()):
                if index == i:
                    return item
        return self.entries[index]

    def __len__(self):
        return len(self.entries)

    def __repr__(self):
        rval = ' '.join([entry.summarize() for entry in self.entries.values()])
        return '<TsVector (%s)>' % (rval,)

    def __str__(self):
        rval = "' '".join([entry.summarize() for entry in self.entries.values()])
        return "'" + rval + "'"

    def load_words_file(self):
        if TsVector.words:
            return

        try:
            fh = open('/usr/share/dict/words', 'r')
            TsVector.words = set([word.lower() for word in fh.read().strip().split()])
            fh.close()
        except Exception as e:
            return

        words = list(TsVector.words)

        for index, word in enumerate(words):
            words[index] = word.rsplit("'",1)[0]

            if word.endswith(("ing", "ed", "er", "s")):
                words[index] = self.find_stem(word)
        TsVector.words = set(words)
        del words

    def find_stem(self, word):
        word = word.lower()
        if word.endswith(("ies", "ier", "ied")):
            # tries, fried
            stem = word[0:-3] + 'y'
            if stem in TsVector.words:
                return stem

        if word.endswith("ly"):
            if word.endswith("ally"):
                # automatically
                if word[0:-4] in TsVector.words:
                    return word[0:-4]
            elif word[0:-2] in TsVector.words:
                # unfortunately
                return word[0:-2]

        if word.endswith("ation"):
            # confirmation
            if word[0:-5] in TsVector.words:
                return word[0:-5]

        if word.endswith(("er", "ed", "es")):
            # watcher, watched, watches
            if word[0:-2] in TsVector.words:
                return word[0:-2]
            # spited, spites
            if word[0:-1] in TsVector.words:
                return word[0:-1]
            # stopper, stopped
            if word[-4] == word[-3] and word[0:-3] in TsVector.words:
                return word[0:-3]

        if word.endswith("ing"):
            # watching
            if len(word) > 4 and word[0:-3] in TsVector.words:
                return word[0:-3]

            if len(word) > 5 and word[-5] == word[-4] and word[0:-4] in TsVector.words:
                # upping, stopping
                return word[0:-4]

            # pausing
            if len(word) > 5 and word[0:-3] + 'e' in TsVector.words:
                return word[0:-3] + 'e'

        if word.endswith("s"):
            if word == 'is':
                return word
            if word[0:-1] in TsVector.words:
                return word[0:-1]

        return word

    def normalize(self, word):
        return self.find_stem(word)

    def normalize_and_add_document(self, document):
        words = [x for x in self.rgx.split(document) if x not in ('s','')]
        for index, word in enumerate(words):
            self.normalize_and_add(word, position=index+1)

    def normalize_and_add(self, word, position=None, weight='D'):
        word = self.normalize(word)
        self.add_entry(word, position, weight)

    def add_entry(self, text, position=None, weight='D'):
        if text in self.entries:
            entry = self.entries.get(text)
            if position and weight:
                entry.add_position(position, weight)
            return entry

        entry = TsVectorEntry(text, position, weight)
        self.entries[text] = entry

