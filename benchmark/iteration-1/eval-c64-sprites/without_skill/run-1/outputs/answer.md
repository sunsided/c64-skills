```basic
10 POKE 53269,1      : REM ENABLE SPRITE 0 (VIC REG $D015)
20 POKE 2040,13      : REM SPRITE 0 DATA POINTER -> BLOCK 13 ($07F8), ADDR 13*64=832
30 POKE 53248,160    : REM SPRITE 0 X = 160 ($D000)
40 POKE 53249,100    : REM SPRITE 0 Y = 100 ($D001)
50 POKE 53287,2      : REM SPRITE 0 COLOR = RED ($D027)
```

Register notes:
- `53269` ($D015) — sprite enable. Bit 0 = sprite 0.
- `2040` ($07F8) — sprite 0 pointer. Value × 64 = data address. 13 → 832.
- `53248`/`53249` ($D000/$D001) — sprite 0 X/Y.
- `53287` ($D027) — sprite 0 color. 2 = red.

X=160 fine — no MSB needed ($D010 only for X>255).

Caveat: block 13 (832–894) must hold 63 bytes sprite data or sprite show garbage. Add data:

```basic
5 FOR I=832 TO 894:POKE I,255:NEXT : REM FILL = SOLID BLOCK
```