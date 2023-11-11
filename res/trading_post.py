#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Trading post resources module.

This module can be used to generate trades for the online trading post.

TODO:
 - Find trades specific to the sandstorm.
"""

import struct

from collections import namedtuple, OrderedDict
from itertools import islice


Slot = namedtuple("Slot", ["item_id", "qty"])
Trade = namedtuple("Trade", ["item", "cost"])

NULL_SLOT = Slot(0x0000, 0)
ADAMANT_SEED_X3 = Slot(0x0087, 3)
ARMOR_STONE_X3 = Slot(0x01bb, 3)
BARIOTH_SHELL_X1 = Slot(0x0194, 1)
BARROTH_SHELL_X1 = Slot(0x012b, 1)
BITTERBUG_X10 = Slot(0x0074, 10)
BLUE_MUSHROOM_X10 = Slot(0x008e, 10)
BOMBERRY_X10 = Slot(0x0084, 10)
BOMB_AROWANA_X3 = Slot(0x00d5, 3)
BONE_HUSK_L_X2 = Slot(0x0157, 2)
BONE_HUSK_S_X10 = Slot(0x0156, 10)
BUGHOPPER_X10 = Slot(0x0160, 10)
BURST_AROWANA_X10 = Slot(0x00d4, 10)
DIABLOS_SHELL_X1 = Slot(0x0128, 1)
DRAGONFELL_BERRY_X4 = Slot(0x0170, 4)
DRAGON_TOADSTOOL_X5 = Slot(0x014d, 5)
DUNG_X5 = Slot(0x00c5, 5)
EXCITESHROOM_X5 = Slot(0x0091, 5)
FIRE_HERB_X10 = Slot(0x007e, 10)
FIREDOUSE_BERRY_X3 = Slot(0x0187, 3)
FLASHBUG_X5 = Slot(0x0075, 5)
GOBUL_HIDE_X1 = Slot(0x0144, 1)
GODBUG_X5 = Slot(0x0073, 5)
GREAT_JAGGI_HIDE_X1 = Slot(0x0134, 1)
HERB_X10 = Slot(0x007b, 10)
HONEY_X5 = Slot(0x008d, 5)
ICE_CRYSTAL_X5 = Slot(0x006b, 5)
ICETHAW_PELLET_X3 = Slot(0x0189, 3)
IVY_X10 = Slot(0x0085, 10)
LAGIACRUS_HIDE_X1 = Slot(0x0136, 1)
MEGA_HARPOON_X5 = Slot(0x0184, 5)
MIGHT_SEED_X3 = Slot(0x0086, 3)
MONSTER_BONE_M_X5 = Slot(0x009a, 5)
MONSTER_BONE_S_X5 = Slot(0x0099, 5)
NITROSHROOM_X10 = Slot(0x0093, 10)
PAINTBERRY_X10 = Slot(0x0080, 10)
PARASHROOM_X5 = Slot(0x0092, 5)
PIN_TUNA_X10 = Slot(0x00d1, 10)
POPFISH_X8 = Slot(0x00d2, 8)
PRIZE_GOLD_SWORD_X1 = Slot(0x025d, 1)
QURUPECO_SCALE_X1 = Slot(0x011f, 1)
RATHALOS_SCALE_X1 = Slot(0x0119, 1)
RATHIAN_SCALE_X1 = Slot(0x0112, 1)
SAP_PLANT_X10 = Slot(0x007f, 10)
SCATTERFISH_X2 = Slot(0x00d7, 2)
SCREAMER_X3 = Slot(0x0135, 3)
SHARPENED_FANG_X5 = Slot(0x0232, 5)
SLEEP_HERB_X10 = Slot(0x007d, 10)
SLEEPYFISH_X8 = Slot(0x00d3, 8)
SNAKEBEE_LARVA_X5 = Slot(0x0162, 5)
SPIDER_WEB_X5 = Slot(0x00c6, 5)
STONE_X10 = Slot(0x0061, 10)
STORMSENDER_SEED_X3 = Slot(0x018a, 3)
SUSHIFISH_X10 = Slot(0x00d0, 10)
TOADSTOOL_X5 = Slot(0x0158, 5)
WATERBLOCK_SEED_X3 = Slot(0x0188, 3)
WELL_DONE_STEAK_X5 = Slot(0x001a, 5)
WHETFISH_X10 = Slot(0x00cf, 10)
WYVERN_CLAW_X8 = Slot(0x0167, 8)
WYVERN_FANG_X8 = Slot(0x0165, 8)
YAMBUG_X10 = Slot(0x015e, 10)

TRADES = OrderedDict([
    # Source: https://monsterhunter.fandom.com/wiki/Loc_Lac_City

    # Adamant Seed x3 <- Immature Sponge x1 | Barroth Coin x1
    Trade(item=ADAMANT_SEED_X3, cost=(Slot(0x0142, 1), Slot(0x0260, 1))),

    # Armor Stone x3 <- Deviljho Coin x1 | Pinnacle Coin x1
    Trade(item=ARMOR_STONE_X3, cost=(Slot(0x024d, 1), Slot(0x0267, 1))),

    # Barioth Shell x1 <- Barioth Coin x3 | Pinnacle Coin x2
    Trade(item=BARIOTH_SHELL_X1, cost=(Slot(0x024a, 3), Slot(0x0267, 2))),

    # Barroth Shell x1 <- Barroth Coin x3 | Pinnacle Coin x2
    Trade(item=BARROTH_SHELL_X1, cost=(Slot(0x0260, 3), Slot(0x0267, 2))),

    # Bitterbug x10 <- Jaggi Hide x3 | Qurupeco Coin x2
    Trade(item=BITTERBUG_X10, cost=(Slot(0x0131, 3), Slot(0x025f, 2))),

    # Blue Mushroom x10 <- Bird Wyvern Fang x2 | Qurupeco Coin x2
    Trade(item=BLUE_MUSHROOM_X10, cost=(Slot(0x0130, 2), Slot(0x025f, 2))),

    # Bomberry x10 <- Vivid Feather x1 | Barroth Coin x2
    Trade(item=BOMBERRY_X10, cost=(Slot(0x0121, 1), Slot(0x0260, 2))),

    # Bomb Arowana x3 <- Iron Ore x1 | R.Ludroth Coin x1
    Trade(item=BOMB_AROWANA_X3, cost=(Slot(0x0063, 1), Slot(0x0261, 1))),

    # Bone Husk L x2 <- Great Baggi Claw x1 | Barroth Coin x2
    Trade(item=BONE_HUSK_L_X2, cost=(Slot(0x021d, 1), Slot(0x0260, 2))),

    # Bone Husk S x10 <- Bone x2 | Barroth Coin x2
    Trade(item=BONE_HUSK_S_X10, cost=(Slot(0x00c4, 2), Slot(0x0260, 2))),

    # Bughopper x10 <- Big Fin x3 | R.Ludroth Coin x2
    Trade(item=BUGHOPPER_X10, cost=(Slot(0x0230, 3), Slot(0x0261, 2))),

    # Burst Arowana x10 <- Earth Crystal x5 | Rathian Coin x2
    Trade(item=BURST_AROWANA_X10, cost=(Slot(0x0064, 5), Slot(0x0262, 2))),

    # Diablos Shell x1 <- Diablos Coin x3 | Pinnacle Coin x2
    Trade(item=DIABLOS_SHELL_X1, cost=(Slot(0x024c, 3), Slot(0x0267, 2))),

    # Dragonfell Berry x4 <- Thunderbug x1 | Rathian Coin x1
    Trade(item=DRAGONFELL_BERRY_X4, cost=(Slot(0x0076, 1), Slot(0x0262, 1))),

    # Dragon Toadstool x5 <- Flabby Hide x2 | Barioth Coin x4
    Trade(item=DRAGON_TOADSTOOL_X5, cost=(Slot(0x0123, 2), Slot(0x024a, 4))),

    # Dung x5 <- Monster Fluid x1 | R.Ludroth Coin x1
    Trade(item=DUNG_X5, cost=(Slot(0x0155, 1), Slot(0x0261, 1))),

    # Exciteshroom x5 <- Immature Sponge x1 | Barroth Coin x2
    Trade(item=EXCITESHROOM_X5, cost=(Slot(0x0142, 1), Slot(0x0260, 2))),

    # Fire Herb x10 <- Monster Bone M x1 | Qurupeco Coin x2
    Trade(item=FIRE_HERB_X10, cost=(Slot(0x009a, 1), Slot(0x025f, 2))),

    # Firedouse Berry x3 <- Mystery Bone x4 | Qurupeco Coin x1
    Trade(item=FIREDOUSE_BERRY_X3, cost=(Slot(0x010e, 4), Slot(0x025f, 1))),

    # Flashbug x5 <- Rhenoplos Scalp x1 | R.Ludroth Coin x2
    Trade(item=FLASHBUG_X5, cost=(Slot(0x0221, 1), Slot(0x0261, 2))),

    # Gobul Hide x1 <- Gobul Coin x3 | Pinnacle Coin x2
    Trade(item=GOBUL_HIDE_X1, cost=(Slot(0x0249, 3), Slot(0x0267, 2))),

    # Godbug x5 <- Blue Kelbi Horn x1 | R.Ludroth Coin x2
    Trade(item=GODBUG_X5, cost=(Slot(0x0152, 1), Slot(0x0261, 2))),

    # Great Jaggi Hide x1 <- Great Jaggi Coin x1 | Pinnacle Coin x1
    Trade(item=GREAT_JAGGI_HIDE_X1, cost=(Slot(0x025e, 1), Slot(0x0267, 1))),

    # Herb x10 <- Giggi Stinger x2 | Great Jaggi Coin x2
    Trade(item=HERB_X10, cost=(Slot(0x0234, 2), Slot(0x025e, 2))),

    # Honey x5 <- Sharpened Fang x1 | Qurupeco Coin x1
    Trade(item=HONEY_X5, cost=(Slot(0x0232, 1), Slot(0x025f, 1))),

    # Ice Crystal x5 <- Sharpened Fang x3 | Great Jaggi Coin x2
    Trade(item=ICE_CRYSTAL_X5, cost=(Slot(0x0232, 3), Slot(0x025e, 2))),

    # Icethaw Pellet x3 <- Mystery Bone x4 | R.Ludroth Coin x1
    Trade(item=ICETHAW_PELLET_X3, cost=(Slot(0x010e, 4), Slot(0x0261, 1))),

    # Ivy x10 <- Kelbi Horn x2 | Great Jaggi Coin x2
    Trade(item=IVY_X10, cost=(Slot(0x0151, 2), Slot(0x025e, 2))),

    # Lagiacrus Hide x1 <- Lagiacrus Coin x3 | Pinnacle Coin x2
    Trade(item=LAGIACRUS_HIDE_X1, cost=(Slot(0x0263, 3), Slot(0x0267, 2))),

    # Mega Harpoon x5 <- Immature Sponge x2 | Barroth Coin x1
    Trade(item=MEGA_HARPOON_X5, cost=(Slot(0x0142, 2), Slot(0x0260, 1))),

    # Might Seed x3 <- Immature Sponge x1 | Barroth Coin x1
    Trade(item=MIGHT_SEED_X3, cost=(Slot(0x0142, 1), Slot(0x0260, 1))),

    # Monster Bone M x5 <- Rathian Webbing x1 | Rathian Coin x2
    Trade(item=MONSTER_BONE_M_X5, cost=(Slot(0x0114, 1), Slot(0x0262, 2))),

    # Monster Bone S x5 <- Blue Kelbi Horn x1 | Barroth Coin x2
    Trade(item=MONSTER_BONE_S_X5, cost=(Slot(0x0152, 1), Slot(0x0260, 2))),

    # Nitroshroom x10 <- Jaggi Hide x2 | R.Ludroth Coin x1
    Trade(item=NITROSHROOM_X10, cost=(Slot(0x0131, 2), Slot(0x0261, 1))),

    # Paintberry x10 <- Bnahabra Wing x1 | Qurupeco Coin x2
    Trade(item=PAINTBERRY_X10, cost=(Slot(0x0154, 1), Slot(0x025f, 2))),

    # Parashroom x5 <- Sharpened Fang x1 | Qurupeco Coin x1
    Trade(item=PARASHROOM_X5, cost=(Slot(0x0232, 1), Slot(0x025f, 1))),

    # Pin Tuna x10 <- Iron Ore x4 | Barroth Coin x2
    Trade(item=PIN_TUNA_X10, cost=(Slot(0x0063, 4), Slot(0x0260, 2))),

    # Popfish x8 <- Machalite Ore x2 | Rathian Coin x2
    Trade(item=POPFISH_X8, cost=(Slot(0x0065, 2), Slot(0x0262, 2))),

    # Prize Gold Sword x1 <- Lagiacrus Coin x15 | Pinnacle Coin x8
    Trade(item=PRIZE_GOLD_SWORD_X1, cost=(Slot(0x0263, 15), Slot(0x0267, 8))),

    # Qurupeco Scale x1 <- Qurupeco Coin x3 | Pinnacle Coin x1
    Trade(item=QURUPECO_SCALE_X1, cost=(Slot(0x025f, 3), Slot(0x0267, 1))),

    # Rathalos Scale x1 <- Rathalos Coin x1 | Pinnacle Coin x2
    Trade(item=RATHALOS_SCALE_X1, cost=(Slot(0x0248, 1), Slot(0x0267, 2))),

    # Rathian Scale x1 <- Rathian Coin x3 | Pinnacle Coin x2
    Trade(item=RATHIAN_SCALE_X1, cost=(Slot(0x0262, 3), Slot(0x0267, 2))),

    # Sap Plant x10 <- Kelbi Horn x2 | Great Jaggi Coin x2
    Trade(item=SAP_PLANT_X10, cost=(Slot(0x0151, 2), Slot(0x025e, 2))),

    # Scatterfish x2 <- Machalite Ore x2 | Gobul Coin x1
    Trade(item=SCATTERFISH_X2, cost=(Slot(0x0065, 2), Slot(0x0249, 1))),

    # Screamer x3 <- R.Ludroth Scale x1 | Gobul Coin x1
    Trade(item=SCREAMER_X3, cost=(Slot(0x013d, 1), Slot(0x0249, 1))),

    # Sharpened Fang x5 <- Hydro Hide x2 | R.Ludroth Coin x2
    Trade(item=SHARPENED_FANG_X5, cost=(Slot(0x0141, 2), Slot(0x0261, 2))),

    # Sleep Herb x10 <- Velvety Hide x1 | Qurupeco Coin x2
    Trade(item=SLEEP_HERB_X10, cost=(Slot(0x0233, 1), Slot(0x025f, 2))),

    # Sleepyfish x8 <- Iron Ore x3 | R.Ludroth Coin x2
    Trade(item=SLEEPYFISH_X8, cost=(Slot(0x0063, 3), Slot(0x0261, 2))),

    # Snakebee Larva x5 <- Rhenoplos Scalp x2 | Barroth Coin x2
    Trade(item=SNAKEBEE_LARVA_X5, cost=(Slot(0x0221, 2), Slot(0x0260, 2))),

    # Spider Web x5 <- Monster Fluid x1 | Barroth Coin x1
    Trade(item=SPIDER_WEB_X5, cost=(Slot(0x0155, 1), Slot(0x0260, 1))),

    # Stone x10 <- Monster Bone M x1 | Great Jaggi Coin x2
    Trade(item=STONE_X10, cost=(Slot(0x009a, 1), Slot(0x025e, 2))),

    # Stormsender Seed x3 <- Bone x4 | R.Ludroth Coin x1
    Trade(item=STORMSENDER_SEED_X3, cost=(Slot(0x00c4, 4), Slot(0x0261, 1))),

    # Sushifish x10 <- Giggi Stinger x3 | Qurupeco Coin x2
    Trade(item=SUSHIFISH_X10, cost=(Slot(0x0234, 3), Slot(0x025f, 2))),

    # Toadstool x5 <- Sharpened Fang x1 | Qurupeco Coin x1
    Trade(item=TOADSTOOL_X5, cost=(Slot(0x0232, 1), Slot(0x025f, 1))),

    # Waterblock Seed x3 <- Bone x4 | Qurupeco Coin x1
    Trade(item=WATERBLOCK_SEED_X3, cost=(Slot(0x00c4, 4), Slot(0x025f, 1))),

    # Well-done Steak x5 <- Iron Ore x4 | R.Ludroth Coin x1
    Trade(item=WELL_DONE_STEAK_X5, cost=(Slot(0x0063, 4), Slot(0x0261, 1))),

    # Whetfish x10 <- Giggi Stinger x3 | Qurupeco Coin x2
    Trade(item=WHETFISH_X10, cost=(Slot(0x0234, 3), Slot(0x025f, 2))),

    # Wyvern Claw x8 <- Great Baggi Claw x1 | Rathian Coin x1
    Trade(item=WYVERN_CLAW_X8, cost=(Slot(0x021d, 1), Slot(0x0262, 1))),

    # Wyvern Fang x8 <- Qurupeco Scale x1 | Barroth Coin x1
    Trade(item=WYVERN_FANG_X8, cost=(Slot(0x011f, 1), Slot(0x0260, 1))),

    # Yambug x10 <- Sharpened Fang x3 | R.Ludroth Coin x2
    Trade(item=YAMBUG_X10, cost=(Slot(0x0232, 3), Slot(0x0261, 2)))
])

KNOWN_TRADES_1 = [
    # Source: https://youtu.be/Ie_9lRIZF20?t=478
    POPFISH_X8, WATERBLOCK_SEED_X3, BONE_HUSK_S_X10, DUNG_X5, SHARPENED_FANG_X5,  # noqa
    TOADSTOOL_X5, STONE_X10, SPIDER_WEB_X5, BUGHOPPER_X10, ICETHAW_PELLET_X3,
    RATHIAN_SCALE_X1, WYVERN_CLAW_X8, PRIZE_GOLD_SWORD_X1, BARIOTH_SHELL_X1, ARMOR_STONE_X3  # noqa
]

KNOWN_TRADES_2 = [
    # Source: https://youtu.be/lPFQW3B1Kt0?t=84
    IVY_X10, WATERBLOCK_SEED_X3, BLUE_MUSHROOM_X10, FLASHBUG_X5, ICE_CRYSTAL_X5,  # noqa
    YAMBUG_X10, HERB_X10, BURST_AROWANA_X10, MEGA_HARPOON_X5, SHARPENED_FANG_X5,  # noqa
    DRAGON_TOADSTOOL_X5, DIABLOS_SHELL_X1, BARROTH_SHELL_X1, PRIZE_GOLD_SWORD_X1, DRAGONFELL_BERRY_X4  # noqa
]

# For testing purposes (TRADES has 60 entries)
TRADES_SLICE_1 = list(islice(TRADES, 0, 15))
TRADES_SLICE_2 = list(islice(TRADES, 15, 30))
TRADES_SLICE_3 = list(islice(TRADES, 30, 45))
TRADES_SLICE_4 = list(islice(TRADES, 45, 60))


def pack_trades(known_trades):
    """Pack trades into binary.

    Each trade should contain 3 slots and end with a null one.
    The last 5 trades (page 3) are only visible during sandstorm.
    """
    def pad(known_trade):
        return sum(TRADES[known_trade], known_trade) + NULL_SLOT
    return b"".join(
        struct.pack(">HHHHHHHH", *pad(known_trade))
        for known_trade in known_trades
    )


CURRENT_TRADES = pack_trades(KNOWN_TRADES_1)
