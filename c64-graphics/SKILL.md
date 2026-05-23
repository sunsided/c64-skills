---
name: c64-graphics
description: >-
  C64 screen graphics from the programmer's view: the five VIC-II display modes
  (standard/multicolor text, ECM, standard/multicolor bitmap), custom 8x8
  character sets, screen/color/character memory layout, video bank selection, and
  smooth scrolling. Use this skill WHEN you see "how do I define custom
  characters", "turn on multicolor mode", "POKE 53272 / 53265 / 53270 / 53281",
  "$D011 $D016 $D018 bitmap mode", "switch VIC-II video banks", "where is screen
  RAM / color RAM", "set the bitmap base", or "smooth scroll the screen". Pairs
  with c64-sprites, c64-vic-ii (raster timing, full chip spec), and
  c64-memory-map.
---

# C64 Graphics (VIC-II display modes)

Programming the C64 screen: text and bitmap modes, custom charsets, the
screen/color/char memory map, video banks, and smooth scrolling. **Hardware
sprites (MOBs) are the separate `c64-sprites` skill.** For cycle-exact raster
timing, bad lines, the invalid modes, and the full register spec, use
**`c64-vic-ii`**; for ROM/RAM/IO banking under the VIC see **`c64-memory-map`**.

The VIC-II (6567 NTSC / 6569 PAL) lives at **$D000–$D02E** (53248–53294). A
display is 40 columns x 25 rows of text, or 320 x 200 dots in bitmap mode.

## The five display modes and their control bits

Three bits across two registers select the mode. **ECM=$D011 bit6, BMM (bitmap)
=$D011 bit5, MCM (multicolor)=$D016 bit4.**

| Mode | ECM | BMM | MCM | Resolution / cell | Colors per cell |
|------|-----|-----|-----|-------------------|-----------------|
| Standard text       | 0 | 0 | 0 | 40x25 chars, 8x8 | 1 (per-cell from color RAM) + shared background |
| Multicolor text     | 0 | 0 | 1 | 8x8, dots 2 wide | 3 shared ($D021/$D022/$D023) + 1 per-cell |
| Extended bg (ECM)   | 1 | 0 | 0 | 40x25, 8x8       | 1 fg + 1 of 4 backgrounds ($D021–$D024) per char |
| Standard bitmap     | 0 | 1 | 0 | 320x200          | 2 per 8x8 cell, both from screen RAM nibbles |
| Multicolor bitmap   | 0 | 1 | 1 | 160x200          | 4 per 8x8 cell |

`$D011` = 53265, `$D016` = 53270. These are read-modify-write registers — always
preserve the other bits:

```
POKE 53265,PEEK(53265)OR 64    : REM ECM on  ($D011 bit6)
POKE 53265,PEEK(53265)OR 32    : REM bitmap on ($D011 bit5)
POKE 53270,PEEK(53270)OR 16    : REM multicolor on ($D016 bit4)
POKE 53270,PEEK(53270)AND 239  : REM multicolor off
```

Assembly equivalents (set bitmap mode, keep other bits):

```asm
    LDA $D011
    ORA #$20        ; set BMM (bit 5)
    STA $D011
```

ECM and MCM together (ECM+MCM, or ECM+BMM) select **invalid/illegal modes**
that blank to black — documented in `c64-vic-ii`.

## Memory map: screen RAM, color RAM, character memory

| What | Default address | Notes |
|------|-----------------|-------|
| Screen RAM (char codes) | $0400–$07E7 (1024–2023), 1000 bytes | one screen-code byte per cell |
| Color RAM | $D800–$DBE7 (55296–56295), 1000 nibbles | **4-bit only**, fixed location, never moves |
| Character ROM | $D000–$DFFF | 2 sets (uppercase/gfx + lowercase), under the I/O |
| Character generator base | default $1000 (ROM image) | set by $D018 |
| Border color | $D020 (53280) | |
| Background color #0 | $D021 (53281) | screen background |

Color RAM is **only the low 4 bits** at $D800 — you cannot store 8-bit values
there, and it is the same physical RAM regardless of video bank. Background
colors #1–#3 are $D022/$D023/$D024 (used by multicolor text and ECM).

### $D018 — screen + character memory pointer (53272)

```
$D018 bits 7-4 : VM13-VM10  screen RAM base   = (bits 7-4) * $0400  within bank
$D018 bits 3-1 : CB13-CB11  char memory base  = (bits 3-1) * $0800  within bank
                 (in bitmap mode, bit 3 alone selects the $2000 bitmap base)
```

```
POKE 53272,(PEEK(53272)AND240)OR A   : REM A picks SCREEN base, hi nibble
POKE 53272,(PEEK(53272)AND15) OR A   : REM A picks CHAR base, low nibble
```

Char-memory `A` values (add the bank base): 0=$0000, 2=$0800, **4=$1000 ROM
image (default)**, 6=$1800 ROM image, 8=$2000, 10=$2800, **12=$3000**, 14=$3800.
`POKE 53272,(PEEK(53272)AND240)+12` is the standard "put my charset at 12288"
move. `POKE 53272,21` restores the normal C64 setup.

## Custom (programmable) characters

A character is **8x8 = 8 bytes** (1 byte per row, MSB = leftmost pixel). A full
set is 256 chars x 8 = **2K (2048 bytes)**, and must start on a 2K boundary
(the $D018 low-nibble values above).

Steps in BASIC:
1. Lower the top of BASIC to protect the charset (e.g. `POKE 52,48:POKE 56,48:CLR`
   to reserve from 12288 up).
2. Point VIC at it: `POKE 53272,(PEEK(53272)AND240)+12` (charset at 12288).
3. Copy any ROM chars you want to keep (the char ROM is under I/O — see Gotchas),
   then POKE your 8-byte patterns: char N's rows live at `base + N*8 .. +7`.

Compute a row byte from 8 pixels: `b = b1*128 + b2*64 + ... + b8*1`.

## Video bank selection (CIA2 $DD00)

The VIC sees only **16K at a time**. Bits 0–1 of CIA #2 port A ($DD00, 56576)
select which 16K bank — but the bits are **inverted** (value 3 = bank 0):

| $DD00 bits 1,0 | Bank | VIC range |
|----------------|------|-----------|
| 11 (POKE val 3) | 0 | $0000–$3FFF (default) |
| 10 (val 2) | 1 | $4000–$7FFF |
| 01 (val 1) | 2 | $8000–$BFFF |
| 00 (val 0) | 3 | $C000–$FFFF |

```
POKE 56578,PEEK(56578)OR 3              : REM make $DD00 bits 0,1 outputs
POKE 56576,(PEEK(56576)AND 252)OR A     : REM A = value from table above
```

The character ROM image is only visible to the VIC in **banks 0 and 2** (at
$1000 and $9000 respectively). In banks 1 and 3 you must supply your own charset
(or copy the ROM into bank RAM). All VIC base addresses ($D018, sprite pointers)
are relative to the selected bank's start.

## Bitmap mode specifics

Standard hi-res bitmap: 8000 bytes (320x200 / 8). Color comes from screen RAM
(NOT color RAM): upper nibble = "1" pixel color, lower nibble = "0" pixel color,
per 8x8 cell.

Multicolor bitmap (160x200, 2-bit pixels) color sources per cell:

```
00  Background color #0 ($D021)
01  upper 4 bits of screen memory
10  lower 4 bits of screen memory
11  the color-RAM nibble ($D800+)
```

Set bitmap base with $D018 bit 3 (e.g. `POKE 53272,PEEK(53272)OR 8` puts the
bitmap at offset $2000 in the bank). You must clear the 8K bitmap yourself
before drawing.

## Smooth scrolling

The fine-scroll registers are the **low 3 bits** of $D011 (vertical) and $D016
(horizontal); they shift the whole screen 0–7 pixels. To scroll new data on you
shrink the visible area so the covered edge has room:

- **38-column mode**: $D016 bit 3 = 0 (`POKE 53270,PEEK(53270)AND247`) for
  horizontal scroll — still 40 cols in RAM, only 38 shown.
- **24-row mode**: $D011 bit 3 = 0 (`POKE 53265,PEEK(53265)AND247`) for vertical.

```
POKE 53270,(PEEK(53270)AND 248)+X   : REM X = 0..7 horizontal fine scroll
POKE 53265,(PEEK(53265)AND 248)+Y   : REM Y = 0..7 vertical fine scroll
```

Loop the fine value 0→7, then do a full character-cell shift of screen RAM (in
machine language for speed) and reset the fine register. Exact raster-stable
scrolling lives in **c64-vic-ii**.

## Quick answers

- **Default screen RAM?** $0400 (1024). **Color RAM?** $D800 (55296), 4-bit.
- **Change border / background?** `POKE 53280,c` / `POKE 53281,c`, c = 0–15.
- **Where's the charset normally?** Char ROM imaged at $1000 in bank 0; the
  default $D018 is $15 (21), and its char-base field selects that $1000 image
  (bit 0 is unused).
- **Why did my chars vanish after switching banks?** The ROM charset image only
  exists in banks 0 and 2; supply your own in banks 1/3.

## Gotchas

- **Color RAM is 4-bit nibbles** at $D800 and is fixed — it does not move with
  the screen or the bank. Don't expect to read back a full byte.
- **The character ROM is "under" the I/O at $D000–$DFFF** — the source notes it
  "begins at location 53248 ($D000) when the I/O is switched off." To copy it
  from the CPU you must bank the I/O block out via the $0001 processor port (and
  disable interrupts while it's out); see **c64-memory-map** for the exact
  banking POKEs. The VIC always sees the ROM image at $1000/$9000 in banks 0/2
  regardless of CPU banking.
- **$DD00 bank bits are inverted** (3 = bank 0). And you must set them as outputs
  in $DD02 first.
- Always read-modify-write $D011 and $D016 — they pack mode bits, the fine-scroll
  bits, the 24/25-row and 38/40-col bits, and raster bit 8 together.
- Sprite pointers sit at the **end of screen RAM** ($07F8 for the default screen);
  moving the screen moves them too — see **c64-sprites**.

## How to read the references

- **`references/graphics-programming.md`** — the Programmer's Reference Guide
  Chapter 3 graphics half, verbatim: every mode, full char-memory and bank
  tables, the worked custom-character and bitmap BASIC programs, and the smooth-
  scroll walkthrough. Read this for the authoritative POKE values and listings.
- **`references/color-graphics-tutorial.md`** — the User's Guide Chapter 5
  gentle tutorial (PRINTing colors, CHR$ color codes, POKEing the screen,
  bouncing-ball example). Read this when you want the beginner-level framing.
- **`references/screen-color-memory-map.md`** — App D screen and color memory
  maps with the address-of-each-row diagrams and the 16 color codes. Read when
  you need the exact address of a screen/color cell.
- **`references/vic-register-map.md`** — App G VIC register map ($D000–$D02E)
  as a convenience copy. The deep, cycle-exact reference is **c64-vic-ii**;
  start there for anything timing-related.
