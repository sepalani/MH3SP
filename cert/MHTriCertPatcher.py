#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
from argparse import ArgumentParser
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


class NetworkWiiMediatorIsECTicket(object):
    """NetworkWiiMediator::IsECTicket patcher."""

    ADDRESS = 0x803f7fcc

    SIGNATURE = bytearray([
        0x80, 0x6d, 0xbd, 0xb0,  # lwz r3, -0x4250 (r13)
        0x2c, 0x03, 0x00, 0x00,  # cmpwi r3, 0
        0x41, 0x82, 0x00, 0x08,  # beq- 0x803F7FDC
        0x4b, 0xff, 0xb5, 0xec,  # b 0x803F35C4
        0x38, 0x60, 0x00, 0x00,  # li r3, 0
        0x4e, 0x80, 0x00, 0x20   # blr
    ])

    PATCH = bytearray([
        0x60, 0x00, 0x00, 0x00,  # nop
        0x60, 0x00, 0x00, 0x00,  # nop
        0x60, 0x00, 0x00, 0x00,  # nop
        0x60, 0x00, 0x00, 0x00,  # nop
        0x38, 0x60, 0x00, 0x01,  # li r3, 1
        0x4e, 0x80, 0x00, 0x20   # blr
    ])

    def patch(self, path):
        """Patches NetworkWiiMediator::IsECTicket function.

        It removes the EC ticket check required to play online."""
        with open(path, "rb+") as f, \
             closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            signature = bytes(self.SIGNATURE)
            patch = bytes(self.PATCH)
            pos = m.find(signature)
            if pos == -1:
                if m.find(patch) != -1:
                    print("- NetworkWiiMediator::IsECTicket already patched!")
                    return
                raise IndexError("Can't find NetworkWiiMediator::IsECTicket")
            m.seek(pos)
            m.write(patch)


def prompt():
    message = "\nPress Enter to exit the program\n"
    try:
        raw_input(message)
    except Exception as e:
        input(message)


def main():
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
        "--patch-ec", dest="patch_ec", action="store_true",
        help="patch isECTicket function"
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

    patcher_class = \
        JAPCertPatcher if args.jap else \
        USACertPatcher if args.usa else \
        PALCertPatcher if args.pal else \
        CertPatcher
    patcher = patcher_class(args.dol, args.force)

    if args.cert:
        print("+ Patching root CA certificate")
        patcher.patch_cert(args.cert)

    if args.patch_ec:
        if args.jap:
            print("+ Patching isECTicket function")
            ec_patcher = NetworkWiiMediatorIsECTicket()
            ec_patcher.patch(args.dol)
        else:
            print("- Patching isECTicket is for the japanese version!")

    if args.dump:
        print("+ Dumping root CA certificate")
        patcher.dump_cert(args.dump)

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
