#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter PAT item module.

    Monster Hunter 3 Server Project
    Copyright (C) 2021  Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import struct

from collections import OrderedDict


class ItemType:
    Custom = 0
    Byte = 1
    Word = 2
    Long = 3
    LongLong = 4
    String = 5
    Binary = 6
    Object = 7


def lp_string(s):
    """1-byte length-prefixed string."""
    if isinstance(s, str):
        s = s.encode("ascii")
    return struct.pack(">B", len(s)) + s


def unpack_lp_string(data, offset=0):
    """Unpack lp_string."""
    size, = struct.unpack_from(">B", data, offset)
    return data[offset+1:offset+1+size]


def lp2_string(s):
    """2-bytes length-prefixed string."""
    if isinstance(s, str):
        s = s.encode("ascii")
    return struct.pack(">H", len(s)) + s


def unpack_lp2_string(data, offset=0):
    """Unpack lp2_string."""
    size, = struct.unpack_from(">H", data, offset)
    return data[offset+2:offset+2+size]


class Item(bytes):
    pass


def pack_byte(b):
    """Pack PAT item byte."""
    return struct.pack(">BB", ItemType.Byte, b)


def unpack_byte(data, offset=0):
    """Unpack PAT item byte."""
    item_type, value = struct.unpack_from(">BB", data, offset)
    if item_type != ItemType.Byte:
        raise AssertionError("Invalid type for byte item: {}".format(
            item_type
        ))
    return value


class Byte(Item):
    """PAT item byte class."""
    def __new__(cls, b):
        return Item.__new__(cls, pack_byte(b))

    def __repr__(self):
        return "Byte({!r})".format(unpack_byte(self))


class ByteDec(Byte):
    """PAT item byte that will be decremented."""
    pass


def pack_word(w):
    """Pack PAT item word."""
    return struct.pack(">BH", ItemType.Word, w)


def unpack_word(data, offset=0):
    """Unpack PAT item word."""
    item_type, value = struct.unpack_from(">BH", data, offset)
    if item_type != ItemType.Word:
        raise AssertionError("Invalid type for word item: {}".format(
            item_type
        ))
    return value


class Word(Item):
    """PAT item word class."""
    def __new__(cls, w):
        return Item.__new__(cls, pack_word(w))

    def __repr__(Word):
        return "Word({!r})".format(unpack_word(self))


class WordDec(Word):
    """PAT item word that will be decremented."""
    pass


def pack_long(lg):
    """Pack PAT item long."""
    return struct.pack(">BI", ItemType.Long, lg)


def unpack_long(data, offset=0):
    """Unpack PAT item long."""
    item_type, value = struct.unpack_from(">BI", data, offset)
    if item_type != ItemType.Long:
        raise AssertionError("Invalid type for long item: {}".format(
            item_type
        ))
    return value


class Long(Item):
    """PAT item long class."""
    def __new__(cls, lg):
        return Item.__new__(cls, pack_long(lg))

    def __repr__(self):
        return "Long({!r})".format(unpack_long(self))


def pack_longlong(q):
    """Pack PAT item long long."""
    return struct.pack(">BQ", ItemType.LongLong, q)


def unpack_longlong(data, offset=0):
    """Unpack PAT item long long."""
    item_type, value = struct.unpack_from(">BQ", data, offset)
    if item_type != ItemType.LongLong:
        raise AssertionError("Invalid type for long long item: {}".format(
            item_type
        ))
    return value


class LongLong(Item):
    """PAT item long long class."""
    def __new__(cls, q):
        return Item.__new__(cls, pack_longlong(q))

    def __repr__(self):
        return "LongLong({!r})".format(unpack_longlong(self))


def pack_string(s):
    """Pack PAT item string."""
    if isinstance(s, str):
        s = s.encode("ascii")
    return struct.pack(">B", ItemType.String) + lp2_string(s)


def unpack_string(data, offset=0):
    """Unpack PAT item string."""
    item_type, length = struct.unpack_from(">BH", data, offset)
    if item_type != ItemType.String:
        raise AssertionError("Invalid type for string item: {}".format(
            item_type
        ))
    return data[offset+3:offset+3+length]


class String(Item):
    """PAT item string class."""
    def __new__(cls, s):
        return Item.__new__(cls, pack_string(s))

    def __repr__(self):
        return "String({!r})".format(unpack_string(self))


def pack_binary(s):
    """Pack PAT item binary."""
    if isinstance(s, str):
        s = s.encode("ascii")
    return struct.pack(">BH", ItemType.Binary, len(s)) + s


def unpack_binary(data, offset=0):
    """Unpack PAT item binary."""
    item_type, length = struct.unpack_from(">BH", data, offset)
    if item_type != ItemType.Binary:
        raise AssertionError("Invalid type for binary item: {}".format(
            item_type
        ))
    return data[offset+3:offset+3+length]


class Binary(Item):
    """PAT item binary class."""
    def __new__(cls, b):
        return Item.__new__(cls, pack_binary(b))

    def __repr__(self):
        return "Binary({!r})".format(repr(unpack_binary(self)))


def unpack_any(data, offset=0):
    """Unpack PAT item."""
    item_type, = struct.unpack_from(">B", data, offset)
    handler = {
        ItemType.Byte: unpack_byte,
        ItemType.Word: unpack_word,
        ItemType.Long: unpack_long,
        ItemType.LongLong: unpack_longlong,
        ItemType.String: unpack_string,
        ItemType.Binary: unpack_binary
    }
    return item_type, handler[item_type](data, offset)


class Custom(Item):
    """PAT custom item class."""
    def __new__(cls, b, item_type=b'\0'):
        return Item.__new__(cls, item_type + b)

    def __repr__(self):
        return "Custom({!r})".format(repr(self[1:]))


def unpack_bytes(data, offset=0):
    """Unpack bytes list."""
    count, = struct.unpack_from(">B", data, offset)
    return struct.unpack_from(">" + count * "B", data, offset+1)


class PatData(OrderedDict):
    """Pat structure holding items."""
    FIELDS = (
        (1, "field_0x01"),
        (2, "field_0x02"),
        (3, "field_0x03"),
        (4, "field_0x04")
    )

    def __repr__(self):
        items = [
            (index, value)
            for index, value in self.items()
            if value is not None
        ]
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                "{}={}".format(self.field_name(index), repr(value))
                for index, value in items
            )
        )

    def __getattr__(self, name):
        for field_id, field_name in self.FIELDS:
            if name == field_name:
                if field_id not in self:
                    raise AttributeError("{} not set".format(name))
                return self[field_id]
        raise AttributeError("Unknown field: {}".format(name))

    def __setattr__(self, name, value):
        for field_id, field_name in self.FIELDS:
            if name == field_name:
                if not isinstance(value, Item):
                    raise ValueError("{!r} not a valid PAT item".format(value))
                self[field_id] = value
                return
        if name.startswith("_"):
            return OrderedDict.__setattr__(self, name, value)
        raise AttributeError("Cannot set unknown field: {}".format(name))

    def __delattr__(self, name):
        for field_id, field_name in self.FIELDS:
            if name == field_name:
                del self[field_id]
                return
        return OrderedDict.__delattr__(self, name)

    def __setitem__(self, key, value):
        if not isinstance(key, int) or not (0 <= key <= 255):
            raise IndexError("index must be a valid numeric value")
        elif not isinstance(value, Item):
            raise ValueError("{!r} not a valid PAT item".format(value))
        return OrderedDict.__setitem__(self, key, value)

    def field_name(self, index):
        for field_id, field_name in self.FIELDS:
            if index == field_id:
                return field_name
        return "field_0x{:02x}".format(index)

    def pack(self):
        """Pack PAT items."""
        items = [
            (index, value)
            for index, value in self.items()
            if value is not None
        ]
        return struct.pack(">B", len(items)) + b"".join(
            (struct.pack(">B", index) + value)
            for index, value in items
        )

    @classmethod
    def unpack(cls, data, offset=0):
        obj = cls()
        field_count, = struct.unpack_from(">B", data, offset)
        offset += 1
        for _ in range(field_count):
            field_id, = struct.unpack_from(">B", data, offset)
            offset += 1
            item_type, value = unpack_any(data, offset)
            offset += 1
            if item_type == ItemType.Byte:
                obj[field_id] = Byte(value)
                offset += 1
            elif item_type == ItemType.Word:
                obj[field_id] = Word(value)
                offset += 2
            elif item_type == ItemType.Long:
                obj[field_id] = Long(value)
                offset += 4
            elif item_type == ItemType.LongLong:
                obj[field_id] = LongLong(value)
                offset += 8
            elif item_type == ItemType.String:
                obj[field_id] = String(value)
                offset += 2 + len(value)
            elif item_type == ItemType.Binary:
                obj[field_id] = Binary(value)
                offset += 2 + len(value)
            else:
                raise ValueError("Unknown type: {}".format(item_type))
        return obj


class DummyData(PatData):
    FIELDS = tuple()


class CollectionLog(PatData):
    FIELDS = (
        (0x01, "error_code"),
        (0x02, "unk_long_0x02"),
        (0x03, "timeout_value"),
    )


class ConnectionData(PatData):
    # Constants are based on the US version of the game
    FIELDS = (
        (0x01, "online_support_code"),
        (0x02, "pat_ticket"),
        (0x03, "constant_0x3"),
        (0x04, "constant_0x2"),
        (0x05, "converted_country_code"),
        (0x06, "unknown_long_0x06"),
        (0x07, "media_version"),
        (0x08, "constant_0x4000"),
        (0x09, "country_code"),
        (0x0a, "language_code"),
    )


class ChargeInfo(PatData):
    FIELDS = (
        (0x01, "ticket_validity1"),
        (0x02, "ticket_validity2"),
        (0x05, "unk_binary_0x05"),
        (0x07, "online_support_code"),
    )


class LoginInfo(PatData):
    FIELDS = (
        (0x01, "ticket_validity1"),
        (0x02, "ticket_validity2"),
        (0x06, "unk_binary_0x06"),
        (0x07, "online_support_code"),
        (0x08, "unk_string_0x08"),
        (0x09, "state"),
        (0x0a, "nas_token"),
    )


class UserObject(PatData):
    FIELDS = (
        (0x01, "slot_index"),
        (0x02, "save_id"),
        (0x03, "hunter_name"),
        (0x04, "unk_long_0x04"),
        (0x05, "unk_long_0x05"),
        (0x06, "unk_long_0x06"),
        (0x07, "unk_long_0x07"),
        (0x08, "unk_string_0x08"),
    )


class FmpData(PatData):
    FIELDS = (
        (0x01, "index"),
        (0x02, "server_address"),
        (0x03, "server_port"),
        (0x07, "unk_longlong_0x07"),
        (0x08, "player_count"),
        (0x09, "player_capacity"),
        (0x0a, "server_name"),
        (0x0b, "unk_string_0x0b"),
        (0x0c, "unk_long_0x0c"),
    )


class UserSearchInfo(PatData):
    FIELDS = (
        (0x01, "unk_string_0x01"),
        (0x02, "unk_string_0x02"),
        (0x03, "unk_binary_0x03"),
        (0x04, "unk_binary_0x04"),
        (0x07, "unk_byte_0x07"),
        (0x08, "unk_string_0x08"),
        (0x0b, "unk_byte_0x0b"),
        (0x0c, "unk_string_0x0c"),
        (0x0d, "unk_long_0x0d"),
        (0x0e, "unk_long_0x0e"),
        (0x0f, "unk_long_0x0f"),
        (0x10, "unk_long_0x10"),
    )


class LayerData(PatData):
    FIELDS = (
        (0x01, "unk_long_0x01"),
        (0x02, "unk_custom_0x02"),
        (0x03, "unk_string_0x03"),
        (0x05, "unk_worddec_0x05"),
        (0x06, "unk_long_0x06"),
        (0x07, "unk_long_0x07"),
        (0x08, "unk_long_0x08"),
        (0x09, "unk_long_0x09"),
        (0x0a, "unk_long_0x0a"),
        (0x0b, "unk_long_0x0b"),
        (0x0c, "unk_long_0x0c"),
        (0x0d, "unk_word_0x0d"),
        (0x10, "unk_byte_0x10"),
        (0x11, "unk_long_0x11"),
        (0x12, "unk_byte_0x12"),
        (0x15, "unk_bytedec_0x15"),
        (0x16, "unk_string_0x16"),
        (0x17, "unk_binary_0x17"),
    )


class FriendData(PatData):
    FIELDS = (
        (0x01, "index"),
        (0x02, "capcom_id"),
        (0x03, "hunter_name"),
    )


class BlackListUserData(FriendData):
    pass


class UserStatusSet(PatData):
    FIELDS = (
        (0x01, "unk_byte_0x01"),
        (0x02, "unk_byte_0x02"),
        (0x03, "unk_byte_0x03"),
        (0x04, "unk_byte_0x04"),
        (0x05, "unk_byte_0x05"),
        (0x08, "unk_byte_0x08"),
        (0x09, "unk_byte_0x09"),
    )


def getDummyLayerData():
    layer = LayerData()
    layer.unk_long_0x01 = Long(1)
    # layer.unk_custom_0x02 = Custom(b"")
    layer.unk_string_0x03 = String("LayerStart")
    layer.unk_worddec_0x05 = Word(2)
    layer.unk_long_0x06 = Long(1)
    layer.unk_long_0x07 = Long(1)
    layer.unk_long_0x08 = Long(1)
    layer.unk_long_0x09 = Long(1)
    layer.unk_long_0x0a = Long(1)
    layer.unk_long_0x0b = Long(1)
    layer.unk_long_0x0c = Long(1)
    layer.unk_word_0x0d = Word(3)
    layer.unk_byte_0x10 = Byte(1)
    layer.unk_long_0x11 = Long(1)
    layer.unk_byte_0x12 = Byte(1)
    layer.unk_bytedec_0x15 = Byte(2)
    layer.unk_string_0x16 = String("UnkStart")
    # layer.unk_binary_0x17 = Binary(b"binStart")
    return layer
