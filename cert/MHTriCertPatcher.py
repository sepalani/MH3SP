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
