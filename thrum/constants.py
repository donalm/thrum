#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# Copyright (c) Dónal McMullan
# See LICENSE for details.

import os
import sys
import socket

from . import binary

# Format code
FC_TEXT = 0
FC_BINARY = 1

# IP address family codes
PGSQL_AF_INET = 2  # IPv4
PGSQL_AF_INET6 = 3  # IPv6

# PG constants for numeric types
NUMERIC_POS = 0x0000
NUMERIC_NEG = 0x4000
NUMERIC_NAN = 0xC000

# Default protocol version
VERSION_MAJOR    = 3
VERSION_MINOR    = 0
DEFAULT_PROTOCOL_VERSION = (VERSION_MAJOR << 16) | VERSION_MINOR

# Message codes
NOTICE_RESPONSE = b'N'
AUTHENTICATION_REQUEST = b'R'
PARAMETER_STATUS = b'S'
BACKEND_KEY_DATA = b'K'
READY_FOR_QUERY = b'Z'
ROW_DESCRIPTION = b'T'
ERROR_RESPONSE = b'E'
DATA_ROW = b'D'
COMMAND_COMPLETE = b'C'
PARSE_COMPLETE = b'1'
BIND_COMPLETE = b'2'
CLOSE_COMPLETE = b'3'
PORTAL_SUSPENDED = b's'
NO_DATA = b'n'
PARAMETER_DESCRIPTION = b't'
NOTIFICATION_RESPONSE = b'A'
COPY_DONE = b'c'
COPY_DATA = b'd'
COPY_IN_RESPONSE = b'G'
COPY_OUT_RESPONSE = b'H'
EMPTY_QUERY_RESPONSE = b'I'

BIND = b'B'
PARSE = b'P'
EXECUTE = b'E'
FLUSH = b'H'
SYNC = b'S'
PASSWORD = b'p'
DESCRIBE = b'D'
TERMINATE = b'X'
CLOSE = b'C'

FLUSH_MSG = FLUSH + binary.i_pack(4)
SYNC_MSG = SYNC + binary.i_pack(4)
TERMINATE_MSG = TERMINATE + binary.i_pack(4)
COPY_DONE_MSG = COPY_DONE + binary.i_pack(4)

# DESCRIBE constants
STATEMENT = b'S'
PORTAL = b'P'

# ErrorResponse codes
RESPONSE_CODE = b'C'  # always present

# READY FOR QUERY VALUES
IDLE = b'I'
IDLE_IN_TRANSACTION = b'T'
IDLE_IN_FAILED_TRANSACTION = b'E'

# typtype from pg_type table:
# https://www.postgresql.org/docs/9.6/static/catalog-pg-type.html
ENUM_TYPE = 'e'
BASE_TYPE = 'b'
COMPOSITE_TYPE = 'c'
DOMAIN_TYPE = 'd'
PSEUDO_TYPE = 'p'
RANGE_TYPE = 'r'

try:
    HOSTNAME = socket.gethostname()
except Exception as e:
    HOSTNAME = 'UNKNOWNHOST'

try:
    PID = str(os.getpid())
except Exception as e:
    PID = 'UNKNOWNPID'

try:
    EXECUTABLE = os.path.basename(sys.executable)
except Exception as e:
    EXECUTABLE = 'UNKNOWNEXECUTABLE'

APPLICATION_NAME = '%s_%s_%s' % (HOSTNAME, PID, EXECUTABLE,)

MIN_INT2 = -2 ** 15
MAX_INT2 =  2 ** 15 - 1
MIN_INT4 = -2 ** 31
MAX_INT4 =  2 ** 31 - 1
MIN_INT8 = -2 ** 63
MAX_INT8 =  2 ** 63 - 1

MIN_INT2U = 0
MAX_INT2U = 2 ** 16 - 1
MIN_INT4U = 0
MAX_INT4U = 2 ** 32 - 1
MIN_INT8U = 0
MAX_INT8U = 2 ** 64 - 1

BINARY_SPACE = b' '
DDL_COMMANDS = b'ALTER', b'CREATE'
NULL = binary.i_pack(-1)
NULL_BYTE = b'\x00'

BINARY = bytes

"""
Direct copy from pg8000
"""
pg_to_py = {
    # Not supported:
    'mule_internal': None,
    'euc_tw': None,

    # Name fine as-is:
    # 'euc_jp',
    # 'euc_jis_2004',
    # 'euc_kr',
    # 'gb18030',
    # 'gbk',
    # 'johab',
    # 'sjis',
    # 'shift_jis_2004',
    # 'uhc',
    # 'utf8',

    # Different name:
    'euc_cn': 'gb2312',
    'iso_8859_5': 'is8859_5',
    'iso_8859_6': 'is8859_6',
    'iso_8859_7': 'is8859_7',
    'iso_8859_8': 'is8859_8',
    'koi8': 'koi8_r',
    'latin1': 'iso8859-1',
    'latin2': 'iso8859_2',
    'latin3': 'iso8859_3',
    'latin4': 'iso8859_4',
    'latin5': 'iso8859_9',
    'latin6': 'iso8859_10',
    'latin7': 'iso8859_13',
    'latin8': 'iso8859_14',
    'latin9': 'iso8859_15',
    'sql_ascii': 'ascii',
    'win866': 'cp886',
    'win874': 'cp874',
    'win1250': 'cp1250',
    'win1251': 'cp1251',
    'win1252': 'cp1252',
    'win1253': 'cp1253',
    'win1254': 'cp1254',
    'win1255': 'cp1255',
    'win1256': 'cp1256',
    'win1257': 'cp1257',
    'win1258': 'cp1258',
    'unicode': 'utf-8',  # Needed for Amazon Redshift
}

