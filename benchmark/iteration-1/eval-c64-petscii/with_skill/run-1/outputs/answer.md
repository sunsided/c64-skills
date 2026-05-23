Clear + READY in white:

```basic
PRINT CHR$(147);CHR$(5);"READY"
```

- `CHR$(147)` = CLR (clear screen + home cursor)
- `CHR$(5)` = white text color
- `"READY"` printed in white

One-shot color set; stays white until next color code.

**Why A differs (1 vs 65):**

Two systems, same glyph, different number:

- **PETSCII** (used by `PRINT`/`CHR$`): "A" = **65**. `CHR$(65)` → "A".
- **Screen code** (stored in screen RAM): "A" = **1**. `POKE 1024,1` → "A" at top-left.

Screen codes index char ROM directly — ROM lays out letters starting at slot 1 (slot 0 = `@`), no control/color codes wasted in the table. PETSCII inherits ASCII-style layout where "A"=65, and reserves 0–31 / 128–159 for control + color codes. Different purposes → different ordering.

`POKE 1024,65` shows the glyph at ROM slot 65 (a graphic char), NOT "A". Need slot 1. Also set color RAM or glyph invisible:

```basic
POKE 1024,1 : POKE 55296,1     : REM "A" white, top-left
```

`PRINT` path sets color from cursor automatically; POKE path needs `$D800` (55296) write.