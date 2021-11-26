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
from other.utils import to_bytearray, get_config, get_ip


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
    s = to_bytearray(s)
    return struct.pack(">B", len(s)) + s


def unpack_lp_string(data, offset=0):
    """Unpack lp_string."""
    size, = struct.unpack_from(">B", data, offset)
    return data[offset + 1:offset + 1 + size]


def lp2_string(s):
    """2-bytes length-prefixed string."""
    s = to_bytearray(s)
    return struct.pack(">H", len(s)) + s


def unpack_lp2_string(data, offset=0):
    """Unpack lp2_string."""
    size, = struct.unpack_from(">H", data, offset)
    return data[offset + 2:offset + 2 + size]


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


def pack_extra_info(info):
    """Pack extra info (list of field_id and int value).

    Extra info are retrieved after the following function calls:
     - getLayerData
     - getLayerUserInfo
     - getCircleInfo
     - getUserSearchInfo

    It follows a simple format:
     - field_id, a byte used as an identifier
     - has_value, a byte telling if it has a value
     - value: an integer with the field's value (only set if has_value is true)

    TODO: Rename "extra_info" to something meaningful.
    """
    data = struct.pack(">B", len(info))
    for field_id, value in info:
        has_value = value is not None
        data += struct.pack(">BB", field_id, int(has_value))
        if has_value:
            data += struct.pack(">I", value)
    return data


def unpack_extra_info(data, offset=0):
    """Unpack extra info (list of field_id and int value).

    Extra info are stored after the following function calls:
     - putLayerSet
     - putCircleInfo
    and is also used in PatInterface::sendReqUserSearchSet.

    TODO: Rename "extra_info" to something meaningful.
    It seems related to the city info. If correct:
     - field_id 0x01: ???
     - field_id 0x02: City's HR limit (if not applicable, 0xffffffff is set)
     - field_id 0x03: City's goal (if not applicable, 0xffffffff is set)
     - field_id 0x04: City's seeking
    """
    info = []
    count, = struct.unpack_from(">B", data, offset)
    offset += 1
    for _ in range(count):
        field_id, has_value = struct.unpack_from(">BB", data, offset)
        offset += 2
        if has_value:
            value, = struct.unpack_from(">I", data, offset)
            offset += 4
        else:
            value = None
        info.append((field_id, value))
    return info


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

    def __repr__(self):
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
    return struct.pack(">B", ItemType.String) + lp2_string(s)


def unpack_string(data, offset=0):
    """Unpack PAT item string."""
    item_type, length = struct.unpack_from(">BH", data, offset)
    if item_type != ItemType.String:
        raise AssertionError("Invalid type for string item: {}".format(
            item_type
        ))
    return data[offset + 3:offset + 3 + length]


class String(Item):
    """PAT item string class."""

    def __new__(cls, s):
        return Item.__new__(cls, pack_string(s))

    def __repr__(self):
        return "String({!r})".format(unpack_string(self))


def pack_binary(s):
    """Pack PAT item binary."""
    s = to_bytearray(s)
    return struct.pack(">BH", ItemType.Binary, len(s)) + s


def unpack_binary(data, offset=0):
    """Unpack PAT item binary."""
    item_type, length = struct.unpack_from(">BH", data, offset)
    if item_type != ItemType.Binary:
        raise AssertionError("Invalid type for binary item: {}".format(
            item_type
        ))
    return data[offset + 3:offset + 3 + length]


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


class FallthroughBug(Custom):
    """Wordaround a fallthrough bug.

    After reading LayerData's field_0x17 it falls through a getItemAny call.
    It clobbers the next field by reading the field_id. Then, the game tries
    to read the next field which was clobbered.

    The workaround uses a dummy field_0xff which will be clobbered on purpose.
    """
    def __new__(cls):
        return Custom.__new__(cls, b"\xff", b"\xff")


def unpack_bytes(data, offset=0):
    """Unpack bytes list."""
    count, = struct.unpack_from(">B", data, offset)
    return struct.unpack_from(">" + count * "B", data, offset + 1)


class PatData(OrderedDict):
    """Pat structure holding items."""
    FIELDS = (
        (1, "field_0x01"),
        (2, "field_0x02"),
        (3, "field_0x03"),
        (4, "field_0x04")
    )

    def __len__(self):
        return len(self.pack())

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

    def pack_fields(self, fields):
        """Pack PAT items specified fields."""
        items = [
            (index, value)
            for index, value in self.items()
            if value is not None and index in fields
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

    def assert_fields(self, fields):
        items = set(self.keys())
        fields = set(fields)
        message = "Fields mismatch: {}\n -> Expected: {}".format(items, fields)
        assert items == fields, message


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
        (0x02, "capcom_id"),
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
        (0x07, "server_type"),
        (0x08, "player_count"),
        (0x09, "player_capacity"),
        (0x0a, "server_name"),
        (0x0b, "unk_string_0x0b"),
        (0x0c, "unk_long_0x0c"),
    )


class UserSearchInfo(PatData):
    FIELDS = (
        (0x01, "capcom_id"),
        (0x02, "name"),
        (0x03, "unk_binary_0x03"),  # Hunter stat/HR related
        (0x04, "unk_binary_0x04"),  # Warp related
        (0x07, "unk_byte_0x07"),
        (0x08, "server_name"),
        (0x0b, "unk_byte_0x0b"),
        (0x0c, "unk_string_0x0c"),
        (0x0d, "city_size"),
        (0x0e, "city_capacity"),
        (0x0f, "info_mine_0x0f"),
        (0x10, "info_mine_0x10"),
    )


class LayerData(PatData):
    FIELDS = (
        (0x01, "unk_long_0x01"),
        (0x02, "unk_custom_0x02"),
        (0x03, "name"),
        (0x05, "index"),
        (0x06, "size"),
        (0x07, "unk_long_0x07"),
        (0x08, "unk_long_0x08"),
        (0x09, "capacity"),
        (0x0a, "unk_long_0x0a"),
        (0x0b, "unk_long_0x0b"),
        (0x0c, "unk_long_0x0c"),
        (0x0d, "unk_word_0x0d"),
        (0x10, "state"),  # 0 = Joinable / 1 = Empty / 2 = Full
        (0x11, "unk_long_0x11"),
        (0x12, "unk_byte_0x12"),
        (0x15, "unk_bytedec_0x15"),
        (0x16, "unk_string_0x16"),
        (0x17, "unk_binary_0x17"),
        (0xff, "fallthrough_bug")  # Fill this if field 0x17 is set !!!
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
        (0x09, "unk_byte_0x09"),  # Byte(4) = Deny Friend Requests
    )


class LayerSet(PatData):
    FIELDS = (
        (0x01, "unk_long_0x01"),
        (0x02, "unk_binary_0x02"),
        (0x03, "unk_string_0x03"),
        (0x05, "unk_binary_0x05"),
        (0x09, "unk_long_0x09"),
        (0x0a, "unk_long_0x0a"),
        (0x0c, "unk_long_0x0c"),
        (0x17, "unk_binary_0x17"),
    )


class MediationListItem(PatData):
    FIELDS = (
        (0x01, "name"),
        (0x02, "unk_byte_0x02"),
        (0x03, "unk_byte_0x03"),
    )


class CircleInfo(PatData):
    FIELDS = (
        (0x01, "index"),
        (0x02, "unk_string_0x02"),
        (0x03, "has_password"),
        (0x04, "password"),
        (0x05, "unk_binary_0x05"),  # party members?
        (0x06, "remarks"),
        (0x07, "unk_long_0x07"),
        (0x08, "unk_long_0x08"),
        (0x09, "team_size"),
        (0x0a, "unk_long_0x0a"),
        (0x0b, "unk_long_0x0b"),
        (0x0c, "unk_long_0x0c"),
        (0x0d, "unk_string_0x0d"),
        (0x0e, "unk_byte_0x0e"),
        (0x0f, "unk_byte_0x0f"),
        (0x0f, "unk_byte_0x10"),
    )


class MatchOptionSet(PatData):
    FIELDS = (
        (0x01, "unk_binary_0x01"),
        (0x02, "unk_word_0x02"),
        (0x03, "unk_byte_0x03"),
        (0x04, "unk_bytedec_0x04"),
        (0x05, "unk_string_0x05"),
        (0x06, "unk_string_0x06"),
    )


class MessageInfo(PatData):
    FIELDS = (
        (0x01, "text_color"),  # RGBA
        (0x02, "unk_long_0x02"),  # Probably time related?
        (0x03, "sender_id"),
        (0x04, "sender_name"),
    )


class LayerUserInfo(PatData):
    FIELDS = (
        (0x01, "capcom_id"),
        (0x02, "hunter_name"),
        (0x03, "layer_host"),
        (0x06, "unk_long_0x06"),
        (0x07, "stats"),
    )


class LayerBinaryInfo(PatData):
    FIELDS = (
        (0x01, "unk_long_0x01"),  # time related
        (0x02, "capcom_id"),
        (0x03, "hunter_name")
    )


def get_fmp_servers(session, first_index, count):
    assert first_index > 0, "Invalid list index"

    config = get_config("FMP")
    fmp_addr = get_ip(config["IP"])
    fmp_port = config["Port"]

    data = b""
    start = first_index - 1
    end = start + count
    servers = session.get_servers()[start:end]
    for i, server in enumerate(servers, first_index):
        fmp_data = FmpData()
        fmp_data.index = Long(i)  # The server might be full, if zero
        server.addr = server.addr or fmp_addr
        server.port = server.port or fmp_port
        fmp_data.server_address = String(server.addr)
        fmp_data.server_port = Word(server.port)
        # Might produce invalid reads if too high
        # fmp_data.server_type = LongLong(i+0x10000000)
        # fmp_data.server_type = LongLong(i + (1<<32)) # OK
        fmp_data.server_type = LongLong(server.server_type)
        fmp_data.player_count = Long(server.get_population())
        fmp_data.player_capacity = Long(server.get_capacity())
        fmp_data.server_name = String(server.name)
        fmp_data.unk_string_0x0b = String("X")
        fmp_data.unk_long_0x0c = Long(0x12345678)
        data += fmp_data.pack()
    return data


def get_layer_children(session, first_index, count, sibling=False):
    assert first_index > 0, "Invalid list index"

    data = b""
    start = first_index - 1
    end = start + count
    if not sibling:
        children = session.get_layer_children()[start:end]
    else:
        children = session.get_layer_sibling()[start:end]
    for i, child in enumerate(children, first_index):
        layer = LayerData()
        layer.index = Word(i)
        layer.name = String(child.name)
        layer.size = Long(child.get_population())
        layer.capacity = Long(child.get_capacity())
        layer.state = Byte(child.get_state())
        # layer.unk_binary_0x17 = Binary("test")
        # layer.fallthrough_bug = FallthroughBug()
        layer.unk_byte_0x12 = Byte(1)
        data += layer.pack()
        # A strange struct is also used, try to skip it
        data += struct.pack(">B", 0)
    return data


def get_layer_sibling(session, first_index, count):
    return get_layer_children(session, first_index, count, True)


def getDummyLayerData():
    layer = LayerData()
    layer.index = Word(1)  # Index
    # layer.unk_custom_0x02 = Custom(b"")
    layer.name = String("LayerStart")
    # layer.unk_worddec_0x05 = Word(2)  # City no longer exists message

    # Player in the city, displayed at the gate
    layer.size = Long(0)

    # layer.unk_long_0x07 = Long(1)
    # layer.unk_long_0x08 = Long(1)

    # Maximum number of players in the city, displayed at the gate
    layer.capacity = Long(4)
    # layer.unk_long_0x0a = Long(1)

    # In city population, displayed at the gate
    # layer.unk_long_0x0b = Long(0)

    # layer.unk_long_0x0c = Long(1)
    # layer.unk_word_0x0d = Word(1)
    layer.state = Byte(1)
    # layer.unk_long_0x11 = Long(1)
    # layer.unk_long_0x11 = Long(1)

    # Might be needed to be >=1 to keep NetworkConnectionStable alive
    layer.unk_byte_0x12 = Byte(1)
    # layer.unk_bytedec_0x15 = Byte(1)
    # layer.unk_string_0x16 = String("UnkStart")
    # layer.unk_binary_0x17 = Binary(b"binStart")
    return layer


def getHunterStats(hr=921, profile=b"Navaldeus",
                   title=117, status=1, hr_limit=2, goal=35, seeking=23,
                   server_type=3):
    """
    Offsets:
     - 0x00: Hunter Rank
     - 0x10~0x7c: Equipment
     - 0x9c: Profile description
     - 0xf2: Profile titles
     - 0xf3: Profile status
     - 0xf5: City's HR limit
     - 0xf6: City's goal
     - 0xf7: City's seeking
     - 0xf8: Server type
    """
    from other import fuzz

    profile = to_bytearray(profile)
    if profile[-1] != b"\0":
        profile += b"\0"

    data = fuzz.repeat(fuzz.MSF_PATTERN, 0x100)

    def slot(type_id, equipment_id, slots=0):
        """Equipment slot / TODO: Handle gems"""
        return struct.pack(">BBHII", type_id, slots, equipment_id, 0, 0)

    data[:2] = struct.pack(">H", hr)

    # Weapon / Gun slots (Lance: Nega-Babylon)
    data[0x10:0x1c] = slot(10, 11)
    data[0x1c:0x28] = b"\xff" * 0xc
    data[0x28:0x34] = b"\xff" * 0xc

    # Armors (Helios+ set)
    data[0x34:0x40] = slot(5, 111)
    data[0x40:0x4c] = slot(1, 116)
    data[0x4c:0x58] = slot(3, 115)
    data[0x58:0x64] = slot(2, 109)
    data[0x64:0x70] = slot(4, 113)
    data[0x70:0x7c] = slot(6, 7, slots=3)

    data[0x9c:0x9c + len(profile)] = profile
    data[0xf2] = title
    data[0xf3] = status
    data[0xf5] = hr_limit
    data[0xf6] = goal
    data[0xf7] = seeking
    data[0xf8] = server_type

    return Binary(data)
