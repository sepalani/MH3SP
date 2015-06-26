# Certificate Patcher

In this directory you'll find a set of tools allowing to manipulate Monster Hunter Tri main.dol certificate. The size of the new certificate **MUST NOT** exceed the original size!

This program takes as parameter the following files: the **main.dol** file, then the certificate in **DER format**. The region has to be specified as well via one of these flags: ```--jap```, ```--usa```, ```--pal``` or equivalents.



JAP Certificate
---------------
 * ```python MHTriCertPatcher.py -J main.dol cert.der```



USA Certificate
---------------
 * ```python MHTriCertPatcher.py -E main.dol cert.der```



PAL Certificate
---------------
 * ```python MHTriCertPatcher.py -P main.dol cert.der```
