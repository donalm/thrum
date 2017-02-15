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

import six
import struct

try:
    from exceptions import KeyError
    from exceptions import ValueError
except ImportError:
    pass


from twisted.trial import unittest

from thrum import constants
from thrum import binary

class BinaryTests(unittest.TestCase):

    def test_get_unpack_ints_for_index(self):
        cached_unpack_int = binary.Cache.get_unpack_ints_for_index(1)
        unpack_int = struct.Struct('!i').unpack_from

        one = b'\x00\x00\x00\x01'
        self.assertEqual(cached_unpack_int(one), unpack_int(one))

    def test_get_pack_shorts_for_index(self):
        cached_pack_short = binary.Cache.get_pack_shorts_for_index(1)
        pack_short = struct.Struct('!h').pack

        two = 2
        self.assertEqual(cached_pack_short(two), pack_short(two))

    def test_h_pack(self):
        # signed short

        self.assertEqual(b'\x7f\xff', binary.h_pack(constants.MAX_INT2))
        with self.assertRaises(binary.error):
            binary.h_pack(constants.MAX_INT2 +1)

        self.assertEqual(b'\x80\x00', binary.h_pack(constants.MIN_INT2))
        with self.assertRaises(binary.error):
            binary.h_pack(constants.MIN_INT2 -1)

    def test_h_unpack(self):
        self.assertEqual(binary.h_unpack(b'\x7f\xff'), (constants.MAX_INT2,))
        self.assertEqual(binary.h_unpack(b'\x80\x00'), (constants.MIN_INT2,))

    def test_H_pack(self):
        # Unsigned short

        self.assertEqual(b'\xff\xff', binary.H_pack(constants.MAX_INT2U))
        with self.assertRaises(binary.error):
            binary.H_pack(constants.MAX_INT2U +1)

        self.assertEqual(b'\x00\x00', binary.H_pack(constants.MIN_INT2U))
        with self.assertRaises(binary.error):
            binary.H_pack(constants.MIN_INT2U -1)

    def test_H_unpack(self):
        self.assertEqual(binary.H_unpack(b'\xff\xff'), (constants.MAX_INT2U,))
        self.assertEqual(binary.H_unpack(b'\x00\x00'), (constants.MIN_INT2U,))

    def test_i_pack(self):
        self.assertEqual(b'\x7f\xff\xff\xff', binary.i_pack(constants.MAX_INT4))
        with self.assertRaises(binary.error):
            binary.i_pack(constants.MAX_INT4 +1)

        self.assertEqual(b'\x80\x00\x00\x00', binary.i_pack(constants.MIN_INT4))
        with self.assertRaises(binary.error):
            binary.i_pack(constants.MIN_INT4 -1)

    def test_i_unpack(self):
        self.assertEqual(binary.i_unpack(b'\x7f\xff\xff\xff'), (constants.MAX_INT4,))
        self.assertEqual(binary.i_unpack(b'\x80\x00\x00\x00'), (constants.MIN_INT4,))

    def test_I_pack(self):
        self.assertEqual(b'\xff\xff\xff\xff', binary.I_pack(constants.MAX_INT4U))
        with self.assertRaises(binary.error):
            binary.I_pack(constants.MAX_INT4U +1)

        self.assertEqual(b'\x00\x00\x00\x00', binary.I_pack(constants.MIN_INT4U))
        with self.assertRaises(binary.error):
            binary.I_pack(constants.MIN_INT4U -1)

    def test_I_unpack(self):
        self.assertEqual(binary.I_unpack(b'\xff\xff\xff\xff'), (constants.MAX_INT4U,))
        self.assertEqual(binary.I_unpack(b'\x00\x00\x00\x00'), (constants.MIN_INT4U,))

    def test_q_pack(self):
        self.assertEqual(b'\x7f\xff\xff\xff\xff\xff\xff\xff', binary.q_pack(constants.MAX_INT8))
        with self.assertRaises(binary.error):
            binary.q_pack(constants.MAX_INT8 +1)

        self.assertEqual(b'\x80\x00\x00\x00\x00\x00\x00\x00', binary.q_pack(constants.MIN_INT8))
        with self.assertRaises(binary.error):
            binary.q_pack(constants.MIN_INT8 -1)

    def test_q_unpack(self):
        self.assertEqual(binary.q_unpack(b'\x7f\xff\xff\xff\xff\xff\xff\xff'), (constants.MAX_INT8,))
        self.assertEqual(binary.q_unpack(b'\x80\x00\x00\x00\x00\x00\x00\x00'), (constants.MIN_INT8,))

    def test_Q_pack(self):
        self.assertEqual(b'\xff\xff\xff\xff\xff\xff\xff\xff', binary.Q_pack(constants.MAX_INT8U))
        with self.assertRaises(binary.error):
            binary.Q_pack(constants.MAX_INT8U +1)

        if six.PY2:
            self.assertEqual(b'\x00\x00\x00\x00\x00\x00\x00\x00', binary.Q_pack(constants.MIN_INT8U))
            with self.assertRaises(Exception):
                binary.Q_pack(constants.MIN_INT8U -1)
        else:
            self.assertEqual(b'\x00\x00\x00\x00\x00\x00\x00\x00', binary.Q_pack(constants.MIN_INT8U))
            with self.assertRaises(binary.error):
                binary.Q_pack(constants.MIN_INT8U -1)

    def test_Q_unpack(self):
        self.assertEqual(binary.Q_unpack(b'\xff\xff\xff\xff\xff\xff\xff\xff'), (constants.MAX_INT8U,))
        self.assertEqual(binary.Q_unpack(b'\x00\x00\x00\x00\x00\x00\x00\x00'), (constants.MIN_INT8U,))

    def test_d_pack(self):
        self.assertEqual(b'\x001\xfa\x18,@\xc6\r', binary.d_pack(1E-307))

    def test_d_unpack(self):
        self.assertEqual(binary.d_unpack(b'\x001\xfa\x18,@\xc6\r'), (1E-307,))

    def test_dd_pack(self):
        self.assertEqual(
            b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r',
            binary.dd_pack(1e-307, 1e-307))

    def test_dd_unpack(self):
        self.assertEqual(
            binary.dd_unpack(b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r'),
            (1e-307, 1e-307))

    def test_ddd_pack(self):
        self.assertEqual(
            b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r',
            binary.ddd_pack(1e-307, 1e-307, 1e-307))

    def test_ddd_unpack(self):
        self.assertEqual(
            binary.ddd_unpack(b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r'),
            (1e-307, 1e-307, 1e-307))

    def test_dddd_pack(self):
        self.assertEqual(
            b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r',
            binary.dddd_pack(1e-307, 1e-307, 1e-307, 1e-307))

    def test_dddd_unpack(self):
        self.assertEqual(
            binary.dddd_unpack(
                b'\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r\x001\xfa\x18,@\xc6\r'
            ), (1e-307, 1e-307, 1e-307, 1e-307))

    def test_f_pack(self):
        self.assertEqual(b'?\xc0\x00\x00', binary.f_pack(1.5))

    def test_f_unpack(self):
        self.assertEqual(binary.f_unpack(b'?\xc0\x00\x00'), (1.5,))

    def test_bh_pack(self):
        self.assertEqual(
            b'\x7f\x04\x00',
            binary.bh_pack(127, 1024))

    def test_bh_unpack(self):
        self.assertEqual(
            binary.bh_unpack(b'\x7f\x04\x00'),
            (127, 1024))

    def test_ci_pack(self):
        self.assertEqual(
            b'D\x00\x00\x04\x00',
            binary.ci_pack(b'D', 1024))

    def test_ci_unpack(self):
        self.assertEqual(
            binary.ci_unpack(b'D\x00\x00\x04\x00'),
            (b'D', 1024))

    def test_qi_pack(self):
        self.assertEqual(
            b'\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x04\x00',
            binary.qi_pack(4096, 1024))

    def test_qi_unpack(self):
        self.assertEqual(
            binary.qi_unpack(b'\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x04\x00'),
            (4096, 1024))

    def test_qii_pack(self):
        self.assertEqual(
            b'\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x04\x00\x00\x00\x08\x00',
            binary.qii_pack(4096, 1024, 2048))

    def test_qii_unpack(self):
        self.assertEqual(
            binary.qii_unpack(b'\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x04\x00\x00\x00\x08\x00'),
            (4096, 1024, 2048))

    def test_dii_pack(self):
        self.assertEqual(
            b'\x001\xfa\x18,@\xc6\r\x00\x00\x04\x00\x00\x00\x08\x00',
            binary.dii_pack(1e-307, 1024, 2048))

    def test_dii_unpack(self):
        self.assertEqual(
            binary.dii_unpack(b'\x001\xfa\x18,@\xc6\r\x00\x00\x04\x00\x00\x00\x08\x00'),
            (1e-307, 1024, 2048))

    def test_b_pack(self):
        self.assertEqual(
            b'\x7f',
            binary.b_pack(127))

    def test_b_unpack(self):
        self.assertEqual(
            binary.b_unpack(b'\x7f'),
            (127,))

    def test_bii_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x08\x00',
            binary.bii_pack(127, 1024, 2048))

    def test_bii_unpack(self):
        self.assertEqual(
            binary.bii_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x08\x00'),
            (127, 1024, 2048))

    def test_biq_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00',
            binary.biq_pack(127, 1024, 4096))

    def test_biq_unpack(self):
        self.assertEqual(
            binary.biq_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00'),
            (127, 1024, 4096))

    def test_biqi_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00 \x00',
            binary.biqi_pack(127, 1024, 4096, 8192))

    def test_biqi_unpack(self):
        self.assertEqual(
            binary.biqi_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00 \x00'),
            (127, 1024, 4096, 8192))

    def test_biiq_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00 \x00',
            binary.biiq_pack(127, 1024, 4096, 8192))

    def test_biiq_unpack(self):
        self.assertEqual(
            binary.biiq_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00 \x00'),
            (127, 1024, 4096, 8192))

    def test_biii_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00 \x00',
            binary.biii_pack(127, 1024, 4096, 8192))

    def test_biii_unpack(self):
        self.assertEqual(
            binary.biii_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00 \x00'),
            (127, 1024, 4096, 8192))

    def test_biiii_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x01\x00\x00',
            binary.biiii_pack(127, 1024, 4096, 8192, 65536))

    def test_biiii_unpack(self):
        self.assertEqual(
            binary.biiii_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x01\x00\x00'),
            (127, 1024, 4096, 8192, 65536))

    def test_biqiq_pack(self):
        self.assertEqual(
            b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x01\x00\x00',
            binary.biqiq_pack(127, 1024, 4096, 8192, 65536))

    def test_biqiq_unpack(self):
        self.assertEqual(
            binary.biqiq_unpack(b'\x7f\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x01\x00\x00'),
            (127, 1024, 4096, 8192, 65536))

    def test_c_pack(self):
        self.assertEqual(
            b'G',
            binary.c_pack(b'G'))

    def test_c_unpack(self):
        self.assertEqual(
            binary.c_unpack(b'G'),
            (b'G',))

    def test_cccc_pack(self):
        self.assertEqual(
            b'GIVE',
            binary.cccc_pack(b'G', b'I', b'V', b'E'))

    def test_cccc_unpack(self):
        self.assertEqual(
            binary.cccc_unpack(b'GIVE'),
            (b'G', b'I', b'V', b'E'))

    def test_ihihih_pack(self):
        self.assertEqual(
            b'\x00\x00\x00\x01\x00\x02\x00\x00\x00\x03\x00\x04\x00\x00\x00\x05\x00\x06',
            binary.ihihih_pack(1,2,3,4,5,6))

    def test_ihihih_unpack(self):
        self.assertEqual(
            binary.ihihih_unpack(b'\x00\x00\x00\x01\x00\x02\x00\x00\x00\x03\x00\x04\x00\x00\x00\x05\x00\x06'),
            (1,2,3,4,5,6))

    def test_hhHh_pack(self):
        self.assertEqual(
            b'\x00\x01\x00\x01\x00\x01\x00\x01',
            binary.hhHh_pack(1,1,1,1))

    def test_hhHh_unpack(self):
        self.assertEqual(
            binary.hhHh_unpack(b'\x00\x01\x00\x01\x00\x01\x00\x01'),
            (1,1,1,1))

    def test_B_pack(self):
        self.assertEqual(
            b'\xff',
            binary.B_pack(255))

    def test_B_unpack(self):
        self.assertEqual(
            binary.B_unpack(b'\xff'),
            (255,))

    def test_Bi_pack(self):
        self.assertEqual(
            b'\xff\x00\x00\x00\x01',
            binary.Bi_pack(255, 1))

    def test_Bi_unpack(self):
        self.assertEqual(
            binary.Bi_unpack(b'\xff\x00\x00\x00\x01'),
            (255, 1))

    def test_BBBB_pack(self):
        self.assertEqual(
            b'\xff\x01\xff\x01',
            binary.BBBB_pack(255, 1, 255, 1))

    def test_BBBB_unpack(self):
        self.assertEqual(
            binary.BBBB_unpack(b'\xff\x01\xff\x01'),
            (255, 1, 255, 1))

    def test_BBBBBB_pack(self):
        self.assertEqual(
            b'\xff\x01\xff\x01\xff\x01',
            binary.BBBBBB_pack(255, 1, 255, 1, 255, 1))

    def test_BBBBBB_unpack(self):
        self.assertEqual(
            binary.BBBBBB_unpack(b'\xff\x01\xff\x01\xff\x01'),
            (255, 1, 255, 1, 255, 1))

    def test_cached_methods(self):
        for index, item in enumerate(list(range(1, binary.Cache._limit_ints))):
            candidate = tuple(range(item))
            l = len(candidate)
            int_packer = binary.Cache.pack_ints[l]
            result = int_packer(*candidate)
            int_unpacker = binary.Cache.unpack_ints[l]
            self.assertEqual(candidate, int_unpacker(result))

        for index, item in enumerate(list(range(1, binary.Cache._limit_shorts))):
            candidate = tuple(range(item))
            l = len(candidate)
            short_packer = binary.Cache.pack_shorts[l]
            result = short_packer(*candidate)
            short_unpacker = binary.Cache.unpack_shorts[l]
            self.assertEqual(candidate, short_unpacker(result))


        with self.assertRaises(KeyError):
            packer = binary.Cache.pack_ints[binary.Cache._limit_ints]

        with self.assertRaises(KeyError):
            packer = binary.Cache.pack_shorts[binary.Cache._limit_shorts]






