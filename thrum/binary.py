#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

"""
Pack and unpack data using network (big-endian) byte order per the Postgres
wire protocol
"""

import struct

error = struct.error


class Cache(object):
    '''
    Cache for pack/unpack methods, e.g. to unpack bytes representing a sequence
    of 6 x 32 bit signed ints:
    (1,2,3,4,5,6) = Cache.unpack_ints[6](bytes)

    To pack a sequence of integers as 32 bit signed:
    sequence = (1,2,3,4)
    quantity = len(sequence)
    bytes = Cache.pack_ints[quantity](*sequence)
    '''
    pack_ints = {}
    unpack_ints = {}

    pack_shorts = {}
    unpack_shorts = {}

    _limit_ints = 20
    _limit_shorts = 20

    _ready = False

    @classmethod
    def init(cls):
        if cls._ready:
            return
        cls._ints()
        cls._shorts()
        cls._ready = True

    @classmethod
    def _create_funcs(cls, fmt, limit, packers, unpackers):
        for index in range(1, limit):
            packer, unpacker = cls._create_func_pair(index, fmt)
            packers[index] = packer
            unpackers[index] = unpacker

    @classmethod
    def _create_func_pair(cls, index, fmt):
        struc = struct.Struct('!' + (index * fmt))
        return struc.pack, struc.unpack_from

    @classmethod
    def _ints(cls):
        cls._create_funcs('i', cls._limit_ints,
                          cls.pack_ints, cls.unpack_ints)

    @classmethod
    def _shorts(cls):
        cls._create_funcs('h', cls._limit_shorts,
                          cls.pack_shorts, cls.unpack_shorts)

    @classmethod
    def get_pack_shorts_for_index(cls, index):
        if index not in cls.pack_shorts:
            packer, unpacker = cls._create_func_pair(index, 'h')
            return packer

        return cls.pack_shorts[index]

    @classmethod
    def get_unpack_ints_for_index(cls, index):
        if index not in cls.unpack_ints:
            packer, unpacker = cls._create_func_pair(index, 'i')
            return unpacker

        return cls.unpack_ints[index]


Cache.init()


"""
Precompile some pack/unpack methods that are frequently used in the Postgres
protocol
"""
i_pack = Cache.pack_ints[1]
ii_pack = Cache.pack_ints[2]
iii_pack = Cache.pack_ints[3]

i_unpack = Cache.unpack_ints[1]
ii_unpack = Cache.unpack_ints[2]
iii_unpack = Cache.unpack_ints[3]

h_pack = Cache.pack_shorts[1]
h_unpack = Cache.unpack_shorts[1]


def _pack_funcs(fmt):
    struc = struct.Struct('!' + fmt)
    return struc.pack, struc.unpack_from


H_pack, H_unpack = _pack_funcs('H')
I_pack, I_unpack = _pack_funcs('I')
q_pack, q_unpack = _pack_funcs('q')
Q_pack, Q_unpack = _pack_funcs('Q')
d_pack, d_unpack = _pack_funcs('d')
dd_pack, dd_unpack = _pack_funcs('dd')
ddd_pack, ddd_unpack = _pack_funcs('ddd')
dddd_pack, dddd_unpack = _pack_funcs('dddd')
f_pack, f_unpack = _pack_funcs('f')
bh_pack, bh_unpack = _pack_funcs('bh')
ci_pack, ci_unpack = _pack_funcs('ci')
qi_pack, qi_unpack = _pack_funcs('qi')
qii_pack, qii_unpack = _pack_funcs('qii')
dii_pack, dii_unpack = _pack_funcs('dii')
b_pack, b_unpack = _pack_funcs('b')
bii_pack, bii_unpack = _pack_funcs('bii')
biq_pack, biq_unpack = _pack_funcs('biq')
biqi_pack, biqi_unpack = _pack_funcs('biqi')
biiq_pack, biiq_unpack = _pack_funcs('biiq')
biii_pack, biii_unpack = _pack_funcs('biii')
biiii_pack, biiii_unpack = _pack_funcs('biiii')
biqiq_pack, biqiq_unpack = _pack_funcs('biqiq')
c_pack, c_unpack = _pack_funcs('c')
cccc_pack, cccc_unpack = _pack_funcs('cccc')
ihihih_pack, ihihih_unpack = _pack_funcs('ihihih')
hhHh_pack, hhHh_unpack = _pack_funcs('hhHh')
B_pack, B_unpack = _pack_funcs('B')
Bi_pack, Bi_unpack = _pack_funcs('Bi')
BBBB_pack, BBBB_unpack = _pack_funcs('BBBB')
BBBBBB_pack, BBBBBB_unpack = _pack_funcs('BBBBBB')
