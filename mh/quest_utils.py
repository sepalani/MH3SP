#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Quest utils module.

    Monster Hunter 3 Server Project
    Copyright (C) 2022  Ze SpyRo

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
from other.utils import pad


# LocationType enum
class LocationType:
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

class Monster:
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
    bnahabra1 = 35
    bnahabra2 = 36
    bnahabra3 = 37
    bnahabra4 = 38
    brd_wyv = 39
    fly_wyv = 40
    brt_wyv = 41
    psc_wyv = 42
    levthn = 43
    elddrg = 44
    lynian = 45
    herbvr = 46
    nptron = 47
    fish = 48

class QuestRankType:
    none = 0
    star_1 = 1
    star_2 = 2
    star_3 = 3
    star_4 = 4
    star_5 = 5
    urgent = 6

class ItemsType:
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

class ResourcesType:
    low_rank = 0x0000
    high_rank = 0x0001
    arena = 0x0002

class StartingPositionType:
    camp = 0x00
    random = 0x01
    shrine = 0x02

class QuestRestrictionType:
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


def make_monster_quest_type(monster_type, boss_id, enabled, level, min, size, max):
    data = b""
    #- id: monster_type
    #type: u1
    #enum: Monster
    data += struct.pack(">B", monster_type)

    #- id: boss_id
    #type: u2
    data += struct.pack(">h", boss_id)

    #- id: enabled
    #type: u1
    if enabled:
        data += struct.pack(">B", 0x01)
    else:
        data += struct.pack(">B", 0x00)

    #- id: level
    #type: u1
    data += struct.pack(">B", level)

    #- id: min
    #type: u1
    data += struct.pack(">B", min)

    #- id: size
    #type: u1
    data += struct.pack(">B", size)

    #- id: max
    #type: u1
    data += struct.pack(">B", max)

    return data

def make_quest_properties_type(type, objective_type, objective_count):
    data = b""
    #- id: type
    #type: u4
    data += struct.pack(">I", type)

    #- id: objective_type
    #type: u2
    data += struct.pack(">h", objective_type)

    #- id: objective_count
    #type: u2
    data += struct.pack(">h", objective_count)

    return data

def make_reward_type(item, amount, percent):
    data = b""
    #- id: item
    #type: u2
    #enum: item_type
    data += struct.pack(">h", item)

    #- id: amount
    #type: u1
    data += struct.pack(">B", amount)

    #- id: percent
    #type: u1
    data += struct.pack(">B", percent)

    return data

def generate_rewards(rewards):
    data = b""
    i=-1
    for i, reward in enumerate(rewards):
        data += make_reward_type(reward[0], reward[1], reward[2])
        if i == 10:
            break
    data += b'\0' * (4 * (10-i))
    return data


def make_binary_event_quest(quest_id, name, client, description, flags,
                                monsterType1, monsterType1_bossid, monsterType1_enabled, monsterType1_level, monsterType1_size, monsterType1_min, monsterType1_max,
                                monsterType2, monsterType2_bossid, monsterType2_enabled, monsterType2_level, monsterType2_size, monsterType2_min, monsterType2_max,
                                monsterType3, monsterType3_bossid, monsterType3_enabled, monsterType3_level, monsterType3_size, monsterType3_min, monsterType3_max,
                                main_reward, sub_quest_1_reward, sub_quest_2_reward, penalty_per_cart, quest_fee, time_limit, main_monster1, main_monster2,
                                location, quest_rank, hunter_rank_points, hrp_restriction, resources, supply_set_number,
                                mainquest_type, mainquest_objectivetype, mainquest_objectivenum,
                                subquest1_description, subquest1_type, subquest1_objectivetype, subquest1_objectivenum,
                                subquest2_description, subquest2_type, subquest2_objectivetype, subquest2_objectivenum,
                                details,
                                starting_position, general_enemy_level, unk_12, subquest1_hrp, subquest2_hrp, unk_4, unk_5, unk_6, unk_7,
                                unk_9, unk_10, unk_11, summon,
                                smallmonster_data,
                                mainquest_rewards1, mainquest_rewards2,
                                sq1_rewards, sq2_rewards,
                                success_message="Complete the Main Quest."):
    data = b""

    #- id: name
    #  type: str
    #  size: 44
    data += pad(name, 40)  # Size 0x28
    data += struct.pack(">I", 0x00000000)

    #- id: quest_id
    #  type: u2
    data += struct.pack(">H", quest_id)

    #- id: description
    #  type: str
    #  size: 92
    data += pad(description, 80)
    data += b'\0' * 0xC  # Padding

    #- id: quest_rank
    #  type: u1
    #  enum: QuestRankType
    data += struct.pack(">B", quest_rank)

    #- id: location
    #  type: u1
    #  enum: LocationType
    data += struct.pack(">B", location)  # Offset 0x8C

    #- id: sub_quest_1_title
    #  type: str
    #  size: 41
    data += pad(subquest1_description, 0x29)

    #- id: sub_quest_2_title
    #  type: str
    #  size: 41
    data += pad(subquest2_description, 0x29)

    #- id: sucess_message
    #  type: str
    #  size: 92
    data += pad(success_message, 0x5C)

    #- id: time_limit
    #  type: u2
    data += struct.pack(">h", time_limit)  # Offset 0x13A

    #- id: failure_message
    #  type: str
    #  size: 92
    data += pad("Reward hits 0, or time" + '\x0A' + "expires.", 0x5C)

    #- id: hunter_rank_point_restriction
    #  type: u2
    data += struct.pack(">h", hrp_restriction)

    #- id: client
    #  type: str
    #  size: 41
    data += pad(client, 0x29)

    #- id: unk2
    #  size: 6
    data += b'\0' * 0x06

    #- id: details
    #  type: str
    #  size: 256
    data += pad(details, 0x100)#b'\0' * 0x100

    #- id: unk1
    #  size: 61
    data += b'\0' * 0x3D

    #- id: minion_unsure
    #  size: 3
    data += b'\0' * 0x03

    #- id: quest_flags_unsure
    #  size: 3
    data += b'\0' * 0x03

    #- id: monster_1
    #  type: u1
    #  enum: Monster
    data += struct.pack(">B", main_monster1)  # Offset 0x30C ("Main monsters" 1)

    #- id: monster_2
    #  type: u1
    #  enum: Monster
    data += struct.pack(">B", main_monster2)  # Offset 0x30D ("Main monsters" 2)

    #- id: unk3
    #  size: 2
    data += b'\0' * 0x02  # Padding

    #- id: flags
    #  type: u4
    data += struct.pack(">I", flags)  # Offset 0x310

    #- id: monsters
    #  type: monster_quest_type
    #  repeat: expr
    #  repeat-expr: 3

    # Hunt a Great Jaggi (Low Rank 1*):
    # monster 1, great jaggi: 0c000001 17016403
    #           monster_type: 0x0c,  boss_id: 0x0000,  enabled=0x01,  level=0x17,  min=0x01, size=0x64, max=0x03

    if monsterType1 != 0:
        data += make_monster_quest_type(monster_type=monsterType1, boss_id=monsterType1_bossid, enabled=monsterType1_enabled,
                    level=monsterType1_level, min=monsterType1_min, size=monsterType1_size, max=monsterType1_max)  # size: 0x08
    else:
        data += '\0' * 0x08

    if monsterType2 != 0:
        data += make_monster_quest_type(monster_type=monsterType2, boss_id=monsterType2_bossid, enabled=monsterType2_enabled,
                    level=monsterType2_level, min=monsterType2_min, size=monsterType2_size, max=monsterType2_max)  # size: 0x08
    else:
        data += '\0' * 0x08

    if monsterType3 != 0:
        data += make_monster_quest_type(monster_type=monsterType3, boss_id=monsterType3_bossid, enabled=monsterType3_enabled,
                    level=monsterType3_level, min=monsterType3_min, size=monsterType3_size, max=monsterType3_max)  # size: 0x08
    else:
        data += '\0' * 0x08

    
    # SUMMON / (INVADER?)
    #- id: unk5
    #  type: u4
    data += struct.pack(">I", summon)

    #- id: quests_properties
    #  type: quest_properties_type
    #  repeat: expr
    #  repeat-expr: 3

    # "Hunt 8 jaggia:"              mainquest_type = 0x00008101, mainquest_objectivetype=0x000b, mainquest_objectivecount=0x0008
    # "Hunt 12 jaggi:"              mainquest_type = 0x00000101, mainquest_objectivetype=0x000a, mainquest_objectivecount=0x000c

    # "Hunt a Great Jaggi:"         mainquest_type = 0x00000001, mainquest_objectivetype=0x000c, mainquest_objectivecount=0x0001
    # "Wound Great Jaggi's Head:"   quest_type = 0x00000204, quest_objectivetype=0x000c, quest_objectivecount=0x0001
    # "Stun Great Jaggi:"           quest_type = 0x00001000, quest_objectivetype=0x000c, quest_objectivecount=0x0003

    data += make_quest_properties_type(mainquest_type, mainquest_objectivetype, mainquest_objectivenum)  # Main quest

    if subquest1_type is not None:
        data += make_quest_properties_type(subquest1_type, subquest1_objectivetype, subquest1_objectivenum)  # Subquest 1
    else:
        data += b"\0" * 0x08

    if subquest2_type is not None:
        data += make_quest_properties_type(subquest2_type, subquest2_objectivetype, subquest2_objectivenum)  # Subquest 2
    else:
        data += b"\0" * 0x08

    #- id: contract_fee
    #  type: u4
    data += struct.pack(">I", quest_fee)  # Offset 0x348

    #- id: main_objective_reward
    #  type: u4
    data += struct.pack(">I", main_reward)

    #- id: sub_objective_a_reward
    #  type: u4
    data += struct.pack(">I", sub_quest_1_reward)

    #- id: sub_objective_b_reward
    #  type: u4
    data += struct.pack(">I", sub_quest_2_reward)

    #- id: death_reduction
    #  type: u4
    data += struct.pack(">I", penalty_per_cart)

    #- id: hunter_rank_points
    #  type: u4
    data += struct.pack(">I", hunter_rank_points)

    #- id: unk7
    #  type: u4
    data += struct.pack(">I", 0x0000000f)  # 0x0000000f for the great jaggi quest/(all quests?)

    #- id: unk8
    #  type: u1
    data += b'\0' * 0x01

    #- id: gather_rank (wrong)
    #  type: u1
    data += b'\0' * 0x01

    #- id: unk9
    #  type: u1
    data += b'\0' * 0x01

    #- id: unk10
    #  type: u1
    data += struct.pack(">B", subquest1_hrp)

    #- id: supply_set (wrong)
    #  type: u4
    data += struct.pack(">I", subquest2_hrp)

    #- id: Unknown 4
    #  type: u1
    data += struct.pack(">B", unk_4)

    #- id: supply_type (0x00: low rank, 0x01: high rank, 0x02: arena)
    #  type: u1
    data += struct.pack(">B", resources)
    
    #- id: unk11
    #  size: 2
    #  type: u1
    data += struct.pack(">B", unk_5)
    #  type: u1
    data += struct.pack(">B", unk_6)

    #- id: start_pos (SUPPLY SET NUMBER)
    #  type: u4
    data += struct.pack(">I", supply_set_number)  # 0x00000011 for the great jaggi quest

    #- id: unk12
    #  type: u4
    data += struct.pack(">I", unk_7)

    #- id: unk13
    #  type: u2
    data += b'\0' * 0x02

    #- id: type_flag (STARTING POSITION, 0x0000: basecamp, 0x0001: random, 0x0002: shrine)
    #  type: u2
    data += struct.pack(">h", starting_position)
    
    # UNK
    data += b'\0' * 0x02

    #- id: type_code
    #  type: u2
    data += struct.pack(">h", 0x04b8) 

    #- id: type_amount
    #  type: u2
    data += b'\0' * 0x02

    #- id: general_enemy_level
    #  type: u2
    data += struct.pack(">h", general_enemy_level)

    #- id: unk14
    #  type: u4
    data += struct.pack(">I", unk_9)

    #- id: unk15
    #  type: u4
    data += struct.pack(">I", unk_10)

    #- id: unk16
    #  size: 16
    data += struct.pack(">I", unk_11)
    data += struct.pack(">I", unk_12)  # Unknown 12 (0x00000002 for large monster hunting quests, 0x00000003 for small monster & gathering quests, 0x00000005 for Jhen & Alatreon)
    data += make_quest_properties_type(mainquest_type, mainquest_objectivetype, mainquest_objectivenum)

    #- id: main_objective_rewards
    #  type: reward_type
    #  repeat: expr
    #  repeat-expr: 11
    data += generate_rewards(mainquest_rewards1)

    #- id: main_objective_additional_rewards
    #  type: reward_type
    #  repeat: expr
    #  repeat-expr: 11
    data += generate_rewards(mainquest_rewards2)

    # SUBQUEST 1 REWARDS
    if subquest1_type is not None:
        data += make_quest_properties_type(subquest1_type, subquest1_objectivetype, subquest1_objectivenum)
        data += generate_rewards(sq1_rewards)
    else:
        data += b"\0" * 0x08
        data += b'\0' * (4 * 11)
    data += b'\0' * (4 * 11)

    # SUBQUEST 2 REWARDS
    if subquest2_type is not None:
        data += make_quest_properties_type(subquest2_type, subquest2_objectivetype, subquest2_objectivenum)
        data += generate_rewards(sq2_rewards)
    else:
        data += b"\0" * 0x08
        data += b'\0' * (4 * 11)
    data += b'\0' * (4 * 11)

    assert len(data) == 0x4B4
    try:
        data += read_quest_sm_data(smallmonster_data)
    except Exception as e:
        pass

    return data


# FLAGS INFO:
# (Arena quests have bytes in "QUEST_FLAG_ARENA = 0b10000" set)
# byte 1: Boss Order 1 (+1: Unknown1  +2: All At Once(CombineSubquestsRequireMQAndFirstSubquest)  +4: Marathon (CombineSubquestsRequireMQAndBothSubquests) +8: Unknown4  +16: Unknown5  +32: Unknown6  +64: Unknown7  +128: CombineMainAndSubquests)
# byte 2: Boss Order 2 (+1: Unknown1  +2: Unknown2  +4: RequireMQAndBothSubquests  +8: Unknown4  +16: QualifyingTime  +32: DontAnnounceSubquestCompletion  +64: Unknown7  +128: ElderDragonLeftWounded)
# byte 3: Boss Order 3 (+1: 2Mon_NoSubs_ReqSub1_Unstable  +2: Unknown2  +4: Unknown3  +8: BanjoMusic  +16: Unknown5  +32: Unknown6  +64: Unknown7  +128: Unknown8)
# byte 4: Quest Flags (+1: Slay  +2: Deliver  +4: Capture  +8: Defend  +16: Unknown1  +32: Unknown2  +64: Repel(EndAtMainQuest)  +128: Unknown3)
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
    with open('event/'+fname) as f:
        data = f.read()
    return bytearray.fromhex(data.replace(" ","").replace("\n",""))


"""
EVENT QUEST 1: Jump Four Jaggi
(INCOMPLETE) Only 3 jaggi spawn, and all at once instead of sequentially.
Quest description/rewards/etc from https://www.youtube.com/watch?v=qyQt2Xmpt0g
Quest requirements altered to make it possible to win.
"""
QUEST_EVENT_JUMP_FOUR_JAGGI = make_binary_event_quest(61001, "Jump Three Jaggi", "Guild Subcontractor", "Hunt 3 Great Jaggi", generate_flags((0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(1,0,1,0,0,0,1,1)),  # quest id, name, client, description, flags
    Monster.great_jaggi, 0x0000, True, 0x17, 0x64, 0x01, 0x03,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.great_jaggi, 0x0001, True, 0x17, 0x64, 0x01, 0x03,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.great_jaggi, 0x0002, True, 0x17, 0x64, 0x01, 0x03,  # monster 3:  type, boss id, enabled, level, size, min, max
    4000, 4000, 0, 1400, 400, 50, Monster.bnahabra2, Monster.melynx,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_SANDY_PLAINS, QuestRankType.star_1, 440, QuestRestrictionType.RESTRICTION_NONE, ResourcesType.low_rank, 19,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000001, Monster.great_jaggi, 0x03,  # Main quest: type, target, number
    "Hunt 2 Great Jaggi", 0x00000001, Monster.great_jaggi, 0x02,  # Subquest 1: Description, type, target, number
    "None.", 0, Monster.none, 0,  # Subquest 2: Description, type, target, number
    "I'm gonna get so fired for" + '\x0A' + "this... The Great Jaggi some" + '\x0A' +
        "hunter brought in just" + '\x0A' + "escaped. Mind going after" + '\x0A' +
        "them? You better hurry," + '\x0A' + "though. Bet they've got some" + '\x0A' +
        "incredible materials, too.",  # Quest details
    StartingPositionType.camp, 0x0017, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000050, 0x00000064, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x0002018B, 0x00010000, 0x00000000, 0x64050219,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_jumpfourjaggi.dat', # Small monster data
    [(ItemsType.great_jagi_claw, 1, 3), (ItemsType.great_jagi_hide, 1, 12), (ItemsType.jagi_scale, 1, 10), (ItemsType.screamer, 1, 20),
        (ItemsType.kings_frill, 1, 12), (ItemsType.bone_husk_s, 8, 18), (ItemsType.great_jagi_head, 1, 25)],
    [(ItemsType.mystery_charm, 1, 1), (ItemsType.aquaglow_jewel, 1, 1), (ItemsType.shining_charm, 1, 1), (ItemsType.armor_sphere, 1, 1),
        (ItemsType.armor_sphere_plus, 1, 1)],
    [(ItemsType.great_jagi_claw, 1, 1), (ItemsType.great_jagi_hide, 1, 1), (ItemsType.jagi_scale, 1, 1),
        (ItemsType.screamer, 1, 1), (ItemsType.kings_frill, 1, 1), (ItemsType.bone_husk_s, 8, 1),
        (ItemsType.great_jagi_head, 1, 1)],
    [])

"""
EVENT QUEST 7: The Phantom Uragaan
Quest description from https://www.youtube.com/watch?v=Py5PkCXhf6w
"""
QUEST_EVENT_THE_PHANTOM_URAGAAN = make_binary_event_quest(61007, "The Phantom Uragaan", "Spoiled Princess", "Hunt an Uragaan", generate_flags((0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,1,0,0,0,0),(1,0,1,0,0,0,1,1)),  # quest id, name, client, description, flags
    Monster.uragaan, 0x0000, True, 0x1D, 0x13, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    8800, 0, 0, 3000, 850, 50, Monster.uroktor, Monster.aptonoth,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_VOLCANO, QuestRankType.star_3, 1100, QuestRestrictionType.RESTRICTION_18_INITJOIN, ResourcesType.low_rank, 15,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000001, Monster.uragaan, 0x01,  # Main quest: type, target, number
    "None.", 0x00000000, Monster.none, 0x00,  # Subquest 1: Description, type, target, number
    "None.", 0x00000000, Monster.none, 0x00,  # Subquest 2: Description, type, target, number
    "Oooh, I just heard they've" + '\x0A' + "spotted the cutest, tiniest," + '\x0A' +
        "most adorable little Uragaan" + '\x0A' + "on the Volcano. Hunt me one" + '\x0A' +
        "this instant or I will get" + '\x0A' + "very angry. And if I'm angry," + '\x0A' +
        "Daddy's angry. Now go!",  # Quest details
    StartingPositionType.camp, 0x1D, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_phantomuragaan.dat', # Small monster data
    [(ItemsType.mystery_charm, 1, 1), (ItemsType.uragaan_shell, 1, 16), (ItemsType.uragaan_scale, 1, 20), (ItemsType.uragaan_marrow, 1, 10),
        (ItemsType.monster_bone_l, 1, 10), (ItemsType.bone_husk_l, 15, 13), (ItemsType.shining_charm, 1, 5), (ItemsType.rustshard, 1, 25)],
    [(ItemsType.mystery_charm, 1, 1), (ItemsType.uragaan_shell, 1, 16), (ItemsType.uragaan_scale, 1, 20), (ItemsType.uragaan_marrow, 1, 10),
        (ItemsType.monster_bone_l, 1, 10), (ItemsType.bone_husk_l, 15, 13), (ItemsType.shining_charm, 1, 5), (ItemsType.rustshard, 1, 25)],
    [],
    [])

"""
EVENT QUEST 8: Blood Sport
Quest description from https://www.youtube.com/watch?v=tuRSdC_mlO4
"""
QUEST_EVENT_BLOOD_SPORT = make_binary_event_quest(61008, "Blood Sport", "Spoiled Princess", "Hunt an Uragaan" + '\x0A' + "and a Diablos", generate_flags((0,1,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(1,0,1,0,0,0,0,0)),  # quest id, name, client, description, flags
    Monster.uragaan, 0x0000, True, 0x1D, 0x64, 0x01, 0x03,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.diablos, 0x0001, True, 0x1D, 0x64, 0x01, 0x03,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    17600, 0, 0, 6000, 1750, 50, Monster.uragaan, Monster.diablos,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_LAND_ARENA_1, QuestRankType.star_3, 1760, QuestRestrictionType.RESTRICTION_18_INITJOIN, ResourcesType.low_rank, 43,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000001, Monster.uragaan, 0x01,  # Main quest: type, target, number
    "None.", 0x00000001, Monster.diablos, 0x01,  # Subquest 1: Description, type, target, number
    "None.", 0, Monster.none, 0,  # Subquest 2: Description, type, target, number
    "Oh, boo! I'm tired of watching" + '\x0A' + "run-of-the-mill hunts. The" + '\x0A' +
        "Diablos and the Uragaan are" + '\x0A' + "supposed to be the ultimate" + '\x0A' +
        "monster duo. I'd love to watch" + '\x0A' + "them maim some foolish hunter!" + '\x0A' +
        "Do put on a good show...",  # Quest details
    StartingPositionType.camp, 0x001D, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00010000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_bloodsport.dat', # Small monster data
    [(ItemsType.uragaan_scale, 1, 1), (ItemsType.diablos_ridge, 1, 14), (ItemsType.uragaan_shell, 1, 10), (ItemsType.diablos_shell, 1, 20),
        (ItemsType.twisted_horn, 1, 12), (ItemsType.diablos_marrow, 8, 9), (ItemsType.uragaan_marrow, 1, 9), (ItemsType.incomplete_plans, 1, 25)],
    [(ItemsType.uragaan_scale, 1, 1), (ItemsType.diablos_ridge, 1, 14), (ItemsType.uragaan_shell, 1, 10), (ItemsType.diablos_shell, 1, 20),
        (ItemsType.twisted_horn, 1, 12), (ItemsType.diablos_marrow, 1, 9), (ItemsType.uragaan_marrow, 1, 9), (ItemsType.incomplete_plans, 1, 25)],
    [],
    [])

"""
EVENT QUEST 2: Mercy Mission
(INCOMPLETE) Invading monster not guaranteed to be Royal Ludroth.
"""
QUEST_EVENT_MERCY_MISSION = make_binary_event_quest(61002, "Mercy Mission", "MH3SP Dev Team", "Deliver 10 Monster Guts", generate_flags((0,0,0,0,0,0,0,0),(1,1,1,0,0,0,0,0),(0,0,0,0,0,0,0,0),(0,1,0,0,0,0,0,0)),  # quest id, name, client, description, flags
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    1500, 1200, 2000, 600, 150, 15, Monster.ludroth, Monster.epioth,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_D_ISLAND, QuestRankType.star_1, 70, QuestRestrictionType.RESTRICTION_NONE, ResourcesType.low_rank, 35,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000002, ItemsType.monster_guts, 0x0A,  # Main quest: type, target, number
    "Deliver 12 Red Coral Stones", 0x00000002, ItemsType.red_coral_stone, 0x0C,  # Subquest 1: Description, type, target, number
    "Deliver 3 Goldenfish", 0x00000002, ItemsType.goldenfish, 0x03,  # Subquest 2: Description, type, target, number
    "Wanted:" + '\x0A' + "The description for this" + '\x0A' +
        "quest! If you can find" + '\x0A' + "it, please let us know!" + '\x0A' +
        "Thanks!",  # Quest details
    StartingPositionType.camp, 0x0017, 0x00000003,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    55, 70, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00010000, 0x00000000, 0x64030303,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_mercymission.dat', # Small monster data
    [(ItemsType.mystery_charm, 1, 8), (ItemsType.black_pearl, 1, 20), (ItemsType.honey, 2, 20), (ItemsType.armor_sphere, 1, 18),
        (ItemsType.small_goldenfish, 1, 8), (ItemsType.machalite_ore, 8, 14), (ItemsType.steel_eg, 1, 12)],
    [(ItemsType.mystery_charm, 1, 35), (ItemsType.aquaglow_jewel, 1, 5), (ItemsType.shining_charm, 1, 15), (ItemsType.armor_sphere, 1, 20),
        (ItemsType.armor_sphere_plus, 1, 25)],
    [(ItemsType.mystery_charm, 1, 8), (ItemsType.black_pearl, 1, 20), (ItemsType.honey, 2, 20), (ItemsType.armor_sphere, 1, 18),
        (ItemsType.small_goldenfish, 1, 8), (ItemsType.machalite_ore, 1, 14), (ItemsType.steel_eg, 1, 12)],
    [(ItemsType.mystery_charm, 1, 35), (ItemsType.aquaglow_jewel, 1, 5), (ItemsType.shining_charm, 1, 15), (ItemsType.armor_sphere, 1, 20),
        (ItemsType.armor_sphere_plus, 1, 25)],
    success_message="Complete the Main Quest"+'\x0A'+"and both Subquests.")

"""
EVENT QUEST 20: World Eater
Quest description/rewards/etc from https://www.youtube.com/watch?v=Z6joazT8J78
(INCOMPLETE) Needs invading queropeco
"""
QUEST_EVENT_WORLD_EATER = make_binary_event_quest(61020, "World Eater", "Guildmaster", "Hunt a Deviljho", generate_flags((0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(1,0,1,0,0,0,1,1)),  # quest id, name, client, description, flags
    Monster.deviljho, 0x0000, True, 0x40, 0xC8, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    18000, 0, 0, 6000, 1800, 50, Monster.jaggi, Monster.jaggia,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_D_ISLAND, QuestRankType.urgent, 1800, QuestRestrictionType.RESTRICTION_51_INITJOIN, ResourcesType.high_rank, 31,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000001, Monster.deviljho, 0x01,  # Main quest: type, target, number
    "None.", 0x00000000, Monster.none, 0x00,  # Subquest 1: Description, type, target, number
    "None.", 0x00000000, Monster.none, 0x00,  # Subquest 2: Description, type, target, number
    "Emergency! A huge Deviljho has" + '\x0A' + "appeared. It's twice as big as" + '\x0A' +
        "a normal one and it's eating" + '\x0A' + "everything in sight! Go get" + '\x0A' +
        "it! And now, a haiku: A huge" + '\x0A' + "Deviljho/with no food in its" + '\x0A' +
        "stomach/eats the whole island.",  # Quest details
    StartingPositionType.random, 0x0040, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_worldeater.dat', # Small monster data
    [(ItemsType.timeworn_charm, 1, 33), (ItemsType.deviljho_gem, 1, 4), (ItemsType.deviljho_scalp, 1, 8), (ItemsType.deviljho_hide, 1, 17),
        (ItemsType.hvy_armor_sphere, 1, 11), (ItemsType.shining_charm, 1, 19), (ItemsType.deviljho_fang, 1, 8)],
    [(ItemsType.deviljho_scalp, 1, 20), (ItemsType.timeworn_charm, 1, 34), (ItemsType.deviljho_fang, 1, 6), (ItemsType.deviljho_hide, 1, 17),
        (ItemsType.deviljho_gem, 1, 3), (ItemsType.shining_charm, 1, 11), (ItemsType.hvy_armor_sphere, 1, 9)],
    [],
    [])

"""
EVENT QUEST 20: Where Gods Fear To Tread
Quest description from https://www.youtube.com/watch?v=mQHTdPRlD1w,
    thanks to "soulmizute, emperor of the abyss#5094"
    and "El Matiah#8904"
"""
QUEST_EVENT_WHERE_GODS_FEAR_TO_TREAD = make_binary_event_quest(61021, "Where Gods Fear to Tread", "Scarlet Mystery Man", "Slay the Alatreon", generate_flags((0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(1,0,0,0,0,0,1,0)),  # quest id, name, client, description, flags
    Monster.alatreon, 0x0000, True, 0x40, 0x7D, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    42000, 0, 0, 14000, 4200, 50, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_SACRED_LAND, QuestRankType.urgent, 4200, QuestRestrictionType.RESTRICTION_51_INITJOIN, ResourcesType.high_rank, 0,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000101, Monster.alatreon, 0x01,  # Main quest: type, target, number
    "None", 0x00000000, Monster.none, 0x00,  # Subquest 1: Description, type, target, number
    "None", 0x00000000, Monster.none, 0x00,  # Subquest 2: Description, type, target, number
    "I've been waiting, hunter. Now" + '\x0A' + "comes your final challenge:" + '\x0A' +
        "Alatreon, a dragon of darkness" + '\x0A' + "and light. Can mere mortals" + '\x0A' +
        "fell an elder dragon feared" + '\x0A' + "even by the gods? Don't even" + '\x0A' +
        "bother saying your prayers...",  # Quest details
    StartingPositionType.shrine, 0x0040, 0x00000005,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_wheregodsfeartotread.dat', # Small monster data
    [(ItemsType.alatreon_scute, 1, 40), (ItemsType.brkn_skypiercer, 1, 30), (ItemsType.alatreon_talon, 1, 10), (ItemsType.alatreon_plate, 1, 10),
        (ItemsType.skypiercer, 1, 5), (ItemsType.azure_dragongem, 1, 5)],
    [(ItemsType.alatreon_plate, 1, 11), (ItemsType.brkn_skypiercer, 1, 34), (ItemsType.alatreon_talon, 1, 39), (ItemsType.elderdragonblood, 1, 6),
        (ItemsType.skypiercer, 1, 5), (ItemsType.azure_dragongem, 1, 5)],
    [],
    [])

QUEST_EVENT_GREEN_EGGS = make_binary_event_quest(61050, "[MH3SP] Green Eggs and...", "Ze SpyRo", "Hunt a Gigginox" + '\x0A' + "and an Agnaktor", generate_flags((0,1,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(1,0,1,0,0,0,0,0)),  # quest id, name, client, description, flags
    Monster.gigginox, 0x0000, True, 0x1B, 0x64, 0x00, 0x03,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.agnaktor, 0x0001, True, 0x1B, 0x64, 0x00, 0x03,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0002, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    7000, 5, 0, 2400, 200, 50, Monster.gigginox, Monster.agnaktor,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_LAND_ARENA_1, QuestRankType.star_3, 950, QuestRestrictionType.RESTRICTION_18_INITJOIN, ResourcesType.low_rank, 43,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000001, Monster.gigginox, 0x01,  # Main quest: type, target, number
    "None", 0x00000001, Monster.agnaktor, 0x01,  # Subquest 1: Description, type, target, number
    "None", None, Monster.none, 0x00,  # Subquest 2: Description, type, target, number
    "Why do we live, only to suffer?" + '\x0A' + "Only slayers of pig meat know" + '\x0A' +
        "these things. Take care, Hunter," + '\x0A' + "for those who look to antidote" + '\x0A' +
        "herbs may find their breath" + '\x0A' + "stolen away.",  # Quest details
    StartingPositionType.camp, 0x001B, 0x00000002,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000000, 0x00000000, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x00000000, 0x00000000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_emptylandarena.dat', # Small monster data
    [(ItemsType.flabby_hide, 1, 18), (ItemsType.uncanny_hide, 1, 6), (ItemsType.pale_extract, 1, 11), (ItemsType.poison_sac, 1, 15),
        (ItemsType.agnaktor_shell, 1, 10), (ItemsType.agnaktor_scale, 1, 16), (ItemsType.agnaktor_hide, 1, 13), (ItemsType.agnaktor_fin, 1, 6),
        (ItemsType.agnaktor_beak, 1, 5)],
    [(ItemsType.flabby_hide, 1, 13), (ItemsType.uncanny_hide, 1, 6), (ItemsType.pale_extract, 1, 11), (ItemsType.poison_sac, 1, 10),
        (ItemsType.agnaktor_shell, 1, 9), (ItemsType.agnaktor_scale, 1, 10), (ItemsType.agnaktor_hide, 1, 10), (ItemsType.agnaktor_fin, 1, 6),
        (ItemsType.agnaktor_beak, 1, 5), (ItemsType.commendation, 1, 20)],
    [],
    [])

QUEST_EVENT_DESERT_BUS = make_binary_event_quest(61051, "Desert Bus", "Ze SpyRo", "Deliver 100 Herbivore Eggs", generate_flags((0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(0,1,0,0,0,0,1,1)),  # quest id, name, client, description, flags
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    7000, 5, 0, 2400, 200, 180, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_SANDY_PLAINS, QuestRankType.star_1, 550, QuestRestrictionType.RESTRICTION_NO_ARMOR, ResourcesType.low_rank, 0x0000002C,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000002, 395, 0x64,  # Main quest: type, target, number
    "Deliver 1 Herbivore Egg", 0x00000002, 395, 0x01,  # Subquest 1: Description, type, target, number
    "None", None, Monster.none, 0x00,  # Subquest 2: Description, type, target, number
    "Death." + '\x0A' + "Death, and taxes." + '\x0A' +
        "Death, taxes, and Herbivore Eggs." + '\x0A' + "Look to your sins, Hunter.",  # Quest details
    StartingPositionType.camp, 0x0019, 0x00000003,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000050, 0x00000064, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x0002018B, 0x00010000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_desertbus.dat', # Small monster data
    [(ItemsType.dung, 4, 50), (ItemsType.garbage, 3, 50)],
    [(ItemsType.dung, 1, 50), (ItemsType.garbage, 1, 50)],
    [(ItemsType.garbage, 1, 100)],
    [])

QUEST_EVENT_DEBUG = make_binary_event_quest(61052, "Potion Bus", "Ze SpyRo", "Deliver 1 Potion", generate_flags((0,0,1,0,0,0,0,0),(1,1,0,0,0,0,0,0),(0,0,0,0,0,0,0,0),(0,1,0,0,0,0,0,0)),  # quest id, name, client, description, flags
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 1:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 2:  type, boss id, enabled, level, size, min, max
    Monster.none, 0x0000, False, 0x00, 0x00, 0x00, 0x00,  # monster 3:  type, boss id, enabled, level, size, min, max
    3, 0, 0, 1, 5, 55, Monster.none, Monster.none,  # main reward, sub1 reward, sub2 reward, cart penalty, quest fee, time limit, mainmonst1, mainmonst2
    LocationType.QUEST_LOCATION_SANDY_PLAINS, QuestRankType.star_2, 10, QuestRestrictionType.RESTRICTION_9_INITJOIN, ResourcesType.low_rank, 0x0000002C,  # location, quest rank, hrp reward, rank requirement, resources type, supply set number
    0x00000002, ItemsType.potion, 0x01,  # Main quest: type, target, number
    "Deliver 1 Herb", 0x00000002, ItemsType.herb, 0x01,  # Subquest 1: Description, type, target, number
    "Deliver 1 Whetstone", 0x00000002, ItemsType.whetstone, 0x01,  # Subquest 2: Description, type, target, number
    "Debug debug debug!!!!",  # Quest details
    StartingPositionType.camp, 0x0019, 0x00000003,  # Start position, general enemy level, unk_12 (2 for large mon quest, 3 for small/delivery, 5 for jhen/ala)
    0x00000050, 0x00000064, 0x00, 0x00, 0x00, 0x00000000,  # Subquest1 HRP, Subquest2 HRP, Unknown 4, Unknown 5, Unknown 6, Unknown 7
    0x0002018B, 0x00010000, 0x00000000, 0x00000000,  # Unknown 9, Unknown 10, Unknown 11, Summon
    'sm_desertbus.dat', # Small monster data
    [(ItemsType.earth_crystal, 4, 50), (ItemsType.machalite_ore, 3, 25), (ItemsType.iron_ore, 2, 15), (ItemsType.stone, 4, 3),
        (ItemsType.garbage, 2, 2), (ItemsType.iron_pickaxe, 2, 1), (ItemsType.jagi_scale, 2, 1), (ItemsType.jagi_hide, 2, 1),
        (ItemsType.potion, 2, 1), (ItemsType.raw_meat, 2, 1)],
    [(ItemsType.earth_crystal, 4, 50), (ItemsType.machalite_ore, 3, 25), (ItemsType.iron_ore, 2, 15), (ItemsType.stone, 4, 3),
        (ItemsType.garbage, 2, 1), (ItemsType.iron_pickaxe, 2, 1), (ItemsType.jagi_scale, 2, 1), (ItemsType.jagi_hide, 2, 1),
        (ItemsType.potion, 2, 1), (ItemsType.raw_meat, 2, 1), (ItemsType.monster_bone_s, 2, 1)],
    [(ItemsType.earth_crystal, 4, 50), (ItemsType.machalite_ore, 3, 25), (ItemsType.iron_ore, 2, 15), (ItemsType.stone, 4, 3),
        (ItemsType.garbage, 2, 1), (ItemsType.iron_pickaxe, 2, 1), (ItemsType.jagi_scale, 2, 1), (ItemsType.jagi_hide, 2, 1),
        (ItemsType.potion, 2, 1), (ItemsType.raw_meat, 2, 1), (ItemsType.monster_bone_s, 2, 1)],
    [])
