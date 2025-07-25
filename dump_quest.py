#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Quest dumper.

ARENA INFO (under "strategies" are equipment lists)
https://w.atwiki.jp/mh3wii/pages/62.html#id_3bd26e57

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

bird and brute bowgun:
rathling gun + barrel, poison stinger frame, light bowgun stock

sea power bowgun:
rathling gun barrel, rathling gun + frame, rathling gun + stock

land lords bowgun:
jho barrel, diablos frame, barioth stock

two flames bowgun:
lagiacrus barrel, lagiacrus frame, barioth stock

https://web.archive.org/web/20111012085906/
http://divinewh.im/q/c/Grudge_Match:_Royal_Ludroth

https://web.archive.org/web/20111012085901/
http://divinewh.im/q/c/Grudge_Match:_Rathian

https://web.archive.org/web/20111012090656/
http://divinewh.im/q/c/Grudge_Match:_Uragaan

https://web.archive.org/web/20111012090915/
http://divinewh.im/q/c/Grudge_Match:_Bird_and_Brute
"""

from mh.quest_utils import ItemsType, Monster, LocationType,\
    QuestRankType, QuestRestrictionType, ResourcesType,\
    StartingPositionType, WaveType
from mh.equipment_utils import Chestpiece, Gauntlets, Faulds,\
    Leggings, Helmet, EquipmentClasses, Greatsword,\
    SnS, Hammer, Longsword, Switchaxe, Lance,\
    BowgunFrame, BowgunStock, BowgunBarrel


"""
EVENT QUEST 1: Jump Four Jaggi
Quest description/rewards/etc from https://www.youtube.com/watch?v=qyQt2Xmpt0g
Quest requirements altered to make it possible to win.
"""
QUEST_EVENT_JUMP_FOUR_JAGGI = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 2039.26,'pos_y': 12.70,'pos_z': 210.05,
                'rot_x': 0,'rot_y': 17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 857.89,'pos_y': -41.97,'pos_z': 814.06,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 97.58,'pos_y': -75.54,'pos_z': 135.22,
                'rot_x': 0,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': -393.52,'pos_y': -163.94,'pos_z': -667.01,
                'rot_x': 0,'rot_y': -199,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': -853.86,'pos_y': 19.45,'pos_z': 1381.66,
                'rot_x': 0,'rot_y': -113,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': 2,
                'pos_x': -553.59,'pos_y': -2.57,'pos_z': -369.71,
                'rot_x': 0,'rot_y': 193,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': -1698.75,'pos_y': 5.74,'pos_z': -530.30,
                'rot_x': 0,'rot_y': 398,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 873.28,'pos_y': 85.07,'pos_z': -610.86,
                'rot_x': 0,'rot_y': -153,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 1247.84,'pos_y': 106.65,'pos_z': 25.11,
                'rot_x': 0,'rot_y': -358,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': 2,
                'pos_x': 177.92,'pos_y': 450.70,'pos_z': -32.21,
                'rot_x': 0,'rot_y': -238,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': -78.66,'pos_y': 330.70,'pos_z': 362.86,
                'rot_x': 0,'rot_y': -79,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': 606.18,'pos_y': -12.89,'pos_z': 4145.11,
                'rot_x': 0,'rot_y': 324,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 524.37,'pos_y': -18.65,'pos_z': 2292.05,
                'rot_x': 0,'rot_y': 199,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': -460.08,'pos_y': -71.51,'pos_z': 3044.50,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 1,
                'pos_x': 300.40,'pos_y': 4.00,'pos_z': -211.14,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 458.16,'pos_y': 1.49,'pos_z': -918.94,
                'rot_x': 0,'rot_y': 51,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 4,
                'pos_x': 1813.83,'pos_y': 3.06,'pos_z': 925.68,
                'rot_x': 0,'rot_y': 494,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -504.37,'pos_y': 3.05,'pos_z': -757.30,
                'rot_x': 0,'rot_y': 676,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': 1118.48,'pos_y': 4.00,'pos_z': -420.89,
                'rot_x': 0,'rot_y': 364,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 2658.84,'pos_y': 3.24,'pos_z': 222.99,
                'rot_x': 0,'rot_y': 756,'rot_z': 0,
            },
        ],
        [
            # Area 6 (Area 8 in Sandy Plains)
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': 1612.71,'pos_y': -30.27,'pos_z': 695.30,
                'rot_x': 0,'rot_y': 517,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -2050.04,'pos_y': -31.90,'pos_z': -266.33,
                'rot_x': 0,'rot_y': 28,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 5,
                'pos_x': -344.14,'pos_y': -13.00,'pos_z': -26.14,
                'rot_x': 0,'rot_y': 443,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 4,
                'pos_x': -161.74,'pos_y': 4.80,'pos_z': -416.52,
                'rot_x': 0,'rot_y': 472,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 2,
                'pos_x': -481.05,'pos_y': 15.34,'pos_z': -643.19,
                'rot_x': 0,'rot_y': 568,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -692.26,'pos_y': -11.02,'pos_z': -235.13,
                'rot_x': 0,'rot_y': 608,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 3,
                'pos_x': -417.82,'pos_y': -1.44,'pos_z': -343.46,
                'rot_x': 0,'rot_y': 147,'rot_z': 0,
            },
        ],
        [
            # Area 7 (Area 9 in Sandy Plains)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 4294.59,'pos_y': -75.65,'pos_z': -2925.29,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 3995.30,'pos_y': -45.09,'pos_z': -2049.22,
                'rot_x': 0,'rot_y': -85,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 4187.00,'pos_y': -17.07,'pos_z': -1574.97,
                'rot_x': 0,'rot_y': -17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 1,
                'pos_x': 3781.64,'pos_y': -66.86,'pos_z': -2570.78,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 7,
                'pos_x': 293.99,'pos_y': -170.31,'pos_z': 4049.95,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 5,
                'pos_x': 124.95,'pos_y': -186.54,'pos_z': 3440.16,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 3,
                'pos_x': -425.01,'pos_y': -179.30,'pos_z': 4509.84,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': -714.48,'pos_y': -183.78,'pos_z': 4108.50,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1021.27,'pos_y': -215.48,'pos_z': 3726.09,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1974.57,'pos_y': -209.48,'pos_z': -316.05,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1825.11,'pos_y': -210.91,'pos_z': -382.90,
                'rot_x': 0,'rot_y': 130,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': 3383.92,'pos_y': 2.65,'pos_z': 592.49,
                'rot_x': 0,'rot_y': -193,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 1,
                'pos_x': 2653.55,'pos_y': -22.59,'pos_z': 987.24,
                'rot_x': 0,'rot_y': -73,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2838.69,'pos_y': -28.00,'pos_z': 445.91,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2109.53,'pos_y': -26.57,'pos_z': 575.43,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': -1,
                'pos_x': -1713.72,'pos_y': 1262.50,'pos_z': 2199.24,
                'rot_x': 273,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': 6,
                'pos_x': -1174.44,'pos_y': 1319.50,'pos_z': 1682.19,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
        ],
        [
            # Area 10
        ],
        [
            # Area 11 (Area 6 in Sandy Plains)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2195.89,'pos_y': 73.70,'pos_z': -720.92,
                'rot_x': 0,'rot_y': 39,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 1,
                'pos_x': -535.73,'pos_y': 1212.59,'pos_z': 896.44,
                'rot_x': 0,'rot_y': 169,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -434.00,'pos_y': 198.96,'pos_z': 289.52,
                'rot_x': 0,'rot_y': -267,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -802.69,'pos_y': 198.96,'pos_z': 66.62,
                'rot_x': 0,'rot_y': -216,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -645.14,'pos_y': 288.96,'pos_z': -371.21,
                'rot_x': 0,'rot_y': -227,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': -473.33,'pos_y': 168.96,'pos_z': -166.43,
                'rot_x': 0,'rot_y': -210,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61001,
        'name': "Jump Four Jaggi",
        'client': "Guild Subcontractor",
        'description': "Hunt 4 Great Jaggi",
        'details':
            "I'm gonna get so fired for\n"
            "this... The Great Jaggi some\n"
            "hunter brought in just\n"
            "escaped. Mind going after\n"
            "them? You better hurry,\n"
            "though. Bet they've got some\n"
            "incredible materials, too.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 1400,
        'quest_fee': 400,
        'time_limit': 50,
        'main_monster_1': Monster.bnahabra2,
        'main_monster_2': Monster.melynx,
        'location': LocationType.QUEST_LOCATION_SANDY_PLAINS,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 19,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x64050219,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.great_jaggi,
            'starting_area': 0x00,
            'boss_id': 0xFF,
            'spawn_count': 0x04,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.great_jaggi,
            'objective_num': 0x04,
            'zenny_reward': 4000,
            'hrp_reward': 440,
            'rewards_row_1': [
                (ItemsType.great_jagi_claw, 1, 3),
                (ItemsType.great_jagi_hide, 1, 12),
                (ItemsType.jagi_scale, 1, 10),
                (ItemsType.screamer, 1, 20),
                (ItemsType.kings_frill, 1, 12),
                (ItemsType.bone_husk_s, 8, 18),
                (ItemsType.great_jagi_head, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.mystery_charm, 1, 1),
                (ItemsType.aquaglow_jewel, 1, 1),
                (ItemsType.shining_charm, 1, 1),
                (ItemsType.armor_sphere, 1, 1),
                (ItemsType.armor_sphere_plus, 1, 1)
            ],
        },
        'subquest_1': {
            'description': "Hunt 2 Great Jaggi",
            'type': 0x00000001,
            'objective_type': Monster.great_jaggi,
            'objective_num': 0x02,
            'zenny_reward': 4000,
            'hrp_reward': 440,
            'rewards_row_1': [
                (ItemsType.great_jagi_claw, 1, 1),
                (ItemsType.great_jagi_hide, 1, 1),
                (ItemsType.jagi_scale, 1, 1),
                (ItemsType.screamer, 1, 1),
                (ItemsType.kings_frill, 1, 1),
                (ItemsType.bone_husk_s, 8, 1),
                (ItemsType.great_jagi_head, 1, 1)
            ],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 2: Mercy Mission
(INCOMPLETE) Invading monster is "faked" by hardcoding a Royal Ludroth
from the start.
"""
QUEST_EVENT_MERCY_MISSION = {
    'quest_info': {
        'quest_id': 61002,
        'name': "Mercy Mission",
        'client': "MH3SP Dev Team",
        'description': "Deliver 10 Monster Guts",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message':
            "Complete the Main Quest\n"
            "and both Subquests.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 1, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 600,
        'quest_fee': 150,
        'time_limit': 15,
        'main_monster_1': Monster.ludroth,
        'main_monster_2': Monster.epioth,
        'location': LocationType.QUEST_LOCATION_D_ISLAND,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 35,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x64030303,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_mercymission.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000002,
            'objective_type': ItemsType.monster_guts,
            'objective_num': 0x0A,
            'zenny_reward': 1500,
            'hrp_reward': 70,
            'rewards_row_1': [
                (ItemsType.mystery_charm, 1, 8),
                (ItemsType.black_pearl, 1, 20),
                (ItemsType.honey, 2, 20),
                (ItemsType.armor_sphere, 1, 18),
                (ItemsType.small_goldenfish, 1, 8),
                (ItemsType.machalite_ore, 8, 14),
                (ItemsType.steel_eg, 1, 12)
            ],
            'rewards_row_2': [
                (ItemsType.mystery_charm, 1, 35),
                (ItemsType.aquaglow_jewel, 1, 5),
                (ItemsType.shining_charm, 1, 15),
                (ItemsType.armor_sphere, 1, 20),
                (ItemsType.armor_sphere_plus, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "Deliver 12 Red Coral Stones",
            'type': 0x00000002,
            'objective_type': ItemsType.red_coral_stone,
            'objective_num': 0x0C,
            'zenny_reward': 1200,
            'hrp_reward': 55,
            'rewards_row_1': [
                (ItemsType.mystery_charm, 1, 8),
                (ItemsType.black_pearl, 1, 20),
                (ItemsType.honey, 2, 20),
                (ItemsType.armor_sphere, 1, 18),
                (ItemsType.small_goldenfish, 1, 8),
                (ItemsType.machalite_ore, 1, 14),
                (ItemsType.steel_eg, 1, 12)
            ],
        },
        'subquest_2': {
            'description': "Deliver 3 Goldenfish",
            'type': 0x00000002,
            'objective_type': ItemsType.goldenfish,
            'objective_num': 0x03,
            'zenny_reward': 2000,
            'hrp_reward': 70,
            'rewards_row_1': [
                (ItemsType.mystery_charm, 1, 35),
                (ItemsType.aquaglow_jewel, 1, 5),
                (ItemsType.shining_charm, 1, 15),
                (ItemsType.armor_sphere, 1, 20),
                (ItemsType.armor_sphere_plus, 1, 25)
            ],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000003,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 3: Animal Attractions
Quest description from https://www.youtube.com/watch?v=uvMYbmIl08E&t=12s
    Thanks to Goabie
"""
QUEST_EVENT_ANIMAL_ATTRACTIONS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 2039.26,'pos_y': 12.70,'pos_z': 210.05,
                'rot_x': 0,'rot_y': 17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 857.89,'pos_y': -41.97,'pos_z': 814.06,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 97.58,'pos_y': -75.54,'pos_z': 135.22,
                'rot_x': 0,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': -393.52,'pos_y': -163.94,'pos_z': -667.01,
                'rot_x': 0,'rot_y': -199,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': -853.86,'pos_y': 19.45,'pos_z': 1381.66,
                'rot_x': 0,'rot_y': -113,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': 2,
                'pos_x': -553.59,'pos_y': -2.57,'pos_z': -369.71,
                'rot_x': 0,'rot_y': 193,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': -1698.75,'pos_y': 5.74,'pos_z': -530.30,
                'rot_x': 0,'rot_y': 398,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 873.28,'pos_y': 85.07,'pos_z': -610.86,
                'rot_x': 0,'rot_y': -153,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 1247.84,'pos_y': 106.65,'pos_z': 25.11,
                'rot_x': 0,'rot_y': -358,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': 2,
                'pos_x': 177.92,'pos_y': 450.70,'pos_z': -32.21,
                'rot_x': 0,'rot_y': -238,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': -78.66,'pos_y': 330.70,'pos_z': 362.86,
                'rot_x': 0,'rot_y': -79,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': 606.18,'pos_y': -12.89,'pos_z': 4145.11,
                'rot_x': 0,'rot_y': 324,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 524.37,'pos_y': -18.65,'pos_z': 2292.05,
                'rot_x': 0,'rot_y': 199,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': -460.08,'pos_y': -71.51,'pos_z': 3044.50,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 1,
                'pos_x': 300.40,'pos_y': 4.00,'pos_z': -211.14,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 458.16,'pos_y': 1.49,'pos_z': -918.94,
                'rot_x': 0,'rot_y': 51,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 4,
                'pos_x': 1813.83,'pos_y': 3.06,'pos_z': 925.68,
                'rot_x': 0,'rot_y': 494,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -504.37,'pos_y': 3.05,'pos_z': -757.30,
                'rot_x': 0,'rot_y': 676,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': 1118.48,'pos_y': 4.00,'pos_z': -420.89,
                'rot_x': 0,'rot_y': 364,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 2658.84,'pos_y': 3.24,'pos_z': 222.99,
                'rot_x': 0,'rot_y': 756,'rot_z': 0,
            },
        ],
        [
            # Area 6 (Area 8 in Sandy Plains)
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': 1612.71,'pos_y': -30.27,'pos_z': 695.30,
                'rot_x': 0,'rot_y': 517,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -2050.04,'pos_y': -31.90,'pos_z': -266.33,
                'rot_x': 0,'rot_y': 28,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 5,
                'pos_x': -344.14,'pos_y': -13.00,'pos_z': -26.14,
                'rot_x': 0,'rot_y': 443,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 4,
                'pos_x': -161.74,'pos_y': 4.80,'pos_z': -416.52,
                'rot_x': 0,'rot_y': 472,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 2,
                'pos_x': -481.05,'pos_y': 15.34,'pos_z': -643.19,
                'rot_x': 0,'rot_y': 568,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -692.26,'pos_y': -11.02,'pos_z': -235.13,
                'rot_x': 0,'rot_y': 608,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 3,
                'pos_x': -417.82,'pos_y': -1.44,'pos_z': -343.46,
                'rot_x': 0,'rot_y': 147,'rot_z': 0,
            },
        ],
        [
            # Area 7 (Area 9 in Sandy Plains)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 4294.59,'pos_y': -75.65,'pos_z': -2925.29,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 3995.30,'pos_y': -45.09,'pos_z': -2049.22,
                'rot_x': 0,'rot_y': -85,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 4187.00,'pos_y': -17.07,'pos_z': -1574.97,
                'rot_x': 0,'rot_y': -17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 1,
                'pos_x': 3781.64,'pos_y': -66.86,'pos_z': -2570.78,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 7,
                'pos_x': 293.99,'pos_y': -170.31,'pos_z': 4049.95,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 5,
                'pos_x': 124.95,'pos_y': -186.54,'pos_z': 3440.16,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 3,
                'pos_x': -425.01,'pos_y': -179.30,'pos_z': 4509.84,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': -714.48,'pos_y': -183.78,'pos_z': 4108.50,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1021.27,'pos_y': -215.48,'pos_z': 3726.09,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1974.57,'pos_y': -209.48,'pos_z': -316.05,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1825.11,'pos_y': -210.91,'pos_z': -382.90,
                'rot_x': 0,'rot_y': 130,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': 3383.92,'pos_y': 2.65,'pos_z': 592.49,
                'rot_x': 0,'rot_y': -193,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 1,
                'pos_x': 2653.55,'pos_y': -22.59,'pos_z': 987.24,
                'rot_x': 0,'rot_y': -73,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2838.69,'pos_y': -28.00,'pos_z': 445.91,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2109.53,'pos_y': -26.57,'pos_z': 575.43,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': -1,
                'pos_x': -1713.72,'pos_y': 1262.50,'pos_z': 2199.24,
                'rot_x': 273,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': 6,
                'pos_x': -1174.44,'pos_y': 1319.50,'pos_z': 1682.19,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
        ],
        [
            # Area 10
        ],
        [
            # Area 11 (Area 6 in Sandy Plains)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2195.89,'pos_y': 73.70,'pos_z': -720.92,
                'rot_x': 0,'rot_y': 39,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 1,
                'pos_x': -535.73,'pos_y': 1212.59,'pos_z': 896.44,
                'rot_x': 0,'rot_y': 169,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -434.00,'pos_y': 198.96,'pos_z': 289.52,
                'rot_x': 0,'rot_y': -267,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -802.69,'pos_y': 198.96,'pos_z': 66.62,
                'rot_x': 0,'rot_y': -216,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -645.14,'pos_y': 288.96,'pos_z': -371.21,
                'rot_x': 0,'rot_y': -227,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': -473.33,'pos_y': 168.96,'pos_z': -166.43,
                'rot_x': 0,'rot_y': -210,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61003,
        'name': "Animal Attractions",
        'client': "Passionate Hunter",
        'description': "Capture 2 Barroth",
        'details':
            "You'll need more than big\n"
            "muscles and bigger weapons to\n"
            "capture two of the fiercest\n"
            "monsters around -- you'll need\n"
            "finesse! If you live for the\n"
            "art and craft of the hunt,\n"
            "show me what you got!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),  # (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0, 1, 1)  # (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 5200,
        'quest_fee': 1000,
        'time_limit': 50,
        'main_monster_1': Monster.bnahabra2,
        'main_monster_2': Monster.altaroth,
        'location': LocationType.QUEST_LOCATION_SANDY_PLAINS,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_9_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 14,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0019,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x19,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.barroth,
            'starting_area': 0x01,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x19,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000081,
            'objective_type': Monster.barroth,
            'objective_num': 0x02,
            'zenny_reward': 14400,
            'hrp_reward': 1250,
            'rewards_row_1': [
                (ItemsType.barroth_ridge, 1, 2),
                (ItemsType.barroth_shell, 1, 24),
                (ItemsType.barroth_claw, 1, 18),
                (ItemsType.monster_bone_l, 1, 8),
                (ItemsType.monster_bone_m, 1, 8),
                (ItemsType.barroth_scalp, 1, 12),
                (ItemsType.hellhunter_tag, 1, 28)
            ],
            'rewards_row_2': [
                (ItemsType.barroth_ridge, 1, 2),
                (ItemsType.barroth_shell, 1, 24),
                (ItemsType.barroth_claw, 1, 18),
                (ItemsType.monster_bone_l, 1, 8),
                (ItemsType.monster_bone_m, 1, 8),
                (ItemsType.barroth_scalp, 1, 12),
                (ItemsType.hellhunter_tag, 1, 28)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 4: Shut Up and Fish!
Quest description from
"""
QUEST_EVENT_SHUT_UP_AND_FISH = {
    'quest_info': {
        'quest_id': 61004,
        'name': "Shut Up and Fish!",
        'client': "MH3SP Dev Team",
        'description': "Hunt a Gobul",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message':
            "Complete the Main Quest\n"
            "and both Subquests.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 1, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 1900,
        'quest_fee': 550,
        'time_limit': 25,
        'main_monster_1': Monster.ludroth,
        'main_monster_2': Monster.kelbi,
        'location': LocationType.QUEST_LOCATION_FLOODED_FOR,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_9_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 35,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0019,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_ff_free_for_all.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.gobul,
            'starting_area': 0x00,  # 4 -> area 1  # 3 -> area 1  # 2 -> basecamp? # 1 -> area 3 # 0 -> area 4
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x19,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.gobul,
            'objective_num': 0x01,
            'zenny_reward': 5600,
            'hrp_reward': 820,
            'rewards_row_1': [
                (ItemsType.black_pearl, 3, 15),
                (ItemsType.jumbo_pearl, 1, 5),
                (ItemsType.glutton_tuna, 2, 10),
                (ItemsType.popfish, 3, 20),
                (ItemsType.burst_arowana, 2, 7),
                (ItemsType.bomb_arowana, 2, 10),
                (ItemsType.scatterfish, 2, 13),
                (ItemsType.small_goldenfish, 1, 20)
            ],
            'rewards_row_2': [
                (ItemsType.mystery_charm, 1, 35),
                (ItemsType.aquaglow_jewel, 1, 5),
                (ItemsType.shining_charm, 1, 15),
                (ItemsType.armor_sphere, 1, 20),
                (ItemsType.armor_sphere_plus, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "Deliver 4 Goldenfish",
            'type': 0x00000002,
            'objective_type': ItemsType.goldenfish,
            'objective_num': 0x04,
            'zenny_reward': 2400,
            'hrp_reward': 70,
            'rewards_row_1': [
                (ItemsType.mystery_charm, 1, 35),
                (ItemsType.aquaglow_jewel, 1, 5),
                (ItemsType.shining_charm, 1, 15),
                (ItemsType.armor_sphere, 1, 20),
                (ItemsType.armor_sphere_plus, 1, 25)
            ],
        },
        'subquest_2': {
            'description': "Fish out Gobul once",
            'type': 0x00001000,
            'objective_type': Monster.gobul,
            'objective_num': 0x02,
            'zenny_reward': 1200,
            'hrp_reward': 60,
            'rewards_row_1': [
                (ItemsType.black_pearl, 3, 15),
                (ItemsType.jumbo_pearl, 1, 5),
                (ItemsType.glutton_tuna, 2, 10),
                (ItemsType.popfish, 3, 20),
                (ItemsType.burst_arowana, 2, 7),
                (ItemsType.bomb_arowana, 2, 10),
                (ItemsType.scatterfish, 2, 13),
                (ItemsType.small_goldenfish, 1, 20)
            ],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 5: The Motley Mission
Quest description from https://www.youtube.com/watch?v=VOqSv-XAvlU
"""
QUEST_EVENT_MOTLEY_MISSION = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61005,
        'name': "The Motley Mission",
        'client': "Deserted Island Sailor",
        'description':
            "Hunt 2 Royal Ludroth\n"
            "",
        'details':
            "Wanna hear the Hunting Fleet's\n"
            "latest shanty? No? Too bad:\n"
            "\"Bow, port, starboard, stern,\n"
            "fishin' stinks at every turn.\n"
            "Our motley crew has one wish:\n"
            "hey, monsters, QUIT SCARIN'\n"
            "DA FISH!\" Catchy, aye?",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 3000,
        'quest_fee': 800,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_9_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 48,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001D,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x27,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x27,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.royal_ludroth,
            'objective_num': 0x02,
            'zenny_reward': 8000,
            'hrp_reward': 960,
            'rewards_row_1': [
                (ItemsType.black_pearl, 1, 20),
                (ItemsType.jumbo_pearl, 1, 8),
                (ItemsType.quality_sponge, 1, 14),
                (ItemsType.r_ludroth_claw, 1, 24),
                (ItemsType.r_ludroth_scale, 1, 17),
                (ItemsType.spongy_hide, 8, 10),
                (ItemsType.r_ludroth_crest, 1, 7)
            ],
            'rewards_row_2': [
                (ItemsType.black_pearl, 1, 20),
                (ItemsType.jumbo_pearl, 1, 8),
                (ItemsType.quality_sponge, 1, 14),
                (ItemsType.r_ludroth_claw, 1, 24),
                (ItemsType.r_ludroth_scale, 1, 17),
                (ItemsType.spongy_hide, 8, 10),
                (ItemsType.r_ludroth_crest, 1, 7)
            ],
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
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 6: Cold Call
Quest description from https://youtu.be/Z4CeGozzpmM?feature=shared&t=16
"""
QUEST_EVENT_COLD_CALL = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.popo,'unk1': 0,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -559.73,'pos_y': 20.32,'pos_z': -979.26,
                'rot_x': 0,'rot_y': 352,'rot_z': 0,
            },
            {
                'type': Monster.popo,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 1,'quantity': -1,
                'pos_x': 207.09,'pos_y': 5.00,'pos_z': -616.77,
                'rot_x': 0,'rot_y': 238,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': 1189.65,'pos_y': 10.65,'pos_z': -1620.63,
                'rot_x': 0,'rot_y': 28,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': 760.17,'pos_y': 27.35,'pos_z': -1651.16,
                'rot_x': 0,'rot_y': -22,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': 724.92,'pos_y': 2.63,'pos_z': -1902.14,
                'rot_x': 0,'rot_y': -79,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': -1433.39,'pos_y': 13.81,'pos_z': 1144.14,
                'rot_x': 0,'rot_y': 426,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': -1297.70,'pos_y': 12.96,'pos_z': 918.99,
                'rot_x': 0,'rot_y': 477,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': -1437.67,'pos_y': 27.98,'pos_z': 806.39,
                'rot_x': 0,'rot_y': 534,'rot_z': 0,
            },

            {
                'type': Monster.popo,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': -1,
                'pos_x': 1137.17,'pos_y': 5.05,'pos_z': 768.87,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
            {
                'type': Monster.popo,'unk1': 0,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': -1,
                'pos_x': 14.17,'pos_y': 46.50,'pos_z': 1833.63,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.popo,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 2,'quantity': -1,
                'pos_x': 556.11,'pos_y': 18.99,'pos_z': 1106.89,
                'rot_x': 0,'rot_y': 728,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': -1,
                'pos_x': -1739.64,'pos_y': 34.73,'pos_z': 1109.13,
                'rot_x': 0,'rot_y': -102,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': -1,
                'pos_x': 969.57,'pos_y': 0.50,'pos_z': -1964.12,
                'rot_x': 0,'rot_y': -102,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 3,
                'pos_x': 3146.44,'pos_y': 40.98,'pos_z': 314.53,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': 3471.39,'pos_y': 7.00,'pos_z': -709.74,
                'rot_x': 0,'rot_y': -136,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 3589.04,'pos_y': 5.00,'pos_z': -3259.04,
                'rot_x': 0,'rot_y': -11,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 3306.99,'pos_y': 5.00,'pos_z': -3166.77,
                'rot_x': 0,'rot_y': -34,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 3546.64,'pos_y': 15.73,'pos_z': -3692.10,
                'rot_x': 0,'rot_y': -113,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': -1,
                'pos_x': 3742.35,'pos_y': 29.38,'pos_z': -3606.37,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 2,
                'pos_x': 76.48,'pos_y': 18.62,'pos_z': 20.74,
                'rot_x': 0,'rot_y': 298,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 3,
                'pos_x': 643.46,'pos_y': 0.00,'pos_z': -353.74,
                'rot_x': 0,'rot_y': 25696,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': 7,
                'pos_x': 345.94,'pos_y': 3.39,'pos_z': 236.08,
                'rot_x': 0,'rot_y': -59,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': 4,
                'pos_x': 1276.36,'pos_y': 10.24,'pos_z': -299.36,
                'rot_x': 0,'rot_y': -19,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': 3776.99,'pos_y': 0.61,'pos_z': -701.98,
                'rot_x': 0,'rot_y': 46555,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': 3282.63,'pos_y': 0.00,'pos_z': 479.04,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': 2717.68,'pos_y': 0.60,'pos_z': -124.31,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 4,
                'pos_x': -629.64,'pos_y': 1496.43,'pos_z': -347.36,
                'rot_x': 0,'rot_y': 5,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 4,
                'pos_x': -380.25,'pos_y': 1428.15,'pos_z': -1054.46,
                'rot_x': 0,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 4169.78,'pos_y': 7.24,'pos_z': -2848.38,
                'rot_x': 0,'rot_y': 182,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': -1,
                'pos_x': 1700.26,'pos_y': 0.00,'pos_z': 438.18,
                'rot_x': 0,'rot_y': 147,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': -1,
                'pos_x': -2452.98,'pos_y': 44.18,'pos_z': -579.15,
                'rot_x': 0,'rot_y': 51,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 103.34,'pos_y': 41.02,'pos_z': -1208.04,
                'rot_x': 0,'rot_y': 244,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.baggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -11.26,'pos_y': -15.36,'pos_z': 157.88,
                'rot_x': 0,'rot_y': 238,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -1291.40,'pos_y': 4.00,'pos_z': 509.01,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -855.80,'pos_y': 0.48,'pos_z': -1393.44,
                'rot_x': 0,'rot_y': 159,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -525.73,'pos_y': -4.16,'pos_z': -1264.10,
                'rot_x': 0,'rot_y': -182,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -574.99,'pos_y': -4.64,'pos_z': -1717.30,
                'rot_x': 0,'rot_y': 159,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 5,'quantity': -1,
                'pos_x': 865.61,'pos_y': -4.30,'pos_z': -267.32,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 5,'quantity': -1,
                'pos_x': -1246.40,'pos_y': 6.31,'pos_z': -1119.90,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 6
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 2,
                'pos_x': -1266.86,'pos_y': 17.79,'pos_z': 1426.87,
                'rot_x': 0,'rot_y': 26038,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 4,
                'pos_x': -1838.98,'pos_y': -0.78,'pos_z': -1385.65,
                'rot_x': 0,'rot_y': 39,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 1,
                'pos_x': -1219.15,'pos_y': -2.77,'pos_z': -1722.55,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': 1068.11,'pos_y': -9.24,'pos_z': -712.22,
                'rot_x': 0,'rot_y': -73,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': 784.49,'pos_y': -8.94,'pos_z': 187.09,
                'rot_x': 0,'rot_y': -73,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 6,'quantity': -1,
                'pos_x': 758.48,'pos_y': 20.97,'pos_z': -936.30,
                'rot_x': 0,'rot_y': -125,'rot_z': 0,
            },
        ],
        [
            # Area 7
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 1495.12,'pos_y': 21.92,'pos_z': -1641.55,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 1,
                'pos_x': -1936.97,'pos_y': 7.33,'pos_z': -548.03,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': -1706.10,'pos_y': 2.87,'pos_z': 1374.15,
                'rot_x': 0,'rot_y': 136,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 4,
                'pos_x': 399.71,'pos_y': 0.00,'pos_z': -910.88,
                'rot_x': 0,'rot_y': -153,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': -776.39,'pos_y': 27.75,'pos_z': 24.70,
                'rot_x': 0,'rot_y': 23347,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 4,
                'pos_x': -1321.35,'pos_y': 97.17,'pos_z': 214.45,
                'rot_x': 0,'rot_y': 45,'rot_z': 0,
            },
            {
                'type': Monster.baggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': -1395.61,'pos_y': 88.08,'pos_z': -1084.80,
                'rot_x': 0,'rot_y': 30646,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61006,
        'name': "Cold Call",
        'client': "Tundra-expedition Member",
        'description': "Hunt a Gig., Bar. & bird wyv.",
        'details':
            "It was just a typical sub-zero\n"
            "night in the Tundra. But then,\n"
            "BOOM! The sky flashed and the\n"
            "ground quaked, like something\n"
            "big had crashed down. Then the\n"
            "monsters came. Help! We can't\n"
            "work under these conditions!",
        'success_message': "Complete the Main Quest.",
        'flags': (

            (0, 0, 1, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)

            # (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            # (1, 1, 0, 0, 0, 0, 0, 0),  # (1, 1, 0, 0, 0, 0, 0, 0),
            # (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            # (0, 0, 1, 0, 0, 0, 1, 1)  # (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 6000,
        'quest_fee': 1600,
        'time_limit': 50,
        'main_monster_1': Monster.popo,
        'main_monster_2': Monster.giggi,
        'location': LocationType.QUEST_LOCATION_TUNDRA,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_18_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 8,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001B,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.great_baggi,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x22,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.gigginox,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x22,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_3': {
            'type': Monster.barioth,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x23,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.great_baggi,
            'objective_num': 0x01,
            'zenny_reward': 16000,
            'hrp_reward': 2240,
            'rewards_row_1': [
                (ItemsType.barioth_pelt, 1, 2),
                (ItemsType.uncanny_hide, 1, 12),
                (ItemsType.great_bagi_claw, 1, 20),
                (ItemsType.shining_charm, 1, 7),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.frost_sac, 1, 5),
                (ItemsType.lightcrystal, 1, 10),
                (ItemsType.isisium, 1, 5),
                (ItemsType.dark_metal, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.barioth_pelt, 1, 2),
                (ItemsType.uncanny_hide, 1, 12),
                (ItemsType.great_bagi_claw, 1, 20),
                (ItemsType.shining_charm, 1, 7),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.frost_sac, 1, 5),
                (ItemsType.lightcrystal, 1, 10),
                (ItemsType.isisium, 1, 5),
                (ItemsType.dark_metal, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.gigginox,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.barioth,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 7: The Phantom Uragaan
Quest description from https://www.youtube.com/watch?v=Py5PkCXhf6w
"""
QUEST_EVENT_THE_PHANTOM_URAGAAN = {
    'quest_info': {
        'quest_id': 61007,
        'name': "The Phantom Uragaan",
        'client': "Spoiled Princess",
        'description': "Hunt an Uragaan",
        'details':
            "Oooh, I just heard they've\n"
            "spotted the cutest, tiniest,\n"
            "most adorable little Uragaan\n"
            "on the Volcano. Hunt me one\n"
            "this instant or I will get\n"
            "very angry. And if I'm angry,\n"
            "Daddy's angry. Now go!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 3000,
        'quest_fee': 850,
        'time_limit': 50,
        'main_monster_1': Monster.uroktor,
        'main_monster_2': Monster.aptonoth,
        'location': LocationType.QUEST_LOCATION_VOLCANO,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_18_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 15,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x1D,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_phantomuragaan.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x1D,  # 0x01 through 0x3c
            'size': 0x13,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 8800,
            'hrp_reward': 1100,
            'rewards_row_1': [
                (ItemsType.mystery_charm, 1, 1),
                (ItemsType.uragaan_shell, 1, 16),
                (ItemsType.uragaan_scale, 1, 20),
                (ItemsType.uragaan_marrow, 1, 10),
                (ItemsType.monster_bone_l, 1, 10),
                (ItemsType.bone_husk_l, 15, 13),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.rustshard, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.mystery_charm, 1, 1),
                (ItemsType.uragaan_shell, 1, 16),
                (ItemsType.uragaan_scale, 1, 20),
                (ItemsType.uragaan_marrow, 1, 10),
                (ItemsType.monster_bone_l, 1, 10),
                (ItemsType.bone_husk_l, 15, 13),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.rustshard, 1, 25)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 8: Blood Sport
Quest description from https://www.youtube.com/watch?v=tuRSdC_mlO4
"""
QUEST_EVENT_BLOOD_SPORT = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -1404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -3404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -5404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -4404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -2404.5,'pos_y': -4038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61008,
        'name': "Blood Sport",
        'client': "Spoiled Princess",
        'description':
            "Hunt an Uragaan\n"
            "and a Diablos",
        'details':
            "Oh, boo! I'm tired of watching\n"
            "run-of-the-mill hunts. The\n"
            "Diablos and the Uragaan are\n"
            "supposed to be the ultimate\n"
            "monster duo. I'd love to watch\n"
            "them maim some foolish hunter!\n"
            "Do put on a good show...",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 6000,
        'quest_fee': 1750,
        'time_limit': 50,
        'main_monster_1': Monster.uragaan,
        'main_monster_2': Monster.diablos,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_18_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001D,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x1D,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.diablos,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x1D,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 17600,
            'hrp_reward': 1760,
            'rewards_row_1': [
                (ItemsType.uragaan_scale, 1, 1),
                (ItemsType.diablos_ridge, 1, 14),
                (ItemsType.uragaan_shell, 1, 10),
                (ItemsType.diablos_shell, 1, 20),
                (ItemsType.twisted_horn, 1, 12),
                (ItemsType.diablos_marrow, 8, 9),
                (ItemsType.uragaan_marrow, 1, 9),
                (ItemsType.incomplete_plans, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.uragaan_scale, 1, 1),
                (ItemsType.diablos_ridge, 1, 14),
                (ItemsType.uragaan_shell, 1, 10),
                (ItemsType.diablos_shell, 1, 20),
                (ItemsType.twisted_horn, 1, 12),
                (ItemsType.diablos_marrow, 1, 9),
                (ItemsType.uragaan_marrow, 1, 9),
                (ItemsType.incomplete_plans, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.diablos,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 9: Alluring Dress
Quest description from https://www.youtube.com/watch?v=afN7ThaN3Vg&t=18s
    thanks to Goabie
"""
QUEST_EVENT_ALLURING_DRESS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },

            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -100.5,'pos_y': -3038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -91,'rot_z': 0,
            # },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -1200.5,'pos_y': -2538.5,'pos_z': -1042.7,
                'rot_x': 0,'rot_y': -1,'rot_z': 0,
            },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -300.5,'pos_y': -2038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -1538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -161,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -400.5,'pos_y': -1038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -11,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -400.5,'pos_y': -38.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },

            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -100.5,'pos_y': -3038.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -91,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1200.5,'pos_y': -2538.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -300.5,'pos_y': -2038.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -1400.5,'pos_y': -1538.5,'pos_z': -0042.7,
                'rot_x': 0,'rot_y': -161,'rot_z': 0,
            },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -400.5,'pos_y': -1038.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -538.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -11,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -400.5,'pos_y': -38.5,'pos_z': -0042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },

            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -100.5,'pos_y': -3038.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -91,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1200.5,'pos_y': -2538.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -300.5,'pos_y': -2038.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -1538.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -161,'rot_z': 0,
            # },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -400.5,'pos_y': -1038.5,'pos_z': -2042.7,
                'rot_x': 0,'rot_y': -21,'rot_z': 0,
            },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -538.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -11,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -400.5,'pos_y': -38.5,'pos_z': -2042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },

            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1100.5,'pos_y': -3038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -91,'rot_z': 0,
            # },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -2200.5,'pos_y': -2538.5,'pos_z': -1042.7,
                'rot_x': 0,'rot_y': -1,'rot_z': 0,
            },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1300.5,'pos_y': -2038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -2400.5,'pos_y': -1538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -161,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -1038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -2400.5,'pos_y': -538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -11,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': -1400.5,'pos_y': -38.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },

            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 1100.5,'pos_y': -3038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -91,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 2200.5,'pos_y': -2538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 1300.5,'pos_y': -2038.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -21,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 2400.5,'pos_y': -1538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -161,'rot_z': 0,
            # },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': 1400.5,'pos_y': -1038.5,'pos_z': -1042.7,
                'rot_x': 0,'rot_y': -21,'rot_z': 0,
            },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 2400.5,'pos_y': -538.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -11,'rot_z': 0,
            # },
            # {
            #     'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
            #     'variant': 0,'room': 1,'quantity': -1,
            #     'pos_x': 1400.5,'pos_y': -38.5,'pos_z': -1042.7,
            #     'rot_x': 0,'rot_y': -1,'rot_z': 0,
            # },
        ],
    ],
    'quest_info': {
        'quest_id': 61009,
        'name': "Alluring Dress",
        'client': "Elder Princess",
        'description':
            "Hunt 30 Sharq",
        'details':
            "My sister's interest in\n"
            "monsters is beginning to\n"
            "become scandalous! She simply\n"
            "must find a husband --\n"
            "hopefully at the next ball. We\n"
            "need enough Sharqskin for her\n"
            "dress, so please slay 30 fish!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),  # (1, 1, 1, 0, 1, 1, 1, 1)
            (1, 0, 0, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 1500,
        'quest_fee': 400,
        'time_limit': 50,
        'main_monster_1': Monster.fish,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NO_ARMOR,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 48,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001D,
        'summon': 0x6401010C,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.fish,
            'objective_num': 0x1E,
            'zenny_reward': 4000,
            'hrp_reward': 120,
            'rewards_row_1': [
                (ItemsType.armor_stone, 1, 1),
                (ItemsType.immunizer, 1, 5),
                (ItemsType.sharpened_fang, 1, 16),
                (ItemsType.sharqskin, 1, 24),
                (ItemsType.raw_meat, 2, 12),
                (ItemsType.armor_sphere_plus, 1, 12),
                (ItemsType.adv_armor_sphere, 1, 5),
                (ItemsType.sharq_ticket, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.armor_stone, 1, 1),
                (ItemsType.immunizer, 1, 5),
                (ItemsType.sharpened_fang, 1, 16),
                (ItemsType.sharqskin, 1, 24),
                (ItemsType.raw_meat, 2, 12),
                (ItemsType.armor_sphere_plus, 1, 12),
                (ItemsType.adv_armor_sphere, 1, 5),
                (ItemsType.sharq_ticket, 1, 25)
            ],
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
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000003,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}

"""
EVENT QUEST 10: Gobuled Everything in Sight
Quest description from https://www.youtube.com/watch?v=2_4o2zaKM8M
    thanks to "kazuma_6969"
"""
QUEST_EVENT_GOBULED_EVERYTHING_IN_SIGHT = {
    'quest_info': {
        'quest_id': 61010,
        'name': "Gobuled Everything in Sight",
        'client': "Argosy Captain",
        'description': "Hunt a Gobul",
        'details':
            "Taihen! My small ships all\n"
            "gobbled by huge Gobul! The\n"
            "crew all escaped, but goods\n"
            "are in fish's stomach, yes --\n"
            "even some are super-rare items\n"
            "there! Only hunters can get my\n"
            "items back. Onegai!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 1900,
        'quest_fee': 550,
        'time_limit': 50,
        'main_monster_1': Monster.ludroth,
        'main_monster_2': Monster.kelbi,
        'location': LocationType.QUEST_LOCATION_FLOODED_FOR,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_18_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 25,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0020,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_ff_free_for_all.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.gobul,
            'starting_area': 0x00,  # 4 -> area 1  # 3 -> area 1  # 2 -> basecamp? # 1 -> area 3 # 0 -> area 4
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x20,  # 0x01 through 0x3c
            'size': 0x96,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.gobul,
            'objective_num': 0x01,
            'zenny_reward': 5600,
            'hrp_reward': 1230,
            'rewards_row_1': [
                (ItemsType.rustshard, 1, 15),
                (ItemsType.gobul_fin, 1, 13),
                (ItemsType.gobul_spike, 1, 15),
                (ItemsType.mystery_charm, 1, 25),
                (ItemsType.gobul_whisker, 1, 12),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.gobul_lantern, 1, 10)
            ],
            'rewards_row_2': [
                (ItemsType.rustshard, 1, 15),
                (ItemsType.gobul_fin, 1, 13),
                (ItemsType.gobul_spike, 1, 15),
                (ItemsType.mystery_charm, 1, 25),
                (ItemsType.gobul_whisker, 1, 12),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.gobul_lantern, 1, 10)
            ],
        },
        'subquest_1': {
            'description': "Destroy Gobul's lantern",
            'type': 0x00000204,
            'objective_type': Monster.gobul,
            'objective_num': 0x01,
            'zenny_reward': 800,
            'hrp_reward': 100,
            'rewards_row_1': [
                (ItemsType.gobul_fin, 1, 10),
                (ItemsType.gobul_spike, 1, 24),
                (ItemsType.gobul_hide, 1, 20),
                (ItemsType.paralysis_sac, 1, 28),
                (ItemsType.monster_bone_l, 1, 18)
            ],
        },
        'subquest_2': {
            'description': "Fish out Gobul once",
            'type': 0x00001000,
            'objective_type': Monster.gobul,
            'objective_num': 0x02,
            'zenny_reward': 1200,
            'hrp_reward': 60,
            'rewards_row_1': [
                (ItemsType.gobul_fin, 1, 10),
                (ItemsType.gobul_spike, 1, 24),
                (ItemsType.gobul_hide, 1, 20),
                (ItemsType.paralysis_sac, 1, 28),
                (ItemsType.monster_bone_l, 1, 18)
            ],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 11: Poached Wyvern Eggs
Quest description from https://www.youtube.com/watch?v=1GuwMhI6Xy8
    Thanks to "kazuma_6969"
"""
QUEST_EVENT_POACHED_WYVERN_EGGS = {
    'small_monsters': [
        # ----- WAVE 1 -----
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': 1,
                'pos_x': -5057.57,'pos_y': -2.26,'pos_z': -5940.68,
                'rot_x': 0,'rot_y': -68,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': 1,
                'pos_x': -4811.71,'pos_y': -66.91,'pos_z': -6502.93,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
        ],
        [
            # Area 2 (Area 3 in Deserted Island)
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': 3,
                'pos_x': -6654.10,'pos_y': 23.12,'pos_z': 117.64,
                'rot_x': 0,'rot_y': 455,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -4409.86,'pos_y': 160.61,'pos_z': 3585.26,
                'rot_x': 0,'rot_y': -164,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -2714.98,'pos_y': 150.44,'pos_z': 2758.35,
                'rot_x': 0,'rot_y': -244,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -3714.37,'pos_y': 77.64,'pos_z': 2717.77,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
        ],
        [
            # Area 3 (Area 2 in Deserted Island)
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 4,
                'pos_x': 2690.34,'pos_y': 20.00,'pos_z': -843.30,
                'rot_x': 0,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': 3,
                'pos_x': 1508.85,'pos_y': 0.71,'pos_z': 933.94,
                'rot_x': 0,'rot_y': 250,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': 948.50,'pos_y': -19.00,'pos_z': -894.84,
                'rot_x': 0,'rot_y': -307,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': 2,
                'pos_x': -671.47,'pos_y': -14.07,'pos_z': 468.25,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
        [
            # Area 4 (Area 7 in Deserted Island)
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': -877.96,'pos_y': 2.00,'pos_z': 1397.25,
                'rot_x': 0,'rot_y': -125,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': 5,
                'pos_x': -1213.07,'pos_y': 2.00,'pos_z': 704.80,
                'rot_x': 0,'rot_y': 312,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': -1976.37,'pos_y': 2.00,'pos_z': 1759.45,
                'rot_x': 0,'rot_y': -301,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': 2,
                'pos_x': -2320.33,'pos_y': 2.00,'pos_z': 2294.16,
                'rot_x': 0,'rot_y': 119,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': -1,
                'pos_x': -5671.42,'pos_y': 466.03,'pos_z': 3073.44,
                'rot_x': 273,'rot_y': 304,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 3,
                'pos_x': -442.09,'pos_y': 16.00,'pos_z': 734.60,
                'rot_x': 0,'rot_y': 119,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': -1122.44,'pos_y': 16.00,'pos_z': 548.27,
                'rot_x': 0,'rot_y': 182,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': -1077.87,'pos_y': 16.00,'pos_z': 1238.55,
                'rot_x': 0,'rot_y': 307,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 1,
                'pos_x': -573.41,'pos_y': 16.00,'pos_z': 1474.43,
                'rot_x': 0,'rot_y': 392,'rot_z': 0,
            },
        ],
        [
            # Area 6
        ],
        [
            # Area 7 (Area 11 in Deserted Island)
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 4,
                'pos_x': 2237.04,'pos_y': -1090.00,'pos_z': 1586.48,
                'rot_x': 0,'rot_y': 96,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 2469.26,'pos_y': -1330.00,'pos_z': 2832.58,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 1103.05,'pos_y': -2050.00,'pos_z': -1429.32,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': -3054.79,'pos_y': -3047.85,'pos_z': 3126.22,
                'rot_x': 0,'rot_y': -62,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': 1268.03,'pos_y': -2470.00,'pos_z': -557.22,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 1742.13,'pos_y': -3820.00,'pos_z': -1993.49,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 1732.89,'pos_y': -3580.00,'pos_z': -4462.32,
                'rot_x': 0,'rot_y': -278,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 12 in the Deserted Island)
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': 80.95,'pos_y': 35.81,'pos_z': -523.41,
                'rot_x': 0,'rot_y': -420,'rot_z': 0,
            },
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1342.36,'pos_y': -18.00,'pos_z': 465.56,
                'rot_x': 0,'rot_y': -324,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 6 in the Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 965.46,'pos_y': 27.06,'pos_z': 892.53,
                'rot_x': 0,'rot_y': 563,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 732.00,'pos_y': 24.88,'pos_z': 1123.58,
                'rot_x': 0,'rot_y': 637,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 6,
                'pos_x': 962.01,'pos_y': 19.44,'pos_z': -149.63,
                'rot_x': 0,'rot_y': 540,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 4,
                'pos_x': 220.21,'pos_y': 20.45,'pos_z': -417.64,
                'rot_x': 0,'rot_y': 557,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': -439.60,'pos_y': 13.03,'pos_z': 98.15,
                'rot_x': 0,'rot_y': 631,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 1,
                'pos_x': -237.23,'pos_y': 2.00,'pos_z': 803.55,
                'rot_x': 0,'rot_y': 648,'rot_z': 0,
            },
        ],
        [
            # Area 10 (Area 8 in the Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 2,
                'pos_x': -2085.64,'pos_y': -283.99,'pos_z': 1193.70,
                'rot_x': 0,'rot_y': -204,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 1,
                'pos_x': -2525.41,'pos_y': -190.61,'pos_z': -207.68,
                'rot_x': 0,'rot_y': -51,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 1,
                'pos_x': -2950.76,'pos_y': -249.78,'pos_z': 505.61,
                'rot_x': 0,'rot_y': 204,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 2,
                'pos_x': -1914.32,'pos_y': -281.12,'pos_z': 889.95,
                'rot_x': 0,'rot_y': 329,'rot_z': 0,
            },
        ],
        [
            # Area 11 (Area 4 in the Deserted Island)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 2,
                'pos_x': -453.62,'pos_y': 705.50,'pos_z': 2253.55,
                'rot_x': 0,'rot_y': -5,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 4,
                'pos_x': 142.14,'pos_y': 336.98,'pos_z': 3677.44,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4363.26,'pos_y': 426.27,'pos_z': 5818.19,
                'rot_x': 0,'rot_y': 171,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4782.14,'pos_y': 426.27,'pos_z': 5556.53,
                'rot_x': 0,'rot_y': 164,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4617.08,'pos_y': 426.27,'pos_z': 6208.15,
                'rot_x': 0,'rot_y': 284,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 5099.46,'pos_y': 426.27,'pos_z': 5456.15,
                'rot_x': 0,'rot_y': 161,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 4,
                'pos_x': 2767.15,'pos_y': 611.59,'pos_z': 4297.09,
                'rot_x': 0,'rot_y': -301,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2793.18,'pos_y': 1205.81,'pos_z': 5908.79,
                'rot_x': 0,'rot_y': -295,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': 3210.49,'pos_y': 845.81,'pos_z': 5369.26,
                'rot_x': 0,'rot_y': -398,'rot_z': 0,
            },
        ],
        [
            # Area 12 (Area 10 in the Deserted Island)
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': 572.89,'pos_y': -618.12,'pos_z': -2648.11,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -501.62,'pos_y': -210.00,'pos_z': -3356.64,
                'rot_x': 0,'rot_y': 45,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -1624.63,'pos_y': -888.12,'pos_z': -2880.06,
                'rot_x': 0,'rot_y': 113,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2352.88,'pos_y': -523.55,'pos_z': -7478.20,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -1957.86,'pos_y': -1228.41,'pos_z': -7734.46,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2821.80,'pos_y': -988.41,'pos_z': -8174.07,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2435.99,'pos_y': -988.41,'pos_z': -7780.24,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
        ],
        # ----- WAVE 2 -----
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': 1,
                'pos_x': -5057.57,'pos_y': -2.26,'pos_z': -5940.68,
                'rot_x': 0,'rot_y': -68,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': 1,
                'pos_x': -4811.71,'pos_y': -66.91,'pos_z': -6502.93,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
        ],
        [
            # Area 2 (Area 3 in Deserted Island)
            {
                'type': Monster.melynx,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': -6114.99,'pos_y': 1.01,'pos_z': -305.99,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 2,
                'pos_x': -5573.24,'pos_y': 28.24,'pos_z': 89.46,
                'rot_x': 0,'rot_y': 62,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 2,
                'pos_x': -5266.61,'pos_y': 18.27,'pos_z': -366.28,
                'rot_x': 0,'rot_y': 324,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': -4974.18,'pos_y': 24.04,'pos_z': 118.41,
                'rot_x': 0,'rot_y': 39,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -4409.86,'pos_y': 160.61,'pos_z': 3585.26,
                'rot_x': 0,'rot_y': -164,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -2714.98,'pos_y': 150.44,'pos_z': 2758.35,
                'rot_x': 0,'rot_y': -244,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 2,'quantity': 1,
                'pos_x': -3714.37,'pos_y': 77.64,'pos_z': 2717.77,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
        ],
        [
            # Area 3 (Area 2 in Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 4,
                'pos_x': -2866.17,'pos_y': 4.00,'pos_z': 207.60,
                'rot_x': 0,'rot_y': -22,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': -3281.49,'pos_y': 5.72,'pos_z': 1054.53,
                'rot_x': 0,'rot_y': -119,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': -2077.49,'pos_y': -0.82,'pos_z': 614.59,
                'rot_x': 0,'rot_y': -113,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 3,
                'pos_x': 1844.04,'pos_y': 13.37,'pos_z': -1285.39,
                'rot_x': 0,'rot_y': 238,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 1,
                'pos_x': 2591.03,'pos_y': -11.64,'pos_z': -1490.38,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
        [
            # Area 4 (Area 7 in Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 4,
                'pos_x': -3806.09,'pos_y': 2.00,'pos_z': 1899.19,
                'rot_x': 0,'rot_y': 324,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 2,
                'pos_x': -2228.14,'pos_y': 2.00,'pos_z': 2084.72,
                'rot_x': 0,'rot_y': 278,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 2,
                'pos_x': -3075.68,'pos_y': 2.00,'pos_z': 2687.36,
                'rot_x': 0,'rot_y': 244,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': -4162.06,'pos_y': 2.00,'pos_z': 2924.56,
                'rot_x': 0,'rot_y': 221,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': -1,
                'pos_x': -5671.42,'pos_y': 466.03,'pos_z': 3073.44,
                'rot_x': 273,'rot_y': 304,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 6,
                'pos_x': -2138.97,'pos_y': 18.00,'pos_z': -355.64,
                'rot_x': 0,'rot_y': 432,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 4,
                'pos_x': -1641.20,'pos_y': 17.36,'pos_z': -875.79,
                'rot_x': 0,'rot_y': 472,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': -1951.09,'pos_y': 18.00,'pos_z': -1441.74,
                'rot_x': 0,'rot_y': 506,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 1,
                'pos_x': -2578.55,'pos_y': 25.21,'pos_z': -1423.47,
                'rot_x': 0,'rot_y': 540,'rot_z': 0,
            },
        ],
        [
            # Area 6
        ],
        [
            # Area 7 (Area 11 in Deserted Island)
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 4,
                'pos_x': 2237.04,'pos_y': -1090.00,'pos_z': 1586.48,
                'rot_x': 0,'rot_y': 96,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 2469.26,'pos_y': -1330.00,'pos_z': 2832.58,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 1103.05,'pos_y': -2050.00,'pos_z': -1429.32,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': -3054.79,'pos_y': -3047.85,'pos_z': 3126.22,
                'rot_x': 0,'rot_y': -62,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': 1268.03,'pos_y': -2470.00,'pos_z': -557.22,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 1742.13,'pos_y': -3820.00,'pos_z': -1993.49,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 1732.89,'pos_y': -3580.00,'pos_z': -4462.32,
                'rot_x': 0,'rot_y': -278,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 12 in the Deserted Island)
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': 80.95,'pos_y': 35.81,'pos_z': -523.41,
                'rot_x': 0,'rot_y': -420,'rot_z': 0,
            },
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1342.36,'pos_y': -18.00,'pos_z': 465.56,
                'rot_x': 0,'rot_y': -324,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 6 in the Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 965.46,'pos_y': 27.06,'pos_z': 892.53,
                'rot_x': 0,'rot_y': 563,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 732.00,'pos_y': 24.88,'pos_z': 1123.58,
                'rot_x': 0,'rot_y': 637,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 9,'quantity': 6,
                'pos_x': -2618.42,'pos_y': 168.02,'pos_z': -385.05,
                'rot_x': 0,'rot_y': 625,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 3,
                'pos_x': -3005.70,'pos_y': 19.00,'pos_z': 276.54,
                'rot_x': 0,'rot_y': 961,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': -659.60,'pos_y': 21.89,'pos_z': -1327.15,
                'rot_x': 0,'rot_y': 369,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 1,
                'pos_x': -549.09,'pos_y': 15.82,'pos_z': -103.05,
                'rot_x': 0,'rot_y': -79,'rot_z': 0,
            },
        ],
        [
            # Area 10 (Area 8 in the Deserted Island)
        ],
        [
            # Area 11 (Area 4 in the Deserted Island)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 2,
                'pos_x': -453.62,'pos_y': 705.50,'pos_z': 2253.55,
                'rot_x': 0,'rot_y': -5,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 4,
                'pos_x': 142.14,'pos_y': 336.98,'pos_z': 3677.44,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4363.26,'pos_y': 426.27,'pos_z': 5818.19,
                'rot_x': 0,'rot_y': 171,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4782.14,'pos_y': 426.27,'pos_z': 5556.53,
                'rot_x': 0,'rot_y': 164,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4617.08,'pos_y': 426.27,'pos_z': 6208.15,
                'rot_x': 0,'rot_y': 284,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 5099.46,'pos_y': 426.27,'pos_z': 5456.15,
                'rot_x': 0,'rot_y': 161,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 4,
                'pos_x': 2767.15,'pos_y': 611.59,'pos_z': 4297.09,
                'rot_x': 0,'rot_y': -301,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2793.18,'pos_y': 1205.81,'pos_z': 5908.79,
                'rot_x': 0,'rot_y': -295,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': 3210.49,'pos_y': 845.81,'pos_z': 5369.26,
                'rot_x': 0,'rot_y': -398,'rot_z': 0,
            },
        ],
        [
            # Area 12 (Area 10 in the Deserted Island)
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': 572.89,'pos_y': -618.12,'pos_z': -2648.11,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -501.62,'pos_y': -210.00,'pos_z': -3356.64,
                'rot_x': 0,'rot_y': 45,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -1624.63,'pos_y': -888.12,'pos_z': -2880.06,
                'rot_x': 0,'rot_y': 113,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2352.88,'pos_y': -523.55,'pos_z': -7478.20,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -1957.86,'pos_y': -1228.41,'pos_z': -7734.46,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2821.80,'pos_y': -988.41,'pos_z': -8174.07,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2435.99,'pos_y': -988.41,'pos_z': -7780.24,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61011,
        'name': "Poached Wyvern Eggs",
        'client': "The Lady Gourmet",
        'description': "Deliver 9 Wyvern Eggs",
        'details':
            "Why, hellooo! I mean to hold\n"
            "a dinner party, but I've\n"
            "discovered the most dreadful\n"
            "news -- I don't have enough\n"
            "eggs for my recipe! I simply\n"
            "mustn't disappoint my guests,\n"
            "so please save this supper!",
        'success_message':
            "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 10000,
        'quest_fee': 1200,
        'time_limit': 15,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_D_ISLAND,
        'quest_rank': QuestRankType.star_4,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 31,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x002A,
        'summon': 0x64010129,  # 28 (0x1C) or 41 (0x29)
        'wave_1_transition_type': WaveType.item,
        'wave_1_transition_target': ItemsType.wyvern_eg,
        'wave_1_transition_quantity': 0x0001,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000002,
            'objective_type': ItemsType.wyvern_eg,
            'objective_num': 0x09,
            'zenny_reward': 30000,
            'hrp_reward': 400,
            'rewards_row_1': [
                (ItemsType.commendation, 1, 5),
                (ItemsType.rustshard, 1, 15),
                (ItemsType.ancient_shard, 2, 10),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.golden_eg, 1, 8),
                (ItemsType.silver_eg, 1, 18),
                (ItemsType.steel_eg, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.commendation, 1, 5),
                (ItemsType.rustshard, 1, 15),
                (ItemsType.ancient_shard, 2, 10),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.golden_eg, 1, 8),
                (ItemsType.silver_eg, 1, 18),
                (ItemsType.steel_eg, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "Deliver 2 Wyvern Tears",
            'type': 0x00000002,
            'objective_type': ItemsType.wyvern_tear,
            'objective_num': 0x02,
            'zenny_reward': 3200,
            'hrp_reward': 80,
            'rewards_row_1': [
                (ItemsType.commendation, 1, 5),
                (ItemsType.rustshard, 1, 15),
                (ItemsType.ancient_shard, 2, 10),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.golden_eg, 1, 8),
                (ItemsType.silver_eg, 1, 18),
                (ItemsType.steel_eg, 1, 25)
            ],
        },
        'subquest_2': {
            'description': "Sever Rathian's Tail",
            'type': 0x00000204,
            'objective_type': Monster.rathian,
            'objective_num': 0x01,
            'zenny_reward': 1200,
            'hrp_reward': 80,
            'rewards_row_1': [
                (ItemsType.commendation, 1, 5),
                (ItemsType.rustshard, 1, 15),
                (ItemsType.ancient_shard, 2, 10),
                (ItemsType.mystery_charm, 1, 14),
                (ItemsType.shining_charm, 1, 5),
                (ItemsType.golden_eg, 1, 8),
                (ItemsType.silver_eg, 1, 18),
                (ItemsType.steel_eg, 1, 25)
            ],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000003,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 12: Speak of the Deviljho
Quest description from https://youtu.be/Py5PkCXhf6w&t=681
"""
QUEST_EVENT_SPEAK_OF_THE_DEVILJHO = {
    'quest_info': {
        'quest_id': 61012,
        'name': "Speak of the Deviljho",
        'client': "Eccentric Aristocrat",
        'description': "Capture a Deviljho",
        'details':
            "Some wyvern named Deviljho has\n"
            "Loc Lac hunters fouling their\n"
            "armor. I hear it has a taste\n"
            "for captured animals. I simply\n"
            "must have one! What will I do\n"
            "with it? That's for me to know\n"
            "and you to NEVER find out!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 7500,
        'quest_fee': 1800,
        'time_limit': 50,
        'main_monster_1': Monster.fish,
        'main_monster_2': Monster.altaroth,
        'location': LocationType.QUEST_LOCATION_FLOODED_FOR,
        'quest_rank': QuestRankType.star_4,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 18,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x0040,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_ff_free_for_all.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.deviljho,
            'starting_area': 0x00,  # 4 -> area 1  # 3 -> area 1  # 2 -> basecamp? # 1 -> area 3 # 0 -> area 4
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x34,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000081,
            'objective_type': Monster.deviljho,
            'objective_num': 0x01,
            'zenny_reward': 22000,
            'hrp_reward': 1820,
            'rewards_row_1': [
                (ItemsType.hrd_armor_sphere, 1, 3),
                (ItemsType.deviljho_talon, 1, 16),
                (ItemsType.deviljho_scale, 1, 23),
                (ItemsType.deviljho_hide, 1, 20),
                (ItemsType.deviljho_fang, 1, 10),
                (ItemsType.deviljho_gem, 1, 3),
                (ItemsType.lion_kings_seal, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.hrd_armor_sphere, 1, 3),
                (ItemsType.deviljho_talon, 1, 16),
                (ItemsType.deviljho_scale, 1, 23),
                (ItemsType.deviljho_hide, 1, 20),
                (ItemsType.deviljho_fang, 1, 10),
                (ItemsType.deviljho_gem, 1, 3),
                (ItemsType.lion_kings_seal, 1, 25)
            ],
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
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 13: Marine Warfare
Quest description from https://www.youtube.com/watch?v=Gdl8A1AkXU4
    Thanks to kazuma_6969
"""
QUEST_EVENT_MARINE_WARFARE = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61013,
        'name': "Marine Warfare",
        'client': "Guild Weapons Development",
        'description':
            "Hunt 2 Gobul\n"
            "",
        'details':
            "Seeking hunters to aid in the\n"
            "development of underwater\n"
            "weaponry by hunting aquatic\n"
            "monsters. The Guild will\n"
            "provide the venue and the\n"
            "monster, but applicants should\n"
            "have their own equipment.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 5600,
        'quest_fee': 1650,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_4,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 48,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0036,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.gobul,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x36,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.gobul,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x36,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.gobul,
            'objective_num': 0x02,
            'zenny_reward': 16800,
            'hrp_reward': 1480,
            'rewards_row_1': [
                (ItemsType.hrd_armor_sphere, 1, 8),
                (ItemsType.gobul_fin_plus, 1, 15),
                (ItemsType.gobul_spike_plus, 1, 24),
                (ItemsType.gobul_hide_plus, 1, 20),
                (ItemsType.paralysis_sac, 1, 8),
                (ItemsType.gourmet_voucher, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.mystery_charm, 1, 16),
                (ItemsType.timeworn_charm, 1, 3),
                (ItemsType.monster_bone_m, 2, 23),
                (ItemsType.monster_bone_s, 3, 20),
                (ItemsType.bone_husk_l, 10, 14),
                (ItemsType.bone_husk_s, 18, 14)
            ],
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
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 14: Double Diablos
Quest description from https://www.youtube.com/watch?v=l-mqoeORTi8
    Thanks to kazuma_6969
"""
QUEST_EVENT_DOUBLE_DIABLOS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61014,
        'name': "Double Diablos",
        'client': "Passionate Hunter",
        'description': "Capture 2 Diablos",
        'details':
            "One Diablos would dismember\n"
            "your average weekend warrior,\n"
            "but two Diablos!? Only true\n"
            "hunters need apply for this\n"
            "Quest. Plan your tactics well,\n"
            "and perhaps we can compare\n"
            "notes later... if you survive.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),  # (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0, 1, 1)  # (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 12800,
        'quest_fee': 2600,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_40_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x003B,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.diablos,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x3B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0A
        },
        'monster_2': {
            'type': Monster.diablos,
            'starting_area': 0x01,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x3B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0B
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000081,
            'objective_type': Monster.diablos,
            'objective_num': 0x02,
            'zenny_reward': 38400,
            'hrp_reward': 1920,
            'rewards_row_1': [
                (ItemsType.hrd_armor_sphere, 1, 1),
                (ItemsType.diablos_ridge, 1, 11),
                (ItemsType.diablos_carapace, 1, 20),
                (ItemsType.diablos_fang, 1, 18),
                (ItemsType.monster_bone_plus, 1, 8),
                (ItemsType.diablos_marrow, 1, 7),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.soulhunter_tag, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.hrd_armor_sphere, 1, 1),
                (ItemsType.diablos_ridge, 1, 11),
                (ItemsType.diablos_carapace, 1, 20),
                (ItemsType.diablos_fang, 1, 18),
                (ItemsType.monster_bone_plus, 1, 8),
                (ItemsType.diablos_marrow, 1, 7),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.soulhunter_tag, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 15: Hot Deal
Quest description from https://www.youtube.com/watch?v=8X4P35Y8p60
    thanks to "kazuma_6969"
"""
QUEST_EVENT_HOT_DEAL = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 2,
                'pos_x': -494.25,'pos_y': 47.01,'pos_z': -947.91,
                'rot_x': 0,'rot_y': 112147,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': -1361.42,'pos_y': 20.60,'pos_z': -712.51,
                'rot_x': 0,'rot_y': 79456,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': 1,
                'pos_x': 1031.98,'pos_y': 26.73,'pos_z': -1406.32,
                'rot_x': 0,'rot_y': 152977,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 4,
                'pos_x': 3139.21,'pos_y': -16.41,'pos_z': 1809.58,
                'rot_x': 0,'rot_y': 14105,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': 2598.00,'pos_y': 64.57,'pos_z': 2280.01,
                'rot_x': 0,'rot_y': 14478,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 2,
                'pos_x': 2184.05,'pos_y': 66.73,'pos_z': 2453.70,
                'rot_x': 0,'rot_y': 11582,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': 2741.80,'pos_y': -53.82,'pos_z': 1680.05,
                'rot_x': 0,'rot_y': 14128,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 6982.80,'pos_y': 73.73,'pos_z': 4494.92,
                'rot_x': 0,'rot_y': 5856,'rot_z': 0,
            },
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': -1,
                'pos_x': 7778.32,'pos_y': 66.41,'pos_z': 4957.68,
                'rot_x': 0,'rot_y': 2872,'rot_z': 0,
            },
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': -1,
                'pos_x': 8087.79,'pos_y': 83.54,'pos_z': 5160.52,
                'rot_x': 0,'rot_y': 5774,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': -1,
                'pos_x': 8676.94,'pos_y': 515.74,'pos_z': 2473.30,
                'rot_x': 273,'rot_y': 6351,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.rhenoplos,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 672.08,'pos_y': 25.43,'pos_z': 639.95,
                'rot_x': 0,'rot_y': 2264,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 0,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': -1151.12,'pos_y': -43.31,'pos_z': 2402.83,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 3,
                'pos_x': 1580.62,'pos_y': 129.42,'pos_z': 3042.75,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 2,
                'pos_x': 1743.00,'pos_y': 339.42,'pos_z': 2633.18,
                'rot_x': 0,'rot_y': 91,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 1303.26,'pos_y': 189.42,'pos_z': 2724.68,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': -1485.68,'pos_y': 36.65,'pos_z': 104.92,
                'rot_x': 0,'rot_y': 3032,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': 897.01,'pos_y': 25.14,'pos_z': -27.96,
                'rot_x': 0,'rot_y': 56,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': 2948.85,'pos_y': 7.51,'pos_z': 1861.15,
                'rot_x': 0,'rot_y': 20656,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -775.56,'pos_y': 73.07,'pos_z': 542.20,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -3498.99,'pos_y': 67.50,'pos_z': -1218.55,
                'rot_x': 0,'rot_y': 4835,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 486.74,'pos_y': 38.66,'pos_z': -422.06,
                'rot_x': 0,'rot_y': 1331,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 2864.76,'pos_y': 49.34,'pos_z': -1059.79,
                'rot_x': 0,'rot_y': 7296,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 1202.49,'pos_y': 57.63,'pos_z': -1571.42,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -1733.55,'pos_y': 56.88,'pos_z': -1510.18,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 6
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': 393.15,'pos_y': -35.75,'pos_z': 1076.53,
                'rot_x': 0,'rot_y': -85,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': -1170.83,'pos_y': -30.77,'pos_z': 447.51,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': 1020.10,'pos_y': 4.72,'pos_z': -202.83,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': -435.28,'pos_y': -28.37,'pos_z': -1280.39,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 7
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 7,'quantity': 3,
                'pos_x': 95.05,'pos_y': -6.35,'pos_z': 228.22,
                'rot_x': 0,'rot_y': 1399,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': -2114.33,'pos_y': 17.37,'pos_z': 268.38,
                'rot_x': 0,'rot_y': 19692,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 7,'quantity': 1,
                'pos_x': -1877.72,'pos_y': -22.42,'pos_z': 1532.47,
                'rot_x': 0,'rot_y': 32312,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 7,'quantity': 1,
                'pos_x': 625.43,'pos_y': 3.37,'pos_z': -496.28,
                'rot_x': 0,'rot_y': 6283,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': -1447.72,'pos_y': 21.43,'pos_z': 61.89,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': 316.55,'pos_y': -3.36,'pos_z': -1209.27,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': 1008.65,'pos_y': -9.18,'pos_z': 1099.80,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 4,
                'pos_x': 728.75,'pos_y': -19.44,'pos_z': 1581.60,
                'rot_x': 0,'rot_y': 1581.60,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 3,
                'pos_x': -375.43,'pos_y': 6.66,'pos_z': 301.92,
                'rot_x': 0,'rot_y': 40860,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': 479.45,'pos_y': 30.53,'pos_z': -50.40,
                'rot_x': 0,'rot_y': 59178,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': 2190.05,'pos_y': -6.53,'pos_z': 1552.73,
                'rot_x': 0,'rot_y': 24814,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 9,'quantity': 2,
                'pos_x': 1226.78,'pos_y': 14.44,'pos_z': -971.03,
                'rot_x': 0,'rot_y': 49126,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': 3,
                'pos_x': 30.91,'pos_y': 11.00,'pos_z': -556.52,
                'rot_x': 0,'rot_y': 19871,'rot_z': 0,
            },
        ],
        [
            # Area 10
        ],
    ],
    'quest_info': {
        'quest_id': 61015,
        'name': "Hot Deal",
        'client': "Shady Merchant",
        'description': "Hunt 2 Agnaktor",
        'details':
            "A coupla Agnaktor are meltin'\n"
            "my profits on the Volcano,\n"
            "see? Deal with 'em, and I'll\n"
            "give you a weapon recipe I...\n"
            "acquired. They say this\n"
            "armament can bring wealth,\n"
            "or a mysterious death...",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 5000,
        'quest_fee': 2750,
        'time_limit': 50,
        'main_monster_1': Monster.uroktor,
        'main_monster_2': Monster.rhenoplos,
        'location': LocationType.QUEST_LOCATION_VOLCANO,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_40_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 27,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x39,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.agnaktor,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x02,
            'level': 0x39,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.agnaktor,
            'objective_num': 0x02,
            'zenny_reward': 13800,
            'hrp_reward': 1240,
            'rewards_row_1': [
                (ItemsType.agnaktorcarapace, 1, 8),
                (ItemsType.agnaktor_scale, 1, 18),
                (ItemsType.agnaktor_hide_plus, 1, 20),
                (ItemsType.monster_bone_plus, 1, 12),
                (ItemsType.firecell_stone, 1, 5),
                (ItemsType.agnaktor_fin_plus, 15, 12),
                (ItemsType.smiths_notebook, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.agnaktorcarapace, 1, 8),
                (ItemsType.agnaktor_scale, 1, 18),
                (ItemsType.agnaktor_hide_plus, 1, 20),
                (ItemsType.monster_bone_plus, 1, 12),
                (ItemsType.firecell_stone, 1, 5),
                (ItemsType.agnaktor_fin_plus, 15, 12),
                (ItemsType.smiths_notebook, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "Hunt an Agnaktor",
            'type': 0x00000001,
            'objective_type': Monster.agnaktor,
            'objective_num': 0x01,
            'zenny_reward': 13800,
            'hrp_reward': 1240,
            'rewards_row_1': [
                (ItemsType.agnaktorcarapace, 1, 8),
                (ItemsType.agnaktor_scale, 1, 18),
                (ItemsType.agnaktor_hide_plus, 1, 20),
                (ItemsType.monster_bone_plus, 1, 12),
                (ItemsType.firecell_stone, 1, 5),
                (ItemsType.agnaktor_fin_plus, 15, 12),
                (ItemsType.smiths_notebook, 1, 25)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 16: Sea Power
Quest description from https://www.youtube.com/watch?v=oQL3NtB_GMM
    Thanks to kazuma_6969
"""
QUEST_EVENT_SEA_POWER = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61016,
        'name': "Sea Power",
        'client': "Retired Hunter",
        'description':
            "Hunt 2 Lagiacrus\n"
            "",
        'details':
            "I once knew a fool of a hunter\n"
            "who found a legendary clue --\n"
            "but paid for it with his life.\n"
            "He left those plans behind.\n"
            "They're useless to a retired\n"
            "hunter like me, so I figured\n"
            "I'd pass them to another fool.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 3800,
        'quest_fee': 2250,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_40_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 48,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0036,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.lagiacrus,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x02,
            'level': 0x3B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.lagiacrus,
            'objective_num': 0x02,
            'zenny_reward': 11400,
            'hrp_reward': 1100,
            'rewards_row_1': [
                (ItemsType.lagiacrus_claw_plus, 1, 5),
                (ItemsType.lagiacrus_hide_plus, 1, 16),
                (ItemsType.lagiacrus_scale_plus, 1, 22),
                (ItemsType.shell_shocker_plus, 1, 8),
                (ItemsType.monster_bone_plus, 1, 14),
                (ItemsType.lagiacrus_plate, 1, 10),
                (ItemsType.lagia_sapphire, 1, 2),
                (ItemsType.lightning_ticket, 1, 23)
            ],
            'rewards_row_2': [
                (ItemsType.lagiacrus_claw_plus, 1, 5),
                (ItemsType.lagiacrus_hide_plus, 1, 16),
                (ItemsType.lagiacrus_scale_plus, 1, 22),
                (ItemsType.shell_shocker_plus, 1, 8),
                (ItemsType.monster_bone_plus, 1, 14),
                (ItemsType.lagiacrus_plate, 1, 10),
                (ItemsType.lagia_sapphire, 1, 2),
                (ItemsType.lightning_ticket, 1, 23)
            ],
        },
        'subquest_1': {
            'description': "Hunt a Lagiacrus",
            'type': 0x00000001,
            'objective_type': Monster.lagiacrus,
            'objective_num': 0x01,
            'zenny_reward': 11400,
            'hrp_reward': 1100,
            'rewards_row_1': [
                (ItemsType.lagiacrus_claw_plus, 1, 5),
                (ItemsType.lagiacrus_hide_plus, 1, 16),
                (ItemsType.lagiacrus_scale_plus, 1, 22),
                (ItemsType.shell_shocker_plus, 1, 8),
                (ItemsType.monster_bone_plus, 1, 14),
                (ItemsType.lagiacrus_plate, 1, 10),
                (ItemsType.lagia_sapphire, 1, 2),
                (ItemsType.lightning_ticket, 1, 23)
            ],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 17: Flooded Forest Free-For-All
Quest description from https://www.youtube.com/watch?v=mWHonz4dXHk
    thanks to "kazuma_6969"
"""
QUEST_EVENT_FF_FREE_FOR_ALL = {
    'quest_info': {
        'quest_id': 61017,
        'name': "Flooded Forest Free-For-All",
        'client': "Argosy Captain",
        'description': "Hunt a Royal L., Lag. & Gobul",
        'details':
            "Taihen! Means very bad, yes?\n"
            "Flooded Forest overrun by pack\n"
            "of leviathans -- Argosy cannot\n"
            "get anywhere near area! Big\n"
            "problem for trade, yes? Only\n"
            "hunters can return fair seas\n"
            "to Flooded Forest. Onegai!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 1, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 9000,
        'quest_fee': 2550,
        'time_limit': 50,
        'main_monster_1': Monster.ludroth,
        'main_monster_2': Monster.kelbi,
        'location': LocationType.QUEST_LOCATION_FLOODED_FOR,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_40_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x0040,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
        'smallmonster_data_file': 'sm_ff_free_for_all.dat',
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,  # 4 -> area 1  # 3 -> area 1  # 2 -> basecamp? # 1 -> area 3 # 0 -> area 4
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x36,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.lagiacrus,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x36,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.gobul,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x36,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.royal_ludroth,
            'objective_num': 0x01,
            'zenny_reward': 25800,
            'hrp_reward': 2600,
            'rewards_row_1': [
                (ItemsType.hrd_armor_sphere, 1, 1),
                (ItemsType.hvy_armor_sphere, 1, 5),
                (ItemsType.quality_sponge, 1, 14),
                (ItemsType.gobul_spike_plus, 1, 20),
                (ItemsType.gobul_fin_plus, 1, 7),
                (ItemsType.lagiacrus_hide_plus, 1, 10),
                (ItemsType.lagiacrus_scale_plus, 1, 8),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.black_gem_ticket, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.hrd_armor_sphere, 1, 1),
                (ItemsType.hvy_armor_sphere, 1, 5),
                (ItemsType.quality_sponge, 1, 14),
                (ItemsType.gobul_spike_plus, 1, 20),
                (ItemsType.gobul_fin_plus, 1, 7),
                (ItemsType.lagiacrus_hide_plus, 1, 10),
                (ItemsType.lagiacrus_scale_plus, 1, 8),
                (ItemsType.shining_charm, 1, 10),
                (ItemsType.black_gem_ticket, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.lagiacrus,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.gobul,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""

EVENT QUEST 18: Rage Match
Quest description from https://www.youtube.com/watch?v=rbbiLgsAoGU
    thanks to "kazuma_6969"
(INCOMPLETE) Second deviljho does not spawn on a delay.
"""
QUEST_EVENT_RAGE_MATCH = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61018,
        'name': "Rage Match",
        'client': "Arena Manager",
        'description': "Hunt 2 Deviljho",
        'details':
            "We've all heard of that\n"
            "outrageous dragon of rage,\n"
            "the Deviljho! Now, we've got\n"
            "not one -- but two -- stalking\n"
            "the Arena! What hunter has the\n"
            "cojones to challenge these\n"
            "pernicious predators? Not me.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 13000,
        'quest_fee': 3600,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 244,
        'summon': 0x00000000,  # 0x64010232,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.deviljho,
            'starting_area': 0x01,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0A
        },
        'monster_2': {
            'type': Monster.deviljho,
            'starting_area': 0x01,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x5A,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0A
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.deviljho,
            'objective_num': 0x02,
            'zenny_reward': 36000,
            'hrp_reward': 2880,
            'rewards_row_1': [
                (ItemsType.deviljho_fang, 1, 6),
                (ItemsType.deviljho_talon, 1, 13),
                (ItemsType.deviljho_scale, 1, 26),
                (ItemsType.deviljho_hide, 1, 20),
                (ItemsType.shining_charm, 1, 6),
                (ItemsType.deviljho_gem, 1, 4),
                (ItemsType.wyvrnhide_ticket, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.deviljho_fang, 1, 6),
                (ItemsType.deviljho_talon, 1, 13),
                (ItemsType.deviljho_scale, 1, 26),
                (ItemsType.deviljho_hide, 1, 20),
                (ItemsType.shining_charm, 1, 6),
                (ItemsType.deviljho_gem, 1, 4),
                (ItemsType.wyvrnhide_ticket, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000000,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 19: Lords of the Sea and Sky
Quest description from https://www.youtube.com/watch?v=x_uN2UtCA9Y
    Thanks to "kazuma_6969"
"""
QUEST_EVENT_LORDS_OF_THE_SEA_AND_SKY = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61019,
        'name': "Lords of the Sea and Sky",
        'client': "Arena Manager",
        'description':
            "Hunt a Lagiacrus\n"
            "and a Rathalos",
        'details':
            "In the Arena tonight, reunited\n"
            "and it feels so--gahh! It's\n"
            "the king and lord of sky and\n"
            "sea, Rathalos and Lagiacrus!\n"
            "Their victims: our hunters!\n"
            "Prepare for a bout that'll\n"
            "go down in hunting history!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 7800,
        'quest_fee': 2300,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x003C,
        'summon': 0x64010332,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.lagiacrus,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.lagiacrus,
            'objective_num': 0x01,
            'zenny_reward': 23400,
            'hrp_reward': 1760,
            'rewards_row_1': [
                (ItemsType.lagiacrus_hide_plus, 1, 10),
                (ItemsType.shell_shocker_plus, 1, 14),
                (ItemsType.rathaloscarapace, 1, 23),
                (ItemsType.rathalos_scale_plus, 1, 15),
                (ItemsType.rathalos_ruby, 1, 4),
                (ItemsType.lagia_sapphire, 1, 4),
                (ItemsType.mystery_charm, 1, 17),
                (ItemsType.shining_charm, 1, 8),
                (ItemsType.timeworn_charm, 1, 5)
            ],
            'rewards_row_2': [
                (ItemsType.shining_charm, 1, 25),
                (ItemsType.mystery_charm, 1, 18),
                (ItemsType.timeworn_charm, 1, 5),
                (ItemsType.adv_armor_sphere, 1, 12),
                (ItemsType.hrd_armor_sphere, 1, 20),
                (ItemsType.hvy_armor_sphere, 1, 6),
                (ItemsType.rustshard, 1, 14)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 20: World Eater
Quest description/rewards/etc from https://www.youtube.com/watch?v=Z6joazT8J78
(INCOMPLETE) Needs invading queropeco
"""
QUEST_EVENT_WORLD_EATER = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': 1,
                'pos_x': 247.42,'pos_y': 560.37,'pos_z': -3613.80,
                'rot_x': 0,'rot_y': -119,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 3,
                'pos_x': -474.90,'pos_y': 491.91,'pos_z': -3857.25,
                'rot_x': 0,'rot_y': -267,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': 3,
                'pos_x': 897.01,'pos_y': 418.60,'pos_z': -4931.83,
                'rot_x': 0,'rot_y': -284,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 2,
                'pos_x': 219.95,'pos_y': 402.97,'pos_z': -4449.25,
                'rot_x': 0,'rot_y': 244,'rot_z': 0,
            },
        ],
        [
            # Area 2 (Area 3 in Deserted Island)
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': 3,
                'pos_x': -6654.10,'pos_y': 23.12,'pos_z': 117.64,
                'rot_x': 0,'rot_y': 455,'rot_z': 0,
            },
        ],
        [
            # Area 3 (Area 2 in Deserted Island)
            {
                'type': Monster.aptonoth,'unk1': 0,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 2567.38,'pos_y': -4.58,'pos_z': -1280.44,
                'rot_x': 0,'rot_y': 352,'rot_z': 0,
            },
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': -1,
                'pos_x': 2119.14,'pos_y': -14.21,'pos_z': -787.00,
                'rot_x': 0,'rot_y': 335,'rot_z': 0,
            },
        ],
        [
            # Area 4 (Area 7 in Deserted Island)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 2,
                'pos_x': 39.65,'pos_y': 2.00,'pos_z': 2631.32,
                'rot_x': 0,'rot_y': 113,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 2,
                'pos_x': -538.14,'pos_y': 2.00,'pos_z': 2165.99,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 360.98,'pos_y': 2.00,'pos_z': 820.71,
                'rot_x': 0,'rot_y': -187,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 4,'quantity': -1,
                'pos_x': -5671.42,'pos_y': 466.03,'pos_z': 3071.35,
                'rot_x': 273,'rot_y': 304,'rot_z': 0,
            },
        ],
        [
            # Area 5
        ],
        [
            # Area 6
        ],
        [
            # Area 7 (Area 11 in Deserted Island)
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 4,
                'pos_x': 2237.04,'pos_y': -1090.00,'pos_z': 1586.48,
                'rot_x': 0,'rot_y': 96,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 2469.26,'pos_y': -1330.00,'pos_z': 2832.58,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 2,
                'pos_x': 1103.05,'pos_y': -2050.00,'pos_z': -1429.32,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': -3054.79,'pos_y': -3047.85,'pos_z': 3126.22,
                'rot_x': 0,'rot_y': -62,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 4,'room': 7,'quantity': 1,
                'pos_x': 1268.03,'pos_y': -2470.00,'pos_z': -557.22,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 1742.13,'pos_y': -3820.00,'pos_z': -1993.49,
                'rot_x': 0,'rot_y': -108,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 1732.89,'pos_y': -3580.00,'pos_z': -4462.32,
                'rot_x': 0,'rot_y': -278,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 12 in the Deserted Island)
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': 80.95,'pos_y': 35.81,'pos_z': -523.41,
                'rot_x': 0,'rot_y': -420,'rot_z': 0,
            },
            {
                'type': Monster.ludroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1342.36,'pos_y': -18.00,'pos_z': 465.56,
                'rot_x': 0,'rot_y': -324,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 6 in the Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 3,
                'pos_x': 1059.13,'pos_y': 5.78,'pos_z': -3228.47,
                'rot_x': 0,'rot_y': -261,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 4,
                'pos_x': 390.83,'pos_y': 20.44,'pos_z': -746.07,
                'rot_x': 0,'rot_y': -176,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': -482.31,'pos_y': 16.39,'pos_z': 5.01,
                'rot_x': 0,'rot_y': 250,'rot_z': 0,
            },
        ],
        [
            # Area 10 (Area 8 in the Deserted Island)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 5,
                'pos_x': -1846.87,'pos_y': -263.00,'pos_z': 931.19,
                'rot_x': 0,'rot_y': -5,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 3,
                'pos_x': -3160.63,'pos_y': -206.32,'pos_z': -355.73,
                'rot_x': 0,'rot_y': 307,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 2,
                'pos_x': -1949.45,'pos_y': -276.13,'pos_z': 1228.73,
                'rot_x': 0,'rot_y': 216,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': -1,
                'pos_x': -1552.64,'pos_y': -186.42,'pos_z': 1504.30,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': -1,
                'pos_x': -1352.11,'pos_y': -174.80,'pos_z': 1441.92,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 1,
                'pos_x': -653.75,'pos_y': 306.58,'pos_z': 2295.24,
                'rot_x': 0,'rot_y': 221,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 10,'quantity': 4,
                'pos_x': -615.28,'pos_y': 96.58,'pos_z': 2086.81,
                'rot_x': 0,'rot_y': 119,'rot_z': 0,
            },
        ],
        [
            # Area 11 (Area 4 in the Deserted Island)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 2,
                'pos_x': -453.62,'pos_y': 705.50,'pos_z': 2253.55,
                'rot_x': 0,'rot_y': -5,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 4,
                'pos_x': 142.14,'pos_y': 336.98,'pos_z': 3677.44,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4363.26,'pos_y': 426.27,'pos_z': 5818.19,
                'rot_x': 0,'rot_y': 171,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4782.14,'pos_y': 426.27,'pos_z': 5556.53,
                'rot_x': 0,'rot_y': 164,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 4617.08,'pos_y': 426.27,'pos_z': 6208.15,
                'rot_x': 0,'rot_y': 284,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 11,'quantity': 1,
                'pos_x': 5099.46,'pos_y': 426.27,'pos_z': 5456.15,
                'rot_x': 0,'rot_y': 161,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 4,
                'pos_x': 2767.15,'pos_y': 611.59,'pos_z': 4297.09,
                'rot_x': 0,'rot_y': -301,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2793.18,'pos_y': 1205.81,'pos_z': 5908.79,
                'rot_x': 0,'rot_y': -295,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra2,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': 3210.49,'pos_y': 845.81,'pos_z': 5369.26,
                'rot_x': 0,'rot_y': -398,'rot_z': 0,
            },
        ],
        [
            # Area 12 (Area 10 in the Deserted Island)
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': 572.89,'pos_y': -618.12,'pos_z': -2648.11,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -501.62,'pos_y': -210.00,'pos_z': -3356.64,
                'rot_x': 0,'rot_y': 45,'rot_z': 0,
            },
            {
                'type': Monster.epioth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 12,'quantity': -1,
                'pos_x': -1624.63,'pos_y': -888.12,'pos_z': -2880.06,
                'rot_x': 0,'rot_y': 113,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2352.88,'pos_y': -523.55,'pos_z': -7478.20,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -1957.86,'pos_y': -1228.41,'pos_z': -7734.46,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2821.80,'pos_y': -988.41,'pos_z': -8174.07,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
            {
                'type': Monster.fish,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 12,'quantity': -1,
                'pos_x': -2435.99,'pos_y': -988.41,'pos_z': -7780.24,
                'rot_x': 0,'rot_y': -91,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61020,
        'name': "World Eater",
        'client': "Guildmaster",
        'description': "Hunt a Deviljho",
        'details':
            "Emergency! A huge Deviljho has\n"
            "appeared. It's twice as big as\n"
            "a normal one and it's eating\n"
            "everything in sight! Go get\n"
            "it! And now, a haiku: A huge\n"
            "Deviljho/with no food in its\n"
            "stomach/eats the whole island.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 6000,
        'quest_fee': 1800,
        'time_limit': 50,
        'main_monster_1': Monster.jaggi,
        'main_monster_2': Monster.jaggia,
        'location': LocationType.QUEST_LOCATION_D_ISLAND,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 31,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x0034,
        'summon': 0x64010234,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.deviljho,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x40,  # 0x01 through 0x3c
            'size': 0xC8,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.deviljho,
            'objective_num': 0x01,
            'zenny_reward': 18000,
            'hrp_reward': 1800,
            'rewards_row_1': [
                (ItemsType.timeworn_charm, 1, 33),
                (ItemsType.deviljho_gem, 1, 4),
                (ItemsType.deviljho_scalp, 1, 8),
                (ItemsType.deviljho_hide, 1, 17),
                (ItemsType.hvy_armor_sphere, 1, 11),
                (ItemsType.shining_charm, 1, 19),
                (ItemsType.deviljho_fang, 1, 8)
            ],
            'rewards_row_2': [
                (ItemsType.deviljho_scalp, 1, 20),
                (ItemsType.timeworn_charm, 1, 34),
                (ItemsType.deviljho_fang, 1, 6),
                (ItemsType.deviljho_hide, 1, 17),
                (ItemsType.deviljho_gem, 1, 3),
                (ItemsType.shining_charm, 1, 11),
                (ItemsType.hvy_armor_sphere, 1, 9)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 21: Where Gods Fear To Tread
Quest description from https://www.youtube.com/watch?v=mQHTdPRlD1w,
    thanks to "soulmizute, emperor of the abyss#5094"
    and "El Matiah#8904"
"""
QUEST_EVENT_WHERE_GODS_FEAR_TO_TREAD = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61021,
        'name': "Where Gods Fear to Tread",
        'client': "Scarlet Mystery Man",
        'description': "Slay the Alatreon",
        'details':
            "I've been waiting, hunter. Now\n"
            "comes your final challenge:\n"
            "Alatreon, a dragon of darkness\n"
            "and light. Can mere mortals\n"
            "fell an elder dragon feared\n"
            "even by the gods? Don't even\n"
            "bother saying your prayers...",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0, 1, 0)
        ),
        'penalty_per_cart': 14000,
        'quest_fee': 4200,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_SACRED_LAND,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.shrine,
        'general_enemy_level': 0x0040,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.alatreon,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x40,  # 0x01 through 0x3c
            'size': 0x7D,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.alatreon,
            'objective_num': 0x01,
            'zenny_reward': 42000,
            'hrp_reward': 4200,
            'rewards_row_1': [
                (ItemsType.alatreon_scute, 1, 40),
                (ItemsType.brkn_skypiercer, 1, 30),
                (ItemsType.alatreon_talon, 1, 10),
                (ItemsType.alatreon_plate, 1, 10),
                (ItemsType.skypiercer, 1, 5),
                (ItemsType.azure_dragongem, 1, 5)
            ],
            'rewards_row_2': [
                (ItemsType.alatreon_plate, 1, 11),
                (ItemsType.brkn_skypiercer, 1, 34),
                (ItemsType.alatreon_talon, 1, 39),
                (ItemsType.elderdragonblood, 1, 6),
                (ItemsType.skypiercer, 1, 5),
                (ItemsType.azure_dragongem, 1, 5)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000005,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 21: Red Hot Party!
Quest description from https://www.youtube.com/watch?v=v-pnNyO9-GM,
    thanks to "kazuma_6969"
"""
QUEST_EVENT_RED_HOT_PARTY = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 2,
                'pos_x': -494.25,'pos_y': 47.01,'pos_z': -947.91,
                'rot_x': 0,'rot_y': 112147,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': -1361.42,'pos_y': 20.60,'pos_z': -712.51,
                'rot_x': 0,'rot_y': 79456,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': 1,
                'pos_x': 1031.98,'pos_y': 26.73,'pos_z': -1406.32,
                'rot_x': 0,'rot_y': 152977,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 4,
                'pos_x': 3139.21,'pos_y': -16.41,'pos_z': 1809.58,
                'rot_x': 0,'rot_y': 14105,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': 2598.00,'pos_y': 64.57,'pos_z': 2280.01,
                'rot_x': 0,'rot_y': 14478,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 2,
                'pos_x': 2184.05,'pos_y': 66.73,'pos_z': 2453.70,
                'rot_x': 0,'rot_y': 11582,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': 2741.80,'pos_y': -53.82,'pos_z': 1680.05,
                'rot_x': 0,'rot_y': 14128,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 6982.80,'pos_y': 73.73,'pos_z': 4494.92,
                'rot_x': 0,'rot_y': 5856,'rot_z': 0,
            },
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': -1,
                'pos_x': 7778.32,'pos_y': 66.41,'pos_z': 4957.68,
                'rot_x': 0,'rot_y': 2872,'rot_z': 0,
            },
            {
                'type': Monster.aptonoth,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': -1,
                'pos_x': 8087.79,'pos_y': 83.54,'pos_z': 5160.52,
                'rot_x': 0,'rot_y': 5774,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 3,'quantity': -1,
                'pos_x': 8676.94,'pos_y': 515.74,'pos_z': 2473.30,
                'rot_x': 273,'rot_y': 6351,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.rhenoplos,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 672.08,'pos_y': 25.43,'pos_z': 639.95,
                'rot_x': 0,'rot_y': 2264,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 0,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': -1151.12,'pos_y': -43.31,'pos_z': 2402.83,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 3,
                'pos_x': 1580.62,'pos_y': 129.42,'pos_z': 3042.75,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 4,'quantity': 2,
                'pos_x': 1743.00,'pos_y': 339.42,'pos_z': 2633.18,
                'rot_x': 0,'rot_y': 91,'rot_z': 0,
            },
            {
                'type': Monster.brd_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 1303.26,'pos_y': 189.42,'pos_z': 2724.68,
                'rot_x': 0,'rot_y': -28,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': -1485.68,'pos_y': 36.65,'pos_z': 104.92,
                'rot_x': 0,'rot_y': 3032,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': 897.01,'pos_y': 25.14,'pos_z': -27.96,
                'rot_x': 0,'rot_y': 56,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 4,'quantity': -1,
                'pos_x': 2948.85,'pos_y': 7.51,'pos_z': 1861.15,
                'rot_x': 0,'rot_y': 20656,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -775.56,'pos_y': 73.07,'pos_z': 542.20,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -3498.99,'pos_y': 67.50,'pos_z': -1218.55,
                'rot_x': 0,'rot_y': 4835,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 486.74,'pos_y': 38.66,'pos_z': -422.06,
                'rot_x': 0,'rot_y': 1331,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 2864.76,'pos_y': 49.34,'pos_z': -1059.79,
                'rot_x': 0,'rot_y': 7296,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': 1202.49,'pos_y': 57.63,'pos_z': -1571.42,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 5,'quantity': -1,
                'pos_x': -1733.55,'pos_y': 56.88,'pos_z': -1510.18,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 6
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': 393.15,'pos_y': -35.75,'pos_z': 1076.53,
                'rot_x': 0,'rot_y': -85,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': -1170.83,'pos_y': -30.77,'pos_z': 447.51,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': 1020.10,'pos_y': 4.72,'pos_z': -202.83,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 6,'quantity': -1,
                'pos_x': -435.28,'pos_y': -28.37,'pos_z': -1280.39,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 7
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 7,'quantity': 3,
                'pos_x': 95.05,'pos_y': -6.35,'pos_z': 228.22,
                'rot_x': 0,'rot_y': 1399,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': -2114.33,'pos_y': 17.37,'pos_z': 268.38,
                'rot_x': 0,'rot_y': 19692,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 7,'quantity': 1,
                'pos_x': -1877.72,'pos_y': -22.42,'pos_z': 1532.47,
                'rot_x': 0,'rot_y': 32312,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 7,'quantity': 1,
                'pos_x': 625.43,'pos_y': 3.37,'pos_z': -496.28,
                'rot_x': 0,'rot_y': 6283,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': -1447.72,'pos_y': 21.43,'pos_z': 61.89,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': 316.55,'pos_y': -3.36,'pos_z': -1209.27,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 7,'quantity': -1,
                'pos_x': 1008.65,'pos_y': -9.18,'pos_z': 1099.80,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 4,
                'pos_x': 728.75,'pos_y': -19.44,'pos_z': 1581.60,
                'rot_x': 0,'rot_y': 1581.60,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 3,
                'pos_x': -375.43,'pos_y': 6.66,'pos_z': 301.92,
                'rot_x': 0,'rot_y': 40860,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': 479.45,'pos_y': 30.53,'pos_z': -50.40,
                'rot_x': 0,'rot_y': 59178,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': 2190.05,'pos_y': -6.53,'pos_z': 1552.73,
                'rot_x': 0,'rot_y': 24814,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 9,'quantity': 2,
                'pos_x': 1226.78,'pos_y': 14.44,'pos_z': -971.03,
                'rot_x': 0,'rot_y': 49126,'rot_z': 0,
            },
            {
                'type': Monster.uroktor,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': 3,
                'pos_x': 30.91,'pos_y': 11.00,'pos_z': -556.52,
                'rot_x': 0,'rot_y': 19871,'rot_z': 0,
            },
        ],
        [
            # Area 10
        ],
    ],
    'quest_info': {
        'quest_id': 61022,
        'name': "Red Hot Party!",
        'client': "Deserted Island Chief",
        'description': "Hunt a Ratha., Urag. & Agnak.",
        'details':
            "You're back! While you were\n"
            "away, three wyverns moved into\n"
            "the volcano and are reeking\n"
            "havoc throughout the area!\n"
            "We haven't a moment to spare!\n"
            "Please get rid of all three\n"
            "of them for me and my people!",
        'success_message': "Complete the Main Quest.",
        'flags': (

            (0, 0, 1, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)

            # (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            # (1, 1, 0, 0, 0, 0, 0, 0),  # (1, 1, 0, 0, 0, 0, 0, 0),
            # (0, 0, 0, 0, 0, 0, 0, 0),  # (0, 0, 0, 0, 0, 0, 0, 0),
            # (0, 0, 1, 0, 0, 0, 1, 1)  # (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 15000,
        'quest_fee': 4050,
        'time_limit': 50,
        'main_monster_1': Monster.bnahabra2,
        'main_monster_2': Monster.felyne,
        'location': LocationType.QUEST_LOCATION_VOLCANO,
        'quest_rank': QuestRankType.star_5,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_40_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 27,
        'starting_position': StartingPositionType.random,
        'general_enemy_level': 0x0034,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x38,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x38,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_3': {
            'type': Monster.agnaktor,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x38,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 41000,
            'hrp_reward': 3870,
            'rewards_row_1': [
                (ItemsType.rathaloscarapace, 1, 8),
                (ItemsType.rathalos_scale_plus, 1, 8),
                (ItemsType.rath_medulla, 1, 8),
                (ItemsType.agnaktor_fin_plus, 1, 10),
                (ItemsType.agnaktorcarapace, 1, 10),
                (ItemsType.uragaan_marrow, 1, 10),
                (ItemsType.uragaan_carapace, 1, 10),
                (ItemsType.ancient_shard, 1, 10),
                (ItemsType.rathalos_plate, 1, 8),
                (ItemsType.uragaan_ruby, 1, 6),
                (ItemsType.rathalos_ruby, 1, 6),
                (ItemsType.wyvern_stone, 1, 6)
            ],
            'rewards_row_2': [
                (ItemsType.rathaloscarapace, 1, 8),
                (ItemsType.rathalos_scale_plus, 1, 8),
                (ItemsType.rath_medulla, 1, 8),
                (ItemsType.agnaktor_fin_plus, 1, 10),
                (ItemsType.agnaktorcarapace, 1, 10),
                (ItemsType.uragaan_marrow, 1, 10),
                (ItemsType.uragaan_carapace, 1, 10),
                (ItemsType.ancient_shard, 1, 10),
                (ItemsType.rathalos_plate, 1, 8),
                (ItemsType.uragaan_ruby, 1, 6),
                (ItemsType.rathalos_ruby, 1, 6),
                (ItemsType.wyvern_stone, 1, 6)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00000001,  # 0x00020101  <-- Fails on capture, also reduced quest complete timer
            'objective_type': Monster.agnaktor,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST 22: Fiery Skies, Frozen Fields
Quest description from https://www.youtube.com/watch?v=KRGHjgHagXY,
    thanks to "kazuma_6969"
"""
QUEST_EVENT_FIERY_SKIES_FROZEN_FIELDS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
        ],
    ],
    'quest_info': {
        'quest_id': 61023,
        'name': "Fiery Skies, Frozen Fields",
        'client': "Deserted Island Maiden",
        'description':
            "Hunt a Barioth and\n"
            "a Rathalos",
        'details':
            "It's time for a FESTIVAL!\n"
            "Presenting the King of the\n"
            "Skies and the Knight of the\n"
            "Tundra -- the flash of fire\n"
            "and ice from above and\n"
            "below -- only at the arena!\n"
            "Do you have what it takes?",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 14000,
        'quest_fee': 4200,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.high_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x003C,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barioth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0B
        },
        'monster_2': {
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x3B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x0A
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.barioth,
            'objective_num': 0x01,
            'zenny_reward': 42000,
            'hrp_reward': 4290,
            'rewards_row_1': [
                (ItemsType.rathaloscarapace, 2, 25),
                (ItemsType.barioth_carapace, 2, 24),
                (ItemsType.hrd_armor_sphere, 2, 17),
                (ItemsType.hvy_armor_sphere, 1, 15),
                (ItemsType.rathalos_ruby, 1, 10),
                (ItemsType.wyvern_stone, 1, 9)
            ],
            'rewards_row_2': [
                (ItemsType.rathaloscarapace, 2, 25),
                (ItemsType.barioth_carapace, 2, 24),
                (ItemsType.hrd_armor_sphere, 2, 17),
                (ItemsType.hvy_armor_sphere, 1, 15),
                (ItemsType.rathalos_ruby, 1, 10),
                (ItemsType.wyvern_stone, 1, 9)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


QUEST_EVENT_GREEN_EGGS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra1,'unk1': 3,'unk2': 0xFF,
                'variant': 1,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61050,
        'name': "[MH3SP] Green Eggs and...",
        'client': "Ze SpyRo",
        'description':
            "Hunt a Gigginox\n"
            "and an Agnaktor",
        'details':
            "Why do we live, only to suffer?\n"
            "Only slayers of pig meat know\n"
            "these things. Take care, Hunter,\n"
            "for those who look to antidote\n"
            "herbs may find their breath\n"
            "stolen away.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 2400,
        'quest_fee': 200,
        'time_limit': 50,
        'main_monster_1': Monster.gigginox,
        'main_monster_2': Monster.agnaktor,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_18_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001B,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.gigginox,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x1B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.agnaktor,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x1B,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.gigginox,
            'objective_num': 0x01,
            'zenny_reward': 7000,
            'hrp_reward': 950,
            'rewards_row_1': [
                (ItemsType.flabby_hide, 1, 18),
                (ItemsType.uncanny_hide, 1, 6),
                (ItemsType.pale_extract, 1, 11),
                (ItemsType.poison_sac, 1, 15),
                (ItemsType.agnaktor_shell, 1, 10),
                (ItemsType.agnaktor_scale, 1, 16),
                (ItemsType.agnaktor_hide, 1, 13),
                (ItemsType.agnaktor_fin, 1, 6),
                (ItemsType.agnaktor_beak, 1, 5)
            ],
            'rewards_row_2': [
                (ItemsType.flabby_hide, 1, 13),
                (ItemsType.uncanny_hide, 1, 6),
                (ItemsType.pale_extract, 1, 11),
                (ItemsType.poison_sac, 1, 10),
                (ItemsType.agnaktor_shell, 1, 9),
                (ItemsType.agnaktor_scale, 1, 10),
                (ItemsType.agnaktor_hide, 1, 10),
                (ItemsType.agnaktor_fin, 1, 6),
                (ItemsType.agnaktor_beak, 1, 5),
                (ItemsType.commendation, 1, 20)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000001,
            'objective_type': Monster.agnaktor,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}


"""
EVENT QUEST ???: Jump Fourty-Eight Jaggi
Quest description/rewards/etc from https://www.youtube.com/watch?v=qyQt2Xmpt0g
Quest requirements altered to make it possible to win.
"""
QUEST_EVENT_JUMP_FOURTY_EIGHT_JAGGI = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 2039.26,'pos_y': 12.70,'pos_z': 210.05,
                'rot_x': 0,'rot_y': 17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 857.89,'pos_y': -41.97,'pos_z': 814.06,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': 97.58,'pos_y': -75.54,'pos_z': 135.22,
                'rot_x': 0,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 1,'quantity': 1,
                'pos_x': -393.52,'pos_y': -163.94,'pos_z': -667.01,
                'rot_x': 0,'rot_y': -199,'rot_z': 0,
            },
        ],
        [
            # Area 2
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 1,
                'pos_x': -853.86,'pos_y': 19.45,'pos_z': 1381.66,
                'rot_x': 0,'rot_y': -113,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 2,'quantity': 2,
                'pos_x': -553.59,'pos_y': -2.57,'pos_z': -369.71,
                'rot_x': 0,'rot_y': 193,'rot_z': 0,
            },
            {
                'type': Monster.kelbi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 2,'quantity': 3,
                'pos_x': -1698.75,'pos_y': 5.74,'pos_z': -530.30,
                'rot_x': 0,'rot_y': 398,'rot_z': 0,
            },
        ],
        [
            # Area 3
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 873.28,'pos_y': 85.07,'pos_z': -610.86,
                'rot_x': 0,'rot_y': -153,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': -1,
                'pos_x': 1247.84,'pos_y': 106.65,'pos_z': 25.11,
                'rot_x': 0,'rot_y': -358,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 2,'room': 3,'quantity': 2,
                'pos_x': 177.92,'pos_y': 450.70,'pos_z': -32.21,
                'rot_x': 0,'rot_y': -238,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 3,'quantity': 2,
                'pos_x': -78.66,'pos_y': 330.70,'pos_z': 362.86,
                'rot_x': 0,'rot_y': -79,'rot_z': 0,
            },
        ],
        [
            # Area 4
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 3,
                'pos_x': 606.18,'pos_y': -12.89,'pos_z': 4145.11,
                'rot_x': 0,'rot_y': 324,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': 1,
                'pos_x': 524.37,'pos_y': -18.65,'pos_z': 2292.05,
                'rot_x': 0,'rot_y': 199,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 4,'quantity': -1,
                'pos_x': -460.08,'pos_y': -71.51,'pos_z': 3044.50,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
        ],
        [
            # Area 5
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 1,
                'pos_x': 300.40,'pos_y': 4.00,'pos_z': -211.14,
                'rot_x': 0,'rot_y': 0,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 458.16,'pos_y': 1.49,'pos_z': -918.94,
                'rot_x': 0,'rot_y': 51,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 4,
                'pos_x': 1813.83,'pos_y': 3.06,'pos_z': 925.68,
                'rot_x': 0,'rot_y': 494,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': -504.37,'pos_y': 3.05,'pos_z': -757.30,
                'rot_x': 0,'rot_y': 676,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': 2,
                'pos_x': 1118.48,'pos_y': 4.00,'pos_z': -420.89,
                'rot_x': 0,'rot_y': 364,'rot_z': 0,
            },
            {
                'type': Monster.jaggia,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 5,'quantity': -1,
                'pos_x': 2658.84,'pos_y': 3.24,'pos_z': 222.99,
                'rot_x': 0,'rot_y': 756,'rot_z': 0,
            },
        ],
        [
            # Area 6 (Area 8 in Sandy Plains)
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': 1612.71,'pos_y': -30.27,'pos_z': 695.30,
                'rot_x': 0,'rot_y': 517,'rot_z': 0,
            },
            {
                'type': Monster.rhenoplos,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -2050.04,'pos_y': -31.90,'pos_z': -266.33,
                'rot_x': 0,'rot_y': 28,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 5,
                'pos_x': -344.14,'pos_y': -13.00,'pos_z': -26.14,
                'rot_x': 0,'rot_y': 443,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 4,
                'pos_x': -161.74,'pos_y': 4.80,'pos_z': -416.52,
                'rot_x': 0,'rot_y': 472,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 2,
                'pos_x': -481.05,'pos_y': 15.34,'pos_z': -643.19,
                'rot_x': 0,'rot_y': 568,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': -1,
                'pos_x': -692.26,'pos_y': -11.02,'pos_z': -235.13,
                'rot_x': 0,'rot_y': 608,'rot_z': 0,
            },
            {
                'type': Monster.altaroth,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 6,'quantity': 3,
                'pos_x': -417.82,'pos_y': -1.44,'pos_z': -343.46,
                'rot_x': 0,'rot_y': 147,'rot_z': 0,
            },
        ],
        [
            # Area 7 (Area 9 in Sandy Plains)
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 3,
                'pos_x': 4294.59,'pos_y': -75.65,'pos_z': -2925.29,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 3995.30,'pos_y': -45.09,'pos_z': -2049.22,
                'rot_x': 0,'rot_y': -85,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 2,
                'pos_x': 4187.00,'pos_y': -17.07,'pos_z': -1574.97,
                'rot_x': 0,'rot_y': -17,'rot_z': 0,
            },
            {
                'type': Monster.jaggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 7,'quantity': 1,
                'pos_x': 3781.64,'pos_y': -66.86,'pos_z': -2570.78,
                'rot_x': 0,'rot_y': -130,'rot_z': 0,
            },
        ],
        [
            # Area 8 (Area 10 in Sandy Plains)
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 7,
                'pos_x': 293.99,'pos_y': -170.31,'pos_z': 4049.95,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 5,
                'pos_x': 124.95,'pos_y': -186.54,'pos_z': 3440.16,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 3,
                'pos_x': -425.01,'pos_y': -179.30,'pos_z': 4509.84,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 2,
                'pos_x': -714.48,'pos_y': -183.78,'pos_z': 4108.50,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.delex,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': 1,
                'pos_x': -1021.27,'pos_y': -215.48,'pos_z': 3726.09,
                'rot_x': 0,'rot_y': 819,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1974.57,'pos_y': -209.48,'pos_z': -316.05,
                'rot_x': 0,'rot_y': -56,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 8,'quantity': -1,
                'pos_x': -1825.11,'pos_y': -210.91,'pos_z': -382.90,
                'rot_x': 0,'rot_y': 130,'rot_z': 0,
            },
        ],
        [
            # Area 9 (Area 7 in Sandy Plains)
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 2,
                'pos_x': 3383.92,'pos_y': 2.65,'pos_z': 592.49,
                'rot_x': 0,'rot_y': -193,'rot_z': 0,
            },
            {
                'type': Monster.felyne,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': 1,
                'pos_x': 2653.55,'pos_y': -22.59,'pos_z': 987.24,
                'rot_x': 0,'rot_y': -73,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2838.69,'pos_y': -28.00,'pos_z': 445.91,
                'rot_x': 0,'rot_y': -142,'rot_z': 0,
            },
            {
                'type': Monster.melynx,'unk1': 3,'unk2': 0xFF,
                'variant': 0,'room': 9,'quantity': -1,
                'pos_x': 2109.53,'pos_y': -26.57,'pos_z': 575.43,
                'rot_x': 0,'rot_y': -460,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': -1,
                'pos_x': -1713.72,'pos_y': 1262.50,'pos_z': 2199.24,
                'rot_x': 273,'rot_y': -45,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 1,'room': 9,'quantity': 6,
                'pos_x': -1174.44,'pos_y': 1319.50,'pos_z': 1682.19,
                'rot_x': 0,'rot_y': -39,'rot_z': 0,
            },
        ],
        [
            # Area 10
        ],
        [
            # Area 11 (Area 6 in Sandy Plains)
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': 2195.89,'pos_y': 73.70,'pos_z': -720.92,
                'rot_x': 0,'rot_y': 39,'rot_z': 0,
            },
            {
                'type': Monster.giggi,'unk1': 1,'unk2': 0xFF,
                'variant': 6,'room': 11,'quantity': 1,
                'pos_x': -535.73,'pos_y': 1212.59,'pos_z': 896.44,
                'rot_x': 0,'rot_y': 169,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -434.00,'pos_y': 198.96,'pos_z': 289.52,
                'rot_x': 0,'rot_y': -267,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -802.69,'pos_y': 198.96,'pos_z': 66.62,
                'rot_x': 0,'rot_y': -216,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 2,
                'pos_x': -645.14,'pos_y': 288.96,'pos_z': -371.21,
                'rot_x': 0,'rot_y': -227,'rot_z': 0,
            },
            {
                'type': Monster.bnahabra3,'unk1': 1,'unk2': 0xFF,
                'variant': 0,'room': 11,'quantity': 1,
                'pos_x': -473.33,'pos_y': 168.96,'pos_z': -166.43,
                'rot_x': 0,'rot_y': -210,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 61001,
        'name': "Jump Fourty-Eight Jaggi",
        'client': "Guild Subcontractor",
        'description': "Hunt 48 Great Jaggi",
        'details':
            "I'm gonna get so fired for\n"
            "this... The Great Jaggi some\n"
            "hunter brought in just\n"
            "escaped. Mind going after\n"
            "them? You better hurry,\n"
            "though. Bet they've got some\n"
            "incredible materials, too.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0, 1, 1)
        ),
        'penalty_per_cart': 1400,
        'quest_fee': 400,
        'time_limit': 50,
        'main_monster_1': Monster.bnahabra2,
        'main_monster_2': Monster.melynx,
        'location': LocationType.QUEST_LOCATION_SANDY_PLAINS,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 19,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x64050219,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.great_jaggi,
            'starting_area': 0x00,
            'boss_id': 0xFF,
            'spawn_count': 0x10,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_2': {
            'type': Monster.great_jaggi,
            'starting_area': 0x00,
            'boss_id': 0xFF,
            'spawn_count': 0x10,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        },
        'monster_3': {
            'type': Monster.great_jaggi,
            'starting_area': 0x00,
            'boss_id': 0xFF,
            'spawn_count': 0x10,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x01,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x01
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000001,
            'objective_type': Monster.great_jaggi,
            'objective_num': 0x30,
            'zenny_reward': 15000,
            'hrp_reward': 750,
            'rewards_row_1': [
                (ItemsType.great_jagi_claw, 2, 3),
                (ItemsType.great_jagi_hide, 2, 12),
                (ItemsType.kings_frill, 1, 10),
                (ItemsType.rustshard, 1, 20),
                (ItemsType.commendation, 1, 12),
                (ItemsType.voucher, 2, 18),
                (ItemsType.great_jagi_head, 1, 25)
            ],
            'rewards_row_2': [
                (ItemsType.mystery_charm, 1, 1),
                (ItemsType.aquaglow_jewel, 1, 1),
                (ItemsType.shining_charm, 1, 1),
                (ItemsType.armor_sphere, 1, 1),
                (ItemsType.armor_sphere_plus, 1, 1)
            ],
        },
        'subquest_1': {
            'description': "Hunt 24 Great Jaggi",
            'type': 0x00000001,
            'objective_type': Monster.great_jaggi,
            'objective_num': 0x18,
            'zenny_reward': 8000,
            'hrp_reward': 255,
            'rewards_row_1': [
                (ItemsType.great_jagi_claw, 1, 1),
                (ItemsType.great_jagi_hide, 1, 1),
                (ItemsType.jagi_scale, 1, 1),
                (ItemsType.screamer, 1, 1),
                (ItemsType.kings_frill, 1, 1),
                (ItemsType.bone_husk_s, 8, 1),
                (ItemsType.great_jagi_head, 1, 1)
            ],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0,
            'rewards_row_1': [],
        }
    },
    'unknown': {
        # (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}

"""
EVENT QUEST ??: Dark Side of the Moon
"""
QUEST_EVENT_DARK_SIDE_OF_THE_MOON = {
    'small_monsters': [
        [
            # Area 0
        ],
        [

        ],
        [

        ],
        [

        ]
    ],
    'quest_info': {
        'quest_id': 61008,
        'name': "[MH3SP] Dark Side of the Moon",
        'client': "Moga Village Chief",
        'description':
            "Slay a Ceadeus",
        'details':
            "Gambala! The sea drake has\n"
            "returned! Moga is barely clinging\n"
            "to the island after its last\n"
            "appearance -- we need this taken\n"
            "care of FAST! Get a group of your\n"
            "peers from Loc Lac and get your\n"
            "tail back here! PRONTO!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0, 0, 0)
        ),
        'penalty_per_cart': 10000,
        'quest_fee': 3100,
        'time_limit': 15,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_UW_RUIN,
        'quest_rank': QuestRankType.urgent,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_51_INITJOIN,
        'resources': ResourcesType.low_rank,
        'supply_set_number': 48,  # 43,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0010,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.ceadeus,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x3C,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.ceadeus,
            'objective_num': 0x01,
            'zenny_reward': 30000,
            'hrp_reward': 1500,
            'rewards_row_1': [
                (ItemsType.luminous_organ, 1, 15),
                (ItemsType.ceadeus_hide, 1, 25),
                (ItemsType.ceadeus_scale, 1, 14),
                (ItemsType.deep_dragongem, 1, 15),
                (ItemsType.ceadeus_fur, 1, 18),
                (ItemsType.elderdragonblood, 1, 13)
            ],
            'rewards_row_2': [
                (ItemsType.sunspire_jewel, 1, 12),
                (ItemsType.ceadeus_hide, 1, 18),
                (ItemsType.ceadeus_scale, 1, 30),
                (ItemsType.monster_bone_l, 1, 15),
                (ItemsType.aquaglow_jewel, 1, 25)
            ],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00002000,
            'objective_type': 0x0001,
            'objective_num': 0x00,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0,
            'objective_type': Monster.none,
            'objective_num': 0,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000005,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    }
}

# ---------- ARENA QUESTS ----------

"""
00 00 00 28
00 00 00 FF
FF
01
01
03
00 00 00 00
BF 00 00 00
C5 9D 74 00
C5 3E 2B 33
00 00 00 00
FF FF A4 00
00 00 00 00
FF 00 00 00
00 00 00 00
"""

GRUDGE_MATCH_QURUPECO = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA60,
        'name': "Grudge Match: Qurupeco",
        'client': "Announcer/Receptionist",
        'description': "Slay a Qurupeco",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 200,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.qurupeco,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.qurupeco,
            'objective_num': 0x01,
            'zenny_reward': 500,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.qurupeco_coin, 1, 27),
                (ItemsType.qurupeco_coin, 2, 10),
                (ItemsType.voucher, 1, 10),
                (ItemsType.armor_sphere, 1, 22),
                (ItemsType.steel_eg, 1, 16),
                (ItemsType.pinnacle_coin, 1, 15)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.AziDahaka),
            None, None,
            Helmet.RangersHeadgear, Chestpiece.RangersGirdle,
            Gauntlets.RangersGauntlets, Faulds.RangersFaulds,
            Leggings.RangersEspadrilles,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.might_seed, 5),
             (ItemsType.firedouse_berry, 2), (ItemsType.pitfall_trap, 1),
             (ItemsType.sonic_bomb, 2), (ItemsType.ez_barrel_bomb_l, 1),
             (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Greatsword, Greatsword.BusterSwordPlus),
            None, None,
            Helmet.AlloyHelm, Chestpiece.SteelMail,
            Gauntlets.AlloyVambraces, Faulds.SteelFaulds,
            Leggings.BaggiGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.WarHammerPlus),
            None, None,
            Helmet.JaggiHelm, Chestpiece.HuntersMail,
            Gauntlets.BlastBracelet, Faulds.BarrothFaulds,
            Leggings.BoneGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.mega_dash_juice, 1),
             (ItemsType.ez_flash_bomb, 1), (ItemsType.ez_barrel_bomb_l, 1),
             (ItemsType.barrel_bomb_s, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.LightBowgun),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.RoyalLauncher),
            (EquipmentClasses.BowgunStock, BowgunStock.RoyalLauncher),
            Helmet.BarrothCap, Chestpiece.BarrothVest,
            Gauntlets.NoEquipment, Faulds.HuntersCoat,
            Leggings.AlloyLeggings,
            ((ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.ez_flash_bomb, 1), (ItemsType.barrel_bomb_l, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99),
             (ItemsType.clust_s_lv1, 5), (ItemsType.pellet_s_lv1, 50),
             (ItemsType.armor_s_i, 3), (ItemsType.para_s_lv1, 12)),
        )
    )
}

GRUDGE_MATCH_ROYAL_LUDROTH = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA61,
        'name': "Grudge Match: Royal Ludroth",
        'client': "Announcer/Receptionist",
        'description': "Slay a Royal Ludroth",
        'details':
            "Ahoy, adrenaline junkies!\n"
            "Next up is the regally maned\n"
            "Royal Ludroth! Will the pressure\n"
            "of facing this sea dragon on\n"
            "its home surf with a strict\n"
            "time limit leave the hunters\n"
            "all washed up?",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_1,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.royal_ludroth,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.r_ludroth_coin, 1, 24),
                (ItemsType.r_ludroth_coin, 2, 8),
                (ItemsType.voucher, 1, 10),
                (ItemsType.armor_sphere, 1, 24),
                (ItemsType.steel_eg, 1, 18),
                (ItemsType.pinnacle_coin, 1, 16)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.HydraKnife),
            None, None,
            Helmet.QurupecoHelm, Chestpiece.QurupecoMail,
            Gauntlets.BlastBracelet, Faulds.SteelFaulds,
            Leggings.IngotGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.barrel_bomb_l, 3),
             (ItemsType.barrel_bomb_s, 10)),
            ()
        ),
        (
            (EquipmentClasses.Greatsword, Greatsword.ChieftainsGrtSwd),
            None, None,
            Helmet.DrawEarring, Chestpiece.SteelMail,
            Gauntlets.GobulVambraces, Faulds.GobulFaulds,
            Leggings.HuntersGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10),
             (ItemsType.might_pill, 2), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.BoneBludgeon),
            None, None,
            Helmet.BarrothHelm, Chestpiece.BarrothMail,
            Gauntlets.AlloyVambraces, Faulds.BarrothFaulds,
            Leggings.BarrothGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.oxygen_supply, 10),
             (ItemsType.paralysis_knife, 5), (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.RoyalLauncher),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.JaggidFire),
            (EquipmentClasses.BowgunStock, BowgunStock.LightBowgun),
            Helmet.AlloyCap, Chestpiece.AlloyVest,
            Gauntlets.LagiacrusGuards, Faulds.AlloyCoat,
            Leggings.PiscineLeggings,
            ((ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.oxygen_supply, 10), (ItemsType.lifepowder, 2),
             (ItemsType.shock_trap, 1), (ItemsType.barrel_bomb_l_plus, 2),
             (ItemsType.barrel_bomb_l, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv1, 60),
             (ItemsType.pierce_s_lv2, 50), (ItemsType.clust_s_lv1, 5),
             (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12))
        )
    )
}

GRUDGE_MATCH_RATHIAN = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA62,
        'name': "Grudge Match: Rathian",
        'client': "Announcer/Receptionist",
        'description': "Slay a Rathian",
        'details':
            "Hey there, fight fanatics!\n"
            "Tonight's target is the Queen of\n"
            "the Land, Rathian! A fan of\n"
            "flame attacks, she also packs a\n"
            "potent charge from on high!\n"
            "Hunters better wear asbestos\n"
            "underwear for this fight!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x001a,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.rathian,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x1a,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.rathian,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.rathian_coin, 1, 21),
                (ItemsType.rathian_coin, 2, 7),
                (ItemsType.voucher, 1, 13),
                (ItemsType.armor_sphere_plus, 1, 8),
                (ItemsType.armor_sphere, 1, 14),
                (ItemsType.steel_eg, 1, 19),
                (ItemsType.pinnacle_coin, 1, 18)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Switchaxe, Switchaxe.RoughEdge),
            None, None,
            Helmet.SilenceEarring, Chestpiece.BoneMail,
            Gauntlets.BariothVambraces, Faulds.BariothFaulds,
            Leggings.BariothGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.lifepowder, 2),
             (ItemsType.antidote, 2), (ItemsType.dung_bomb, 1),
             (ItemsType.ez_flash_bomb, 2), (ItemsType.ez_barrel_bomb_l, 1),
             (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.Thunderclap),
            None, None,
            Helmet.ChargeEarring, Chestpiece.RathianMail,
            Gauntlets.RathianVambraces, Faulds.IngotCoil,
            Leggings.QurupecoGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.lifepowder, 2),
             (ItemsType.antidote, 2), (ItemsType.dung_bomb, 1),
             (ItemsType.ez_shock_trap, 1), (ItemsType.ez_flash_bomb, 1),
             (ItemsType.barrel_bomb_l, 2), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.AzureCrest),
            None, None,
            Helmet.GigginoxHelm, Chestpiece.GigginoxMail,
            Gauntlets.AgnaktorVambraces, Faulds.BnahabraCoil,
            Leggings.BnahabraBoots,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 2), (ItemsType.dung_bomb, 1),
             (ItemsType.firedouse_berry, 2), (ItemsType.ez_flash_bomb, 1),
             (ItemsType.barrel_bomb_l, 1), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.HeavyBowgun),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.JaggidFire),
            (EquipmentClasses.BowgunStock, BowgunStock.HeavyBowgun),
            Helmet.BoneCap, Chestpiece.IngotVest,
            Gauntlets.IngotGuards, Faulds.BoneCoat,
            Leggings.AlloyLeggings,
            ((ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.antidote, 2), (ItemsType.lifepowder, 2),
             (ItemsType.dung_bomb, 1), (ItemsType.barrel_bomb_l, 1)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv1, 60),
             (ItemsType.clust_s_lv1, 5), (ItemsType.wyvernfire_lv1, 9),
             (ItemsType.para_s_lv1, 12), (ItemsType.sleep_s_lv1, 12),
             (ItemsType.exhaust_s, 10)),
        )
    )
}

GRUDGE_MATCH_LAGIACRUS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA63,
        'name': "Grudge Match: Lagiacrus",
        'client': "Announcer/Receptionist",
        'description': "Slay a Lagiacrus",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.lagiacrus,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.lagiacrus,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.lagiacrus_coin, 1, 21),
                (ItemsType.lagiacrus_coin, 2, 7),
                (ItemsType.voucher, 1, 13),
                (ItemsType.armor_sphere_plus, 1, 8),
                (ItemsType.armor_sphere, 1, 13),
                (ItemsType.steel_eg, 1, 20),
                (ItemsType.pinnacle_coin, 1, 18)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Switchaxe, Switchaxe.BlitzkriegB),
            None, None,
            Helmet.SilenceEarring, Chestpiece.LagiacrusMail,
            Gauntlets.UpstreamBracelet, Faulds.LagiacrusFaulds,
            Leggings.LagiacrusGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.stormsender_seed, 2), (ItemsType.lifepowder, 2),
             (ItemsType.poison_knife, 5), (ItemsType.flash_bomb, 2),
             (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.WyvernBladeFire),
            None, None,
            Helmet.BariothHelm, Chestpiece.BariothMail,
            Gauntlets.BariothVambraces, Faulds.ChainmailBelt,
            Leggings.ChainmailPants,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.sleep_knife, 5),
             (ItemsType.shock_trap, 1)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.SmaltCraterR),
            None, None,
            Helmet.DemonEdgeEarring, Chestpiece.BarrothMail,
            Gauntlets.RathalosVambraces, Faulds.RathalosFaulds,
            Leggings.RathalosGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.might_seed, 3),
             (ItemsType.shock_trap, 1), (ItemsType.flash_bomb, 1),
             (ItemsType.barrel_bomb_l, 2), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.TropecoGun),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.TropecoGun),
            (EquipmentClasses.BowgunStock, BowgunStock.TropecoGun),
            Helmet.JumpEarring, Chestpiece.LudrothVest,
            Gauntlets.LudrothGuards, Faulds.GigginoxCoat,
            Leggings.LudrothLeggings,
            ((ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.mini_oxy_supply, 10), (ItemsType.lifepowder, 2),
             (ItemsType.ez_barrel_bomb_l, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99),
             (ItemsType.crag_s_lv1, 9), (ItemsType.recov_s_lv1, 12),
             (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12),
             (ItemsType.flaming_s, 60))
        )
    )
}

GRUDGE_MATCH_URAGAAN = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -1404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -3404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -5404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -4404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type':Monster.fly_wyv, 'unk1': 3, 'unk2': 0xFF,
                'variant': 8, 'room': 1, 'quantity': -1,
                'pos_x': -2404.5,'pos_y': -4038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA64,
        'name': "Grudge Match: Uragaan",
        'client': "Announcer/Receptionist",
        'description': "Slay an Uragaan",
        'details':
            "Riled up, fight fans? Here comes\n"
            "a dragon whose name is\n"
            "synonymous with pain: Uragaan!\n"
            "Oh, and we've added a time limit\n"
            "to make the fight extra fun. Are\n"
            "the hunters up to the challenge?\n"
            "Outlook not good!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 600,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_2,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0017,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 1500,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.uragaan_coin, 1, 19),
                (ItemsType.uragaan_coin, 2, 7),
                (ItemsType.voucher, 1, 14),
                (ItemsType.armor_sphere_plus, 1, 8),
                (ItemsType.armor_sphere, 1, 12),
                (ItemsType.steel_eg, 1, 20),
                (ItemsType.pinnacle_coin, 1, 20)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.ShadowSaberPlus),
            None, None,
            Helmet.RathianHelm, Chestpiece.BnahabraSuit,
            Gauntlets.GigginoxVambraces, Faulds.BnahabraCoil,
            Leggings.BnahabraBoots,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.firedouse_berry, 2), (ItemsType.lifepowder, 2),
             (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 2),
             (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.AnantaBonebladePlus),
            None, None,
            Helmet.SwordSaintEarring, Chestpiece.AgnaktorMail,
            Gauntlets.GrinderBracelet, Faulds.RathalosFaulds,
            Leggings.AgnaktorGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.lifepowder, 2), (ItemsType.paralysis_knife, 5),
             (ItemsType.pitfall_trap, 1), (ItemsType.ez_flash_bomb, 1),
             (ItemsType.ez_barrel_bomb_l, 2), (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.CarapaceHammerPlus),
            None, None,
            Helmet.DiablosHelm, Chestpiece.DiablosMail,
            Gauntlets.PepBracelet, Faulds.HuntersFaulds,
            Leggings.UragaanGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.dash_juice, 1), (ItemsType.ez_flash_bomb, 1),
             (ItemsType.ez_barrel_bomb_l, 1), (ItemsType.barrel_bomb_s, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.JaggidFire),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.RoyalLauncher),
            (EquipmentClasses.BowgunStock, BowgunStock.Thundacrus),
            Helmet.BarrageEarring, Chestpiece.RathianVest,
            Gauntlets.RathianGuards, Faulds.RathianCoat,
            Leggings.RathianLeggings,
            ((ItemsType.mega_potion, 10), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.lifepowder, 2),
             (ItemsType.barrel_bomb_l, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv1, 60),
             (ItemsType.pierce_s_lv2, 50), (ItemsType.crag_s_lv2, 9),
             (ItemsType.water_s, 30)),
        )
    )
}

GRUDGE_MATCH_WYVERN_TRIO = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA65,
        'name': "Grudge Match: Wyvern Trio",
        'client': "Announcer/Receptionist",
        'description': "Slay all 3 monsters",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 1, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 1200,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_LAND_ARENA_1,
        'quest_rank': QuestRankType.star_3,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_NONE,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0028,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x28,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.barioth,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x28,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x28,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00020101,
            'objective_type': Monster.barroth,
            'objective_num': 0x01,
            'zenny_reward': 3000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.barroth_coin, 1, 5),
                (ItemsType.barioth_coin, 1, 15),
                (ItemsType.rathalos_coin, 1, 22),
                (ItemsType.voucher, 1, 14),
                (ItemsType.armor_sphere_plus, 1, 12),
                (ItemsType.silver_eg, 1, 8),
                (ItemsType.pinnacle_coin, 1, 24)
            ],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00020101,
            'objective_type': Monster.barioth,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
        'subquest_2': {
            'description': "None",
            'type': 0x00020101,
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 0,
            'hrp_reward': 0x00000000,
            'rewards_row_1': [],
        },
    },
    'unknown': {
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Switchaxe, Switchaxe.BoltAxe),
            None, None,
            Helmet.ChargeEarring, Chestpiece.RathalosMail,
            Gauntlets.RathalosVambraces, Faulds.RathalosFaulds,
            Leggings.RathalosGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 3), (ItemsType.dung_bomb, 1),
             (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 2), (ItemsType.ez_barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Greatsword, Greatsword.GolemBladePlus),
            None, None,
            Helmet.UragaanHelm, Chestpiece.UragaanMail,
            Gauntlets.UragaanVambraces, Faulds.UragaanFaulds,
            Leggings.UragaanGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 3), (ItemsType.dung_bomb, 1),
             (ItemsType.paralysis_knife, 5), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 2), (ItemsType.ez_barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_s, 2)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.GobuluMurukaPlus),
            None, None,
            Helmet.AgnaktorHelm, Chestpiece.AgnaktorMail,
            Gauntlets.RathalosVambraces, Faulds.AgnaktorFaulds,
            Leggings.AgnaktorGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.mega_potion, 10),
             (ItemsType.potion, 10), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 3), (ItemsType.dung_bomb, 1),
             (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1),
             (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.Agnablaster),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.Thundacrus),
            (EquipmentClasses.BowgunStock, BowgunStock.RathlingGun),
            Helmet.KirinEarring, Chestpiece.BariothVest,
            Gauntlets.BariothGuards, Faulds.BariothCoat,
            Leggings.BariothLeggings,
            ((ItemsType.mega_potion, 10), (ItemsType.potion, 10),
             (ItemsType.ration, 10), (ItemsType.cleanser, 5),
             (ItemsType.antidote, 2), (ItemsType.lifepowder, 3),
             (ItemsType.dung_bomb, 1), (ItemsType.pitfall_trap, 1),
             (ItemsType.ez_barrel_bomb_l, 2), (ItemsType.ez_flash_bomb, 2),
             (ItemsType.flaming_s, 60), (ItemsType.thunder_s, 60)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv2, 50),
             (ItemsType.pellet_s_lv1, 60), (ItemsType.pellet_s_lv2, 60),
             (ItemsType.clust_s_lv2, 5), (ItemsType.clust_s_lv3, 5),
             (ItemsType.wyvernfire_lv2, 10), (ItemsType.para_s_lv1, 12),
             (ItemsType.demon_s_ii, 5))
        )
    )
}

GRUDGE_MATCH_BIRD_BRUTE = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA66,
        'name': "Grudge Match: Bird and Brute",
        'client': "Announcer/Receptionist",
        'description':
            "Slay a Qurupeco\n"
            "and a Barroth",
        'details':
            "Double trouble! It's the\n"
            "dirty-bird Qurupeco and the\n"
            "land dragon Barroth -- heaven\n"
            "and earth, laughter and tears,\n"
            "in an ultimate contest! When\n"
            "the dust clears, will it\n"
            "reveal victory? Or tragedy?",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
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
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.qurupeco,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.qurupeco,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.qurupeco_coin, 1, 16),
                (ItemsType.barroth_coin, 1, 20),
                (ItemsType.voucher, 1, 14),
                (ItemsType.armor_sphere_plus, 1, 10),
                (ItemsType.adv_armor_sphere, 1, 5),
                (ItemsType.steel_eg, 1, 15),
                (ItemsType.silver_eg, 1, 5),
                (ItemsType.hunter_king_coin, 1, 15)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Switchaxe, Switchaxe.AssaultAxePlus),
            None, None,
            Helmet.GigginoxCapPlus, Chestpiece.AlloyMail,
            Gauntlets.BaggiVambracesPlus, Faulds.GigginoxFauldsPlus,
            Leggings.GigginoxGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.lifepowder, 1), (ItemsType.ez_shock_trap, 1),
             (ItemsType.ez_flash_bomb, 2)),
            ()
        ),
        (
            (EquipmentClasses.Greatsword, Greatsword.CataclysmSword),
            None, None,
            Helmet.DrawEarring, Chestpiece.JaggiMailPlus,
            Gauntlets.JaggiVambracesPlus, Faulds.JaggiFauldsPlus,
            Leggings.BoneGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.barrel_bomb_l, 3),
             (ItemsType.barrel_bomb_s, 2), (ItemsType.pitfall_trap, 1),
             (ItemsType.ez_flash_bomb, 2)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.Undertaker),
            None, None,
            Helmet.DiablosCap, Chestpiece.AgnaktorMailPlus,
            Gauntlets.SteelVambracesPlus, Faulds.SteelCoilPlus,
            Leggings.AlloyGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.PoisonStinger),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.RathlingGunPlus),
            (EquipmentClasses.BowgunStock, BowgunStock.LightBowgun),
            Helmet.AgnaktorCapPlus, Chestpiece.AgnaktorVestPlus,
            Gauntlets.AgnaktorGuardsPlus, Faulds.AgnaktorCoatPlus,
            Leggings.RathalosLeggingsPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.cleanser, 5),
             (ItemsType.lifepowder, 2), (ItemsType.ez_flash_bomb, 1),
             (ItemsType.sonic_bomb, 2)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99),
             (ItemsType.pierce_s_lv2, 50), (ItemsType.clust_s_lv2, 5),
             (ItemsType.crag_s_lv2, 9), (ItemsType.poison_s_lv1, 12),
             (ItemsType.para_s_lv1, 12), (ItemsType.sleep_s_lv1, 12))
        )
    )
}

GRUDGE_MATCH_SEA_POWER = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -0.5,'pos_y': -5038.5,'pos_z': -3042.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA67,
        'name': "Grudge Match: Sea Power",
        'client': "Announcer/Receptionist",
        'description':
            "Slay a Royal Ludroth\n"
            "and a Gobul",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 350,
        'quest_fee': 0,
        'time_limit': 50,
        'main_monster_1': Monster.none,
        'main_monster_2': Monster.none,
        'location': LocationType.QUEST_LOCATION_WATER_ARENA_2,
        'quest_rank': QuestRankType.star_4,
        'hrp_restriction': QuestRestrictionType.RESTRICTION_31_INITJOIN,
        'resources': ResourcesType.arena,
        'supply_set_number': 0,
        'starting_position': StartingPositionType.camp,
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.royal_ludroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c   0x17,  0x37, or 0x3a
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.gobul,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.royal_ludroth,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.gobul_coin, 1, 10),
                (ItemsType.r_ludroth_coin, 2, 23),
                (ItemsType.voucher, 1, 14),
                (ItemsType.armor_sphere_plus, 1, 10),
                (ItemsType.adv_armor_sphere, 1, 6),
                (ItemsType.steel_eg, 1, 16),
                (ItemsType.silver_eg, 1, 6),
                (ItemsType.hunter_king_coin, 1, 15)
            ],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000101,
            'objective_type': Monster.gobul,
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Switchaxe, Switchaxe.VoltAxeY),
            None, None,
            Helmet.PiscineMaskPlus, Chestpiece.LagiacrusMailPlus,
            Gauntlets.BaggiVambracesPlus, Faulds.PiscineBeltPlus,
            Leggings.PiscineLeggingsPlus,
            ((ItemsType.mega_potion, 10), (ItemsType.whetstone, 20),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 2)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.DancingHellfire),
            None, None,
            Helmet.RathianHelmPlus, Chestpiece.RathianMailPlus,
            Gauntlets.ChainmailVambracesPlus, Faulds.AlloyCoil,
            Leggings.AlloyGreaves,
            ((ItemsType.mega_potion, 10), (ItemsType.whetstone, 20),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_s, 2), (ItemsType.ez_flash_bomb, 3)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.CarapaceHammerPlus),
            None, None,
            Helmet.StimulusEarring, Chestpiece.DoberMail,
            Gauntlets.DoberVambraces, Faulds.BoneFauldsPlus,
            Leggings.BoneGreavesPlus,
            ((ItemsType.mega_potion, 10), (ItemsType.whetstone, 20),
             (ItemsType.ration, 10), (ItemsType.mini_oxy_supply, 10),
             (ItemsType.lifepowder, 2), (ItemsType.mega_dash_juice, 1),
             (ItemsType.paralysis_knife, 5), (ItemsType.shock_trap, 1),
             (ItemsType.flash_bomb, 1), (ItemsType.ez_barrel_bomb_l, 1),
             (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 2),
             (ItemsType.powercharm, 1), (ItemsType.powertalon, 1)),
            ()
        ),
        (  # rathling gun barrel, rathling gun + frame, rathling gun + stock
            (EquipmentClasses.BowgunFrame, BowgunFrame.RathlingGunPlus),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.RathlingGunPlus),  # RathlingGun),
            (EquipmentClasses.BowgunStock, BowgunStock.RathlingGunPlus),
            Helmet.LagiacrusCapPlus, Chestpiece.LagiacrusVestPlus,
            Gauntlets.LagiacrusGuardsPlus, Faulds.LagiacrusCoatPlus,
            Leggings.LagiacrusLeggingsPlus,
            ((ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.mini_oxy_supply, 10), (ItemsType.lifepowder, 2),
             (ItemsType.flash_bomb, 2), (ItemsType.shock_trap, 1),
             (ItemsType.ez_barrel_bomb_l, 2), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99),
             (ItemsType.pierce_s_lv2, 50), (ItemsType.wyvernfire_lv2, 10),
             (ItemsType.flaming_s, 60))
        )
    )
}

GRUDGE_MATCH_TWO_FLAMES = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA68,
        'name': "Grudge Match: The Two Flames",
        'client': "Announcer/Receptionist",
        'description':
            "Slay a Rathalos\n"
            "and a Rathian",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
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
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.rathian,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.rathalos,
            'objective_num': 0x01,
            'zenny_reward': 1000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.rathalos_coin, 1, 10),
                (ItemsType.rathian_coin, 1, 24),
                (ItemsType.voucher, 1, 14),
                (ItemsType.armor_sphere_plus, 1, 10),
                (ItemsType.adv_armor_sphere, 1, 5),
                (ItemsType.steel_eg, 1, 15),
                (ItemsType.silver_eg, 1, 5),
                (ItemsType.hunter_king_coin, 1, 17)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.IcicleSpikePlus),
            None, None,
            Helmet.QurupecoHelmPlus, Chestpiece.QurupecoMailPlus,
            Gauntlets.QurupecoVambracesPlus, Faulds.QurupecoCoilPlus,
            Leggings.QurupecoGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.might_pill, 2), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 1), (ItemsType.dung_bomb, 1),
             (ItemsType.paralysis_knife, 5), (ItemsType.pitfall_trap, 1),
             (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 1),
             (ItemsType.barrel_bomb_s, 1)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.Thunderclap),
            None, None,
            Helmet.SilenceEarring, Chestpiece.AlloyMailPlus,
            Gauntlets.SteelVambracesPlus, Faulds.SteelCoilPlus,
            Leggings.VangisGreaves,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.antidote, 2), (ItemsType.lifepowder, 1),
             (ItemsType.dung_bomb, 1), (ItemsType.ez_flash_bomb, 2)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.SpiralLancePlus),
            None, None,
            Helmet.DemonEdgeEarring, Chestpiece.IngotMailPlus,
            Gauntlets.AgnaktorVambracesPlus, Faulds.RhenoplosCoilPlus,
            Leggings.IngotGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.well_done_steak, 10),
             (ItemsType.antidote, 2), (ItemsType.lifepowder, 1),
             (ItemsType.dung_bomb, 1), (ItemsType.poison_knife, 5),
             (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.ThundacrusRex),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.ThundacrusRex),
            (EquipmentClasses.BowgunStock, BowgunStock.BlizzardCannon),
            Helmet.EarringofFate, Chestpiece.UragaanVestPlus,
            Gauntlets.BlastBracelet, Faulds.UragaanCoatPlus,
            Leggings.UragaanLeggingsPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.ration, 10), (ItemsType.antidote, 2),
             (ItemsType.lifepowder, 2), (ItemsType.dung_bomb, 1),
             (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1),
             (ItemsType.pitfall_trap, 1), (ItemsType.ez_barrel_bomb_l, 1),
             (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99),
             (ItemsType.pierce_s_lv3, 40), (ItemsType.demon_s_ii, 5),
             (ItemsType.thunder_s, 60))
        )
    )
}

GRUDGE_MATCH_ICE_AND_FIRE = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA69,
        'name': "Grudge Match: Ice and Fire",
        'client': "Announcer/Receptionist",
        'description':
            "Slay a Barioth\n"
            "and an Agnaktor",
        'details':
            "Double trouble! The forecast\n"
            "today calls for a storm of fire\n"
            "and ice -- with a 90 percent\n"
            "chance of death -- as you take\n"
            "on both Barioth and Agnaktor at\n"
            "once! Days like this I just\n"
            "wanna stay in bed.",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 250,
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
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barioth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.agnaktor,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.barioth,
            'objective_num': 0x01,
            'zenny_reward': 1500,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.agnaktor_coin, 1, 13),
                (ItemsType.barioth_coin, 1, 20),
                (ItemsType.voucher, 1, 14),
                (ItemsType.adv_armor_sphere, 1, 8),
                (ItemsType.hrd_armor_sphere, 1, 5),
                (ItemsType.steel_eg, 1, 13),
                (ItemsType.silver_eg, 1, 8),
                (ItemsType.hunter_king_coin, 1, 19)
            ],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000101,
            'objective_type': Monster.agnaktor,
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.BlazingFalchion),
            None, None,
            Helmet.GobulHelmPlus, Chestpiece.GobulMailPlus,
            Gauntlets.GobulVambracesPlus, Faulds.GobulFauldsPlus,
            Leggings.GobulGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.lifepowder, 2),
             (ItemsType.poison_knife, 5), (ItemsType.paralysis_knife, 5),
             (ItemsType.shock_trap, 1), (ItemsType.flash_bomb, 2),
             (ItemsType.sonic_bomb, 2), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_s, 2), (ItemsType.max_potion, 1)),
            ()
        ),
        (
            (EquipmentClasses.Greatsword, Greatsword.RathalosFlamesword),
            None, None,
            Helmet.BaggiHelmPlus, Chestpiece.BaggiMailPlus,
            Gauntlets.BaggiVambracesPlus, Faulds.BaggiCoilPlus,
            Leggings.BaggiGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.lifepowder, 2),
             (ItemsType.firedouse_berry, 2), (ItemsType.paralysis_knife, 5),
             (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 1), (ItemsType.barrel_bomb_l, 3),
             (ItemsType.barrel_bomb_s, 2), (ItemsType.max_potion, 1)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.GreatGaiarchG),
            None, None,
            Helmet.DemonEdgeEarring, Chestpiece.GobulMailPlus,
            Gauntlets.RathalosVambracesPlus, Faulds.RathalosFauldsPlus,
            Leggings.RathalosGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.lifepowder, 2),
             (ItemsType.mega_dash_juice, 2), (ItemsType.sleep_knife, 5),
             (ItemsType.shock_trap, 1), (ItemsType.flash_bomb, 2),
             (ItemsType.sonic_bomb, 2), (ItemsType.max_potion, 2)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.BarbrianSharqP),
            None, None,
            Helmet.BariothHelmPlus, Chestpiece.BariothMailPlus,
            Gauntlets.BariothVambracesPlus, Faulds.BariothFauldsPlus,
            Leggings.BariothGreavesPlus,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.whetstone, 20), (ItemsType.ration, 10),
             (ItemsType.cleanser, 5), (ItemsType.lifepowder, 2),
             (ItemsType.firedouse_berry, 2), (ItemsType.poison_knife, 5),
             (ItemsType.shock_trap, 1), (ItemsType.ez_flash_bomb, 2),
             (ItemsType.ez_barrel_bomb_l, 1), (ItemsType.max_potion, 2)),
            ()
        )
    )
}

GRUDGE_MATCH_BRUTE_HORNS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA6A,
        'name': "Grudge Match: Brute Horns",
        'client': "Announcer/Receptionist",
        'description':
            "Slay an Uragaan\n"
            "and a Diablos",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 1, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
        'penalty_per_cart': 700,
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
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x12,  # 0x01 through 0x3c   0x0f, 0x12, or 0x38
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.diablos,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.none,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x00,
            'level': 0x00,  # 0x01 through 0x3c
            'size': 0x00,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00000101,
            'objective_type': Monster.uragaan,
            'objective_num': 0x01,
            'zenny_reward': 2000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.diablos_coin, 1, 10),
                (ItemsType.uragaan_coin, 1, 20),
                (ItemsType.voucher, 1, 10),
                (ItemsType.adv_armor_sphere, 1, 10),
                (ItemsType.hrd_armor_sphere, 1, 5),
                (ItemsType.steel_eg, 1, 15),
                (ItemsType.silver_eg, 1, 8),
                (ItemsType.hunter_king_coin, 1, 22)
            ],
            'rewards_row_2': [],
        },
        'subquest_1': {
            'description': "None",
            'type': 0x00000101,
            'objective_type': Monster.diablos,
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.Greatsword, Greatsword.HighSieglindeP),
            None, None,
            Helmet.SwordSaintEarring, Chestpiece.SteelMailPlus,
            Gauntlets.SteelVambracesPlus, Faulds.SteelCoilPlus,
            Leggings.LagiacrusGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 20), (ItemsType.well_done_steak, 10),
             (ItemsType.paralysis_knife, 5), (ItemsType.pitfall_trap, 1),
             (ItemsType.ez_flash_bomb, 2), (ItemsType.sonic_bomb, 2),
             (ItemsType.ez_barrel_bomb_l, 2), (ItemsType.max_potion, 2)),
            ()
        ),
        (
            (EquipmentClasses.Hammer, Hammer.JhenMohranHammer),
            None, None,
            Helmet.ChargeEarring, Chestpiece.DamascusMail,
            Gauntlets.DiablosVambracesPlus, Faulds.IngotCoilPlus,
            Leggings.AgnaktorGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.lifepowder, 2), (ItemsType.sleep_knife, 5),
             (ItemsType.poison_knife, 5), (ItemsType.shock_trap, 1),
             (ItemsType.flash_bomb, 2), (ItemsType.sonic_bomb, 2),
             (ItemsType.max_potion, 2)),
            ()
        ),
        (
            (EquipmentClasses.Lance, Lance.SabertoothG),
            None, None,
            Helmet.LudrothCapPlus, Chestpiece.LudrothMailPlus,
            Gauntlets.PepBracelet, Faulds.VangisCoil,
            Leggings.DamascusGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.lifepowder, 2), (ItemsType.shock_trap, 1),
             (ItemsType.ez_shock_trap, 1), (ItemsType.flash_bomb, 2),
             (ItemsType.sonic_bomb, 2), (ItemsType.barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_s, 2), (ItemsType.max_potion, 1)),
            ()
        ),
        (
            (EquipmentClasses.Switchaxe, Switchaxe.InceadeusPlus),
            None, None,
            Helmet.DiablosHelmPlus, Chestpiece.DiablosMailPlus,
            Gauntlets.DiablosVambracesPlus, Faulds.LagiacrusFauldsPlus,
            Leggings.LagiacrusGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.ration, 10),
             (ItemsType.lifepowder, 2), (ItemsType.shock_trap, 1),
             (ItemsType.flash_bomb, 2), (ItemsType.sonic_bomb, 2),
             (ItemsType.barrel_bomb_l, 2), (ItemsType.max_potion, 2)),
            ()
        )
    )
}

GRUDGE_MATCH_LAND_LORDS = {
    'small_monsters': [
        [
            # Area 0
        ],
        [
            # Area 1
            {
                'type': Monster.fly_wyv,'unk1': 1,'unk2': 0xFF,
                'variant': 3,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 170,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
            {
                'type': Monster.fly_wyv,'unk1': 3,'unk2': 0xFF,
                'variant': 8,'room': 1,'quantity': -1,
                'pos_x': -2404.5,'pos_y': -5038.5,'pos_z': -3542.7,
                'rot_x': 0,'rot_y': 1828,'rot_z': 0,
            },
        ],
    ],
    'quest_info': {
        'quest_id': 0xEA6B,
        'name': "Grudge Match: Land Lords",
        'client': "Announcer/Receptionist",
        'description': "Slay all 3 monsters",
        'details':
            "Wanted:\n"
            "The description for this\n"
            "quest! If you can find\n"
            "it, please let us know!\n"
            "Thanks!",
        'success_message': "Complete the Main Quest.",
        'flags': (
            (0, 0, 1, 0, 0, 1, 0, 0),
            (1, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 1, 0, 1, 0)
        ),
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
        'general_enemy_level': 0x0037,
        'summon': 0x00000000,
        'wave_1_transition_type': WaveType.none,
        'wave_1_transition_target': 0x0000,
        'wave_1_transition_quantity': 0x0000,
        'wave_2_transition_type': WaveType.none,
        'wave_2_transition_target': 0x0000,
        'wave_2_transition_quantity': 0x0000,
    },
    'large_monsters': {
        'monster_1': {
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x37,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x37,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.deviljho,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x38,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        }
    },
    'objective_details': {
        'main_quest': {
            'type': 0x00020101,
            'objective_type': Monster.barroth,
            'objective_num': 0x01,
            'zenny_reward': 3000,
            'hrp_reward': 0,
            'rewards_row_1': [
                (ItemsType.deviljho_coin, 1, 10),
                (ItemsType.barroth_coin, 1, 10),
                (ItemsType.uragaan_coin, 1, 15),
                (ItemsType.voucher, 1, 14),
                (ItemsType.adv_armor_sphere, 1, 10),
                (ItemsType.hrd_armor_sphere, 1, 7),
                (ItemsType.silver_eg, 1, 10),
                (ItemsType.hunter_king_coin, 1, 24)
            ],
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
        # 2 for large mon quest, 3 for small/delivery, 5 for jhen/ala
        'unk_12': 0x00000002,
        'unk_4': 0x00,
        'unk_5': 0x00,
        'unk_6': 0x00,
        'unk_7': 0x00000000,
    },
    'arena_equipment': (
        (
            (EquipmentClasses.SnS, SnS.PlagueTabar),
            None, None,
            Helmet.UragaanHelmPlus, Chestpiece.UragaanMailPlus,
            Gauntlets.UragaanVambracesPlus, Faulds.UragaanFauldsPlus,
            Leggings.UragaanGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5),
             (ItemsType.lifepowder, 3), (ItemsType.paralysis_knife, 5),
             (ItemsType.sleep_knife, 5), (ItemsType.poison_knife, 5),
             (ItemsType.tinged_meat, 5), (ItemsType.druged_meat, 5),
             (ItemsType.poisoned_meat, 5), (ItemsType.pitfall_trap, 1),
             (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1),
             (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 2),
             (ItemsType.barrel_bomb_l, 3), (ItemsType.barrel_bomb_s, 10),
             (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1),
             (ItemsType.powercharm, 1), (ItemsType.armorcharm, 1),
             (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ()
        ),
        (
            (EquipmentClasses.Switchaxe, Switchaxe.GreatDemonbindG),
            None, None,
            Helmet.RathalosHelmPlus, Chestpiece.RathalosMailPlus,
            Gauntlets.RathalosVambracesPlus, Faulds.RathalosFauldsPlus,
            Leggings.RathalosGreavesPlus,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5),
             (ItemsType.lifepowder, 3), (ItemsType.dung_bomb, 5),
             (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5),
             (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
             (ItemsType.druged_meat, 5), (ItemsType.poisoned_meat, 5),
             (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1),
             (ItemsType.ez_flash_bomb, 5), (ItemsType.barrel_bomb_l_plus, 1),
             (ItemsType.max_potion, 2), (ItemsType.ancient_potion, 1),
             (ItemsType.powercharm, 1), (ItemsType.armorcharm, 1),
             (ItemsType.powertalon, 1), (ItemsType.armortalon, 1)),
            ()
        ),
        (
            (EquipmentClasses.Longsword, Longsword.ReaverCalamity),
            None, None,
            Helmet.StimulusEarring, Chestpiece.VangisMail,
            Gauntlets.DoberVambraces, Faulds.DoberCoil,
            Leggings.DamascusGreaves,
            ((ItemsType.whetstone, 20), (ItemsType.potion, 10),
             (ItemsType.mega_potion, 10), (ItemsType.energy_drink, 5),
             (ItemsType.cleanser, 5), (ItemsType.lifepowder, 5),
             (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5),
             (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
             (ItemsType.druged_meat, 5), (ItemsType.poisoned_meat, 5),
             (ItemsType.pitfall_trap, 1), (ItemsType.shock_trap, 1),
             (ItemsType.ez_shock_trap, 1), (ItemsType.ez_flash_bomb, 5),
             (ItemsType.barrel_bomb_l_plus, 2), (ItemsType.barrel_bomb_l, 3),
             (ItemsType.barrel_bomb_s, 10), (ItemsType.max_potion, 2),
             (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1),
             (ItemsType.armorcharm, 1), (ItemsType.armortalon, 1)),
            ()
        ),
        (
            (EquipmentClasses.BowgunFrame, BowgunFrame.Diablazooka),
            (EquipmentClasses.BowgunBarrel, BowgunBarrel.DevilsGrin),
            (EquipmentClasses.BowgunStock, BowgunStock.BlizzardCannon),
            Helmet.BarrageEarring, Chestpiece.DamascusVest,
            Gauntlets.DamascusGuards, Faulds.DamascusCoat,
            Leggings.DamascusLeggings,
            ((ItemsType.potion, 10), (ItemsType.mega_potion, 10),
             (ItemsType.energy_drink, 5), (ItemsType.lifepowder, 3),
             (ItemsType.paralysis_knife, 5), (ItemsType.sleep_knife, 5),
             (ItemsType.poison_knife, 5), (ItemsType.tinged_meat, 5),
             (ItemsType.druged_meat, 5), (ItemsType.pitfall_trap, 1),
             (ItemsType.shock_trap, 1), (ItemsType.ez_shock_trap, 1),
             (ItemsType.ez_flash_bomb, 5), (ItemsType.ez_barrel_bomb_l, 2),
             (ItemsType.barrel_bomb_l_plus, 2), (ItemsType.barrel_bomb_l, 3),
             (ItemsType.barrel_bomb_s, 10), (ItemsType.max_potion, 2),
             (ItemsType.ancient_potion, 1), (ItemsType.powercharm, 1),
             (ItemsType.armorcharm, 1), (ItemsType.powertalon, 1),
             (ItemsType.armortalon, 1)),
            ((ItemsType.normal_s_lv2, 99), (ItemsType.pierce_s_lv3, 40),
             (ItemsType.crag_s_lv2, 9), (ItemsType.crag_s_lv3, 9),
             (ItemsType.wyvernfire_lv1, 10), (ItemsType.water_s, 60),
             (ItemsType.sleep_s_lv2, 8), (ItemsType.dragon_s, 20),
             (ItemsType.demon_s_ii, 5))
        )
    )
}


if __name__ == "__main__":
    import json

    QUESTS = [
        QUEST_EVENT_JUMP_FOUR_JAGGI,
        QUEST_EVENT_ANIMAL_ATTRACTIONS,
        QUEST_EVENT_SHUT_UP_AND_FISH,
        QUEST_EVENT_MOTLEY_MISSION,
        QUEST_EVENT_COLD_CALL,
        QUEST_EVENT_THE_PHANTOM_URAGAAN,
        QUEST_EVENT_BLOOD_SPORT,
        QUEST_EVENT_ALLURING_DRESS,
        QUEST_EVENT_GOBULED_EVERYTHING_IN_SIGHT,
        QUEST_EVENT_POACHED_WYVERN_EGGS,
        QUEST_EVENT_MERCY_MISSION,
        QUEST_EVENT_SPEAK_OF_THE_DEVILJHO,
        QUEST_EVENT_MARINE_WARFARE,
        QUEST_EVENT_DOUBLE_DIABLOS,
        QUEST_EVENT_HOT_DEAL,
        QUEST_EVENT_SEA_POWER,
        QUEST_EVENT_FF_FREE_FOR_ALL,
        QUEST_EVENT_RAGE_MATCH,
        QUEST_EVENT_LORDS_OF_THE_SEA_AND_SKY,
        QUEST_EVENT_WORLD_EATER,
        QUEST_EVENT_WHERE_GODS_FEAR_TO_TREAD,
        QUEST_EVENT_RED_HOT_PARTY,
        QUEST_EVENT_FIERY_SKIES_FROZEN_FIELDS,
        QUEST_EVENT_GREEN_EGGS,
        QUEST_EVENT_JUMP_FOURTY_EIGHT_JAGGI,
        QUEST_EVENT_DARK_SIDE_OF_THE_MOON,
        GRUDGE_MATCH_QURUPECO,
        GRUDGE_MATCH_ROYAL_LUDROTH,
        GRUDGE_MATCH_RATHIAN,
        GRUDGE_MATCH_LAGIACRUS,
        GRUDGE_MATCH_URAGAAN,
        GRUDGE_MATCH_WYVERN_TRIO,
        GRUDGE_MATCH_BIRD_BRUTE,
        GRUDGE_MATCH_SEA_POWER,
        GRUDGE_MATCH_TWO_FLAMES,
        GRUDGE_MATCH_ICE_AND_FIRE,
        GRUDGE_MATCH_BRUTE_HORNS,
        GRUDGE_MATCH_LAND_LORDS,
    ]

    for quest in QUESTS:
        name = quest['quest_info']['name'].replace(':', '')
        with open('event/{}.json'.format(name), "w") as outfile:
            json.dump(quest, outfile, indent=4)

    print("done")
