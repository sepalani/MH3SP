#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2024 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Quest dumper.

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


def EXPORT(quest):
    import json
    name = quest['quest_info']['name'].replace(':', '')
    with open('event/{}.json'.format(name), "w") as outfile:
        json.dump(quest, outfile, indent=4)


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
            'hrp_reward': 220,
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
EVENT QUEST 18: Flooded Forest Free-For-All
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
            'level': 0x1F,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_2': {
            'type': Monster.lagiacrus,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x1F,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x03
        },
        'monster_3': {
            'type': Monster.gobul,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x1F,  # 0x01 through 0x3c
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
        'summon': 0x64010232,
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
EVENT QUEST 20: Where Gods Fear To Tread
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
        'quest_id': 61003,
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
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
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
            'type': Monster.rathalos,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.rathian,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x17,  # 0x01 through 0x3c
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
            'type': Monster.barroth,
            'starting_area': 0x00,
            'boss_id': 0x00,
            'spawn_count': 0x01,
            'level': 0x17,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_2': {
            'type': Monster.uragaan,
            'starting_area': 0x00,
            'boss_id': 0x01,
            'spawn_count': 0x01,
            'level': 0x17,
            'size': 0x64,
            'hp_spread': 0x00,  # 0: fixed, 1: spread of 5, 2: spread of 3
            'size_spread': 0x00
        },
        'monster_3': {
            'type': Monster.deviljho,
            'starting_area': 0x00,
            'boss_id': 0x02,
            'spawn_count': 0x01,
            'level': 0x12,  # 0x01 through 0x3c
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
    QUESTS = []
    QUESTS.append(QUEST_EVENT_JUMP_FOUR_JAGGI)
    QUESTS.append(QUEST_EVENT_THE_PHANTOM_URAGAAN)
    QUESTS.append(QUEST_EVENT_BLOOD_SPORT)
    QUESTS.append(QUEST_EVENT_MERCY_MISSION)
    QUESTS.append(QUEST_EVENT_FF_FREE_FOR_ALL)
    QUESTS.append(QUEST_EVENT_RAGE_MATCH)
    QUESTS.append(QUEST_EVENT_WORLD_EATER)
    QUESTS.append(QUEST_EVENT_WHERE_GODS_FEAR_TO_TREAD)
    QUESTS.append(QUEST_EVENT_GREEN_EGGS)
    QUESTS.append(QUEST_EVENT_JUMP_FOURTY_EIGHT_JAGGI)
    QUESTS.append(GRUDGE_MATCH_ROYAL_LUDROTH)
    QUESTS.append(GRUDGE_MATCH_BIRD_BRUTE)
    QUESTS.append(GRUDGE_MATCH_TWO_FLAMES)
    QUESTS.append(GRUDGE_MATCH_LAND_LORDS)
    for q in QUESTS:
        EXPORT(q)
    print("done")
