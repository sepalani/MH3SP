#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2022-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Quest utils module."""

from os import path
import struct
from other.utils import pad
from mh.equipment_utils import create_arena_equipment_set


class Enum(object):
    def __getitem__(self, idx):
        return getattr(self, idx)


class WaveType(Enum):
    none = 0
    monster = 1
    item = 2
    unknown = 3


class LocationType(Enum):
    QUEST_LOCATION_NONE = 0
    QUEST_LOCATION_D_ISLAND = 1
    QUEST_LOCATION_SANDY_PLAINS = 2
    QUEST_LOCATION_FLOODED_FOR = 3
    QUEST_LOCATION_TUNDRA = 4
    QUEST_LOCATION_VOLCANO = 5
    QUEST_LOCATION_GRT_DESERT = 6
    QUEST_LOCATION_UW_RUIN = 7
    QUEST_LOCATION_LAND_ARENA_1 = 8
    QUEST_LOCATION_LAND_ARENA_2 = 9
    QUEST_LOCATION_WATER_ARENA_1 = 10
    QUEST_LOCATION_SACRED_LAND = 11
    QUEST_LOCATION_WATER_ARENA_2 = 12
LocationType = LocationType()


LOCATION_SIZE = {
    LocationType.QUEST_LOCATION_NONE: 0,
    LocationType.QUEST_LOCATION_D_ISLAND: 13,
    LocationType.QUEST_LOCATION_SANDY_PLAINS: 12,
    LocationType.QUEST_LOCATION_FLOODED_FOR: 11,
    LocationType.QUEST_LOCATION_TUNDRA: 10,
    LocationType.QUEST_LOCATION_VOLCANO: 11,
    LocationType.QUEST_LOCATION_GRT_DESERT: 3,
    LocationType.QUEST_LOCATION_UW_RUIN: 4,
    LocationType.QUEST_LOCATION_LAND_ARENA_1: 2,
    LocationType.QUEST_LOCATION_LAND_ARENA_2: 2,
    LocationType.QUEST_LOCATION_WATER_ARENA_1: 2,
    LocationType.QUEST_LOCATION_SACRED_LAND: 2,
    LocationType.QUEST_LOCATION_WATER_ARENA_2: 2,
}


class Monster(Enum):
    none = 0
    rathian = 1
    rathalos = 2
    qurupeco = 3
    gigginox = 4
    barioth = 5
    diablos = 6
    deviljho = 7
    barroth = 8
    uragaan = 9
    jaggi = 10
    jaggia = 11
    great_jaggi = 12
    baggi = 13
    great_baggi = 14
    lagiacrus = 15
    royal_ludroth = 16
    ludroth = 17
    gobul = 18
    agnaktor = 19
    ceadeus = 20
    uroktor = 21
    delex = 22
    epioth = 23
    alatreon = 24
    jhen_mohran = 25
    giggi = 26
    aptonoth = 27
    popo = 28
    rhenoplos = 29
    felyne = 30
    melynx = 31
    fish = 32
    altaroth = 33
    kelbi = 34
    bnahabra1 = 35  # Gigginox Egg
    bnahabra2 = 36  # Bnahabra (Blue Wing)
    bnahabra3 = 37  # Bnahabra (Orange Wing)
    bnahabra4 = 38  # Bnahabra (Green Wing)
    brd_wyv = 39  # Bnahabra (Red Wing)
    fly_wyv = 40  # ---- INVALID AS AN IN-QUEST MONSTER ---
    brt_wyv = 41  # ---- INVALID AS AN IN-QUEST MONSTER ---
    psc_wyv = 42  # ---- INVALID AS AN IN-QUEST MONSTER ---
    levthn = 43  # ---- INVALID AS AN IN-QUEST MONSTER ---
    elddrg = 44  # ---- INVALID AS AN IN-QUEST MONSTER ---
    lynian = 45  # ---- INVALID AS AN IN-QUEST MONSTER ---
    herbvr = 46  # ---- INVALID AS AN IN-QUEST MONSTER ---
    nptron = 47  # ---- INVALID AS AN IN-QUEST MONSTER ---
    unk = 48  # ---- INVALID AS AN IN-QUEST MONSTER ---
Monster = Monster()


class QuestRankType(Enum):
    none = 0
    star_1 = 1
    star_2 = 2
    star_3 = 3
    star_4 = 4
    star_5 = 5
    urgent = 6
QuestRankType = QuestRankType()


class ItemsType(Enum):
    none = 0
    barrel_bomb_s = 1
    barrel_bomb_l = 2
    pitfall_trap = 3
    shock_trap = 4
    flash_bomb = 5
    oxygen_supply = 6
    sonic_bomb = 7
    throwing_knife = 8
    poison_knife = 9
    sleep_knife = 10
    paralysis_knife = 11
    tranq_knife = 12
    potion = 13
    mega_potion = 14
    dash_juice = 15
    mega_dash_juice = 16
    antidote = 17
    demondrug = 18
    mega_demondrug = 19
    might_pill = 20
    armorskin = 21
    mega_armorskin = 22
    adamant_pill = 23
    cool_drink = 24
    hot_drink = 25
    well_done_steak = 26
    rare_steak = 27
    burnt_meat = 28
    raw_meat = 29
    poisoned_meat = 30
    tinged_meat = 31
    druged_meat = 32
    paintball = 33
    old_pickaxe = 34
    iron_pickaxe = 35
    mega_pickaxe = 36
    old_bug_net = 37
    bug_net = 38
    mega_bug_net = 39
    bbq_spit = 40
    great_jagi_head = 41
    map = 42
    torch = 43
    first_aid_med = 44
    ration = 45
    mini_oxy_supply = 46
    portable_spit = 47
    mini_whetstone = 48
    ez_shock_trap = 49
    ez_flash_bomb = 50
    max_potion = 51
    barrel_bomb_l_plus = 52
    normal_s_lv1 = 53
    normal_s_lv2 = 54
    normal_s_lv3 = 55
    pierce_s_lv1 = 56
    pierce_s_lv2 = 57
    pierce_s_lv3 = 58
    pellet_s_lv1 = 59
    pellet_s_lv2 = 60
    pellet_s_lv3 = 61
    crag_s_lv1 = 62
    crag_s_lv2 = 63
    crag_s_lv3 = 64
    clust_s_lv1 = 65
    clust_s_lv2 = 66
    clust_s_lv3 = 67
    flaming_s = 68
    water_s = 69
    thunder_s = 70
    freeze_s = 71
    dragon_s = 72
    recov_s_lv1 = 73
    recov_s_lv2 = 74
    poison_s_lv1 = 75
    poison_s_lv2 = 76
    para_s_lv1 = 77
    para_s_lv2 = 78
    sleep_s_lv1 = 79
    sleep_s_lv2 = 80
    tranq_s = 81
    paint_s = 82
    demon_s_i = 83
    demon_s_ii = 84
    armor_s_i = 85
    armor_s_ii = 86
    sub_s_lv1 = 87
    sub_s_lv2 = 88
    exhaust_s = 89
    err89 = 90
    slicing_s = 91
    wyvernfire_lv1 = 92
    wyvernfire_lv2 = 93
    wyvernfire_lv3 = 94
    binoculars = 95
    tranq_bomb = 96
    stone = 97
    whetstone = 98
    iron_ore = 99
    earth_crystal = 100
    machalite_ore = 101
    dragonite_ore = 102
    carbalite_ore = 103
    pelagicite_ore = 104
    bathycite_ore = 105
    firestone = 106
    ice_crystal = 107
    lightcrystal = 108
    sharq_ticket = 109
    rustshard = 110
    ancient_shard = 111
    isisium = 112
    gracium = 113
    err113 = 114
    godbug = 115
    bitterbug = 116
    flashbug = 117
    thunderbug = 118
    gluehopper = 119
    killer_beetle = 120
    rare_scarab = 121
    royal_rhino = 122
    herb = 123
    antidote_herb = 124
    sleep_herb = 125
    fire_herb = 126
    sap_plant = 127
    paintberry = 128
    needleberry = 129
    huskberry = 130
    scatternut = 131
    bomberry = 132
    ivy = 133
    might_seed = 134
    adamant_seed = 135
    hot_pepper = 136
    cactus_flower = 137
    airweed = 138
    wyvern_eg = 139
    unknown_skull = 140
    honey = 141
    blue_mushroom = 142
    choice_mushroom = 143
    unique_mushroom = 144
    exciteshroom = 145
    parashroom = 146
    nitroshroom = 147
    err147 = 148
    black_pearl = 149
    jumbo_pearl = 150
    broken_shell = 151
    dragonbone_relic = 152
    monster_bone_s = 153
    monster_bone_m = 154
    monster_bone_l = 155
    err155 = 156
    eldest_saturnian = 157
    err157 = 158
    err158 = 159
    err159 = 160
    err160 = 161
    err161 = 162
    err162 = 163
    hercudrome = 164
    err164 = 165
    chilled_meat = 166
    hot_meat = 167
    err167 = 168
    rathian_scale_plus = 169
    rathian_carapace = 170
    rath_medulla = 171
    rathian_spike_plus = 172
    rathian_ruby = 173
    rathalos_ruby = 174
    inferno_sac = 175
    rathalos_scale_plus = 176
    rathaloscarapace = 177
    qurupeco_scale_plus = 178
    err178 = 179
    wonderful_beak = 180
    unnerving_talon = 181
    fearsome_maw = 182
    wyvern_stone = 183
    freezer_sac = 184
    wyvrnhide_ticket = 185
    black_gem_ticket = 186
    flabby_hide_plus = 187
    uncanny_hide_plus = 188
    toxin_sac = 189
    unnerving_talon_plus = 190
    stunning_quill = 191
    pittance_fang = 192
    vermilion_scale = 193
    fishing_harpoon = 194
    insect_husk = 195
    bone = 196
    dung = 197
    spider_web = 198
    bomb_casing = 199
    small_barrel = 200
    large_barrel = 201
    cricket = 202
    worm = 203
    firefly = 204
    mega_fishing_fly = 205
    frog = 206
    whetfish = 207
    sushifish = 208
    pin_tuna = 209
    popfish = 210
    sleepyfish = 211
    burst_arowana = 212
    bomb_arowana = 213
    glutton_tuna = 214
    scatterfish = 215
    small_goldenfish = 216
    goldenfish = 217
    err217 = 218
    beautiful_scale = 219
    giant_skull = 220
    pirate_booty = 221
    net = 222
    no_item = 223
    shroom_germ = 224
    bugmaker_pro = 225
    bizzy_bees = 226
    saturnian = 227
    fortune_fang = 228
    shining_starfish = 229
    mystic_narwhal = 230
    atlantis_crab = 231
    gold_needle = 232
    armorfish_morsel = 233
    fish_finder = 234
    treasure_tracker = 235
    spare_spear = 236
    perfect_paddle = 237
    shroom_germ_plus = 238
    pink_liver = 239
    ethnic_wyvrnmeat = 240
    ancient_skin_oil = 241
    queens_spirit = 242
    err242 = 243
    funky_pheromones = 244
    saturnian_trap = 245
    err245 = 246
    super_sized_dung = 247
    fine_pelt = 248
    moonlight_fang = 249
    queen_needle = 250
    power_paddle = 251
    curved_fang = 252
    flamboyant_quill = 253
    glittering_scale = 254
    sea_kings_scale = 255
    wyverngold = 256
    err256 = 257
    err257 = 258
    err258 = 259
    err259 = 260
    err260 = 261
    err261 = 262
    err262 = 263
    felvine_bomb = 264
    double_bbq_spit = 265
    dragonbone_piece = 266
    abalone_piece = 267
    fossil_piece = 268
    odd_eg = 269
    mystery_bone = 270
    err270 = 271
    err271 = 272
    herbal_medicine = 273
    rathian_scale = 274
    rathian_shell = 275
    rathian_webbing = 276
    rathian_spike = 277
    rathian_plate = 278
    flame_sac = 279
    wyvern_tear = 280
    rathalos_scale = 281
    rathalos_shell = 282
    rathalos_webbing = 283
    rath_marrow = 284
    rathalos_plate = 285
    rathalos_tail = 286
    qurupeco_scale = 287
    qurupeco_feather = 288
    vivid_feather = 289
    strange_beak = 290
    flabby_hide = 291
    uncanny_hide = 292
    poison_sac = 293
    pale_extract = 294
    diablos_fang = 295
    diablos_shell = 296
    diablos_ridge = 297
    diablos_tailcase = 298
    barroth_shell = 299
    barroth_ridge = 300
    barroth_claw = 301
    barroth_tail = 302
    barroth_scalp = 303
    bird_wyvern_fang = 304
    jagi_hide = 305
    jagi_scale = 306
    great_jagi_claw = 307
    great_jagi_hide = 308
    screamer = 309
    lagiacrus_hide = 310
    lagiacrus_scale = 311
    lagiacrus_claw = 312
    shell_shocker_plus = 313
    lagiacrus_tail = 314
    lagiacrus_plate = 315
    spongy_hide = 316
    r_ludroth_scale = 317
    r_ludroth_claw = 318
    r_ludroth_tail = 319
    dash_extract = 320
    hydro_hide = 321
    immature_sponge = 322
    gobul_spike = 323
    gobul_hide = 324
    paralysis_sac = 325
    gobul_fin = 326
    armor_sphere = 327
    armor_sphere_plus = 328
    gobul_lantern = 329
    warm_pelt = 330
    nutrients = 331
    mega_nutrients = 332
    dragon_toadstool = 333
    immunizer = 334
    catalyst = 335
    bomb_sac = 336
    kelbi_horn = 337
    blue_kelbi_horn = 338
    bnahabra_shell = 339
    bnahabra_wing = 340
    monster_fluid = 341
    bone_husk_s = 342
    bone_husk_l = 343
    toadstool = 344
    smoke_bomb = 345
    poison_smoke_bmb = 346
    dung_bomb = 347
    gunpowder = 348
    trap_tool = 349
    yambug = 350
    tuna_bait = 351
    bughopper = 352
    arowana_bait = 353
    snakebee_larva = 354
    goldenfish_bait = 355
    antiseptic_stone = 356
    wyvern_fang = 357
    lifecrystals = 358
    wyvern_claw_ = 359
    lifepowder = 360
    hunting_horn = 361
    health_horn = 362
    antidote_horn = 363
    demon_horn = 364
    armor_horn = 365
    farcaster = 366
    tranquilizer = 367
    dragonfell_berry = 368
    err368 = 369
    err369 = 370
    err370 = 371
    err371 = 372
    err372 = 373
    energy_drink = 374
    cleanser = 375
    garbage = 376
    ancient_potion = 377
    psychoserum = 378
    agnaktor_coin = 379
    ballista_ammo = 380
    cannon_ammo = 381
    powderstone = 382
    anti_dragon_bomb = 383
    ballista_binder = 384
    rath_talon = 385
    twisted_horn = 386
    majestic_horn = 387
    mega_harpoon = 388
    whetfish_bait = 389
    sushifish_bait = 390
    firedouse_berry = 391
    waterblock_seed = 392
    icethaw_pellet = 393
    stormsender_seed = 394
    herbivore_eg = 395
    crystal_bone = 396
    golden_bone = 397
    air_philter = 398
    mega_air_philter = 399
    altaroth_stomach = 400
    altaroth_jaw = 401
    ripened_mushroom = 402
    r_ludroth_crest = 403
    barioth_shell = 404
    barioth_pelt = 405
    amber_tusks = 406
    barioth_claw = 407
    barioth_spike = 408
    frost_sac = 409
    uragaan_shell = 410
    uragaan_scute = 411
    uragaan_marrow = 412
    uragaan_jaw = 413
    agnaktor_shell = 414
    agnaktor_hide = 415
    agnaktor_fin = 416
    agnaktor_claw = 417
    agnaktor_scale = 418
    agnaktor_beak = 419
    kings_frill = 420
    fertile_mud = 421
    gobul_whisker = 422
    shell_shocker = 423
    lagiacrus_horn = 424
    flintstone = 425
    barioth_tail = 426
    bloodstone = 427
    paw_pass_ticket = 428
    monster_guts = 429
    red_coral_stone = 430
    voucher = 431
    gourmet_voucher = 432
    alatreon_scute = 433
    alatreon_plate = 434
    alatreon_talon = 435
    azure_dragongem = 436
    skypiercer = 437
    bbq_with_mask = 438
    no_mask = 439
    mystery_charm = 440
    shining_charm = 441
    timeworn_charm = 442
    armor_stone = 443
    adv_armor_sphere = 444
    hrd_armor_sphere = 445
    hvy_armor_sphere = 446
    aquaglow_jewel = 447
    sunspire_jewel = 448
    bloodrun_jewel = 449
    lazurite_jewel = 450
    barioth_carapace = 451
    barioth_pelt_plus = 452
    amber_tusks_plus = 453
    barioth_claw_plus = 454
    diablos_marrow = 455
    diablos_carapace = 456
    diablos_ridge = 457
    stout_horn = 458
    ceadeus_hide = 459
    ceadeus_scale = 460
    ceadeus_fur = 461
    ceadeus_tail = 462
    luminous_organ = 463
    deep_dragongem = 464
    crooked_horn = 465
    elderdragonblood = 466
    mohran_shell = 467
    mohran_brace = 468
    mohran_scale = 469
    sturdy_fang = 470
    earth_dragongem = 471
    mohran_carapace = 472
    mohran_scale_plus = 473
    sturdy_fang_plus = 474
    mohran_brace_plus = 475
    barroth_carapace = 476
    barroth_ridge_plus = 477
    barroth_claw_plus = 478
    uragaan_scale = 479
    uragaan_scale_plus = 480
    uragaan_ruby = 481
    uragaan_carapace = 482
    deviljho_hide = 483
    deviljho_scale = 484
    deviljho_talon = 485
    deviljho_fang = 486
    deviljho_gem = 487
    deviljho_scalp = 488
    deviljho_tail = 489
    quality_sponge = 490
    spongy_hide_plus = 491
    r_ludroth_scale_plus = 492
    r_ludroth_claw_plus = 493
    r_ludroth_crest_plus = 494
    gobul_spike_plus = 495
    gobul_hide_plus = 496
    gobul_lantern_plus = 497
    gobul_fin_plus = 498
    lagiacrus_hide_plus = 499
    lagiacrus_scale_plus = 500
    lagiacrus_claw_plus = 501
    lagiacrus_horn_plus = 502
    lagia_sapphire = 503
    agnaktor_tail = 504
    agnaktorcarapace = 505
    agnaktor_hide_plus = 506
    agnaktor_fin_plus = 507
    agnaktor_claw_plus = 508
    firecell_stone = 509
    brkn_skypiercer = 510
    alatreon_tail = 511
    alatreon_webbing = 512
    kelbi_horn_objet = 513
    twstd_horn_objet = 514
    mohranfang_objet = 515
    pigie = 516
    egie_pigie = 517
    rath_pigie = 518
    sandstone_plant = 519
    marshland_plant = 520
    snowflake_plant = 521
    prismshroom_lamp = 522
    qurupeco_lamp = 523
    sirensea_lamp = 524
    oceanic_fountain = 525
    bubbly_fountain = 526
    magma_fountain = 527
    iron_figure = 528
    machalite_figure = 529
    dragonite_figure = 530
    model_sandskiff = 531
    model_airship = 532
    model_pigieship = 533
    guildie_red = 534
    guildie_green = 535
    guildie_blue = 536
    great_pigie = 537
    qurupeco_wing = 538
    jagi_hide_plus = 539
    lightning_ticket = 540
    great_bagi_claw = 541
    high_qualty_pelt = 542
    popo_tongue = 543
    rhenoplos_shell = 544
    rhenoplos_scalp = 545
    rheno_carapace = 546
    bnahabracarapace = 547
    monster_broth = 548
    quality_sac = 549
    sleep_sac = 550
    coma_sac = 551
    bagi_hide = 552
    bagi_scale = 553
    great_bagi_hide = 554
    leaders_crest = 555
    bird_wyvern_gem = 556
    uroktor_scale = 557
    smiths_notebook = 558
    bird_wyvern_bone = 559
    big_fin = 560
    quality_fin = 561
    sharpened_fang = 562
    velvety_hide = 563
    gigi_stinger = 564
    commendation = 565
    bird_wyvern_claw = 566
    barrel_bomb_s_plus = 567
    felvine = 568
    steel_eg = 569
    silver_eg = 570
    golden_eg = 571
    incomplete_crown = 572
    crowns_gemstone = 573
    dazzling_crown = 574
    book_of_combos_1 = 575
    book_of_combos_2 = 576
    book_of_combos_3 = 577
    book_of_combos_4 = 578
    book_of_combos_5 = 579
    organizer_guide = 580
    pack_rat_guide = 581
    ez_barrel_bomb_l = 582
    uw_ballista_ammo = 583
    rathalos_coin = 584
    gobul_coin = 585
    barioth_coin = 586
    hunter_king_coin = 587
    diablos_coin = 588
    deviljho_coin = 589
    hellhunter_tag = 590
    dark_metal = 591
    incomplete_plans = 592
    lion_kings_seal = 593
    soulhunter_tag = 594
    monster_bone_plus = 595
    powercharm = 596
    powertalon = 597
    armorcharm = 598
    armortalon = 599
    bounce_bomb = 600
    bounce_bomb_plus = 601
    sharqskin = 602
    conquerors_seal = 603
    golden_medallion = 604
    prize_gold_sword = 605
    great_jagi_coin = 606
    qurupeco_coin = 607
    barroth_coin = 608
    r_ludroth_coin = 609
    rathian_coin = 610
    lagiacrus_coin = 611
    uragaan_coin = 612
    wyvern_lord_coin = 613
    sea_lord_coin = 614
    pinnacle_coin = 615
    antidote_jewel = 616
    antidote_jewel_plus = 617
    paralysis_jewel = 618
    paralysis_jewel_plus = 619
    pep_jewel = 620
    pep_jewel_plus = 621
    steadfast_jewel = 622
    steadfast_jewel_plus = 623
    weather_jewel = 624
    weather_jewel_plus = 625
    ninja_jewel = 626
    vitality_jewel = 627
    recovery_jewel = 628
    resurgence_jewel = 629
    razor_jewel = 630
    cutter_jewel = 631
    handicraft_jewel = 632
    architect_jewel = 633
    fencer_jewel = 634
    swordsman_jewel = 635
    expert_jewel = 636
    master_jewel = 637
    hermit_jewel = 638
    grinder_jewel = 639
    stone_wall_jewel = 640
    iron_wall_jewel = 641
    shield_jewel = 642
    aegis_jewel = 643
    quickload_jewel = 644
    flashload_jewel = 645
    absorber_jewel = 646
    flinchfree_jewel = 647
    forceshot_jewel = 648
    forceshot_jewel_plus = 649
    pierce_jewel = 650
    pierce_jewel_plus = 651
    pellet_jewel = 652
    pellet_jewel_plus = 653
    shotplus_jewel = 654
    shotplus_jewel_plus = 655
    piercplus_jewel = 656
    piercplus_jewel_plus = 657
    pelletplus_jewel = 658
    cragplus_jewel = 659
    clustplus_jewel = 660
    disabler_jewel = 661
    disabler_jewel_plus = 662
    element_jewel = 663
    element_jewel_plus = 664
    bombardier_jewel = 665
    lite_eater_jewel = 666
    hungerless_jewel = 667
    metabolism_jewel = 668
    attack_jewel = 669
    assault_jewel = 670
    onslaught_jewel = 671
    defense_jewel = 672
    turtle_jewel = 673
    protection_jewel = 674
    asylum_jewel = 675
    earplug_jewel = 676
    silencer_jewel = 677
    alarm_jewel = 678
    friendship_jewel = 679
    alliance_jewel = 680
    transportr_jewel = 681
    crimson_jewel = 682
    torrent_jewel = 683
    storm_jewel = 684
    glacier_jewel = 685
    dragonbane_jewel = 686
    breeze_jewel = 687
    warmth_jewel = 688
    sandbag_jewel = 689
    anchor_jewel = 690
    map_jewel = 691
    gathering_jewel = 692
    spree_jewel = 693
    blessing_jewel = 694
    fate_jewel = 695
    destiny_jewel = 696
    fisher_jewel = 697
    psychic_jewel = 698
    medicine_jewel = 699
    panacea_jewel = 700
    professor_jewel = 701
    factory_jewel = 702
    evade_jewel = 703
    lightfoot_jewel = 704
    crisis_jewel = 705
    peril_jewel = 706
    enduring_jewel = 707
    sprinter_jewel = 708
    marathon_jewel = 709
    chamber_jewel = 710
    magazine_jewel = 711
    sniper_jewel = 712
    gobbler_jewel = 713
    voracious_jewel = 714
    carver_jewel = 715
    looter_jewel = 716
    footing_jewel = 717
    tectonic_jewel = 718
    bbq_jewel = 719
    jumping_jewel = 720
    leaping_jewel = 721
    draw_jewel = 722
    critical_jewel = 723
    trapmaster_jewel = 724
    workout_jewel = 725
    physique_jewel = 726
    tranq_jewel = 727
    capture_jewel = 728
    perception_jewel = 729
    charger_jewel = 730
    dynamo_jewel = 731
    fresh_air_jewel = 732
    upstream_jewel = 733
    swimmer_jewel = 734
    diver_jewel = 735
    gambit_jewel = 736
    checkmate_jewel = 737
    resistor_jewel = 738
    release_jewel = 739
    catalyst_jewel = 740
    guts_jewel = 741
    fortitude_jewel = 742
    salvo_jewel = 743
    fusillade_jewel = 744
    dung_jewel = 745
    torchlight_jewel = 746
ItemsType = ItemsType()


class ResourcesType(Enum):
    low_rank = 0x0000
    high_rank = 0x0001
    arena = 0x0002
ResourcesType = ResourcesType()


class StartingPositionType(Enum):
    camp = 0x00
    random = 0x01
    shrine = 0x02
StartingPositionType = StartingPositionType()


class QuestRestrictionType(Enum):
    RESTRICTION_NONE = 0
    RESTRICTION_9_JOIN = 1
    RESTRICTION_18_JOIN = 2
    RESTRICTION_31_JOIN = 3
    RESTRICTION_40_JOIN = 4
    RESTRICTION_51_JOIN = 5
    RESTRICTION_100_JOIN = 6
    RESTRICTION_9_INITJOIN = 7
    RESTRICTION_18_INITJOIN = 8
    RESTRICTION_31_INITJOIN = 9
    RESTRICTION_40_INITJOIN = 10
    RESTRICTION_51_INITJOIN = 11
    RESTRICTION_100_INITJOIN = 12
    RESTRICTION_1_8_INITJOIN = 13
    RESTRICTION_1_17_INITJOIN = 14
    RESTRICTION_1_30_INITJOIN = 15
    RESTRICTION_31_39_INITJOIN = 16
    RESTRICTION_31_50_INITJOIN = 17
    RESTRICTION_MEN_ONLY = 18
    RESTRICTION_LADIES_ONLY = 19
    RESTRICTION_NO_ARMOR = 20
    RESTRICTION_CHACHA = 21
    RESTRICTION_5_JOIN = 22
    RESTRICTION_14_JOIN = 23
    RESTRICTION_27_JOIN = 24
    RESTRICTION_35_JOIN = 25
    RESTRICTION_46_JOIN = 26
QuestRestrictionType = QuestRestrictionType()


def make_monster_quest_type(monster_type, starting_area, boss_id, spawn_count, level,
                            min, size, max):
    data = b""
    # - id: monster_type
    # type: u1
    # enum: Monster
    data += struct.pack(">B", monster_type)

    # - id: boss_id
    # type: u2
    data += struct.pack(">B", starting_area)
    data += struct.pack(">B", boss_id)

    # - id: spawn_count
    # type: u1
    data += struct.pack(">B", spawn_count)

    # - id: level
    # type: u1
    data += struct.pack(">B", level)

    # - id: min
    # type: u1
    data += struct.pack(">B", min)

    # - id: size
    # type: u1
    data += struct.pack(">B", size)

    # - id: max
    # type: u1
    data += struct.pack(">B", max)

    return data


def make_quest_properties_type(type, objective_type, objective_count):
    data = b""
    # - id: type
    # type: u4
    data += struct.pack(">I", type)

    # - id: objective_type
    # type: u2
    data += struct.pack(">h", objective_type)

    # - id: objective_count
    # type: u2
    data += struct.pack(">h", objective_count)

    return data


def make_reward_type(item, amount, percent):
    data = b""
    # - id: item
    # type: u2
    # enum: item_type
    data += struct.pack(">h", item)

    # - id: amount
    # type: u1
    data += struct.pack(">B", amount)

    # - id: percent
    # type: u1
    data += struct.pack(">B", percent)

    return data


def generate_rewards(rewards):
    data = b""
    i = -1
    for i, reward in enumerate(rewards):
        data += make_reward_type(reward[0], reward[1], reward[2])
        if i == 10:
            break
    data += b'\0' * (4 * (10-i))
    return data


def make_binary_event_quest(quest_data):
    """
    'quest_info': {
        'quest_id': quest_id,
        'name': name,
        'client': client,
        'description': description,
        'details': details,
        # Usually "Complete the Main Quest."
        'success_message': success_message,
        'flags': flags,
        'penalty_per_cart': penalty_per_cart,
        'quest_fee': quest_fee,
        'time_limit': time_limit,
        'main_monster_1': main_monster1,
        'main_monster_2': main_monster2,
        'location': location,
        'quest_rank': quest_rank,
        'hrp_restriction': hrp_restriction,
        'resources': resources,
        'supply_set_number': supply_set_number,
        'starting_position': starting_position,
        'general_enemy_level': general_enemy_level,
        'summon': summon,
        'wave_1_transition_type': wave_1_transition_type,
        'wave_1_transition_target': wave_1_transition_target,
        'wave_1_transition_quantity': wave_1_transition_quantity,
        'wave_2_transition_type': wave_2_transition_type,
        'wave_2_transition_target': wave_2_transition_target,
        'wave_2_transition_quantity': wave_2_transition_quantity,
        'smallmonster_data_file': smallmonster_data (or None),
    },
    """
    quest_info = quest_data['quest_info']

    """
    'large_monsters': {
        'monster_1': {
            'type': monsterType1,
            'boss_id': monsterType1_bossid,
            'enabled': monsterType1_enabled,
            'level': monsterType1_level,  # 0x01 through 0x3c
            'size': monsterType1_size,
            # 0: fixed, 1: spread of 5, 2: spread of 3
            'hp_spread': monsterType1_min,
            # Controls the spread of size but details unknown
            'size_spread': monsterType1_max
        },
        'monster_2': {
            'type': monsterType2,
            'boss_id': monsterType2_bossid,
            'enabled': monsterType2_enabled,
            'level': monsterType2_level,  # 0x01 through 0x3c
            'size': monsterType2_size,
            # 0: fixed, 1: spread of 5, 2: spread of 3
            'hp_spread': monsterType2_min,
            # Controls the spread of size but details unknown
            'size_spread': monsterType2_max
        },
        'monster_3': {
            'type': monsterType3,
            'boss_id': monsterType3_bossid,
            'enabled': monsterType3_enabled,
            'level': monsterType3_level,  # 0x01 through 0x3c
            'size': monsterType3_size,
            # 0: fixed, 1: spread of 5, 2: spread of 3
            'hp_spread': monsterType3_min,
            # Controls the spread of size but details unknown
            'size_spread': monsterType3_max
        }
    },
    """
    large_monsters = quest_data['large_monsters']
    monster_1 = large_monsters['monster_1']
    monster_2 = large_monsters['monster_2']
    monster_3 = large_monsters['monster_3']

    """
    'objective_details': {
        'main_quest': {
            'type': mainquest_type,
            'objective_type': mainquest_objectivetype,
            'objective_num': mainquest_objectivenum,
            'zenny_reward': main_reward,
            'hrp_reward': hunter_rank_points,
            'rewards_row_1': mainquest_rewards1,
            'rewards_row_2': mainquest_rewards2,
        }
        'subquest_1': {
            'description': subquest1_description,
            'type': subquest1_type,
            'objective_type': subquest1_objectivetype,
            'objective_num': subquest1_objectivenum,
            'zenny_reward': sub_quest_1_reward,
            'hrp_reward': subquest1_hrp,
            'rewards_row_1': sq1_rewards,
        }
        'subquest_2': {
            'description': subquest2_description,
            'type': subquest2_type,
            'objective_type': subquest2_objectivetype,
            'objective_num': subquest2_objectivenum,
            'zenny_reward': sub_quest_2_reward,
            'hrp_reward': subquest2_hrp,
            'rewards_row_1': sq2_rewards,
        }
    },
    """
    objective_details = quest_data['objective_details']
    main_quest = objective_details['main_quest']
    subquest_1 = objective_details['subquest_1']
    subquest_2 = objective_details['subquest_2']

    """
    'unknown': {
        'unk_12': unk_12,
        'unk_4': unk_4,
        'unk_5': unk_5,
        'unk_6': unk_6,
        'unk_7': unk_7,
        'unk_9': unk_9,
        'unk_10': unk_10,
        'unk_11': unk_11,
    }
    """
    unknown = quest_data['unknown']

    # TOOO: Remove encode("ascii") and use bytes instead
    data = b""

    # - id: name
    # type: str
    # size: 44
    # offset: 0x0000
    data += pad(quest_info['name'].encode("ascii"), 40)  # Size 0x28
    data += struct.pack(">I", 0x00000000)

    # - id: quest_id
    # type: u2
    # offset: 0x002C
    data += struct.pack(">H", quest_info['quest_id'])

    # - id: description
    # type: str
    # size: 92
    # offset: 0x002E
    data += pad(quest_info['description'].encode("ascii"), 80)
    data += b'\0' * 0xC  # Padding

    # - id: quest_rank
    # type: u1
    # enum: QuestRankType
    # offset: 0x008A
    data += struct.pack(">B", quest_info['quest_rank'])

    # - id: location
    # type: u1
    # enum: LocationType
    # offset: 0x008B
    data += struct.pack(">B", quest_info['location'])  # Offset 0x8C

    # - id: sub_quest_1_title
    # type: str
    # size: 41
    # offset: 0x008C
    data += pad(
        objective_details['subquest_1']['description'].encode("ascii"),
        0x29
    )

    # - id: sub_quest_2_title
    # type: str
    # size: 41
    # offset: 0x00B5
    data += pad(
        objective_details['subquest_2']['description'].encode("ascii"),
        0x29
    )

    # - id: sucess_message
    # type: str
    # size: 92
    # offset: 0x00DE
    data += pad(quest_info['success_message'].encode("ascii"), 0x5C)

    # - id: time_limit
    # type: u2
    # offset: 0x013A
    data += struct.pack(">h", quest_info['time_limit'])

    # - id: failure_message
    # type: str
    # size: 92
    # Presently hardcoded
    # offset: 0x013C
    data += pad(b"Reward hits 0, or time\nexpires.", 0x5C)

    # - id: hunter_rank_point_restriction
    # type: u2
    # offset: 0x0198
    data += struct.pack(">h", quest_info['hrp_restriction'])

    # - id: client
    # type: str
    # size: 41
    # offset: 0x019A
    data += pad(quest_info['client'].encode("ascii"), 0x29)

    # - id: unk2
    # size: 6
    # offset: 0x01C3
    data += b'\0' * 0x06

    # - id: details
    # type: str
    # size: 256
    # offset: 0x01C9
    data += pad(quest_info['details'].encode("ascii"), 0x100)  # b'\0' * 0x100

    # - id: unk1
    # size: 61
    # offset: 0x02C9
    data += b'\0' * 0x3D

    # - id: minion_unsure
    # size: 3
    # offset: 0x0306
    data += b'\0' * 0x03

    # - id: quest_flags_unsure
    # size: 3
    # offset: 0x0309
    data += b'\0' * 0x03

    # - id: monster_1
    # type: u1
    # enum: Monster
    # Offset 0x30C ("Main monsters" 1)
    data += struct.pack(">B", quest_info['main_monster_1'])

    # - id: monster_2
    # type: u1
    # enum: Monster
    # Offset 0x30D ("Main monsters" 2)
    data += struct.pack(">B", quest_info['main_monster_2'])

    # - id: unk3
    # size: 2
    # offset: 0x030E
    data += b'\0' * 0x02  # Padding

    # - id: flags
    # type: u4
    # offset: 0x0310
    data += struct.pack(">I", generate_flags(*(quest_info['flags'])))  # Offset 0x310

    # - id: monsters
    # type: monster_quest_type
    # repeat: expr
    # repeat-expr: 3
    # # offset: 0x0314
    if monster_1['type'] != 0:
        data += make_monster_quest_type(
            monster_type=monster_1['type'],
            starting_area=monster_1['starting_area'],
            boss_id=monster_1['boss_id'],
            spawn_count=monster_1['spawn_count'],
            level=monster_1['level'],
            min=monster_1['hp_spread'],
            size=monster_1['size'],
            max=monster_1['size_spread']
        )  # size: 0x08
    else:
        data += b'\0' * 0x08

    # offset: 0x031C
    if monster_2['type'] != 0:
        data += make_monster_quest_type(
            monster_type=monster_2['type'],
            starting_area=monster_2['starting_area'],
            boss_id=monster_2['boss_id'],
            spawn_count=monster_2['spawn_count'],
            level=monster_2['level'],
            min=monster_2['hp_spread'],
            size=monster_2['size'],
            max=monster_2['size_spread']
        )  # size: 0x08
    else:
        data += b'\0' * 0x08

    # offset: 0x0324
    if monster_3['type'] != 0:
        data += make_monster_quest_type(
            monster_type=monster_3['type'],
            starting_area=monster_3['starting_area'],
            boss_id=monster_3['boss_id'],
            spawn_count=monster_3['spawn_count'],
            level=monster_3['level'],
            min=monster_3['hp_spread'],
            size=monster_3['size'],
            max=monster_3['size_spread']
        )  # size: 0x08
    else:
        data += b'\0' * 0x08

    # SUMMON / (INVADER?)
    # - id: unk5
    # type: u4
    # offset: 0x032C
    data += struct.pack(">I", quest_info['summon'])

    # - id: quests_properties
    # type: quest_properties_type
    # repeat: expr
    # repeat-expr: 3

    # "Hunt 8 jaggia:"
    # mainquest_type = 0x00008101,
    # mainquest_objectivetype=0x000b,
    # mainquest_objectivecount=0x0008

    # "Hunt 12 jaggi:"
    # mainquest_type = 0x00000101,
    # mainquest_objectivetype=0x000a,
    # mainquest_objectivecount=0x000c

    # "Hunt a Great Jaggi:"
    # mainquest_type = 0x00000001,
    # mainquest_objectivetype=0x000c,
    # mainquest_objectivecount=0x0001

    # "Wound Great Jaggi's Head:"
    # quest_type = 0x00000204,
    # quest_objectivetype=0x000c,
    # quest_objectivecount=0x0001

    # "Stun Great Jaggi:"
    # quest_type = 0x00001000,
    # quest_objectivetype=0x000c,
    # quest_objectivecount=0x0003

    # offset: 0x0330
    data += make_quest_properties_type(
        main_quest['type'],
        main_quest['objective_type'],
        main_quest['objective_num']
    )

    # offset: 0x0338
    if subquest_1['type'] is not None:
        data += make_quest_properties_type(
            subquest_1['type'],
            subquest_1['objective_type'],
            subquest_1['objective_num']
        )
    else:
        data += b"\0" * 0x08

    # offset: 0x0340
    if subquest_2['type'] is not None:
        data += make_quest_properties_type(
            subquest_2['type'],
            subquest_2['objective_type'],
            subquest_2['objective_num']
        )
    else:
        data += b"\0" * 0x08

    # - id: contract_fee
    # type: u4
    # offset: 0x0348
    data += struct.pack(">I", quest_info['quest_fee'])

    # - id: main_objective_reward
    # type: u4
    # offset: 0x034C
    data += struct.pack(">I", main_quest['zenny_reward'])

    # - id: sub_objective_a_reward
    # type: u4
    # offset: 0x0350
    data += struct.pack(">I", subquest_1['zenny_reward'])

    # - id: sub_objective_b_reward
    # type: u4
    # offset: 0x0354
    data += struct.pack(">I", subquest_2['zenny_reward'])

    # - id: death_reduction
    # type: u4
    # offset: 0x0358
    data += struct.pack(">I", quest_info['penalty_per_cart'])

    # - id: hunter_rank_points
    # type: u4
    # offset: 0x035C
    data += struct.pack(">I", main_quest['hrp_reward'])

    # - id: unk7
    # type: u4
    # 0x0000000f for the great jaggi quest/(all quests?)
    # offset: 0x0360
    data += struct.pack(">I", 0x0000000f)

    # - id: unk8
    # type: u1
    # offset: 0x0364
    data += b'\0' * 0x01

    # - id: gather_rank (wrong)
    # type: u1
    # offset: 0x0365
    data += b'\0' * 0x01

    # - id: unk9
    # type: u1
    # offset: 0x0366
    data += b'\0' * 0x01

    # - id: unk10
    # type: u1
    # offset: 0x0367
    data += struct.pack(">B", subquest_1['hrp_reward'])

    # - id: supply_set (wrong)
    # type: u4
    # offset: 0x0368
    data += struct.pack(">I", subquest_2['hrp_reward'])

    # - id: Unknown 4
    # type: u1
    # offset: 0x036C
    data += struct.pack(">B", unknown['unk_4'])

    # - id: supply_type (0x00: low rank, 0x01: high rank, 0x02: arena)
    # type: u1
    # offset: 0x036D
    data += struct.pack(">B", quest_info['resources'])

    # - id: unk11
    # size: 2
    # type: u1
    # offset: 0x036E
    data += struct.pack(">B", unknown['unk_5'])
    # type: u1
    # offset: 0x036F
    data += struct.pack(">B", unknown['unk_6'])

    # - id: supply_set_number
    # type: u4
    # 0x00000011 for the great jaggi quest
    # offset: 0x0370
    data += struct.pack(">I", quest_info['supply_set_number'])

    # - id: unk12
    # type: u4
    # offset: 0x0374
    data += struct.pack(">I", unknown['unk_7'])

    # - id: unk13
    # type: u2
    # offset: 0x0378
    data += b'\0' * 0x02

    # - id: type_flag (STARTING POSITION, 0x0000: basecamp,
    #                  0x0001:random, 0x0002: shrine)
    # type: u2
    # offset: 0x037A
    data += struct.pack(">h", quest_info['starting_position'])

    # UNK
    # offset: 0x037C
    data += b'\0' * 0x02

    # - id: small_monster_data_location
    # type: u2
    # offset: 0x037E
    data += struct.pack(">h", 0x04b8)

    # - id: type_amount
    # type: u2
    # offset: 0x0380
    data += b'\0' * 0x02

    # - id: general_enemy_level
    # type: u2
    # offset: 0x0382
    data += struct.pack(">h", quest_info['general_enemy_level'])

    # - id: wave_1_transition_type
    # type: u2
    # offset: 0x0384
    data += struct.pack(">h", quest_info['wave_1_transition_type'])

    # - id: wave_1_transition_target
    # type: u2
    # offset: 0x0386
    data += struct.pack(">h", quest_info['wave_1_transition_target'])

    # - id: wave_1_transition_quantity
    # type: u2
    # offset: 0x0388
    data += struct.pack(">h", quest_info['wave_1_transition_quantity'])

    # - id: wave_2_transition_type
    # type: u2
    # offset: 0x038A
    data += struct.pack(">h", quest_info['wave_2_transition_type'])

    # - id: wave_2_transition_target
    # type: u2
    # offset: 0x038C
    data += struct.pack(">h", quest_info['wave_2_transition_target'])

    # - id: wave_2_transition_quantity
    # type: u2
    # offset: 0x038E
    data += struct.pack(">h", quest_info['wave_2_transition_quantity'])


    # Unknown 12 (0x00000002 for large monster hunting quests,
    #             0x00000003 for small monster & gathering quests,
    #             0x00000005 for Jhen & Alatreon)
    # offset: 0x0390
    data += struct.pack(">I", unknown['unk_12'])
    # offset: 0x0394
    data += make_quest_properties_type(main_quest['type'],
                                       main_quest['objective_type'],
                                       main_quest['objective_num'])

    # - id: main_objective_rewards
    # type: reward_type
    # repeat: expr
    # repeat-expr: 11
    # offset: 0x039C
    data += generate_rewards(main_quest['rewards_row_1'])

    # - id: main_objective_additional_rewards
    # type: reward_type
    # repeat: expr
    # repeat-expr: 11
    # offset: 0x03C8
    data += generate_rewards(main_quest['rewards_row_2'])

    # SUBQUEST 1 REWARDS
    # offset: 0x03F4
    if subquest_1['type'] is not None:
        data += make_quest_properties_type(subquest_1['type'],
                                           subquest_1['objective_type'],
                                           subquest_1['objective_num'])
        data += generate_rewards(subquest_1['rewards_row_1'])
    else:
        data += b"\0" * 0x08
        data += b'\0' * (4 * 11)
    # offset: 0x0428
    data += b'\0' * (4 * 11)

    # SUBQUEST 2 REWARDS
    # offset: 0x0454
    if subquest_2['type'] is not None:
        data += make_quest_properties_type(subquest_2['type'],
                                           subquest_2['objective_type'],
                                           subquest_2['objective_num'])
        data += generate_rewards(subquest_2['rewards_row_1'])
    else:
        data += b"\0" * 0x08
        data += b'\0' * (4 * 11)
    # offset: 0x0488
    data += b'\0' * (4 * 11)

    assert len(data) == 0x4B4

    # Add 2-byte tail between the main quest info and the small monster data
    # that describes how many bytes total the quest takes up before the
    # optional arena equipment data
    tail = 0x4B4 + 4
    if 'smallmonster_data_file' in quest_info:
        # Read small monster data from hex string file
        sm_data = read_quest_sm_data(quest_info['smallmonster_data_file'])
        if sm_data is not None:
            tail += len(sm_data) - 4
            data += struct.pack(">I", tail)
            data += sm_data[4:]
        else:
            data += struct.pack(">I", tail)
    else:
        # Create new small monster data from parameters
        """
        'small_monsters': [
            [
                {
                    'type': monsterType,
                    'variant': variant,
                    'room': room,
                    'quantity': quantity,
                    'unk1': unk1,
                    'pos_x': pos_x,
                    'pos_y': pos_y,
                    'pos_z': pos_z,
                    'rot_x': rot_x,
                    'rot_y': rot_y,
                    'rot_z': rot_z,
                    'unk2': unk2,  # Usually 0xFF
                }
            ] * number of waves * number of areas
        ]
        """
        sm_data = b""
        small_monsters = quest_data['small_monsters']
        location_size = LOCATION_SIZE[quest_info['location']]
        assert len(small_monsters) % location_size == 0
        num_waves = int(len(small_monsters) / location_size)
        assert num_waves <= 3
        # Pre-preamble: Establishing the locations of each of the waves' preambles
        sm_data += struct.pack('>I', 0x0000000C)
        sm_data += struct.pack('>I', 0x0000000C + 8*location_size)
        if num_waves < 3:
            sm_data += struct.pack('>I', 0xCCCCCCCC)
        else:
            sm_data += struct.pack('>I', 0x0000000C + 2*8*location_size)

        monster_data = b""
        # Preamble: Establishing the location and length of each of the
        # small monster areas
        current_sm_index = 0x0C + 8*len(small_monsters)
        for entry, monster_list in enumerate(quest_data['small_monsters']):
            sm_data += struct.pack(">I", current_sm_index)
            area = entry % location_size
            area_monster_data = b""
            for monster in monster_list:
                assert monster['room'] == area
                new_monster_data = b""
                new_monster_data += struct.pack(">I", monster['type'])
                new_monster_data += 3* b"\0"
                new_monster_data += struct.pack(">b", monster['quantity'])
                new_monster_data += struct.pack(">B", monster['unk2'])
                new_monster_data += struct.pack(">B", monster['room'])
                new_monster_data += struct.pack(">B", monster['unk1'])
                new_monster_data += struct.pack(">B", monster['variant'])
                new_monster_data += struct.pack(">I", 0x00000000)
                new_monster_data += struct.pack(">f", monster['pos_x'])
                new_monster_data += struct.pack(">f", monster['pos_y'])
                new_monster_data += struct.pack(">f", monster['pos_z'])
                new_monster_data += struct.pack('>i', int(180.05 * monster['rot_x']))
                new_monster_data += struct.pack('>i', int(180.05 * monster['rot_y']))
                new_monster_data += struct.pack('>i', int(180.05 * monster['rot_z']))
                new_monster_data += struct.pack('>I', 0xFF000000)
                new_monster_data += struct.pack('>I', 0x00000000)
                assert len(new_monster_data) == 0x30
                
                area_monster_data += new_monster_data
            area_monster_data += 0x30 * '\0'
            sm_data += struct.pack(">I", len(area_monster_data))
            current_sm_index += len(area_monster_data)
            monster_data += area_monster_data
        # Main small monster data
        sm_data += monster_data
        tail += len(sm_data)
        data += struct.pack(">I", tail)
        data += sm_data

    # If there is arena equipment data, add it to the end of the quest binary
    if 'arena_equipment' in quest_data:
        assert 0xEA60 <= quest_info['quest_id'] <= 0xEA6B, \
               "Invalid arena quest ID: {:#x}".format(quest_info['quest_id'])
        data += create_arena_equipment_set(quest_data['arena_equipment'])

    return data


# FLAGS INFO:
# (Arena quests have bytes in "QUEST_FLAG_ARENA = 0b10000" set)
# byte 1: Boss Order 1 (
#     +0x1000000: Unknown1
#     +0x2000000: All At Once(CombineSubquestsRequireMQAndFirstSubquest)
#     +0x4000000: Marathon (CombineSubquestsRequireMQAndBothSubquests)
#     +0x8000000: Unknown4
#     +0x10000000: Unknown5
#     +0x20000000: Unknown6
#     +0x40000000: Unknown7
#     +0x80000000: CombineMainAndSubquests
# )
# byte 2: Boss Order 2 (
#     +0x10000: Unknown1
#     +0x20000: Unknown2
#     +0x40000: RequireMQAndBothSubquests
#     +0x80000: Unknown4
#     +0x100000: QualifyingTime
#     +0x200000: DontAnnounceSubquestCompletion
#     +0x400000: Unknown7
#     +0x800000: ElderDragonLeftWounded
# )
# byte 3: Boss Order 3 (
#     +0x100(256): 2Mon_NoSubs_ReqSub1_Unstable
#     +0x200(512): Unknown2
#     +0x400(1024): Unknown3
#     +0x800(2048): BanjoMusic
#     +0x1000(4096): Unknown5
#     +0x2000(8192): Unknown6
#     +0x4000(16384): Unknown7
#     +0x8000(32768): Unknown8
# )
# byte 4: Quest Flags (
#     +1: Slay
#     +2: Deliver
#     +4: Capture
#     +8: Defend
#     +0x10(16): ArenaQuest
#     +0x20(32): Unknown2
#     +0x40(64): Repel(EndAtMainQuest)
#     +0x80(128): Unknown3
# )
def generate_flags(byte1, byte2, byte3, byte4):
    res = 0x00000000

    curr = 0x00
    for i in range(8):
        curr += byte1[i] * 2**i
    res += curr * 16**6

    curr = 0x00
    for i in range(8):
        curr += byte2[i] * 2**i
    res += curr * 16**4

    curr = 0x00
    for i in range(8):
        curr += byte3[i] * 2**i
    res += curr * 16**2

    curr = 0x00
    for i in range(8):
        curr += byte4[i] * 2**i
    res += curr * 16**0

    return res


def read_quest_sm_data(fname):
    data_path = path.join("event", fname)
    if not path.exists(data_path):
        return None
    with open(data_path, 'r') as f:
        data = f.read()
    return bytearray.fromhex(data.replace(" ", "").replace("\n", ""))


def make_event_slot(event):
    return (make_binary_event_quest(event), event)


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def is_arena_quest(flags):
    return ((1 * 2**4) * 16**0) & flags > 0


class QuestLoader:
    def __init__(self, file_loc='event/quest_rotation.json'):
        self.version = 0
        self.version_incrementer = 28
        self.file_loc = file_loc
        self.load_quests()
        self.version = 0

    def load_quests(self):
        import json
        self.version += self.version_incrementer
        quest_list = []
        with open(self.file_loc, 'r') as f:
            quests_json = byteify(json.load(f))
            for day in quests_json:
                curr_quest_list = []
                for quest_file in day:
                    with open(quest_file, 'r') as ff:
                        curr_quest = byteify(json.load(ff))
                        curr_quest = make_event_slot(curr_quest)
                        curr_quest_list.append(curr_quest)
                quest_list.append(curr_quest_list)
        self.quests = quest_list

    def get_quest_dicts(self, idx):
        # Get quest dicts for the day
        true_idx = idx - 1
        return [quest[1] for _, quest in enumerate(self.quests[true_idx])]

    def get_separated_quest_dicts(self, idx):
        # Get quest dicts for the day separated by event and arena
        quest_list = []
        arena_list = []
        for quest in self.get_quest_dicts(idx):
            if quest is None:
                continue
            if is_arena_quest(generate_flags(*(quest['quest_info']['flags']))):
                arena_list.append(quest)
            else:
                quest_list.append(quest)
        return quest_list, arena_list

    def __len__(self):
        # Get number of days
        return len(self.quests)

    def __getitem__(self, idx):
        # Get quests for the day
        true_idx = idx - self.version - 1
        return [quest[0] for _, quest in enumerate(self.quests[true_idx])]


