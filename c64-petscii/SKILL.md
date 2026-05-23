---
name: c64-petscii
description: >-
  The three C64 character-code systems and putting text on screen: PETSCII (what
  PRINT and CHR$/ASC use), screen/display codes (a DIFFERENT mapping you POKE
  into screen RAM at $0400), and ASCII; plus cursor/color/reverse control codes
  and building text UIs with PETSCII box/line graphics. Use this skill WHEN asked
  "what CHR$ code clears the screen", "why does POKE 1024,1 show an A", "PETSCII
  vs screen codes", "how do I print in red", "draw a box/menu in PETSCII", "color
  code for cyan", or "POKE to screen RAM". Pairs with c64-keyboard, c64-graphics,
  and c64-memory-map.
---

# C64 Character Codes: PETSCII, Screen Codes, ASCII

Three different code systems share the 0–255 range. Mixing them up is the #1
text bug on the C64. Keep them straight:

| System | Used by | Range | "A" is | Notes |
|--------|---------|-------|--------|-------|
| **PETSCII** | `PRINT`, `CHR$()`, `ASC()`, the keyboard, files | 0–255 | 65 | Commodore's ASCII variant; includes control + color codes |
| **Screen (display) codes** | what's stored in screen RAM `$0400`+ (POKE/PEEK) | 0–255 | 1 | indexes the character ROM; **no** control codes |
| **ASCII** | true ASCII (printers, modems) | 0–127 | 65 | C64 PETSCII ≈ ASCII for digits/punct, differs for letters & ctrl |

**The core gotcha:** `PRINT CHR$(n)` uses PETSCII; `POKE 1024+offset,n` uses
screen codes. They are *not* the same number for the same glyph. `CHR$(65)`
prints "A"; `POKE 1024,65` shows "▌"(spade-ish) — to get "A" in the top-left you
`POKE 1024,1`. Letters: PETSCII "A"=65, screen-code "A"=1.

## Two ways to put a character on screen

```basic
REM PRINT path — uses PETSCII, honors control codes, scrolls
PRINT CHR$(147);"HELLO"        : REM 147 = clear screen, then text

REM POKE path — uses SCREEN codes, no scrolling, set color separately
POKE 1024,8 : POKE 55296,1     : REM screen code 8 = "H", color 1 = white
```
- Screen RAM default: **$0400–$07E7** (1024–2023), 40×25 = 1000 cells.
  Offset of row r, col c = `r*40 + c`.
- Color RAM: **$D800–$DBE7** (55296–56295), one nibble per cell (0–15). A POKEd
  character is invisible if its color matches the background — always set color
  RAM too. (PRINTing a char sets color from the current cursor color.)
- Reverse video of any screen code: add **128**. Codes 128–255 are the reversed
  images of 0–127.

## PETSCII control codes (CHR$ values) — cheat-sheet

These do something when PRINTed; embed them in string constants (in quote mode
they show as reversed glyphs — see c64-keyboard).

| CHR$ | Effect | CHR$ | Effect |
|------|--------|------|--------|
| 5 | white | 13 | RETURN (CR) |
| 8 / 9 | disable / enable SHIFT+C= charset switch | 14 | switch to lower case |
| 17 | cursor down | 145 | cursor up |
| 29 | cursor right | 157 | cursor left |
| 19 | HOME | 147 | CLR (clear + home) |
| 18 | RVS ON (reverse) | 146 | RVS OFF |
| 20 | DEL | 148 | INST |
| 34 | `"` quote | 141 | shifted RETURN |
| 142 | switch to upper case/graphics | 133–140 | f1,f3,f5,f7,f2,f4,f6,f8 |

### Color codes
PETSCII (for `PRINT CHR$(n)`): 144 black, 5 white, 28 red, 159 cyan, 156 purple,
30 green, 31 blue, 158 yellow, 129 orange, 149 brown, 150 lt red, 151 grey1,
152 grey2, 153 lt green, 154 lt blue, 155 grey3.

Color-RAM / VIC color **nibble** values (0–15, used by POKE and registers like
$D020/$D021): 0 black, 1 white, 2 red, 3 cyan, 4 purple, 5 green, 6 blue,
7 yellow, 8 orange, 9 brown, 10 lt red, 11 grey1, 12 grey2, 13 lt green,
14 lt blue, 15 grey3. (Same 16 colors, two numbering schemes.)

```basic
PRINT CHR$(28);"RED TEXT";CHR$(5);"WHITE AGAIN"
PRINT CHR$(18);"REVERSED";CHR$(146);"NORMAL"
```

## Two character sets (uppercase/graphics vs lowercase)
Only one is active at a time:
- **Set 1** = upper case + graphics (default at power-on). SHIFT gives the
  graphic on the right of the key.
- **Set 2** = lower case + upper case. SHIFT gives upper case.
- Switch by `SHIFT`+`C=` keys, or from BASIC: `POKE 53272,21` → upper/graphics,
  `POKE 53272,23` → lower/upper. ($D018 selects the char-ROM base.)
- The `C=` key with a graphic key gives the *left*-front graphic in either set.

## Building a TUI / box with PETSCII

PETSCII has dedicated line- and box-drawing glyphs (horizontal/vertical lines,
corners, T-pieces). You place them either by PRINTing the character (type it on
a real keyboard, or `CHR$` its PETSCII value) or by POKEing its **screen code**
into screen RAM. Look up the exact screen code for each graphic in the SET 1
column of `references/screen-display-codes.md` — the etext chart shows the POKE
value beside each glyph. Reverse-space (a SPACE screen code + 128) makes solid
color blocks for bars and backgrounds.

Pattern for a POKE-drawn frame (substitute the line/corner screen codes you read
off the chart for `HL` horizontal, `VL` vertical, and the four corner values):

```basic
10 PRINT CHR$(147)                         : REM clear
20 V=1024:C=55296                          : REM screen / color RAM bases
30 FOR I=1 TO 38:POKE V+I,HL:POKE C+I,1:NEXT          : REM top edge
40 FOR I=1 TO 38:POKE V+24*40+I,HL:POKE C+24*40+I,1:NEXT : REM bottom edge
50 FOR R=1 TO 23                                       : REM side edges
60 POKE V+R*40,VL    :POKE C+R*40,1
70 POKE V+R*40+39,VL :POKE C+R*40+39,1
80 NEXT
```
Always POKE color RAM alongside, or the glyph is invisible. For the PRINT
approach, position with HOME + cursor-down/right control codes inside a string,
then PRINT the box characters and reverse-video bars.

## Quick answers
- "Clear the screen": `PRINT CHR$(147)` (or POKE the screen RAM with 32s).
- "Print a quote mark": `PRINT CHR$(34)`.
- "Why does POKE 1024,1 give 'A'?": 1 is the *screen code* for A (POKE path),
  not PETSCII 65 (PRINT path).
- "Make text reverse": `PRINT CHR$(18)` … `CHR$(146)`, or add 128 to a screen code.
- "Read what's on screen at top-left": `PRINT PEEK(1024)` → a screen code.

## How to read the references
- **`references/screen-display-codes.md`** — PRG App B verbatim: the full
  SET 1 / SET 2 / POKE table mapping every glyph to its **screen code** 0–127
  (128–255 = reversed), plus the POKE-to-screen / color-RAM worked example.
  Read when POKEing characters into screen RAM or decoding a PEEK.
- **`references/ascii-and-chr-codes.md`** — PRG App C verbatim: the
  `PRINT CHR$(X)` / `ASC` table for all 0–255 **PETSCII** values, including every
  control and color code and the f-keys. Read when building strings for PRINT,
  decoding a GET, or needing a control/color CHR$ number.

(The User's Guide App E/F cover the same two tables; their content is folded into
these files rather than duplicated.)

## Cross-links
- The physical keys that emit these PETSCII codes, charset switching with
  `C=`+`SHIFT`, and quote/insert-mode behavior → **c64-keyboard**.
- Where screen RAM lives, how to relocate it, and VIC bank/charset selection at
  $D018 → **c64-graphics** and **c64-memory-map**.
