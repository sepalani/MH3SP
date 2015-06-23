"""Monster Hunter 3 (~tri) Certificate Patcher

Patch the in-game certificate according to the region:
 - RMHJ08 [NTSC-J]: 	JAPCertPatcher class
 - RMHE08 [NTSC-U]: 	USACertPatcher class
 - RMHP08 [PAL]:	PALCertPatcher class

The CertPatcher class is the base class for these patchers.
 - CERT_OFF:		Certificate offset
 - CERT_LEN:		Certificate length

"""


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


if __name__ == '__main__':
    pass
