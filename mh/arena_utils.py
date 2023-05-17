#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Arena utils module.

Arena Quest ID List:
EA60 
EA61
EA62
EA63
EA64
EA65
EA66
EA67
EA68
EA69
EA6A
EA6B
"""

# bird and brute bowgun: rathling gun + barrel, poison stinger frame, light bowgun stock
# sea power bowgun: rathling gun barrel, rathling gun + frame, rathling gun + stock
# land lords bowgun: jho barrel, diablos frame, barioth stock
# two flames bowgun: lagiacrus barrel, lagiacrus frame, barioth stock

# https://web.archive.org/web/20111012085906/http://divinewh.im/q/c/Grudge_Match:_Royal_Ludroth
# https://web.archive.org/web/20111012085901/http://divinewh.im/q/c/Grudge_Match:_Rathian
# https://web.archive.org/web/20111012090656/http://divinewh.im/q/c/Grudge_Match:_Uragaan
# https://web.archive.org/web/20111012090915/http://divinewh.im/q/c/Grudge_Match:_Bird_and_Brute

import csv
from mh.quest_utils import make_binary_event_quest,\
    generate_flags, Monster, LocationType,\
    QuestRankType, QuestRestrictionType, ResourcesType,\
    StartingPositionType, ItemsType
from mh.equipment_utils import Chestpiece, Gauntlets, Faulds,\
    Leggings, Helmet, EquipmentClasses, Greatsword,\
    SnS, Hammer, Longsword, Switchaxe, Lance,\
    BowgunFrame, BowgunStock, BowgunBarrel


GRUDGE_MATCH_ROYAL_LUDROTH = {
    'quest_info': {
        'quest_id': 0xEA61,
        'name': "Grudge Match: Royal Ludroth",
        'client': "Announcer/Receptionist",
        'description': "Slay a Royal Ludroth",
        'details': "Ahoy, adrenaline junkies!" + '\x0A' +
            "Next up is the regally maned" + '\x0A' +
            "Royal Ludroth! Will the pressure" + '\x0A' +
            "of facing this sea dragon on" + '\x0A' +
            "its home surf with a strict" + '\x0A' +
            "time limit leave the hunters" + '\x0A' +
            "all washed up?",
        'success_message': "Complete the Main Quest.",
        'flags': generate_flags((0,0,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank':QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp, 
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'smallmonster_data_file': 'sm_underwaterarenarock.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'boss_id': 0x0000,
            'enabled': True,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_2': {
            'type': Monster.none,
            'boss_id': 0x0000,
            'enabled': False,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_3': {
            'type': Monster.none,
            'boss_id': 0x0000,
            'enabled': False,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.royal_ludroth,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [(ItemsType.r_ludroth_coin, 1, 24), (ItemsType.r_ludroth_coin, 2, 8),
                              (ItemsType.voucher, 1, 10), (ItemsType.armor_sphere, 1, 24),
                              (ItemsType.steel_eg, 1, 18), (ItemsType.pinnacle_coin, 1, 16)],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        'unk_12': 0x00000002,  # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
        'unk_9': 0x00000000,
        'unk_10': 0x00000000,
        'unk_11': 0x00000000,
    },
    'arena_equipment': (\
        ((EquipmentClasses.SnS, SnS.HydraKnife), None, None,
            Helmet.QurupecoHelm, Chestpiece.QurupecoMail, Gauntlets.BlastBracelet, Faulds.SteelFaulds, Leggings.IngotGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10), (ItemsType.lifepowder, 2),
                (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10)),
            ()),
        ((EquipmentClasses.Greatsword, Greatsword.ChieftainsGrtSwd), None, None,
            Helmet.DrawEarring, Chestpiece.SteelMail, Gauntlets.GobulVambraces, Faulds.GobulFaulds, Leggings.HuntersGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10), (ItemsType.might_pill, 2),
                (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 1)),
            ()),
        ((EquipmentClasses.Hammer, Hammer.BoneBludgeon), None, None,
            Helmet.BarrothHelm, Chestpiece.BarrothMail, Gauntlets.AlloyVambraces, Faulds.BarrothFaulds, Leggings.BarrothGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10), (ItemsType.paralysis_knife, 5),
                (ItemsType.ez_flash_bomb, 1)),
            ()),
        ((EquipmentClasses.BowgunFrame, BowgunFrame.RoyalLauncher), (EquipmentClasses.BowgunBarrel, BowgunBarrel.JaggidFire), (EquipmentClasses.BowgunStock, BowgunStock.LightBowgun),
            Helmet.AlloyCap, Chestpiece.AlloyVest, Gauntlets.LagiacrusGuards, Faulds.AlloyCoat, Leggings.PiscineLeggings,
            ((ItemsType.potion, 10), (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10), (ItemsType.lifepowder, 2), (ItemsType.shock_trap, 1),
                (ItemsType.barrel_bomb_l_plus, 2), (ItemsType.barrel_bomb_l, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv1, 60), (ItemsType.pierce_s_lv2, 50), (ItemsType.clust_s_lv1, 5),
                (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12))))
}

GRUDGE_MATCH_BIRD_BRUTE = {
    'quest_info': {
        'quest_id': 0xEA66,
        'name': "Grudge Match: Bird and Brute",
        'client': "Announcer/Receptionist",
        'description': "Slay a Qurupeco" + '\x0A' + "and a Barroth",
        'details': "Double trouble! It's the" + '\x0A' +
            "dirty-bird Qurupeco and the" + '\x0A' +
            "land dragon Barroth -- heaven" + '\x0A' +
            "and earth, laughter and tears," + '\x0A' +
            "in an ultimate contest! When" + '\x0A' +
            "the dust clears, will it" + '\x0A' +
            "reveal victory? Or tragedy?",
        'success_message': "Complete the Main Quest.",
        'flags': generate_flags((0,1,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_4,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp, 
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'smallmonster_data_file': 'sm_bloodsport.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.qurupeco,
            'boss_id': 0x0000,
            'enabled': True,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_2': {
            'type': Monster.barroth,
            'boss_id': 0x0001,
            'enabled': True,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_3': {
            'type': Monster.none,
            'boss_id': 0x0000,
            'enabled': False,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.qurupeco,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [(ItemsType.qurupeco_coin, 1, 16), (ItemsType.barroth_coin, 1, 20),
                              (ItemsType.voucher, 1, 14), (ItemsType.armor_sphere_plus, 1, 10),
                              (ItemsType.adv_armor_sphere, 1, 5), (ItemsType.steel_eg, 1, 15),
                              (ItemsType.silver_eg, 1, 5), (ItemsType.hunter_king_coin, 1, 15)],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000101,
            'objective_type': Monster.barroth,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        'unk_12': 0x00000002,  # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
        'unk_9': 0x00000000,
        'unk_10': 0x00000000,
        'unk_11': 0x00000000,
    },
    'arena_equipment': (\
        ((EquipmentClasses.Switchaxe, Switchaxe.AssaultAxePlus), None, None,
            Helmet.GigginoxCapPlus, Chestpiece.AlloyMail, Gauntlets.BaggiVambracesPlus, Faulds.GigginoxFauldsPlus, Leggings.GigginoxGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.ration, 10), (ItemsType.cleanser, 5),
                (ItemsType.barrel_bomb_l, 2), (ItemsType.lifepowder, 1), (ItemsType.ez_shock_trap, 1), (ItemsType.ez_flash_bomb, 2)),
            ()),
        ((EquipmentClasses.Greatsword, Greatsword.CataclysmSword), None, None,
            Helmet.DrawEarring, Chestpiece.JaggiMailPlus, Gauntlets.JaggiVambracesPlus, Faulds.JaggiFauldsPlus, Leggings.BoneGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.ration, 10), (ItemsType.cleanser, 5),
                (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 2), (ItemsType.pitfall_trap, 1), (ItemsType.ez_flash_bomb, 2)),
            ()),
        ((EquipmentClasses.Lance, Lance.Undertaker), None, None,
            Helmet.DiablosCap, Chestpiece.AgnaktorMailPlus, Gauntlets.SteelVambracesPlus, Faulds.SteelCoilPlus, Leggings.AlloyGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.ration, 10), (ItemsType.cleanser, 5),
                (ItemsType.barrel_bomb_l, 2), (ItemsType.ez_flash_bomb, 1)),
            ()),
        ((EquipmentClasses.BowgunFrame, BowgunFrame.PoisonStinger), (EquipmentClasses.BowgunBarrel, BowgunBarrel.RathlingGunPlus), (EquipmentClasses.BowgunStock, BowgunStock.LightBowgun),
            Helmet.AgnaktorCapPlus, Chestpiece.AgnaktorVestPlus, Gauntlets.AgnaktorGuardsPlus, Faulds.AgnaktorCoatPlus, Leggings.RathalosLeggingsPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.ration, 10), (ItemsType.cleanser, 5), (ItemsType.lifepowder, 2),
                (ItemsType.ez_flash_bomb, 1), (ItemsType.sonic_bomb, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99), (ItemsType.pierce_s_lv2, 50), (ItemsType.clust_s_lv2, 5),
                (ItemsType.crag_s_lv2, 9), (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12), (ItemsType.sleep_s_lv1, 12))))
}


GRUDGE_MATCH_TWO_FLAMES = {
    'quest_info': {
        'quest_id': 0xEA68,
        'name': "Grudge Match: Two Flames",
        'client': "Announcer/Receptionist",
        'description': "Slay a Rathalos" + '\x0A' + "and a Rathian",
        'details': "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
            "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': generate_flags((0,1,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp, 
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'smallmonster_data_file': 'sm_bloodsport.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.rathalos,
            'boss_id': 0x0000,
            'enabled': True,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_2': {
            'type': Monster.rathian,
            'boss_id': 0x0001,
            'enabled': True,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_3': {
            'type': Monster.none,
            'boss_id': 0x0000,
            'enabled': False,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [(ItemsType.rathalos_coin, 1, 10), (ItemsType.rathian_coin, 1, 24),
                              (ItemsType.voucher, 1, 14), (ItemsType.armor_sphere_plus, 1, 10),
                              (ItemsType.adv_armor_sphere, 1, 5), (ItemsType.steel_eg, 1, 15),
                              (ItemsType.silver_eg, 1, 5), (ItemsType.hunter_king_coin, 1, 17)],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000101,
            'objective_type': Monster.rathian,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        'unk_12': 0x00000002,  # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
        'unk_9': 0x00000000,
        'unk_10': 0x00000000,
        'unk_11': 0x00000000,
    },
    'arena_equipment': (\
        ((EquipmentClasses.SnS, SnS.IcicleSpikePlus), None, None,
            Helmet.QurupecoHelmPlus, Chestpiece.QurupecoMailPlus, Gauntlets.QurupecoVambracesPlus, Faulds.QurupecoCoilPlus, Leggings.QurupecoGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.ration, 10), (ItemsType.might_pill, 2),
                (ItemsType.antidote, 2), (ItemsType.lifepowder, 1), (ItemsType.dung_bomb, 1), (ItemsType.paralysis_knife, 5),
                (ItemsType.pitfall_trap, 1), (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 1), (ItemsType.barrel_bomb_s, 1)),
            ()),
        ((EquipmentClasses.Longsword, Longsword.Thunderclap), None, None,
            Helmet.SilenceEarring, Chestpiece.AlloyMailPlus, Gauntlets.SteelVambracesPlus, Faulds.SteelCoilPlus, Leggings.VangisGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.ration, 10), (ItemsType.antidote, 2),
                (ItemsType.lifepowder, 1), (ItemsType.dung_bomb, 1), (ItemsType.ez_flash_bomb, 2)),
            ()),
        ((EquipmentClasses.Lance, Lance.SpiralLancePlus), None, None,
            Helmet.DemonEdgeEarring, Chestpiece.IngotMailPlus, Gauntlets.AgnaktorVambracesPlus, Faulds.RhenoplosCoilPlus, Leggings.IngotGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.whetstone, 20), (ItemsType.well_done_steak, 10), (ItemsType.antidote, 2),
                (ItemsType.lifepowder, 1), (ItemsType.dung_bomb, 1), (ItemsType.poison_knife, 5), (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 1)),
            ()),
        ((EquipmentClasses.BowgunFrame, BowgunFrame.ThundacrusRex), (EquipmentClasses.BowgunBarrel, BowgunBarrel.ThundacrusRex), (EquipmentClasses.BowgunStock, BowgunStock.BlizzardCannon),
            Helmet.EarringofFate, Chestpiece.UragaanVestPlus, Gauntlets.BlastBracelet, Faulds.UragaanCoatPlus, Leggings.UragaanLeggingsPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.ration, 10), (ItemsType.antidote, 2), (ItemsType.lifepowder, 2),
                (ItemsType.dung_bomb, 1), (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1), (ItemsType.pitfall_trap, 1), (ItemsType.ez_barrel_bomb_l, 1),
                (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99), (ItemsType.pierce_s_lv3, 40), (ItemsType.demon_s_ii, 5), (ItemsType.thunder_s, 60))))
}


GRUDGE_MATCH_LAND_LORDS = {
    'quest_info': {
        'quest_id': 0xEA6B,
        'name': "Grudge Match: Land Lords",
        'client': "Announcer/Receptionist",
        'description': "Slay all 3 monsters",
        'details': "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
            "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': generate_flags((0,0,1,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),
        'penalty_per_cart': 1150,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp, 
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'smallmonster_data_file': 'sm_bloodsport.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barroth,
            'boss_id': 0x0000,
            'enabled': True,
            'level': 0x17,
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_2': {
            'type': Monster.uragaan,
            'boss_id': 0x0001,
            'enabled': True,
            'level': 0x17,
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        },
        'monster_3': {
            'type': Monster.deviljho,
            'boss_id': 0x0002,
            'enabled': True,
            'level': 0x12,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00, # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00  # controls the spread of size but details unknown
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00020101,
            'objective_type': Monster.barroth,
            'objective_num': 0x01,
            'zenny_reward': 3000,
            'hrp_reward': 0,
            'rewards_row_1': [(ItemsType.deviljho_coin, 1, 10), (ItemsType.barroth_coin, 1, 10),
                              (ItemsType.uragaan_coin, 1, 15), (ItemsType.voucher, 1, 14),
                              (ItemsType.adv_armor_sphere, 1, 10), (ItemsType.hrd_armor_sphere, 1, 7),
                              (ItemsType.silver_eg, 1, 10), (ItemsType.hunter_king_coin, 1, 24)],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00020101,
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00020101,
            'objective_type': Monster.deviljho,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        'unk_12': 0x00000002,  # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
        'unk_9': 0x00000000,
        'unk_10': 0x00000000,
        'unk_11': 0x00000000,
    },
    'arena_equipment': (\
        ((EquipmentClasses.SnS, SnS.PlagueTabar), None, None,
            Helmet.UragaanHelmPlus, Chestpiece.UragaanMailPlus, Gauntlets.UragaanVambracesPlus, Faulds.UragaanFauldsPlus, Leggings.UragaanGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5), (ItemsType.lifepowder, 3),
                (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5), (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
                (ItemsType.druged_meat, 5), (ItemsType.poisoned_meat, 5), (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1),
                (ItemsType.ez_shock_trap, 1), (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 2), (ItemsType.barrel_bomb_l, 3),
                (ItemsType.barrel_bomb_s, 10), (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1),
                (ItemsType.armorcharm, 1), (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ()),
        ((EquipmentClasses.Switchaxe, Switchaxe.GreatDemonbindG), None, None,
            Helmet.RathalosHelmPlus, Chestpiece.RathalosMailPlus, Gauntlets.RathalosVambracesPlus, Faulds.RathalosFauldsPlus, Leggings.RathalosGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5), (ItemsType.lifepowder, 3),
                (ItemsType.dung_bomb, 5), (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5), (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
                (ItemsType.druged_meat, 5), (ItemsType.poisoned_meat, 5), (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 5),
                (ItemsType.barrel_bomb_l_plus, 1), (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1),
                (ItemsType.armorcharm, 1), (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ()),
        ((EquipmentClasses.Longsword, Longsword.ReaverCalamity), None, None,
            Helmet.StimulusEarring, Chestpiece.VangisMail, Gauntlets.DoberVambraces, Faulds.DoberCoil, Leggings.DamascusGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5), (ItemsType.cleanser, 5),
                (ItemsType.lifepowder, 5), (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5), (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
                (ItemsType.druged_meat, 5), (ItemsType.poisoned_meat, 5), (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1),
                (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 2), (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10),
                (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1), (ItemsType.armorcharm, 1), (ItemsType.armortalon, 1)),
            ()),
        ((EquipmentClasses.BowgunFrame, BowgunFrame.Diablazooka), (EquipmentClasses.BowgunBarrel, BowgunBarrel.DevilsGrin), (EquipmentClasses.BowgunStock, BowgunStock.BlizzardCannon),
            Helmet.BarrageEarring, Chestpiece.DamascusVest, Gauntlets.DamascusGuards, Faulds.DamascusCoat, Leggings.DamascusLeggings,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5), (ItemsType.lifepowder, 3), (ItemsType.paralysis_knife, 5),
                (ItemsType.sleep_knife, 5), (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5), (ItemsType.druged_meat, 5), (ItemsType.pitfall_trap, 1),
                (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1), (ItemsType.ez_flash_bomb, 5), (ItemsType.ez_barrel_bomb_l, 2), (ItemsType.barrel_bomb_l_plus, 2),
                (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10), (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1),
                (ItemsType.armorcharm, 1), (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv3, 40), (ItemsType.crag_s_lv2, 9), (ItemsType.crag_s_lv3, 9), (ItemsType.wyvernfire_lv1, 10),
                (ItemsType.water_s, 60), (ItemsType.sleep_s_lv2, 8), (ItemsType.dragon_s, 20), (ItemsType.demon_s_ii, 5))))
}
