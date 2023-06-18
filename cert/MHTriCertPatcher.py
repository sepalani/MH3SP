#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2015-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter 3 (~tri) Certificate Patcher

Patch the in-game certificate according to the region:
 - RMHJ08 [NTSC-J]: JAPCertPatcher class
 - RMHE08 [NTSC-U]: USACertPatcher class
 - RMHP08 [PAL]:    PALCertPatcher class

The CertPatcher class is the base class for these patchers.
 - CERT_OFF: Certificate offset
 - CERT_LEN: Certificate length

It can also patch the EC ticket check for the japanese version of the game.
"""

import os
import mmap
from collections import namedtuple
from contextlib import closing


def warning(message, force):
    if not force:
        raise ValueError(message)
    print("! {}". format(message))


class CertPatcher(object):
    """Generic Certificate Patcher."""

    CERT_OFF = None
    CERT_LEN = None
    CERT_HDR = bytearray([
        # ASN.1 DER encoding
        0x30, 0x82, 0x03, 0x98,  # 0:d=0  hl=4 l= 920 cons: SEQUENCE
        0x30, 0x82,              # 4:d=1  hl=4 l= ??? cons:  SEQUENCE
    ])
    DOL_SIZE = 6 * 1024 ** 2
    KNOWN_OFFSETS = {
        0x00639EA0: "Monster Hunter 3 [RMHJ08]",
        0x0056DF80: "Monster Hunter 3 [RMHE08]",
        0x0056E940: "Monster Hunter 3 [RMHP08]",
        0x005153a0: "Monster Hunter G [ROMJ08]",
    }

    def __init__(self, dol, force=False):
        """Constructor.

        dol - path to the main.dol file
        """
        self.dol = dol
        self.force = force
        if os.path.getsize(dol) < self.DOL_SIZE:
            warning("DOL doesn't seem to be from the DATA partition", force)
        if self.CERT_OFF is None or self.CERT_LEN is None:
            self.auto_detect(dol)
        self.print_version()

    def patch_cert(self, crt):
        """Patch the in-game certificate. Will overwrite original dol file!

        crt - path to the certificate file
        """
        if os.path.getsize(crt) > self.CERT_LEN:
            warning("Invalid certificate size", self.force)
        with open(crt, "rb") as f:
            data = f.read(self.CERT_LEN)
            if not data.startswith(self.CERT_HDR):
                warning("Certificate DER header seems invalid", self.force)
            pad = self.CERT_LEN - len(data)
            data += pad * b'\0'
        with open(self.dol, "rb+") as f:
            f.seek(self.CERT_OFF)
            hdr = f.read(len(self.CERT_HDR))
            if hdr != self.CERT_HDR:
                warning("Region offset doesn't point to a valid certificate",
                        self.force)
            f.seek(self.CERT_OFF)
            f.write(data)

    def dump_cert(self, path):
        """Extract the in-game certificate.

        path - destination path
        """
        with open(self.dol, "rb") as f:
            f.seek(self.CERT_OFF)
            data = f.read(self.CERT_LEN)
        with open(path, "wb") as f:
            f.write(data)

    def auto_detect(self, dol):
        """Auto-detect certificate location.

        dol - path to the main.dol file
        """
        self.CERT_LEN = 924
        with open(dol, "rb") as f, \
             closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            matches = []
            header = bytes(self.CERT_HDR)
            offset = m.find(header)
            while offset != -1:
                if not offset % 4:
                    matches.append(offset)
                offset = m.find(header, offset+1)
            if len(matches) != 1:
                raise ValueError("Auto-detection failed: {}".format(matches))
            self.CERT_OFF = matches[0]
            if self.CERT_OFF not in self.KNOWN_OFFSETS:
                warning("Unknown version detected (offset=0x{:08x})".format(
                    self.CERT_OFF), self.force)

    def print_version(self):
        """Print detected version."""
        print("+ Version used: {}".format(
            self.KNOWN_OFFSETS.get(self.CERT_OFF, "Unknown")
        ))


class JAPCertPatcher(CertPatcher):
    """JAP Certificate Patcher."""

    CERT_OFF = 0x00639EA0
    CERT_LEN = 924


class USACertPatcher(CertPatcher):
    """USA Certificate Patcher."""

    CERT_OFF = 0x0056DF80
    CERT_LEN = 924


class PALCertPatcher(CertPatcher):
    """PAL Certificate Patcher."""

    CERT_OFF = 0x0056E940
    CERT_LEN = 924


CodePatch = namedtuple("CodePatch", ["name", "address", "signature", "patch"])


class ECPatcher(object):
    """EC/Wii Shop patcher."""

    PATCHES = [
        CodePatch(
            name="NetworkWiiMediator::isECConfig",
            address=0x803f7fb4,
            signature=bytearray([
                0x80, 0x6d, 0xbd, 0xb0,  # lwz r3,-0x4250 (r13)
                0x2c, 0x03, 0x00, 0x00,  # cmpwi r3, 0
                0x41, 0x82, 0x00, 0x08,  # beq- 0x803F7FC4
                0x4b, 0xff, 0xb5, 0xfc,  # b 0x803F35BC
                0x38, 0x60, 0x00, 0x00,  # li r3, 0
                0x4e, 0x80, 0x00, 0x20   # blr
            ]),
            patch=bytearray([
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x38, 0x60, 0x00, 0x01,  # li r3, 1
                0x4e, 0x80, 0x00, 0x20   # blr
            ])
        ),
        CodePatch(
            name="NetworkWiiMediator::isECTicket",
            address=0x803f7fcc,
            signature=bytearray([
                0x80, 0x6d, 0xbd, 0xb0,  # lwz r3, -0x4250 (r13)
                0x2c, 0x03, 0x00, 0x00,  # cmpwi r3, 0
                0x41, 0x82, 0x00, 0x08,  # beq- 0x803F7FDC
                0x4b, 0xff, 0xb5, 0xec,  # b 0x803F35C4
                0x38, 0x60, 0x00, 0x00,  # li r3, 0
                0x4e, 0x80, 0x00, 0x20   # blr
            ]),
            patch=bytearray([
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x38, 0x60, 0x00, 0x01,  # li r3, 1
                0x4e, 0x80, 0x00, 0x20   # blr
            ])
        ),
        CodePatch(
            name="EC_Init",
            address=0x804e2088,
            signature=bytearray([
                0x94, 0x21, 0xff, 0xd0,  # stwu sp, -0x0030 (sp)
                0x7c, 0x08, 0x02, 0xa6,  # mflr r0
                0x90, 0x01, 0x00, 0x34,  # stw r0, 0x0034 (sp)
                0x39, 0x61, 0x00, 0x30,  # addi r11, sp, 48
                0x4b, 0xf7, 0x22, 0xf9   # bl 0x80454390
            ]),
            patch=bytearray([
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x38, 0x60, 0x00, 0x00,  # li r3, 0
                0x4e, 0x80, 0x00, 0x20   # blr
            ])
        ),
        CodePatch(
            name="EC_SetParameter",
            address=0x804e2278,
            signature=bytearray([
                0x94, 0x21, 0xff, 0xc0,  # stwu sp, -0x0040 (sp)
                0x7c, 0x08, 0x02, 0xa6,  # mflr r0
                0x90, 0x01, 0x00, 0x44,  # stw r0, 0x0044 (sp)
                0x39, 0x61, 0x00, 0x40,  # addi	r11, sp, 64
                0x4b, 0xf7, 0x20, 0xfd   # bl 0x80454384
            ]),
            patch=bytearray([
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x38, 0x60, 0x00, 0x00,  # li r3, 0
                0x4e, 0x80, 0x00, 0x20   # blr
            ])
        ),
        CodePatch(
            name="EC_GetIsSyncNeeded",
            address=0x804e35d4,
            signature=bytearray([
                0x94, 0x21, 0xff, 0xf0,  # stwu sp, -0x0010 (sp)
                0x7c, 0x08, 0x02, 0xa6,  # mflr r0
                0x3c, 0x60, 0x80, 0x82,  # lis r3, 0x8082
                0x90, 0x01, 0x00, 0x14,  # stw r0, 0x0014 (sp)
                0x80, 0x83, 0xb6, 0xa0,  # lwz	r4, -0x4960 (r3)
                0x2c, 0x04, 0x00, 0x00   # cmpwi r4, 0
            ]),
            patch=bytearray([
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x60, 0x00, 0x00, 0x00,  # nop
                0x38, 0x60, 0x00, 0x00,  # li r3, 0
                0x4e, 0x80, 0x00, 0x20   # blr
            ])
        )
    ]

    def patch(self, path):
        """Patches EC/Wii Shop related functions required to play online."""
        with open(path, "rb+") as f, \
             closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            for code_patch in self.PATCHES:
                m.seek(0)
                signature = bytes(code_patch.signature)
                patch = bytes(code_patch.patch)
                pos = m.find(signature)
                if pos == -1:
                    if m.find(patch) != -1:
                        print("  - {} already patched".format(code_patch.name))
                        continue
                    raise IndexError("Can't find {}".format(code_patch.name))
                m.seek(pos)
                m.write(patch)
            print("  + EC/Wii Shop patching process completed successfully!")


def prompt():
    message = "\nPress Enter to exit the program\n"
    try:
        raw_input(message)  # noqa: F821
    except Exception:
        input(message)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("dol", action="store", help="main.dol file")
    region_group = parser.add_mutually_exclusive_group(required=False)
    region_group.add_argument(
        "-J", "--jap", action="store_true",
        help="use the Japanese patcher [RMHJ08]")
    region_group.add_argument(
        "-E", "--usa", action="store_true",
        help="use the American patcher [RMHE08]")
    region_group.add_argument(
        "-P", "--pal",  action="store_true",
        help="use the European patcher [RMHP08]")
    parser.add_argument(
        "cert", nargs='?', action="store",
        help="replace root CA certificate"
    )
    parser.add_argument(
        "--disable-ec-patch", dest="patch_ec", action="store_false",
        help="disable isECTicket function patch"
    )
    parser.add_argument(
        "--dump-cert", dest="dump", action="store", metavar="OUT.DER",
        help="extract CA certificate"
    )
    parser.add_argument(
        "-n", "--not-interactive", dest="interactive", action="store_false",
        help="disable the prompt after the program ended"
    )
    parser.add_argument(
        "-f", "--force", dest="force", action="store_true",
        help="force insecure operations"
    )

    args = parser.parse_args()
    if not args.cert:
        path = "ca.der"
        if not os.path.exists(path):
            script_path = os.path.realpath(__file__)
            path = os.path.join(os.path.dirname(script_path), "ca.der")
        args.cert = path

    patcher_class = \
        JAPCertPatcher if args.jap else \
        USACertPatcher if args.usa else \
        PALCertPatcher if args.pal else \
        CertPatcher
    patcher = patcher_class(args.dol, args.force)

    if args.dump:
        print("+ Dumping root CA certificate")
        patcher.dump_cert(args.dump)
    else:
        print("+ Patching root CA certificate")
        patcher.patch_cert(args.cert)

        if patcher.CERT_OFF == JAPCertPatcher.CERT_OFF and args.patch_ec:
            print("+ Patching EC/Wii Shop functions")
            ec_patcher = ECPatcher()
            ec_patcher.patch(args.dol)

    if args.interactive:
        prompt()


if __name__ == '__main__':
    from traceback import print_exc

    try:
        main()
    except (Exception, SystemExit) as e:
        if isinstance(e, ValueError):
            print("ERROR: {}!".format(e))
        elif not isinstance(e, SystemExit):
            print_exc()
        prompt()
