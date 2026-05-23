C64 1541 disk commands. Device 8 (default drive).

**1. List directory**
```basic
LOAD"$",8
LIST
```
Note: clobbers BASIC program in memory. `$` = directory pseudo-file.

**2. Load program GAME**
```basic
LOAD"GAME",8
```
For machine-code (load to its own address, not BASIC start):
```basic
LOAD"GAME",8,1
```
Secondary address `1` = use file's stored load address.

**3. Format new disk**
```basic
OPEN 15,8,15,"N0:DISKNAME,ID":CLOSE 15
```
`N0:` = NEW on drive 0. `DISKNAME` = label (≤16 chars). `ID` = 2-char disk ID. Full format. Disk already has ID → quick wipe with `"N0:DISKNAME"` (no ID, dir-only clear).

**4. Read error channel**
```basic
OPEN 15,8,15
INPUT#15,EN,EM$,ET,ES
PRINT EN,EM$,ET,ES
CLOSE 15
```
Channel 15 = command/error channel. Vars: `EN`=error number, `EM$`=message text, `ET`=track, `ES`=sector. `EN=0` → OK. Reading channel also clears blinking drive LED.

Secondary address 15 mandatory for command channel. Device 8 = first 1541; second drive = 9.