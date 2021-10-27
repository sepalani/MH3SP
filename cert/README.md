# Certificate Patcher

In this directory you'll find a set of tools allowing to manipulate Monster
Hunter Tri main.dol certificate. The size of the new certificate **MUST NOT**
exceed the original size!

_If the CA certificate isn't specified, the default one will be used._

## Auto-detection (with default certificate)
```bash
python MHTriCertPatcher.py main.dol
```

## Auto-detection (with specified certificate)
```bash
python MHTriCertPatcher.py main.dol ca.der
```

## JAP Certificate
```bash
python MHTriCertPatcher.py -J main.dol ca.der
```

## USA Certificate
```bash
python MHTriCertPatcher.py -E main.dol ca.der
```

## PAL Certificate
```
python MHTriCertPatcher.py -P main.dol ca.der
```
