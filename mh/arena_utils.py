"""
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

import csv
from quest_utils import make_binary_event_quest,\
    generate_flags, Monster, LocationType,\
    QuestRankType, QuestRestrictionType, ResourcesType,\
    StartingPositionType, ItemsType
from equipment_utils import Chestpiece, Gauntlets, Faulds,\
    Leggings, Helmet, EquipmentClasses, Greatsword,\
    SnS, Hammer, Longsword, Switchaxe, Lance,\
    BowgunFrame, BowgunStock, BowgunBarrel,\
    slot, item_slot


def create_arena_equipment_set(GRUDGE_MATCH, sets):
    for set_num in range(4):
        weapon1, weapon2, weapon3, helm, chestpiece, gauntlets,\
            faulds, leggings, items, gunner_pouch = sets[set_num]
        # ---------- SET 1 ----------
        # Weapon
        GRUDGE_MATCH += slot(*weapon1)
        if weapon2 is not None:
            GRUDGE_MATCH += slot(*weapon2)
        else:
            GRUDGE_MATCH += b"\xff" * 0x04
        if weapon3 is not None:
            GRUDGE_MATCH += slot(*weapon3)
        else:
            GRUDGE_MATCH += b"\xff" * 0x04
        # Armors
        GRUDGE_MATCH += slot(EquipmentClasses.Helmet, helm)
        GRUDGE_MATCH += slot(EquipmentClasses.Chestpiece, chestpiece)
        GRUDGE_MATCH += slot(EquipmentClasses.Faulds, faulds)
        GRUDGE_MATCH += slot(EquipmentClasses.Gauntlets, gauntlets)
        GRUDGE_MATCH += slot(EquipmentClasses.Leggings, leggings)
        # Items (24 4-byte slots available)
        for item in items:
            GRUDGE_MATCH += item_slot(*item)
        GRUDGE_MATCH += b"\x00" * (24*4 - len(items)*4)
        # Gunner pouch (8 4-byte slots available)
        for item in gunner_pouch:
            GRUDGE_MATCH += item_slot(*item)
        GRUDGE_MATCH += b"\x00" * (8*4 - len(gunner_pouch)*4)


GRUDGE_MATCH_ROYAL_LUDROTH = make_binary_event_quest(0xEA61, "Grudge Match: Royal Ludroth", "Announcer/Receptionist", "Slay a Royal Ludroth", generate_flags((0,0,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),  # quest id, name, client, description, flags
    Monster.royal_ludroth, 0x0000, True, 0x17, 0x64, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    1000, 0, 0, 350, 0, 50, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_WATER_ARENA_2, QuestRankType.star_1, 0, QuestRestrictionType.RESTRICTION_NONE, ResourcesType.arena, 0,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000101, Monster.royal_ludroth, 0x01,  # Main quest: type, target, number
    "None.", 0x00000000, Monster.none, 0x00,  # Subquest 1: Description, type, target, number
    "None.", 0, Monster.none, 0,  # Subquest 2: Description, type, target, number
    "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
        "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
        "Thanks!",  # Quest details
    StartingPositionType.camp, 0x0017, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_underwaterarenarock.dat', # Small monster data
    [(ItemsType.r_ludroth_coin, 1, 24), (ItemsType.r_ludroth_coin, 2, 8), (ItemsType.voucher, 1, 10), (ItemsType.armor_sphere, 1, 24),
        (ItemsType.steel_eg, 1, 18), (ItemsType.pinnacle_coin, 1, 16)],
    [],
    [],
    [])

create_arena_equipment_set(GRUDGE_MATCH_ROYAL_LUDROTH,(\
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
            (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12)))))

GRUDGE_MATCH_BIRD_BRUTE = make_binary_event_quest(0xEA66, "Grudge Match: Bird and Brute", "Announcer/Receptionist", "Slay a Qurupeco" + '\x0A' + "and a Barroth", generate_flags((0,1,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),  # quest id, name, client, description, flags
    Monster.qurupeco, 0x0000, True, 0x17, 0x64, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.barroth, 0x0001, True, 0x17, 0x64, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    1000, 0, 0, 350, 0, 50, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_LAND_ARENA_1, QuestRankType.star_4, 0, QuestRestrictionType.RESTRICTION_31_INITJOIN, ResourcesType.arena, 0,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000101, Monster.qurupeco, 0x01,  # Main quest: type, target, number
    "None.", 0x00000101, Monster.barroth, 0x01,  # Subquest 1: Description, type, target, number
    "None.", 0, Monster.none, 0,  # Subquest 2: Description, type, target, number
    "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
        "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
        "Thanks!",  # Quest details
    StartingPositionType.camp, 0x0017, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_bloodsport.dat', # Small monster data
    [(ItemsType.qurupeco_coin, 1, 16), (ItemsType.barroth_coin, 1, 20), (ItemsType.voucher, 1, 14), (ItemsType.armor_sphere_plus, 1, 10),
        (ItemsType.adv_armor_sphere, 1, 5), (ItemsType.steel_eg, 1, 15), (ItemsType.silver_eg, 1, 5), (ItemsType.hunter_king_coin, 1, 15)],
    [],
    [],
    [])

create_arena_equipment_set(GRUDGE_MATCH_BIRD_BRUTE,(\
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
            (ItemsType.crag_s_lv2, 9), (ItemsType.poison_s_lv1, 12), (ItemsType.para_s_lv1, 12), (ItemsType.sleep_s_lv1, 12)))))


GRUDGE_MATCH_TWO_FLAMES = make_binary_event_quest(0xEA68, "Grudge Match: Two Flames", "Announcer/Receptionist", "Slay a Rathalos" + '\x0A' + "and a Rathian", generate_flags((0,1,0,0,0,1,0,0),(1,0,0,0,1,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,1,0,1,0)),  # quest id, name, client, description, flags
    Monster.rathalos, 0x0000, True, 0x17, 0x64, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.rathian, 0x0001, True, 0x17, 0x64, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    1000, 0, 0, 350, 0, 50, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_LAND_ARENA_1, QuestRankType.star_5, 0, QuestRestrictionType.RESTRICTION_31_INITJOIN, ResourcesType.arena, 0,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000101, Monster.rathalos, 0x01,  # Main quest: type, target, number
    "None.", 0x00000101, Monster.rathian, 0x01,  # Subquest 1: Description, type, target, number
    "None.", 0, Monster.none, 0,  # Subquest 2: Description, type, target, number
    "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
        "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
        "Thanks!",  # Quest details
    StartingPositionType.camp, 0x0017, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_bloodsport.dat', # Small monster data
    [(ItemsType.rathalos_coin, 1, 10), (ItemsType.rathian_coin, 1, 24), (ItemsType.voucher, 1, 14), (ItemsType.armor_sphere_plus, 1, 10),
        (ItemsType.adv_armor_sphere, 1, 5), (ItemsType.steel_eg, 1, 15), (ItemsType.silver_eg, 1, 5), (ItemsType.hunter_king_coin, 1, 17)],
    [],
    [],
    [])

create_arena_equipment_set(GRUDGE_MATCH_TWO_FLAMES,(\
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
        ((ItemsType.normal_s_lv2, 99), (ItemsType.normal_s_lv3, 99), (ItemsType.pierce_s_lv3, 40), (ItemsType.demon_s_ii, 5), (ItemsType.thunder_s, 60)))))
