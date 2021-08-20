#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter constants.

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


def pad(s, size, p=b'\0'):
    data = bytearray(s + p * max(0, size - len(s)))
    data[-1] = 0
    return data


def make_binary_server_type_list(is_jap=False):
    data = b""
    PROPERTIES = [
        (b"Open", b"Hunters of all Ranks\ncan gather here.", 0, 999),
        (b"Rookie", b"Only hunters HR 30\nor lower may enter.", 0, 30),
        (b"Expert", b"Only hunters HR 31\nor higher may enter.", 31, 999),
        (b"Recruiting", b"Hunters in search of\n"
         b"hunting companions\ncan gather here.", 0, 999),
        (b"Modding", b"Mods are allowed here.", 0, 999)
    ]

    # Handle server type properties
    for name, desc, hr_min, hr_max in PROPERTIES:
        data += pad(name, 16 if is_jap else 24)
        data += pad(desc, 112 if is_jap else 168)

    # Handle HR rank limits
    p = 0xDDC if is_jap else 0x13AC
    data = pad(data, p + len(PROPERTIES) * 5)
    for i, (name, desc, hr_min, hr_max) in enumerate(PROPERTIES):
        data[p:p+2] = struct.pack(">H", hr_min)
        data[p+2:p+4] = struct.pack(">H", hr_max)
        p += 4

    if is_jap:
        # TODO: Reverse the japanese struct
        return data

    # Handle city seekings
    SEEKINGS = [
        b"Seeking0", b"Seeking1", b"Seeking2",
    ]
    for i, seeking in enumerate(SEEKINGS):
        p = 0x30C + i * 52  # struct size
        data[p:p+len(seeking)] = seeking
        data[0x33D + i * 52] = 0x01
        data[0x33E + i * 52] = 0xFF
    return data


def make_binary_npc_greeters(is_jap=False):
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
    data = b""
    data += pad(b"Plaza Tool Shop\n\nNot supported yet.", offset)
    data += pad(b"Material shop unavailable\nyet.", offset)
    data += pad(b"Trading post closed at\nthe moment.", offset)
    data += pad(b"No event quests.", offset)
    data += pad(b"No arena quests.", offset)
    data += pad(b"To all hunters:\n\nThis is a test server.", offset)
    return data


def make_binary_trading_post():
    data = b""

    def slot(item, qty):
        return struct.pack(">HH", item, qty)

    # Popfish x8 <- Machalite Ore x2 | Rathian Coin x2
    data += slot(0xd2, 8) + slot(0x65, 2) + slot(0x262, 2) + slot(0, 0)

    # Waterblock Seed x3 <- Bone x4 | Qurupeco Coin x1
    data += slot(0x188, 3) + slot(0xc4, 4) + slot(0x25f, 1) + slot(0, 0)

    # Bone Husk S x10 <- Bone x2 | Barroth Coin x2
    data += slot(0x156, 10) + slot(0xc4, 2) + slot(0x260, 2) + slot(0, 0)

    # Dung x5 <- Monster Fluid x1 | R.Ludroth Coin x1
    data += slot(0xc5, 5) + slot(0x155, 1) + slot(0x261, 1) + slot(0, 0)

    # Sharpened Fang x5 <- Hydro Hide x2 | R.Ludroth Coin x2
    data += slot(0x232, 5) + slot(0x141, 1) + slot(0x261, 2) + slot(0, 0)

    # Toadstool x5 <- Sharpened Fang x1 | Qurupeco Coin x1
    data += slot(0x158, 5) + slot(0x232, 1) + slot(0x25f, 1) + slot(0, 0)

    # Stone x10 <- Monster Bone M x1 | Great Jaggi Coin x2
    data += slot(0x61, 10) + slot(0x9a, 1) + slot(0x25e, 2) + slot(0, 0)

    # Spider Web x5 <- Monster Fluid x1 | Barroth Coin x1
    data += slot(0xc6, 5) + slot(0x155, 1) + slot(0x260, 1) + slot(0, 0)

    # Bughopper x10 <- Big Fin x3 | R.Ludroth Coin x2
    data += slot(0x160, 10) + slot(0x230, 3) + slot(0x261, 2) + slot(0, 0)

    # Icethaw Pellet x3 <- Mystery Bone x4 | R.Ludroth Coin x1
    data += slot(0x189, 3) + slot(0x10e, 4) + slot(0x261, 1) + slot(0, 0)

    # Rathian Scale x1 <- Rathian Coin x3 | Pinnacle Coin x2
    data += slot(0x112, 1) + slot(0x262, 3) + slot(0x267, 2) + slot(0, 0)

    # Wyvern Claw x8 <- Great Baggi Claw x1 | Rathian Coin x1
    data += slot(0x167, 8) + slot(0x21d, 1) + slot(0x262, 1) + slot(0, 0)

    # Prize Gold Sword x1 <- Lagiacrus Coin x15 | Pinnacle Coin x8
    data += slot(0x25d, 1) + slot(0x263, 15) + slot(0x267, 8) + slot(0, 0)

    # Barioth Shell x1 <- Barioth Coin x3 | Pinnacle Coin x2
    data += slot(0x194, 1) + slot(0x24a, 3) + slot(0x267, 2) + slot(0, 0)

    # Armor Stone x3 <- Deviljho Coin x1 | Pinnacle Coin x1
    data += slot(0x1bb, 3) + slot(0x24d, 1) + slot(0x267, 1) + slot(0, 0)

    return data


# msf-pattern_create -l 0xe50
MSF_PATTERN = \
    "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac" \
    "3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6A" \
    "e7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0" \
    "Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj" \
    "4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7A" \
    "l8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1" \
    "Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq" \
    "5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8A" \
    "s9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2" \
    "Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax" \
    "6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9B" \
    "a0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3" \
    "Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be" \
    "7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0B" \
    "h1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4" \
    "Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl" \
    "8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1B" \
    "o2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5" \
    "Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs" \
    "9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2B" \
    "v3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6" \
    "Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca" \
    "0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3C" \
    "c4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7" \
    "Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch" \
    "1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4C" \
    "j5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8" \
    "Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co" \
    "2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5C" \
    "q6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1Cs2Cs3Cs4Cs5Cs6Cs7Cs8Cs9" \
    "Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv" \
    "3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6C" \
    "x7Cx8Cx9Cy0Cy1Cy2Cy3Cy4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0" \
    "Da1Da2Da3Da4Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc" \
    "4Dc5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5De6De7D" \
    "e8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6Dg7Dg8Dg9Dh0Dh1" \
    "Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj" \
    "5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7Dk8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8D" \
    "l9Dm0Dm1Dm2Dm3Dm4Dm5Dm6Dm7Dm8Dm9Dn0Dn1Dn2Dn3Dn4Dn5Dn6Dn7Dn8Dn9Do0Do1Do2" \
    "Do3Do4Do5Do6Do7Do8Do9Dp0Dp1Dp2Dp3Dp4Dp5Dp6Dp7Dp8Dp9Dq0Dq1Dq2Dq3Dq4Dq5Dq" \
    "6Dq7Dq8Dq9Dr0Dr1Dr2Dr3Dr4Dr5Dr6Dr7Dr8Dr9Ds0Ds1Ds2Ds3Ds4Ds5Ds6Ds7Ds8Ds9D" \
    "t0Dt1Dt2Dt3Dt4Dt5Dt6Dt7Dt8Dt9Du0Du1Du2Du3Du4Du5Du6Du7Du8Du9Dv0Dv1Dv2Dv3" \
    "Dv4Dv5Dv6Dv7Dv8Dv9Dw0Dw1Dw2Dw3Dw4Dw5Dw6Dw7Dw8Dw9Dx0Dx1Dx2Dx3Dx4Dx5Dx6Dx" \
    "7Dx8Dx9Dy0Dy1Dy2Dy3Dy4Dy5Dy6Dy7Dy8Dy9Dz0Dz1Dz2Dz3Dz4Dz5Dz6Dz7Dz8Dz9Ea0E" \
    "a1Ea2Ea3Ea4Ea5Ea6Ea7Ea8Ea9Eb0Eb1Eb2Eb3Eb4Eb5Eb6Eb7Eb8Eb9Ec0Ec1Ec2Ec3Ec4" \
    "Ec5Ec6Ec7Ec8Ec9Ed0Ed1Ed2Ed3Ed4Ed5Ed6Ed7Ed8Ed9Ee0Ee1Ee2Ee3Ee4Ee5Ee6Ee7Ee" \
    "8Ee9Ef0Ef1Ef2Ef3Ef4Ef5Ef6Ef7Ef8Ef9Eg0Eg1Eg2Eg3Eg4Eg5Eg6Eg7Eg8Eg9Eh0Eh1E" \
    "h2Eh3Eh4Eh5Eh6Eh7Eh8Eh9Ei0Ei1Ei2Ei3Ei4Ei5Ei6Ei7Ei8Ei9Ej0Ej1Ej2Ej3Ej4Ej5" \
    "Ej6Ej7Ej8Ej9Ek0Ek1Ek2Ek3Ek4Ek5Ek6Ek7Ek8Ek9El0El1El2El3El4El5El6El7El8El" \
    "9Em0Em1Em2Em3Em4Em5Em6Em7Em8Em9En0En1En2En3En4En5En6En7En8En9Eo0Eo1Eo2E" \
    "o3Eo4Eo5Eo6Eo7Eo8Eo9Ep0Ep1Ep2Ep3Ep4Ep5Ep6Ep7Ep8Ep9Eq0Eq1Eq2Eq3Eq4Eq5Eq6" \
    "Eq7Eq8Eq9Er0Er1Er2Er3Er4Er5Er6Er7Er8Er9Es0E"


TERMS_VERSION = 1
TERMS = {
    1: b"""MH3 Server Project - Terms.""",
    2: (b"-DEBUG- -DEBUG- -DEBUG- -DEBUG-\n" * 0x200) + b"- ZHIEND"
}
SUBTERMS = {
    1: b"""MH3 Server Project - SubTerms.""",
    2: b"-DEBUG- Subterms"
}
ANNOUNCE = b"""<BODY><CENTER>MH3 Server Project - Announce.<END>"""
CHARGE = b"""<BODY><CENTER>MH3 Server Project - No charge.<END>"""
# VULGARITY_INFO = b"""MH3 Server Project - Vulgarity info (low)."""
VULGARITY_INFO = b""
FMP_VERSION = 1

# Dummy PAT_BINARY
PAT_BINARIES = {
    0x01: {
        "version": 1,
        "content": make_binary_server_type_list(is_jap=False)
    },
    0x02: {
        "version": 1,
        "content": b"2" * 0x10  # b"vivi\tvovo\tvuvu\nbibi\tbobo\bubu\nouba\t"
    },
    0x03: {
        "version": 1,
        "content": make_binary_npc_greeters(is_jap=False)
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
    0x06: {
        "version": 1,
        "content": b"dummy_06\0"
    },
    0x07: {
        "version": 1,
        "content": b"dummy_07\0"
    },
    0x08: {
        "version": 1,
        "content": b"dummy_08\0"
    },
    0x09: {
        "version": 1,
        "content": b"dummy_09\0"
    },
    0x0a: {  # Japanese
        "version": 1,
        "content": b"6" * 0x50  # b"foo\tbar\tfuu\nboo\tfaa\bbaa\nree\t"
    },
    0x0b: {
        "version": 1,
        "content": b"dummy_0b\0"
    },
    0x0c: {
        "version": 1,
        "content": b"dummy_0c\0"
    },
    0x0d: {
        "version": 1,
        "content": b"dummy_0d\0"
    },
    0x0e: {
        "version": 1,
        "content": b"dummy_0e\0"
    },
    0x0f: {
        "version": 1,
        "content": b"dummy_0f\0"
    },
    0x10: {  # French
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x11: {  # French
        "version": 1,
        "content": b"dummy_11\0"
    },
    0x12: {  # French
        "version": 1,
        "content": make_binary_npc_greeters()
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
        "version": 1,
        "content": b"dummy_15\0"
    },
    0x16: {  # French
        "version": 1,
        "content": b"dummy_16\0"
    },
    0x17: {  # French
        "version": 1,
        "content": b"dummy_17\0"
    },
    0x18: {  # French
        "version": 1,
        "content": b"dummy_18\0"
    },
    0x19: {  # French
        "version": 1,
        "content": b"dummy_19\0"
    },
    0x1a: {  # French
        "version": 1,
        "content": b"dummy_1a\0"
    },
    0x1b: {  # French
        "version": 1,
        "content": b"dummy_1b\0"
    },
    0x1c: {  # French
        "version": 1,
        "content": b"dummy_1c\0"
    },
    0x1d: {  # French
        "version": 1,
        "content": b"dummy_1d\0"
    },
    0x1e: {  # French
        "version": 1,
        "content": b"dummy_1e\0"
    },
    0x1f: {  # German
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x20: {  # German
        "version": 1,
        "content": b"dummy_20\0"
    },
    0x21: {  # German
        "version": 1,
        "content": make_binary_npc_greeters()
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
        "version": 1,
        "content": b"dummy_24\0"
    },
    0x25: {  # German
        "version": 1,
        "content": b"dummy_25\0"
    },
    0x26: {  # German
        "version": 1,
        "content": b"dummy_26\0"
    },
    0x27: {  # German
        "version": 1,
        "content": b"dummy_27\0"
    },
    0x28: {  # German
        "version": 1,
        "content": b"dummy_28\0"
    },
    0x29: {  # German
        "version": 1,
        "content": b"dummy_29\0"
    },
    0x2a: {  # German
        "version": 1,
        "content": b"dummy_2a\0"
    },
    0x2b: {  # German
        "version": 1,
        "content": b"dummy_2b\0"
    },
    0x2c: {  # German
        "version": 1,
        "content": b"dummy_2c\0"
    },
    0x2d: {  # German
        "version": 1,
        "content": b"dummy_2d\0"
    },
    0x2e: {  # Italian
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x2f: {  # Italian
        "version": 1,
        "content": b"dummy_2f\0"
    },
    0x30: {  # Italian
        "version": 1,
        "content": make_binary_npc_greeters()
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
        "version": 1,
        "content": b"dummy_33\0"
    },
    0x34: {  # Italian
        "version": 1,
        "content": b"dummy_34\0"
    },
    0x35: {  # Italian
        "version": 1,
        "content": b"dummy_35\0"
    },
    0x36: {  # Italian
        "version": 1,
        "content": b"dummy_36\0"
    },
    0x37: {  # Italian
        "version": 1,
        "content": b"dummy_37\0"
    },
    0x38: {  # Italian
        "version": 1,
        "content": b"dummy_38\0"
    },
    0x39: {  # Italian
        "version": 1,
        "content": b"dummy_39\0"
    },
    0x3a: {  # Italian
        "version": 1,
        "content": b"dummy_3a\0"
    },
    0x3b: {  # Italian
        "version": 1,
        "content": b"dummy_3b\0"
    },
    0x3c: {  # Italian
        "version": 1,
        "content": b"dummy_3c\0"
    },
    0x3d: {  # Spanish
        "version": 1,
        "content": make_binary_server_type_list()
    },
    0x3e: {  # Spanish
        "version": 1,
        "content": b"dummy_3e\0"
    },
    0x3f: {  # Spanish
        "version": 1,
        "content": make_binary_npc_greeters()
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
        "version": 1,
        "content": b"dummy_42\0"
    },
    0x43: {  # Spanish
        "version": 1,
        "content": b"dummy_43\0"
    },
    0x44: {  # Spanish
        "version": 1,
        "content": b"dummy_44\0"
    },
    0x45: {  # Spanish
        "version": 1,
        "content": b"dummy_45\0"
    },
    0x46: {  # Spanish
        "version": 1,
        "content": b"dummy_46\0"
    },
    0x47: {  # Spanish
        "version": 1,
        "content": b"dummy_47\0"
    },
    0x48: {  # Spanish
        "version": 1,
        "content": b"dummy_48\0"
    },
    0x49: {  # Spanish
        "version": 1,
        "content": b"dummy_49\0"
    },
    0x4a: {  # Spanish
        "version": 1,
        "content": b"dummy_4a\0"
    },
    0x4b: {  # Spanish
        "version": 1,
        "content": b"dummy_4b\0"
    },
}

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
    0x64701000: 'Ntc0x6470',
    0x64711000: 'Ntc0x6471',
    0x64721000: 'Ntc0x6472',
    0x64730100: 'ReqLayerTell',
    0x64730200: 'AnsLayerTell',
    0x64731000: 'NtcLayerTell',
    0x64741000: 'Ntc0x6474',
    0x64751000: 'Ntc0x6475',
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
    0x65701000: 'Ntc0x6570',
    0x65711000: 'Ntc0x6571',
    0x65721000: 'Ntc0x6572',
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
    Ntc0x6470 = 0x64701000
    Ntc0x6471 = 0x64711000
    Ntc0x6472 = 0x64721000
    ReqLayerTell = 0x64730100
    AnsLayerTell = 0x64730200
    NtcLayerTell = 0x64731000
    Ntc0x6474 = 0x64741000
    Ntc0x6475 = 0x64751000
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
    Ntc0x6570 = 0x65701000
    Ntc0x6571 = 0x65711000
    Ntc0x6572 = 0x65721000
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
