---
name: c64-sprites
description: >-
  Commodore 64 hardware sprites (MOBs, movable object blocks): the 24x21-pixel /
  63-byte sprite shape, sprite pointers, enabling sprites, X/Y positioning
  including the X MSB ($D010) for positions past 255, sprite color, multicolor
  sprites, 2x X/Y expansion, sprite-to-background and sprite-to-sprite priority,
  and collision detection. Use this skill WHEN you see questions like "how do I
  make a sprite on the C64", "POKE 53269 enable sprite", "move a sprite past x
  255 / $D010 MSB", "$D000 $D015 $D017 $D01C $D01D sprite registers", "set
  sprite pointer 2040", "multicolor sprite", "expand a sprite", "detect sprite
  collision $D01E $D01F", or "sprite priority". Pairs with c64-graphics
  (screen/charset/bank setup) and c64-vic-ii (exact raster timing and chip
  behavior).
---

# C64 Sprites (VIC-II MOBs)

Hardware sprites are small movable objects the VIC-II (6567/6569) draws and
positions for you — up to **8 at once**. Each sprite is **24 dots wide x 21 dots
high = 504 dots = 63 bytes** (21 rows of 3 bytes). The VIC handles drawing,
priority and collision; you set shape, color, position, and flags.

For screen RAM / charset / video-bank setup (which decides where pointers and
sprite data live) see **c64-graphics**. For cycle-exact raster timing, the
sprite DMA fetch cycles, and exact edge behavior see **c64-vic-ii**.

## The sprite register block ($D000–$D02E)

| Reg | Dec | Function |
|-----|-----|----------|
| $D000–$D00F | 53248–53263 | Sprite 0–7 **X,Y position pairs** (X even reg, Y odd reg) |
| $D010 | 53264 | **X MSB** register — bit n = sprite n's 9th X bit (X > 255) |
| $D015 | 53269 | **Enable** — bit n turns sprite n on |
| $D017 | 53271 | **Y expand** (2x vertical) — bit n |
| $D01B | 53275 | **Sprite-to-background priority** — bit n=1: sprite *behind* background |
| $D01C | 53276 | **Multicolor** select — bit n=1: sprite n is multicolor |
| $D01D | 53277 | **X expand** (2x horizontal) — bit n |
| $D01E | 53278 | **Sprite-sprite collision** latch — bit n set if sprite n hit another |
| $D01F | 53279 | **Sprite-background (data) collision** latch — bit n set on hit |
| $D025 | 53285 | Shared multicolor color #0 (bit pair 01) |
| $D026 | 53286 | Shared multicolor color #1 (bit pair 11) |
| $D027–$D02E | 53287–53294 | Per-sprite color, sprite 0–7 (bit pair 10 in MC) |
| $D019 | 53273 | Interrupt **status** latch (bit1=sprite-data, bit2=sprite-sprite collision) |
| $D01A | 53274 | Interrupt **enable** (same bit layout) — set to fire an IRQ |

Every per-sprite flag register uses **bit n for sprite n**. The idiom is
`OR (2^SN)` to set, `AND (255-2^SN)` to clear.

## Sprite pointers — where the shape lives

Sprite data must start on a **64-byte boundary** (63 bytes used + 1 wasted). The
**8 sprite pointers are the last 8 bytes of screen RAM**: default screen at
$0400 → pointers at **$07F8–$07FF (2040–2047)**, one per sprite. Move the screen
and the pointers move with it.

Pointer value P (0–255) selects the block: actual address =
**`(BANK * 16384) + (P * 64)`**. Example: pointer 2040 = 13 → data at
13*64 = 832 ($0340, the cassette buffer — a classic safe spot in bank 0).

```
POKE 2040,13          : REM sprite 0 shape comes from 13*64 = 832
```

## Step-by-step: a sprite in BASIC

```basic
10 V=53248                     : REM VIC base
20 POKE 2040,13                : REM sprite 0 pointer -> data at 832
30 FOR I=0 TO 62:READ A:POKE 832+I,A:NEXT : REM 63 shape bytes
40 POKE V+21,1                 : REM $D015 enable sprite 0 (bit 0)
50 POKE V+39,1                 : REM $D027 sprite 0 color = white
60 POKE V,100:POKE V+1,100     : REM X=100 ($D000), Y=100 ($D001)
```

To compute the 63 bytes: lay out a 24x21 grid, split each row into 3 bytes of 8
pixels (MSB = leftmost), value of a byte = sum of `2^(7-bit)` for lit pixels.

Assembly equivalent of enable + position:

```asm
    LDA #$01
    STA $D015        ; enable sprite 0
    LDA #100
    STA $D000        ; X low
    STA $D001        ; Y
    LDA #$00
    STA $D010        ; clear X MSB (X <= 255)
```

## Positioning, and the X MSB for X > 255

Y is a single 0–255 byte. X needs **9 bits** because the screen is wider than
255 dots, so the 9th bit of each sprite's X lives in **$D010 (53264)**, one bit
per sprite.

- Visible Y for an unexpanded sprite: first becomes visible at Y=30 (partially);
  fully on-screen from Y=50 to Y=229; first fully-off value is 250.
- Visible X spans roughly 24 ($18) to 343 ($157); X > 255 requires the MSB bit.

To place sprite n at X = XPOS (0–511):

```basic
POKE V+2*N, XPOS AND 255                       : REM low 8 bits -> $D000+2N
IF XPOS>255 THEN POKE V+16, PEEK(V+16) OR  (2^N)     : REM set MSB bit n
IF XPOS<256 THEN POKE V+16, PEEK(V+16) AND (255-2^N) : REM clear MSB bit n
```

i.e. low 8 bits to $D000+2N, and set/clear bit n of **$D010** (V+16) for the
9th bit.

## Color and multicolor sprites

- **Single-color**: one color per sprite in $D027+n; pixel on = that color, off =
  transparent (shows background).
- **Multicolor** (set bit n of $D01C): pixels are 2 bits wide, so 12x21 "fat"
  pixels, 4 colors per sprite, at the cost of horizontal resolution:

| Bit pair | Color source |
|----------|--------------|
| 00 | transparent (background shows) |
| 01 | shared multicolor #0 — $D025 (53285) |
| 10 | sprite's own color — $D027+n |
| 11 | shared multicolor #1 — $D026 (53286) |

The two `$D025/$D026` colors are shared by all multicolor sprites; only bit-pair
`10` is per-sprite.

## Expansion (2x)

- `POKE 53277,PEEK(53277)OR(2^SN)` — double width (X expand, $D01D).
- `POKE 53271,PEEK(53271)OR(2^SN)` — double height (Y expand, $D017).
- `AND (255-2^SN)` to undo. Expansion stretches existing pixels — it does not add
  detail.

## Priority

- **Sprite-to-sprite priority is fixed**: sprite 0 is in front of 1, 1 in front
  of 2, … 7 is the lowest. Lower number wins on overlap.
- **Sprite-to-background priority is per-sprite** in $D01B (53275): bit n=0 →
  sprite n in front of the background (default); bit n=1 → sprite behind it (a
  "window" effect, where a sprite passes behind on-screen graphics).

## Collision detection

Two read-and-clear latch registers, each one bit per sprite:

- **$D01E (53278)** sprite-to-sprite: a bit is set when sprites' non-transparent
  pixels overlap.
- **$D01F (53279)** sprite-to-background (data): set when a sprite hits non-zero
  background pixels.

Both latch and **stay set until you PEEK (read) them**, which clears them. To get
an interrupt instead of polling, set the matching bit in the **interrupt enable
register $D01A**: bit1 = sprite-data collision, bit2 = sprite-sprite. The
interrupt **status** is $D019 (write a 1 back to that bit to acknowledge).

```
C = PEEK(53278)        : REM read & clear sprite-sprite collisions
IF (C AND 1) THEN ...  : REM sprite 0 was involved
```

In multicolor sprites, bit-pair `01` ($D025) counts as **transparent for
collisions** — it does not trigger a collision.

## Quick answers

- **Sprite size / bytes?** 24x21 pixels, 63 bytes (one wasted in the 64-byte block).
- **Where are the pointers?** End of screen RAM: $07F8–$07FF for the default $0400 screen.
- **Enable register?** $D015 (53269), bit per sprite. **Per-sprite color?** $D027–$D02E.
- **Move past X=255?** Set bit n of $D010 (53264) and put X−256 in the low byte.
- **How many at once?** 8 (more via raster interrupts — see c64-vic-ii).

## Gotchas

- **Sprite data must start on a 64-byte boundary**, and the pointer holds the
  block number (address/64), not an address.
- **X position is 9-bit**: forgetting $D010 makes a sprite wrap to the left edge
  past X=255.
- **Collision latches clear on read** — read once per frame and stash the value;
  reading twice loses bits.
- The pointers live in the **selected video bank's** screen RAM. Sprite data and
  pointers must be in the 16K the VIC currently sees — set that up via
  **c64-graphics** ($DD00 bank bits, $D018 screen base).
- Multicolor `01` pixels are invisible to the collision logic.
- Sprite-to-sprite priority is **not** configurable; only sprite-to-background
  priority ($D01B) is.

## How to read the references

- **`references/sprites-programming.md`** — Programmer's Reference Guide Chapter
  3 sprite half, verbatim: full position-register table, enable/expand/priority/
  collision/multicolor sections, the X-MSB positioning diagrams, the interrupt
  registers, and the "Programming Sprites — Another Look" worked BASIC programs.
  Read this for the authoritative POKE values and complete listings.
- **`references/sprites-tutorial.md`** — User's Guide Chapter 6, the step-by-step
  beginner walkthrough (designing on a grid, computing the bytes, the balloon
  example, moving and expanding). Read this when you want the gentle framing.
- **`references/sprite-register-map.md`** — User's Guide App O sprite register
  map, the compact bit-by-bit table of $D000–$D02E for sprites plus the color
  codes. Read when you need the exact bit names. For cycle-exact timing and the
  full chip spec, go to **c64-vic-ii**.
