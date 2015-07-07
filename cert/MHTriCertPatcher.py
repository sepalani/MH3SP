"""Monster Hunter 3 (~tri) Certificate Patcher

Patch the in-game certificate according to the region:
 - RMHJ08 [NTSC-J]: 	JAPCertPatcher class
 - RMHE08 [NTSC-U]: 	USACertPatcher class
 - RMHP08 [PAL]:	PALCertPatcher class

The CertPatcher class is the base class for these patchers.
 - CERT_OFF:		Certificate offset
 - CERT_LEN:		Certificate length

"""

from optparse import OptionParser


class CertPatcher(object):
    """Generic Certificate Patcher."""

    CERT_OFF = None
    CERT_LEN = None

    def __init__(self, dol):
        """Constructor.

        dol - path to the main.dol file

        """
        self.dol = dol

    def patch_cert(self, crt):
        """Patch the in-game certificate. Will overwrite original dol file!

        crt - path to the certificate file

        """
        data = b''

        if self.CERT_OFF is None or self.CERT_LEN is None:
            raise ValueError("Unsupported region!")
        with open(crt, 'rb') as f:
            data = f.read(self.CERT_LEN)
            pad = self.CERT_LEN - len(data)
            data += pad * b'\0'
        if len(data) != self.CERT_LEN:
            raise ValueError("Unable to read the certificate!")
        with open(self.dol, 'rb+') as f:
            f.seek(self.CERT_OFF)
            f.write(data)


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


regionPatcher = {
    'RMHJ08': JAPCertPatcher,
    'RMHE08': USACertPatcher,
    'RMHP08': PALCertPatcher
}


if __name__ == '__main__':
    parser = OptionParser("Usage: %prog (--jap|--usa|--pal) <dol> <der cert>")
    parser.add_option("-J", "--jap", action="store_true",
                     default=False, dest="is_jap",
                     help="use the Japanese patcher [RMHJ08]")
    parser.add_option("-E", "--usa", action="store_true",
                     default=False, dest="is_usa",
                     help="use the American patcher [RMHE08]")
    parser.add_option("-P", "--pal", action="store_true",
                     default=False, dest="is_pal",
                     help="use the European patcher [RMHP08]")
    opt, arg = parser.parse_args()

    if len(arg) < 2:
        parser.print_help()
    else:
        region = 'RMHJ08' if opt.is_jap else \
                 'RMHE08' if opt.is_usa else \
                 'RMHP08' if opt.is_pal else \
                 ""
        if not region in regionPatcher:
            parser.print_help()
        else:
            patcher = regionPatcher[region](arg[0])
            patcher.patch_cert(arg[1])
