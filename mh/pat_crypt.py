#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter PAT Crypt module."""

try:
    import camellia
    import hashlib
    ENCRYPTION_ENABLED=True
except ImportError:
    ENCRYPTION_ENABLED=False
    pass

import struct

KEY_BIT_LENGTH = 256
BLOCK_SIZE = 16

SIZE_FMT = struct.Struct(">Hxx")

if not ENCRYPTION_ENABLED:
    def keytable(key):
        # type: (bytes) -> list
        return []
    
    def encrypt(data, keytable):
        # type: (bytes, list) -> bytes
        return data
    
    def decrypt(data, keytable):
        # type: (bytes, list) -> bytes
        return data

else:
    def keytable(key):
        # type: (bytes) -> list
        assert len(key) * 8 == KEY_BIT_LENGTH
        return camellia.Camellia_Ekeygen(key)
    
    def encrypt(data, keytable):
        # type: (bytes, list) -> bytes
        out = b""

        out_block = b"\x00" * BLOCK_SIZE
        block = bytearray(b"\x00" * BLOCK_SIZE)
        block_offset = 0

        # Pack the data size into the encrypted payload
        data_size = len(data)
        SIZE_FMT.pack_into(block, block_offset, data_size)
        block_offset += SIZE_FMT.size

        data_offset = 0
        # Encrypt the data
        while data_offset < data_size:
            space_in_block = BLOCK_SIZE - block_offset
            data_end = min(data_offset + space_in_block, data_size)
            block[block_offset:] = data[data_offset:data_end]

            b = bytes(block)
            camellia.lib.Camellia_EncryptBlock(KEY_BIT_LENGTH, b, keytable, out_block)
            out += out_block

            data_offset += space_in_block
            block_offset = 0
        
        return out
    
    def decrypt(data, keytable):
        # type: (bytes, list) -> bytes
        data_size = len(data)
        if (data_size % BLOCK_SIZE) != 0:
            raise ValueError("Data it's not aligned to BLOCK_SIZE")
        
        out = b""
        out_block = b"\x00" * BLOCK_SIZE
        block = bytearray(b"\x00" * BLOCK_SIZE)
        data_offset = 0
        while data_offset < data_size:
            block[:BLOCK_SIZE] = data[data_offset:data_offset+BLOCK_SIZE]
            b = bytes(block)
            camellia.lib.Camellia_DecryptBlock(KEY_BIT_LENGTH, b, keytable, out_block)
            out += out_block
            data_offset += len(out_block)
        payload_size, = SIZE_FMT.unpack_from(out, 0)
        return out[SIZE_FMT.size:SIZE_FMT.size+payload_size]
    

def test_encrypt_decrypt():
    import hashlib
    key = hashlib.sha256("12345678910".encode('utf-8')).digest()
    key_table = keytable(key)
    data = "Hello".encode('utf-8')

    encrypted = encrypt(data, key_table)
    decrypted = decrypt(encrypted, key_table)

    assert data == decrypted
    print(decrypted.decode('utf-8'))