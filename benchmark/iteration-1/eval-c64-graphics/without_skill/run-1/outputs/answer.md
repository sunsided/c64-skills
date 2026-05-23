Standard hi-res bitmap = 320×200, 1bpp, no multicolor. Three VIC-II registers do it.

## Registers

| Reg | Addr | Job | Value |
|-----|------|-----|-------|
| `$D011` | 53265 | ctrl reg 1 — set **BMM** (bit 5) for bitmap | `PEEK OR 32` → `$3B` |
| `$D018` | 53272 | mem pointers — screen base (bits 4-7), bitmap base (bit 3) | `24` (`$18`) |
| `$D016` | 53270 | ctrl reg 2 — clear **MCM** (bit 4) = hi-res not multicolor | `PEEK AND 239` |

**`$D018 = 24` math:**
- Screen $0400: VM bits = $0400/$0400 = 1 → upper nibble `$10`
- Bitmap $2000: CB13 bit 3 = $2000/$2000 = 1 → `$08`
- `$10 | $08 = $18 = 24`

VIC bank: both addrs in bank 0 ($0000–$3FFF), default. No `$DD00` change needed.

## Runnable BASIC

```basic
10 REM HI-RES BITMAP: BITMAP $2000, SCREEN $0400
20 POKE 53272,24            : REM SCREEN=$0400, BITMAP=$2000
30 POKE 53265,PEEK(53265) OR 32  : REM TURN ON BITMAP MODE (BMM)
40 POKE 53270,PEEK(53270) AND 239: REM CLEAR MCM = STANDARD HI-RES
50 FOR I=8192 TO 16191:POKE I,0:NEXT : REM CLEAR BITMAP $2000-$3F3F
60 FOR I=1024 TO 2023:POKE I,16:NEXT : REM COLOR: WHITE FG, BLACK BG
70 REM PLOT TEST: DIAGONAL LINE
80 FOR X=0 TO 199
90 BA=8192+(INT(X/8)*320)+(X AND 7)+(INT(X/8)*0)
100 BY=8192+320*INT(X/8)+(X AND 7)+8*X
110 POKE BY,PEEK(BY) OR (2^(7-(X AND 7)))
120 NEXT
```

**Color source:** standard bitmap mode pulls color from screen RAM ($0400), per 8×8 cell — upper nibble = foreground, lower = background. Line 60 writes `16` (`$10`) = white fg / black bg everywhere. `$D800` color RAM unused in this mode.

**Bitmap layout:** 8000 bytes $2000–$3F3F. Byte address for pixel (x,y):
```
addr = $2000 + (y AND 248)*40 + (x AND 504) + (y AND 7)
bit  = 7 - (x AND 7)
```

**Watch out:** bitmap fill in BASIC slow (~10s). Line 50 zeroes it. Long BASIC programs risk collide with $2000+ — short demo fine.

Return to text: `POKE 53265,PEEK(53265) AND 223` clears BMM.