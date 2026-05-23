# C64 Keys

**Commodore (C=) key**
Modifier, not standalone action. Combos:
- `C=` + letter → left-side graphic char (PETSCII)
- `C=` + SHIFT → toggle uppercase/graphics ↔ lowercase/uppercase charset. Disable toggle: `POKE 657,128`. Re-enable: `POKE 657,0`.
- `C=` + number key (1–8) → switch text color (1=black, 2=white... matches CTRL row alt).
- Held at boot/reset → no special ROM action (unlike C128).
Read in matrix: `C=` flag at bit in `PEEK(653)` — `653` = shift/ctrl/commodore flags. Values: 1=SHIFT, 2=C=, 4=CTRL (bits OR together).

**RUN/STOP**
- Alone in BASIC → breaks running program. Sets STOP flag. Vector via `$0328` (STOP routine `$F6ED`).
- Detected by `PEEK(653)`? No — STOP checked by reading keyboard col, location `145`/`$91` (`PEEK(145)=127` means STOP pressed). Kernal `STOP` routine `$FFE1`.
- SHIFT + RUN/STOP → auto LOAD+RUN from tape (types `LOAD\rRUN\r`).
- Disable STOP: `POKE 808,239` (alters STOP-check vector behavior, also breaks LIST). Cleaner: redirect `$0328`.

**RESTORE**
- Wired direct to CIA NMI line (not keyboard matrix). Triggers NMI when pressed.
- Alone → nothing visible (NMI handler returns).

**RUN/STOP + RESTORE together**
- Warm reset. NMI handler checks STOP flag; if set → jumps via `$FFFE`→`$FE43` warm-start.
- Clears screen, resets I/O & vectors, returns to READY. BASIC program in RAM NOT erased (`NEW` not run) — recover with care.
- Disable: redirect NMI vector `$0318`/`$0319` (792/793) to own RTI handler:
```basic
POKE 792,71:POKE 793,254
```
Wait — `$FE47` is default. To kill RUN/STOP+RESTORE, point NMI at an RTI:
```basic
POKE 792,193:POKE 793,254
```
(`$FEC1` = RTI in Kernal). Confirm target byte first.

**Function keys f1–f8**
- 4 physical keys; SHIFT gives even numbers: f1/f2, f3/f4, f5/f6, f7/f8.
- No built-in BASIC action — return PETSCII codes:

| Key | PETSCII |
|-----|---------|
| f1 | 133 |
| f3 | 134 |
| f5 | 135 |
| f7 | 136 |
| f2 | 137 |
| f4 | 138 |
| f6 | 139 |
| f8 | 140 |

- Read in BASIC:
```basic
10 GET A$:IF A$="" THEN 10
20 PRINT ASC(A$)
30 GOTO 10
```
- Detect f1 → action:
```basic
10 GET A$:IF A$=CHR$(133) THEN PRINT "F1 HIT"
20 GOTO 10
```

**Quick keyboard scan note**: raw matrix at CIA1 — `POKE 56320,col:PEEK(56321)`. STOP+RESTORE & RESTORE bypass matrix (RESTORE→NMI, hardwired).