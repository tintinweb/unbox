#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>


import struct

class PeFileFormat:
    TYPE_MZ = 1
    TYPE_PE32 = 2
    TYPE_PE64 = 3
    TYPE_DOTNET = 4

    @staticmethod
    def petype(data):
        #
        # MZ header size == 0x40
        # PE Header location at MZ[0x3c] is at least 0x33 long
        if not (len(data) > 0x40 and data[0:2] == "MZ"):
            # not MZ
            return None

        t = PeFileFormat.TYPE_MZ

        offset = struct.unpack('I', data[0x3c:0x3c + 4])[0]
        if not (len(data) > offset + 0x33 and data[offset:offset + 4] == 'PE\0\0'):
            # MZ
            return t

        arch = data[offset + 0x18 + 1]
        if arch == '\x01':
            t = PeFileFormat.TYPE_PE32
        elif arch == '\x02':
            t = PeFileFormat.TYPE_PE64
        else:
            return t
        '''
          /*
Now we are at the end of the PE Header and from here, the
            PE Optional Headers starts...
      To go directly to the datadictionary, we'll increase the
      stream’s current position to with 96 (0x60). 96 because,
            28 for Standard fields
            68 for NT-specific fields
From here DataDictionary starts...and its of total 128 bytes. DataDictionay has 16 directories in total,
doing simple maths 128/16 = 8.
So each directory is of 8 bytes.
            In this 8 bytes, 4 bytes is of RVA and 4 bytes of Size.

btw, the 15th directory consist of CLR header! if its 0, its not a CLR file :)
            */'''

        if not len(data) >= offset + 0x78 + 4:
            return t
        # datadir start
        datadir_offset = offset + 0x78
        # last datadir
        if not len(data) >= 8 * 14 + datadir_offset + 8:
            return t
        # check last datadir: http://geekswithblogs.net/rupreet/archive/2005/11/02/58873.aspx
        datadir_rva, datdir_size = struct.unpack('II', data[8 * 14 + datadir_offset:8 * 14 + datadir_offset + 8])
        if datadir_rva != 0x00:
            t = PeFileFormat.TYPE_DOTNET
        # PE
        return t
