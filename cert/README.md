# Certificate Patcher

In this directory you'll find a set of tools allowing to manipulate Monster
Hunter Tri main.dol certificate. The size of the new certificate **MUST NOT**
exceed the original size!

## JAP Certificate
```bash
python MHTriCertPatcher.py --patch-ec -J main.dol ca.der
```

## USA Certificate
```bash
python MHTriCertPatcher.py -E main.dol ca.der
```

## PAL Certificate
```
python MHTriCertPatcher.py -P main.dol ca.der
```
