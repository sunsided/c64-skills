# C64 Keys

**`C=` (Commodore) — three jobs:**
1. `C=`+`SHIFT` → toggle charset (upper/graphics ↔ upper/lower). Same as `POKE 53272,21` (set 1) / `POKE 53272,23` (set 2).
2. `C=`+number 1–8 → second 8 text colors. (`CTRL`+number = first 8.)
3. `C=`+graphic key → prints **left**-front glyph of key. (`SHIFT` = right-front glyph.)

**RUN/STOP** — breaks running BASIC program → `BREAK`. Held during LIST = slow listing. `SHIFT`+RUN/STOP = LOAD+RUN first program from tape.

**RESTORE** — alone does little. Wired to CPU **NMI** line. Only acts when RUN/STOP held too.

**RUN/STOP + RESTORE** — warm reset. Clears screen, restores default I/O + screen state. **BASIC program survives.** (Cold reset that wipes program: `SYS 64759`.)

**f1–f8** — four physical keys. f1/f3/f5/f7 unshifted, f2/f4/f6/f8 with `SHIFT`. **Not bound by default** — you read + act on them. Emit PETSCII 133–140.

```basic
10 GET K$: IF K$="" THEN 10
20 IF K$=CHR$(133) THEN PRINT "f1"
30 IF K$=CHR$(137) THEN PRINT "f2"
40 GOTO 10
```

CHR$ map: f1=133, f2=137, f3=134, f4=138, f5=135, f6=139, f7=136, f8=140.

Key-now check: `PEEK(197)` = matrix code of key held (64 = none).