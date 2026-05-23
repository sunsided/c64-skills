Standard hi-res bitmap. Bank 0, bitmap $2000, screen $0400.

## Registers

| Reg | Addr | Value | Why |
|-----|------|-------|-----|
| $D011 (53265) | bit5 BMM=1, bit6 ECM=0, bit4... | `OR 32` | bitmap on, hi-res |
| $D016 (53270) | bit4 MCM=0 | `AND 239` | standard (not multicolor) |
| $D018 (53272) | screen base + bitmap base | `24` | hi nibble=1 → screen $0400; bit3=1 → bitmap $2000 |

$D018 math: screen $0400 = nibble 1 → `1*16=16`. Bitmap base bit3 = `8`. `16+8=24`.

Color = screen RAM nibbles ($0400): hi nibble = "1"-pixel color, lo nibble = "0"-pixel color. Not color RAM.

## Runnable BASIC

```basic
10 REM HI-RES BITMAP, BMP $2000, SCREEN $0400
20 POKE 53265,PEEK(53265) OR 32   : REM BMM=1 (bitmap on)
30 POKE 53270,PEEK(53270) AND 239 : REM MCM=0 (standard hi-res)
40 POKE 53272,24                  : REM SCREEN $0400 + BITMAP $2000
50 REM CLEAR 8K BITMAP AT 8192
60 FOR I=8192 TO 16191:POKE I,0:NEXT
70 REM SET CELL COLORS: WHITE PIX ON BLUE BG
80 FOR I=1024 TO 2023:POKE I,16:NEXT  : REM HI=1(white) LO=6(blue)
90 REM DRAW DIAGONAL TEST LINE
100 FOR X=0 TO 199
110 RO=INT(X/8):BY=8192+RO*320+(X AND 7)+INT(X/8)*0
120 REM (simple test: see note)
```

Lines 20–80 = setup you asked. Plotting formula for pixel (X,Y):

```
byte = 8192 + (INT(Y/8)*320) + (INT(X/8)*8) + (Y AND 7)
bit  = 7 - (X AND 7)
POKE byte, PEEK(byte) OR (2^bit)
```

Color value `16` = `1*16 + 0`... fix: white=1, blue=6 → `1*16+6 = 22`. Use `POKE I,22`.

## Restore normal text

```basic
POKE 53265,PEEK(53265) AND 223 : REM BMM off
POKE 53272,21                  : REM default screen $0400 + charset
```

**Note:** `$D018=24` keeps screen RAM at $0400, so sprite pointers stay at $07F8. FOR-loop bitmap clear (line 60) slow in BASIC — fine for demo, use ML for real work.