#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter constants."""

import struct
from other.utils import pad
from mh.time_utils import current_server_time, TICKS_PER_CYCLE, \
    get_jhen_event_times, is_jhen_active, current_event_time_slot
from mh.quest_utils import make_binary_event_quest
from res.trading_post import CURRENT_TRADES

def make_binary_type_time_events(binary_loader=None):
    return struct.pack(">III", *get_jhen_event_times())


def make_event_slot(event):
    return (make_binary_event_quest(event), event)


def get_event_slot(slot_num, temporal_slot):
    return lambda quest_loader, slot_num=slot_num, temporal_slot=temporal_slot: \
        quest_loader[temporal_slot][slot_num] \
        if slot_num < len(quest_loader[temporal_slot]) else b'\0' * 0x4B4


def make_binary_server_type_list(is_jap=False):
    data = bytearray()
    PROPERTIES = [
        (b"Open", b"Hunters of all Ranks\ncan gather here.", 0, 999),
        (b"Rookie", b"Only hunters HR 30\nor lower may enter.", 0, 30),
        (b"Expert", b"Only hunters HR 31\nor higher may enter.", 31, 999),
        (b"Recruiting",
         b"Hunters in search of\nhunting companions\ncan gather here.", 0,
         999),
    ]

    # Handle server type properties
    for name, desc, hr_min, hr_max in PROPERTIES:
        data += pad(name, 16 if is_jap else 24)
        if is_jap:
            desc = bytearray(desc)
            LINE_LENGTH = 24
            while b'\n' in desc:
                i = desc.index(b'\n')
                padding = (LINE_LENGTH - i % LINE_LENGTH) % LINE_LENGTH
                desc[i:i+1] = b' ' * padding
        data += pad(desc, 112 if is_jap else 168)

    data += struct.pack(">I", 0)  # unk
    data += struct.pack(
        ">I", current_server_time()
    )  # Current time at server bootup
    data += struct.pack(
        ">I", TICKS_PER_CYCLE
    )  # Max tick per cycle, if 0 game defaults to 3000

    # Handle city seekings (x32)
    SEEKINGS = [
        # References:
        #  - https://youtu.be/lPFQW3B1Kt0?t=31
        #  - https://youtu.be/Ie_9lRIZF20?t=411
        b"Everyone welcome!", b"Casual play",
        # TODO: "Beginners welcome!" doesn't appear in Expert type servers
        b"Huntin' and chattin'", b"Beginners welcome!",
        # TODO: "Skilled players only" doesn't appear in Rookie type servers?
        b"Skilled players only", b"Let's Quest together",
        b"Event Quest ho!", b"Arena battles!",
        b"Earning money", b"HR grinding",
        b"Gathering materials", b"Rare material search",
        b"Just a Quest or two", b"In for the long haul",
        # TODO: The following seekings don't appear in Recruiting type servers
        b"Playing with friends", b"Solo play",
        # Extra seekings not from the original server
        b"Stream Lobby", b"Turns",
        b"Seeking18", b"Seeking19",
        b"Seeking20", b"Seeking21",
        b"Seeking22", b"Seeking23",
        b"Seeking24", b"Seeking25",
        b"Seeking26", b"Seeking27",
        b"Seeking28", b"Seeking29",
        b"Seeking30", b"Seeking31",
    ]
    for i, seeking in enumerate(SEEKINGS):
        data += pad(seeking, 32 if is_jap else 48)
        data += b"\0\1\xff\0"  # TODO: Figure out the 0xff flag values

    # Handle city HR limits (x8)
    HR_LIMITS = [
        # (Name, HR min, HR max)
        (b"None", 0, 999),
        (b"Low", 0, 30),
        (b"High", 31, 999),
        (b"Limit3", 0, 999),
        (b"Limit4", 0, 999),
        (b"Limit5", 0, 999),
        (b"Limit6", 0, 999),
        (b"Limit7", 0, 999),
    ]
    for name, hr_min, hr_max in HR_LIMITS:
        data += pad(name, 20 if is_jap else 30)
        data += b"\1"  # Enable bit
        data += b"\0"  # Unused / Defaults to HR limit restriction
        data += struct.pack(">H", hr_min)
        data += struct.pack(">H", hr_max)

    # Handle city goals (x64)
    GOALS = [
        b"None", b"HR1~", b"HR9~", b"HR18~",
        b"HR31~", b"HR40~", b"HR51~",
        b"1* Urgent Quest", b"2* Urgent Quest", b"3* Urgent Quest",
        b"4* Urgent Quest", b"5* Urgent Quest",
        b"Great Jaggi", b"Qurupecco", b"Royal Ludroth", b"Barroth",
        b"Gobul", b"Rathian", b"Great Baggi", b"Gigginox",
        b"Lagiacrus", b"Barioth", b"Rathalos", b"Diablos",
        b"Uragaan", b"Agnaktor", b"Jhen Mohran", b"Deviljho",
        b"Alatreon", b"Mining Ore", b"Catching Bugs", b"Fishing",
        b"Small Monsters", b"Gathering", b"Transporting", b"The Arena",
        b"Goal36", b"Goal37", b"Goal38", b"Goal39",
        b"Goal40", b"Goal41", b"Goal42", b"Goal43",
        b"Goal44", b"Goal45", b"Goal46", b"Goal47",
        b"Goal48", b"Goal49", b"Goal50", b"Goal51",
        b"Goal52", b"Goal53", b"Goal54", b"Goal55",
        b"Goal56", b"Goal57", b"Goal58", b"Goal59",
        b"Goal60", b"Goal61", b"Goal62", b"Goal63",
    ]
    for name in GOALS:
        data += pad(name, 20 if is_jap else 30)
        # There are 3 restriction modes:
        #  - 0x00: None
        #  - 0x01: HR limit
        #  - 0x02: An unknown one (TODO: Figure it out)
        data += b"\1"  # Enable bit
        data += b"\0"  # Restriction bit
        data += struct.pack(">H", 0)
        data += struct.pack(">H", 0)

    # Handle server type HR limits
    for i, (name, desc, hr_min, hr_max) in enumerate(PROPERTIES):
        data += struct.pack(">H", hr_min)
        data += struct.pack(">H", hr_max)

    # Timeout values (x8)
    timeout_in_sec = 30
    for _ in range(8):
        data += struct.pack(">H", 30 * timeout_in_sec)

    # TODO: Figure out the missing data at the end

    return data


def make_binary_npc_greeters(binary_loader, is_jap=False, temporal_slot=None):
    """Binary with NPC City Greeter.

    Data offset:
     - 0x000: Tool Shop
     - 0x180: material shop
     - 0x300: Trading Post
     - 0x480: Quest Receptionist
     - 0x600: Arena Clerk
     - 0x780: Guildmaster

     Japanese offset:
     - 0x000: Tool Shop
     - 0x100: material shop
     - 0x200: Trading Post
     - 0x300: Quest Receptionist
     - 0x400: Arena Clerk
     - 0x500: Guildmaster
    """
    US_OFFSET = 0x180
    JP_OFFSET = 0x100
    offset = JP_OFFSET if is_jap else US_OFFSET
    if temporal_slot is None:
        temporal_slot = current_event_time_slot()

    if is_jhen_active():
        tool_shop = b"Half-off sale!"
        material_shop = b"Half-off sale!"
        event_quests = b"The Festival of Fear\n"
    else:
        tool_shop = b"Prices are normal."
        material_shop = b"Prices are normal."
        event_quests = b""

    quest_list, arena_list = binary_loader.get_separated_quest_dicts(temporal_slot)

    event_quests += b"\n".join([
        quest['quest_info']['name'].encode("ascii")
        for quest in quest_list
    ])

    arena_quests = b"\n".join([
        quest['quest_info']['name'].encode("ascii")
        for quest in arena_list
    ])

    guildmaster_str = (
        b'To all hunters:\n'
        b'Loc Lac is in "beta,"\n'
        b'whatever that means. Also,\n'
        b'the Arena is back in\n'
        b'operation! And now, a:\n'
        b'haiku: "Patient warriors /\n'
        b'returning home at long last /\n'
        b'now join hands to hunt!"'
    )

    data = b""
    data += pad(tool_shop, offset)
    data += pad(material_shop, offset)
    data += pad(b"The Trading Post is open!", offset)
    data += pad(event_quests, offset)
    data += pad(arena_quests, offset)
    data += pad(guildmaster_str, offset)
    return data


def make_binary_trading_post():
    return CURRENT_TRADES


LAYER_CHAT_COLORS = (0xbb3385ff, 0xffffffff, 0xffffffff)

TERMS_VERSION = 1
TERMS = {
    1: b"""MH3 Server Project - Terms.""",
    2: (b"-DEBUG- -DEBUG- -DEBUG- -DEBUG-\n" * 0x200)+b"- ZHIEND"
}
SUBTERMS = {
    1: b"""MH3 Server Project - SubTerms.""",
    2: b"-DEBUG- Subterms"
}
ANNOUNCE = b"<BR><BODY>".join([
    b"<BR><CENTER><BODY><SIZE=6>Monster Hunter 3 (Tri) Server Project",
    b"<BR><LEFT><SIZE=4>Welcome to the MH3SP Beta Test! We ask that you",
    b"keep few things in mind while connected in order to",
    b"make the experience as fun as possible for everyone.",
    b"No abusing other players, no exploiting bugs, and",
    b"please report bugs that you find to the server",
    b"staff/dev team. We thank you for your patience as",
    b"we prepared this server to be fit for public use,",
    b"and ask your continued patience in the weeks to",
    b"come as you may encounter some bugs and errors",
    b"while playing. Please see the Public Test Server",
    b"Roadmap for a list of features we are working on.",
    b"<BR><CENTER><C=2>Welcome to Loc Lac!<END>"
])
CHARGE = b"""<BODY><CENTER>MH3 Server Project - No charge.<END>"""
# VULGARITY_INFO = b"""MH3 Server Project - Vulgarity info (low)."""
VULGARITY_INFO = b""
FMP_VERSION = 1

TIME_STATE = 0
IS_JAP = False


def get_binary_loader_assisted_version(binary_loader):
    return current_event_time_slot() + 1 + binary_loader.version


def get_binary_quest_content_from_quest_slot(quest_slot):
    return lambda temporal_slot, quest_slot=quest_slot: get_event_slot(quest_slot, temporal_slot)


# Dummy PAT_BINARY
PAT_BINARIES = {
    0x01: {
        "version": 1,
        "content": make_binary_server_type_list(is_jap=IS_JAP)
    },
    0x02: {
        "version": 1,
        "content": make_binary_type_time_events
    },
    0x03: {
        "version": lambda binary_loader: current_event_time_slot() + 1,
        "content": lambda temporal_slot: lambda binary_loader: make_binary_npc_greeters(binary_loader, is_jap=IS_JAP, temporal_slot=temporal_slot)
    },
    0x04: {
        "version": 1,
        "content": make_binary_trading_post()
    },
    0x05: {  # English
        "version": 1,
        "content": b"5" * 0x10  # b"titi\ttoto\ttutu\nbibi\tbobo\bubu\nouba\t"
        # "version": 1,
        # "content": b"TEST_BINARY"
    },
    0x06: {  # English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(0)
    },
    0x07: {  # English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(1)
    },
    0x08: {  # English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(2)
    },
    0x09: {  # English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(3)
    },
    0x0a: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(4)
    },
    0x0b: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(5)
    },
    0x0c: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(6)
    },
    0x0d: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(7)
    },
    0x0e: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(8)
    },
    0x0f: {  # Japanese(?)English
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(9)
    },
    0x10: {  # French
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x11: {  # French
        "version": 1,
        "content": make_binary_type_time_events
    },
    0x12: {  # French
        "version": lambda binary_loader: current_event_time_slot() + 1,
        "content": lambda temporal_slot: lambda binary_loader: make_binary_npc_greeters(binary_loader, temporal_slot=temporal_slot)
    },
    0x13: {  # French
        "version": 1,
        "content": make_binary_trading_post()
    },
    0x14: {  # French
        "version": 1,
        "content": b"dummy_14\0"
    },
    0x15: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(0)
    },
    0x16: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(1)
    },
    0x17: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(2)
    },
    0x18: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(3)
    },
    0x19: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(4)
    },
    0x1a: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(5)
    },
    0x1b: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(6)
    },
    0x1c: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(7)
    },
    0x1d: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(8)
    },
    0x1e: {  # French
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(9)
    },
    0x1f: {  # German
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x20: {  # German
        "version": 1,
        "content": make_binary_type_time_events
    },
    0x21: {  # German
        "version": lambda binary_loader: current_event_time_slot() + 1,
        "content": lambda temporal_slot: lambda binary_loader: make_binary_npc_greeters(binary_loader, temporal_slot=temporal_slot)
    },
    0x22: {  # German
        "version": 1,
        "content": make_binary_trading_post()
    },
    0x23: {  # German
        "version": 1,
        "content": b"dummy_23\0"
    },
    0x24: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(0)
    },
    0x25: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(1)
    },
    0x26: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(2)
    },
    0x27: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(3)
    },
    0x28: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(4)
    },
    0x29: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(5)
    },
    0x2a: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(6)
    },
    0x2b: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(7)
    },
    0x2c: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(8)
    },
    0x2d: {  # German
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(9)
    },
    0x2e: {  # Italian
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x2f: {  # Italian
        "version": 1,
        "content": make_binary_type_time_events
    },
    0x30: {  # Italian
        "version": lambda binary_loader: current_event_time_slot() + 1,
        "content": lambda temporal_slot: lambda binary_loader: make_binary_npc_greeters(binary_loader, temporal_slot=temporal_slot)
    },
    0x31: {  # Italian
        "version": 1,
        "content": make_binary_trading_post()
    },
    0x32: {  # Italian
        "version": 1,
        "content": b"dummy_32\0"
    },
    0x33: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(0)
    },
    0x34: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(1)
    },
    0x35: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(2)
    },
    0x36: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(3)
    },
    0x37: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(4)
    },
    0x38: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(5)
    },
    0x39: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(6)
    },
    0x3a: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(7)
    },
    0x3b: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(8)
    },
    0x3c: {  # Italian
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(9)
    },
    0x3d: {  # Spanish
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x3e: {  # Spanish
        "version": 1,
        "content": make_binary_type_time_events
    },
    0x3f: {  # Spanish
        "version": lambda binary_loader: current_event_time_slot() + 1,
        "content": lambda temporal_slot: lambda binary_loader: make_binary_npc_greeters(binary_loader, temporal_slot=temporal_slot)
    },
    0x40: {  # Spanish
        "version": 1,
        "content": make_binary_trading_post()
    },
    0x41: {  # Spanish
        "version": 1,
        "content": b"dummy_41\0"
    },
    0x42: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(0)
    },
    0x43: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(1)
    },
    0x44: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(2)
    },
    0x45: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(3)
    },
    0x46: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(4)
    },
    0x47: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(5)
    },
    0x48: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(6)
    },
    0x49: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(7)
    },
    0x4a: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(8)
    },
    0x4b: {  # Spanish
        "version": get_binary_loader_assisted_version,
        "content": get_binary_quest_content_from_quest_slot(9)
    },
}


def get_pat_binary_from_version(binary_type, version):
    static_binaries = (0x01, 0x02, 0x04, 0x05, 0x10, 0x11,
        0x13, 0x14, 0x1f, 0x20, 0x22, 0x23, 0x2e, 0x2f,
        0x31, 0x32, 0x3d, 0x3e, 0x40, 0x41)
    if binary_type in static_binaries:
        return PAT_BINARIES[binary_type]["content"]
    return PAT_BINARIES[binary_type]["content"](version)


PAT_CATEGORIES = {
    0x60: "Opn",
    0x61: "Rfp",
    0x62: "Lmp",
    0x63: "Fmp",
    0x64: "Layer",
    0x65: "Circle",
    0x66: "User",
    0x69: "Agreement"
}

PAT_TYPES = {
    0x01: "Req",
    0x02: "Ans",
    0x10: "Ntc"
}

PAT_FLAGS = {
    0x00: "None",
    0x01: "Alert",
    0xff: "Ng"
}

PAT_NAMES = {
    # Category Opn
    0x60010100: 'ReqLineCheck',
    0x60010200: 'AnsLineCheck',
    0x60020100: 'ReqServerTime',
    0x60020200: 'AnsServerTime',
    0x60100100: 'ReqShut',
    0x60100200: 'AnsShut',
    0x60101000: 'NtcShut',
    0x60111000: 'NtcRecconect',
    0x60200100: 'ReqConnection',
    0x60200200: 'AnsConnection',
    0x60211000: 'NtcLogin',
    0x60300100: 'ReqTicket',
    0x60300200: 'AnsTicket',
    0x60310100: 'ReqTicket',
    0x60310200: 'AnsTicket',
    0x60400100: 'ReqWarning',
    0x60400200: 'AnsWarning',
    0x60501000: 'NtcCollectionLog',
    0x60700100: 'ReqCommonKey',
    0x60700200: 'AnsCommonKey',
    0x60801000: 'NtcCheatCheck',
    0x60810100: 'ReqMemoryCheck',
    0x60810200: 'AnsMemoryCheck',
    # Category Rfp
    0x61010100: 'ReqLoginInfo',
    0x61010200: 'AnsLoginInfo',
    0x61020100: 'ReqChargeInfo',
    0x61020200: 'AnsChargeInfo',
    0x61100100: 'ReqUserListHead',
    0x61100200: 'AnsUserListHead',
    0x61110100: 'ReqUserListData',
    0x61110200: 'AnsUserListData',
    0x61120100: 'ReqUserListFoot',
    0x61120200: 'AnsUserListFoot',
    0x61200100: 'ReqUserObject',
    0x61200200: 'AnsUserObject',
    0x61300100: 'ReqFmpListVersion',
    0x61300200: 'AnsFmpListVersion',
    0x61310100: 'ReqFmpListHead',
    0x61310200: 'AnsFmpListHead',
    0x61320100: 'ReqFmpListData',
    0x61320200: 'AnsFmpListData',
    0x61330100: 'ReqFmpListFoot',
    0x61330200: 'AnsFmpListFoot',
    0x61340100: 'ReqFmpInfo',
    0x61340200: 'AnsFmpInfo',
    0x61400100: 'ReqRfpConnect',
    0x61400200: 'AnsRfpConnect',
    # Category Lmp
    0x62010100: 'ReqLmpConnect',
    0x62010200: 'AnsLmpConnect',
    0x62100100: 'ReqTermsVersion',
    0x62100200: 'AnsTermsVersion',
    0x62110100: 'ReqTerms',
    0x62110200: 'AnsTerms',
    0x62130100: 'ReqSubTermsInfo',
    0x62130200: 'AnsSubTermsInfo',
    0x62140100: 'ReqSubTerms',
    0x62140200: 'AnsSubTerms',
    0x62200100: 'ReqMaintenance',
    0x62200200: 'AnsMaintenance',
    0x62300100: 'ReqAnnounce',
    0x62300200: 'AnsAnnounce',
    0x62310100: 'ReqNoCharge',
    0x62310200: 'AnsNoCharge',
    0x62410100: 'ReqMediaVersionInfo',
    0x62410200: 'AnsMediaVersionInfo',
    0x62500100: 'ReqVulgarityInfoHighJAP',
    0x62500200: 'AnsVulgarityInfoHighJAP',
    0x62510100: 'ReqVulgarityHighJAP',
    0x62510200: 'AnsVulgarityHighJAP',
    0x62520100: 'ReqVulgarityInfoLowJAP',
    0x62520200: 'AnsVulgarityInfoLowJAP',
    0x62530100: 'ReqVulgarityLowJAP',
    0x62530200: 'AnsVulgarityLowJAP',
    0x62540100: 'ReqVulgarityInfoHigh',
    0x62540200: 'AnsVulgarityInfoHigh',
    0x62550100: 'ReqVulgarityHigh',
    0x62550200: 'AnsVulgarityHigh',
    0x62560100: 'ReqVulgarityInfoLow',
    0x62560200: 'AnsVulgarityInfoLow',
    0x62570100: 'ReqVulgarityLow',
    0x62570200: 'AnsVulgarityLow',
    0x62600100: 'ReqAuthenticationToken',
    0x62600200: 'AnsAuthenticationToken',
    # Category Fmp
    0x63010100: 'ReqBinaryVersion',
    0x63010200: 'AnsBinaryVersion',
    0x63020100: 'ReqBinaryHead',
    0x63020200: 'AnsBinaryHead',
    0x63030100: 'ReqBinaryData',
    0x63030200: 'AnsBinaryData',
    0x63040100: 'ReqBinaryFoot',
    0x63040200: 'AnsBinaryFoot',
    0x63100100: 'ReqFmpListVersion',
    0x63100200: 'AnsFmpListVersion',
    0x63110100: 'ReqFmpListHead',
    0x63110200: 'AnsFmpListHead',
    0x63120100: 'ReqFmpListData',
    0x63120200: 'AnsFmpListData',
    0x63130100: 'ReqFmpListFoot',
    0x63130200: 'AnsFmpListFoot',
    0x63140100: 'ReqFmpInfo',
    0x63140200: 'AnsFmpInfo',
    # Category Layer
    0x64010100: 'ReqLayerStart',
    0x64010200: 'AnsLayerStart',
    0x64020100: 'ReqLayerEnd',
    0x64020200: 'AnsLayerEnd',
    0x64031000: 'NtcLayerUserNum',
    0x64100100: 'ReqLayerJump',
    0x64100200: 'AnsLayerJump',
    0x64110100: 'ReqLayerCreateHead',
    0x64110200: 'AnsLayerCreateHead',
    0x64120100: 'ReqLayerCreateSet',
    0x64120200: 'AnsLayerCreateSet',
    0x64130100: 'ReqLayerCreateFoot',
    0x64130200: 'AnsLayerCreateFoot',
    0x64140100: 'ReqLayerDown',
    0x64140200: 'AnsLayerDown',
    0x64141000: 'NtcLayerIn',
    0x64150100: 'ReqLayerUp',
    0x64150200: 'AnsLayerUp',
    0x64151000: 'NtcLayerOut',
    0x64160100: 'ReqLayerJumpReady',
    0x64160200: 'NtcLayerJumpReady',
    0x64170100: 'ReqLayerJumpGo',
    0x64170200: 'NtcLayerJumpGo',
    0x64200100: 'ReqLayerInfoSet',
    0x64200200: 'AnsLayerInfoSet',
    0x64201000: 'NtcLayerInfoSet',
    0x64210100: 'ReqLayerInfo',
    0x64210200: 'AnsLayerInfo',
    0x64220100: 'ReqLayerParentInfo',
    0x64220200: 'AnsLayerParentInfo',
    0x64230100: 'ReqLayerChildInfo',
    0x64230200: 'AnsLayerChildInfo',
    0x64240100: 'ReqLayerChildListHead',
    0x64240200: 'AnsLayerChildListHead',
    0x64250100: 'ReqLayerChildListData',
    0x64250200: 'AnsLayerChildListData',
    0x64260100: 'ReqLayerChildListFoot',
    0x64260200: 'AnsLayerChildListFoot',
    0x64270100: 'ReqLayerSiblingListHead',
    0x64270200: 'AnsLayerSiblingListHead',
    0x64280100: 'ReqLayerSiblingListData',
    0x64280200: 'AnsLayerSiblingListData',
    0x64290100: 'ReqLayerSiblingListFoot',
    0x64290200: 'AnsLayerSiblingListFoot',
    0x64410100: 'ReqLayerHost',
    0x64410200: 'AnsLayerHost',
    0x64411000: 'NtcLayerHost',
    0x64600100: 'ReqLayerUserInfoSet',
    0x64600200: 'AnsLayerUserInfoSet',
    0x64601000: 'NtcLayerUserInfoSet',
    0x64630100: 'ReqLayerUserList',
    0x64630200: 'AnsLayerUserList',
    0x64640100: 'ReqLayerUserListHead',
    0x64640200: 'AnsLayerUserListHead',
    0x64650100: 'ReqLayerUserListData',
    0x64650200: 'AnsLayerUserListData',
    0x64660100: 'ReqLayerUserListFoot',
    0x64660200: 'AnsLayerUserListFoot',
    0x64670100: 'ReqLayerUserSearchHead',
    0x64670200: 'AnsLayerUserSearchHead',
    0x64680100: 'ReqLayerUserSearchData',
    0x64680200: 'AnsLayerUserSearchData',
    0x64690100: 'ReqLayerUserSearchFoot',
    0x64690200: 'AnsLayerUserSearchFoot',
    0x64701000: 'NtcLayerBinary',
    0x64711000: 'NtcLayerUserPosition',
    0x64721000: 'NtcLayerChat',
    0x64730100: 'ReqLayerTell',
    0x64730200: 'AnsLayerTell',
    0x64731000: 'NtcLayerTell',
    0x64741000: 'Ntc0x6474',
    0x64751000: 'NtcLayerBinary2',  # (partner specified)
    0x64800100: 'ReqLayerMediationLock',
    0x64800200: 'AnsLayerMediationLock',
    0x64801000: 'NtcLayerMediationLock',
    0x64810100: 'ReqLayerMediationUnlock',
    0x64810200: 'AnsLayerMediationUnlock',
    0x64811000: 'NtcLayerMediationUnlock',
    0x64820100: 'ReqLayerMediationList',
    0x64820200: 'AnsLayerMediationList',
    0x64900100: 'ReqLayerDetailSearchHead',
    0x64900200: 'AnsLayerDetailSearchHead',
    0x64910100: 'ReqLayerDetailSearchData',
    0x64910200: 'AnsLayerDetailSearchData',
    0x64920100: 'ReqLayerDetailSearchFoot',
    0x64920200: 'AnsLayerDetailSearchFoot',
    # Category Circle
    0x65010100: 'ReqCircleCreate',
    0x65010200: 'AnsCircleCreate',
    0x65020100: 'ReqCircleInfo',
    0x65020200: 'AnsCircleInfo',
    0x65030100: 'ReqCircleJoin',
    0x65030200: 'AnsCircleJoin',
    0x65031000: 'NtcCircleJoin',
    0x65040100: 'ReqCircleLeave',
    0x65040200: 'AnsCircleLeave',
    0x65041000: 'NtcCircleLeave',
    0x65050100: 'ReqCircleBreak',
    0x65050200: 'AnsCircleBreak',
    0x65051000: 'NtcCircleBreak',
    0x65100100: 'ReqCircleMatchOptionSet',
    0x65100200: 'AnsCircleMatchOptionSet',
    0x65101000: 'NtcCircleMatchOptionSet',
    0x65110100: 'ReqCircleMatchOptionGet',
    0x65110200: 'AnsCircleMatchOptionGet',
    0x65120100: 'ReqCircleMatchStart',
    0x65120200: 'AnsCircleMatchStart',
    0x65121000: 'NtcCircleMatchStart',
    0x65130100: 'ReqCircleMatchEnd',
    0x65130200: 'AnsCircleMatchEnd',
    0x65200100: 'ReqCircleInfoSet',
    0x65200200: 'AnsCircleInfoSet',
    0x65201000: 'NtcCircleInfoSet',
    0x65270100: 'ReqCircleListLayer',
    0x65270200: 'AnsCircleListLayer',
    0x65280100: 'ReqCircleSearchHead',
    0x65280200: 'AnsCircleSearchHead',
    0x65290100: 'ReqCircleSearchData',
    0x65290200: 'AnsCircleSearchData',
    0x652a0100: 'ReqCircleSearchFoot',
    0x652a0200: 'AnsCircleSearchFoot',
    0x65350100: 'ReqCircleKick',
    0x65350200: 'AnsCircleKick',
    0x65351000: 'NtcCircleKick',
    0x65360100: 'ReqCircleDeleteKickList',
    0x65360200: 'AnsCircleDeleteKickList',
    0x65400100: 'ReqCircleHostHandover',
    0x65400200: 'AnsCircleHostHandover',
    0x65401000: 'NtcCircleHostHandover',
    0x65410100: 'ReqCircleHost',
    0x65410200: 'AnsCircleHost',
    0x65411000: 'NtcCircleHost',
    0x65600100: 'ReqCircleUserList',
    0x65600200: 'AnsCircleUserList',
    0x65701000: 'NtcCircleBinary',
    0x65711000: 'NtcCircleBinary2',
    0x65721000: 'NtcCircleChat',
    0x65730100: 'ReqCircleTell',
    0x65730200: 'AnsCircleTell',
    0x65731000: 'NtcCircleTell',
    0x65800100: 'ReqCircleInfoNoticeSet',
    0x65800200: 'AnsCircleInfoNoticeSet',
    0x65811000: 'NtcCircleListLayerCreate',
    0x65821000: 'NtcCircleListLayerChange',
    0x65831000: 'NtcCircleListLayerDelete',
    0x65900100: 'ReqMcsCreate',
    0x65900200: 'AnsMcsCreate',
    0x65901000: 'NtcMcsCreate',
    0x65911000: 'NtcMcsStart',
    # Category User
    0x66110100: 'ReqTell',
    0x66110200: 'AnsTell',
    0x66111000: 'NtcTell',
    0x66120100: 'ReqBinaryUser',
    0x66120200: 'AnsBinaryUser',
    0x66121000: 'NtcBinaryUser',
    0x66131000: 'NtcBinaryServer',
    0x66300100: 'ReqUserSearchSet',
    0x66300200: 'AnsUserSearchSet',
    0x66310100: 'ReqUserBinarySet',
    0x66310200: 'AnsUserBinarySet',
    0x66320100: 'ReqUserBinaryNotice',
    0x66320200: 'AnsUserBinaryNotice',
    0x66321000: 'NtcUserBinaryNotice',
    0x66330100: 'ReqUserSearchHead',
    0x66330200: 'AnsUserSearchHead',
    0x66340100: 'ReqUserSearchData',
    0x66340200: 'AnsUserSearchData',
    0x66350100: 'ReqUserSearchFoot',
    0x66350200: 'AnsUserSearchFoot',
    0x66360100: 'ReqUserSearchInfo',
    0x66360200: 'AnsUserSearchInfo',
    0x66370100: 'ReqUserSearchInfoMine',
    0x66370200: 'AnsUserSearchInfoMine',
    0x66400100: 'ReqUserStatusSet',
    0x66400200: 'AnsUserStatusSet',
    0x66410100: 'ReqUserStatus',
    0x66410200: 'AnsUserStatus',
    0x66500100: 'ReqFriendAdd',
    0x66500200: 'AnsFriendAdd',
    0x66501000: 'NtcFriendAdd',
    0x66510100: 'ReqFriendAccept',
    0x66510200: 'AnsFriendAccept',
    0x66511000: 'NtcFriendAccept',
    0x66530100: 'ReqFriendDelete',
    0x66530200: 'AnsFriendDelete',
    0x66540100: 'ReqFriendList',
    0x66540200: 'AnsFriendList',
    0x66600100: 'ReqBlackAdd',
    0x66600200: 'AnsBlackAdd',
    0x66610100: 'ReqBlackDelete',
    0x66610200: 'AnsBlackDelete',
    0x66620100: 'ReqBlackList',
    0x66620200: 'AnsBlackList',
    # Category Agreement
    0x69010100: 'ReqAgreementPageNum',
    0x69010200: 'AnsAgreementPageNum',
    0x69020100: 'ReqAgreementPageInfo',
    0x69020200: 'AnsAgreementPageInfo',
    0x69030100: 'ReqAgreementPage',
    0x69030200: 'AnsAgreementPage',
    0x69100100: 'ReqAgreement',
    0x69100200: 'AnsAgreement'
}


class PatID4:
    # Category Opn
    ReqLineCheck = 0x60010100
    AnsLineCheck = 0x60010200
    ReqServerTime = 0x60020100
    AnsServerTime = 0x60020200
    ReqShut = 0x60100100
    AnsShut = 0x60100200
    NtcShut = 0x60101000
    NtcRecconect = 0x60111000
    ReqConnection = 0x60200100
    AnsConnection = 0x60200200
    NtcLogin = 0x60211000
    ReqTicket = 0x60300100
    AnsTicket = 0x60300200
    ReqTicket2 = 0x60310100
    AnsTicket2 = 0x60310200
    ReqWarning = 0x60400100
    AnsWarning = 0x60400200
    NtcCollectionLog = 0x60501000
    ReqCommonKey = 0x60700100
    AnsCommonKey = 0x60700200
    NtcCheatCheck = 0x60801000
    ReqMemoryCheck = 0x60810100
    AnsMemoryCheck = 0x60810200
    # Category Rfp
    ReqLoginInfo = 0x61010100
    AnsLoginInfo = 0x61010200
    ReqChargeInfo = 0x61020100
    AnsChargeInfo = 0x61020200
    ReqUserListHead = 0x61100100
    AnsUserListHead = 0x61100200
    ReqUserListData = 0x61110100
    AnsUserListData = 0x61110200
    ReqUserListFoot = 0x61120100
    AnsUserListFoot = 0x61120200
    ReqUserObject = 0x61200100
    AnsUserObject = 0x61200200
    ReqFmpListVersion = 0x61300100
    AnsFmpListVersion = 0x61300200
    ReqFmpListHead = 0x61310100
    AnsFmpListHead = 0x61310200
    ReqFmpListData = 0x61320100
    AnsFmpListData = 0x61320200
    ReqFmpListFoot = 0x61330100
    AnsFmpListFoot = 0x61330200
    ReqFmpInfo = 0x61340100
    AnsFmpInfo = 0x61340200
    ReqRfpConnect = 0x61400100
    AnsRfpConnect = 0x61400200
    # Category Lmp
    ReqLmpConnect = 0x62010100
    AnsLmpConnect = 0x62010200
    ReqTermsVersion = 0x62100100
    AnsTermsVersion = 0x62100200
    ReqTerms = 0x62110100
    AnsTerms = 0x62110200
    ReqSubTermsInfo = 0x62130100
    AnsSubTermsInfo = 0x62130200
    ReqSubTerms = 0x62140100
    AnsSubTerms = 0x62140200
    ReqMaintenance = 0x62200100
    AnsMaintenance = 0x62200200
    ReqAnnounce = 0x62300100
    AnsAnnounce = 0x62300200
    ReqNoCharge = 0x62310100
    AnsNoCharge = 0x62310200
    ReqMediaVersionInfo = 0x62410100
    AnsMediaVersionInfo = 0x62410200
    ReqVulgarityInfoHighJAP = 0x62500100
    AnsVulgarityInfoHighJAP = 0x62500200
    ReqVulgarityHighJAP = 0x62510100
    AnsVulgarityHighJAP = 0x62510200
    ReqVulgarityInfoLowJAP = 0x62520100
    AnsVulgarityInfoLowJAP = 0x62520200
    ReqVulgarityLowJAP = 0x62530100
    AnsVulgarityLowJAP = 0x62530200
    ReqVulgarityInfoHigh = 0x62540100
    AnsVulgarityInfoHigh = 0x62540200
    ReqVulgarityHigh = 0x62550100
    AnsVulgarityHigh = 0x62550200
    ReqVulgarityInfoLow = 0x62560100
    AnsVulgarityInfoLow = 0x62560200
    ReqVulgarityLow = 0x62570100
    AnsVulgarityLow = 0x62570200
    ReqAuthenticationToken = 0x62600100
    AnsAuthenticationToken = 0x62600200
    # Category Fmp
    ReqBinaryVersion = 0x63010100
    AnsBinaryVersion = 0x63010200
    ReqBinaryHead = 0x63020100
    AnsBinaryHead = 0x63020200
    ReqBinaryData = 0x63030100
    AnsBinaryData = 0x63030200
    ReqBinaryFoot = 0x63040100
    AnsBinaryFoot = 0x63040200
    ReqFmpListVersion2 = 0x63100100
    AnsFmpListVersion2 = 0x63100200
    ReqFmpListHead2 = 0x63110100
    AnsFmpListHead2 = 0x63110200
    ReqFmpListData2 = 0x63120100
    AnsFmpListData2 = 0x63120200
    ReqFmpListFoot2 = 0x63130100
    AnsFmpListFoot2 = 0x63130200
    ReqFmpInfo2 = 0x63140100
    AnsFmpInfo2 = 0x63140200
    # Category Layer
    ReqLayerStart = 0x64010100
    AnsLayerStart = 0x64010200
    ReqLayerEnd = 0x64020100
    AnsLayerEnd = 0x64020200
    NtcLayerUserNum = 0x64031000
    ReqLayerJump = 0x64100100
    AnsLayerJump = 0x64100200
    ReqLayerCreateHead = 0x64110100
    AnsLayerCreateHead = 0x64110200
    ReqLayerCreateSet = 0x64120100
    AnsLayerCreateSet = 0x64120200
    ReqLayerCreateFoot = 0x64130100
    AnsLayerCreateFoot = 0x64130200
    ReqLayerDown = 0x64140100
    AnsLayerDown = 0x64140200
    NtcLayerIn = 0x64141000
    ReqLayerUp = 0x64150100
    AnsLayerUp = 0x64150200
    NtcLayerOut = 0x64151000
    ReqLayerJumpReady = 0x64160100
    NtcLayerJumpReady = 0x64160200
    ReqLayerJumpGo = 0x64170100
    NtcLayerJumpGo = 0x64170200
    ReqLayerInfoSet = 0x64200100
    AnsLayerInfoSet = 0x64200200
    NtcLayerInfoSet = 0x64201000
    ReqLayerInfo = 0x64210100
    AnsLayerInfo = 0x64210200
    ReqLayerParentInfo = 0x64220100
    AnsLayerParentInfo = 0x64220200
    ReqLayerChildInfo = 0x64230100
    AnsLayerChildInfo = 0x64230200
    ReqLayerChildListHead = 0x64240100
    AnsLayerChildListHead = 0x64240200
    ReqLayerChildListData = 0x64250100
    AnsLayerChildListData = 0x64250200
    ReqLayerChildListFoot = 0x64260100
    AnsLayerChildListFoot = 0x64260200
    ReqLayerSiblingListHead = 0x64270100
    AnsLayerSiblingListHead = 0x64270200
    ReqLayerSiblingListData = 0x64280100
    AnsLayerSiblingListData = 0x64280200
    ReqLayerSiblingListFoot = 0x64290100
    AnsLayerSiblingListFoot = 0x64290200
    ReqLayerHost = 0x64410100
    AnsLayerHost = 0x64410200
    NtcLayerHost = 0x64411000
    ReqLayerUserInfoSet = 0x64600100
    AnsLayerUserInfoSet = 0x64600200
    NtcLayerUserInfoSet = 0x64601000
    ReqLayerUserList = 0x64630100
    AnsLayerUserList = 0x64630200
    ReqLayerUserListHead = 0x64640100
    AnsLayerUserListHead = 0x64640200
    ReqLayerUserListData = 0x64650100
    AnsLayerUserListData = 0x64650200
    ReqLayerUserListFoot = 0x64660100
    AnsLayerUserListFoot = 0x64660200
    ReqLayerUserSearchHead = 0x64670100
    AnsLayerUserSearchHead = 0x64670200
    ReqLayerUserSearchData = 0x64680100
    AnsLayerUserSearchData = 0x64680200
    ReqLayerUserSearchFoot = 0x64690100
    AnsLayerUserSearchFoot = 0x64690200
    NtcLayerBinary = 0x64701000
    NtcLayerUserPosition = 0x64711000
    NtcLayerChat = 0x64721000
    ReqLayerTell = 0x64730100
    AnsLayerTell = 0x64730200
    NtcLayerTell = 0x64731000
    Ntc0x6474 = 0x64741000
    NtcLayerBinary2 = 0x64751000  # (partner specified)
    ReqLayerMediationLock = 0x64800100
    AnsLayerMediationLock = 0x64800200
    NtcLayerMediationLock = 0x64801000
    ReqLayerMediationUnlock = 0x64810100
    AnsLayerMediationUnlock = 0x64810200
    NtcLayerMediationUnlock = 0x64811000
    ReqLayerMediationList = 0x64820100
    AnsLayerMediationList = 0x64820200
    ReqLayerDetailSearchHead = 0x64900100
    AnsLayerDetailSearchHead = 0x64900200
    ReqLayerDetailSearchData = 0x64910100
    AnsLayerDetailSearchData = 0x64910200
    ReqLayerDetailSearchFoot = 0x64920100
    AnsLayerDetailSearchFoot = 0x64920200
    # Category Circle
    ReqCircleCreate = 0x65010100
    AnsCircleCreate = 0x65010200
    ReqCircleInfo = 0x65020100
    AnsCircleInfo = 0x65020200
    ReqCircleJoin = 0x65030100
    AnsCircleJoin = 0x65030200
    NtcCircleJoin = 0x65031000
    ReqCircleLeave = 0x65040100
    AnsCircleLeave = 0x65040200
    NtcCircleLeave = 0x65041000
    ReqCircleBreak = 0x65050100
    AnsCircleBreak = 0x65050200
    NtcCircleBreak = 0x65051000
    ReqCircleMatchOptionSet = 0x65100100
    AnsCircleMatchOptionSet = 0x65100200
    NtcCircleMatchOptionSet = 0x65101000
    ReqCircleMatchOptionGet = 0x65110100
    AnsCircleMatchOptionGet = 0x65110200
    ReqCircleMatchStart = 0x65120100
    AnsCircleMatchStart = 0x65120200
    NtcCircleMatchStart = 0x65121000
    ReqCircleMatchEnd = 0x65130100
    AnsCircleMatchEnd = 0x65130200
    ReqCircleInfoSet = 0x65200100
    AnsCircleInfoSet = 0x65200200
    NtcCircleInfoSet = 0x65201000
    ReqCircleListLayer = 0x65270100
    AnsCircleListLayer = 0x65270200
    ReqCircleSearchHead = 0x65280100
    AnsCircleSearchHead = 0x65280200
    ReqCircleSearchData = 0x65290100
    AnsCircleSearchData = 0x65290200
    ReqCircleSearchFoot = 0x652a0100
    AnsCircleSearchFoot = 0x652a0200
    ReqCircleKick = 0x65350100
    AnsCircleKick = 0x65350200
    NtcCircleKick = 0x65351000
    ReqCircleDeleteKickList = 0x65360100
    AnsCircleDeleteKickList = 0x65360200
    ReqCircleHostHandover = 0x65400100
    AnsCircleHostHandover = 0x65400200
    NtcCircleHostHandover = 0x65401000
    ReqCircleHost = 0x65410100
    AnsCircleHost = 0x65410200
    NtcCircleHost = 0x65411000
    ReqCircleUserList = 0x65600100
    AnsCircleUserList = 0x65600200
    NtcCircleBinary = 0x65701000
    NtcCircleBinary2 = 0x65711000
    NtcCircleChat = 0x65721000
    ReqCircleTell = 0x65730100
    AnsCircleTell = 0x65730200
    NtcCircleTell = 0x65731000
    ReqCircleInfoNoticeSet = 0x65800100
    AnsCircleInfoNoticeSet = 0x65800200
    NtcCircleListLayerCreate = 0x65811000
    NtcCircleListLayerChange = 0x65821000
    NtcCircleListLayerDelete = 0x65831000
    ReqMcsCreate = 0x65900100
    AnsMcsCreate = 0x65900200
    NtcMcsCreate = 0x65901000
    NtcMcsStart = 0x65911000
    # Category User
    ReqTell = 0x66110100
    AnsTell = 0x66110200
    NtcTell = 0x66111000
    ReqBinaryUser = 0x66120100
    AnsBinaryUser = 0x66120200
    NtcBinaryUser = 0x66121000
    NtcBinaryServer = 0x66131000
    ReqUserSearchSet = 0x66300100
    AnsUserSearchSet = 0x66300200
    ReqUserBinarySet = 0x66310100
    AnsUserBinarySet = 0x66310200
    ReqUserBinaryNotice = 0x66320100
    AnsUserBinaryNotice = 0x66320200
    NtcUserBinaryNotice = 0x66321000
    ReqUserSearchHead = 0x66330100
    AnsUserSearchHead = 0x66330200
    ReqUserSearchData = 0x66340100
    AnsUserSearchData = 0x66340200
    ReqUserSearchFoot = 0x66350100
    AnsUserSearchFoot = 0x66350200
    ReqUserSearchInfo = 0x66360100
    AnsUserSearchInfo = 0x66360200
    ReqUserSearchInfoMine = 0x66370100
    AnsUserSearchInfoMine = 0x66370200
    ReqUserStatusSet = 0x66400100
    AnsUserStatusSet = 0x66400200
    ReqUserStatus = 0x66410100
    AnsUserStatus = 0x66410200
    ReqFriendAdd = 0x66500100
    AnsFriendAdd = 0x66500200
    NtcFriendAdd = 0x66501000
    ReqFriendAccept = 0x66510100
    AnsFriendAccept = 0x66510200
    NtcFriendAccept = 0x66511000
    ReqFriendDelete = 0x66530100
    AnsFriendDelete = 0x66530200
    ReqFriendList = 0x66540100
    AnsFriendList = 0x66540200
    ReqBlackAdd = 0x66600100
    AnsBlackAdd = 0x66600200
    ReqBlackDelete = 0x66610100
    AnsBlackDelete = 0x66610200
    ReqBlackList = 0x66620100
    AnsBlackList = 0x66620200
    # Category Agreement
    ReqAgreementPageNum = 0x69010100
    AnsAgreementPageNum = 0x69010200
    ReqAgreementPageInfo = 0x69020100
    AnsAgreementPageInfo = 0x69020200
    ReqAgreementPage = 0x69030100
    AnsAgreementPage = 0x69030200
    ReqAgreement = 0x69100100
    AnsAgreement = 0x69100200


class PatServerType:
    LMP = 0
    FMP = 1
    OPN = 2
    RFP = 3
