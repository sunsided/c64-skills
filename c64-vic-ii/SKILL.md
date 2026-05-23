---
name: c64-vic-ii
description: >-
  Cycle-level hardware reference for the C64 video chip (MOS 6566/6567/6569
  VIC-II): the register map ($D000-$D02E), 16-color palette, raster mechanics
  ($D012 + $D011 RST8), Bad Lines, the memory-access timing model, all eight
  ECM/BMM/MCM graphics modes (incl. the invalid ones), sprite
  DMA/priority/collision, borders, light pen, interrupts ($D019/$D01A), DRAM
  refresh, PAL vs NTSC timing (6569 vs 6567), and raster effects (FLD/FLI). Use
  this skill WHEN you need emulator-accurate timing or register/bit detail:
  "cycles per raster line on PAL", "what is a Bad Line", "set a raster
  interrupt", "the 9th raster bit", "open the border". For drawing see
  c64-graphics / c64-sprites; $DD00 VIC bank bits see c64-memory-map; CIA IRQ
  wiring see c64-cia.
---

# C64 VIC-II (MOS 6566 / 6567 / 6569) — hardware & timing reference

The VIC-II builds the C64 video frame line by line at a fixed line count and
fixed cycles-per-line per chip variant. It is the *bus master*: it generates the
system clock, RAS/CAS, and DRAM refresh, and it can stall the 6510 (via BA→RDY)
when it needs extra cycles. This file is the cycle-level, register-level truth;
the "how to draw a sprite / set up a bitmap" workflow lives in **c64-sprites**
and **c64-graphics**.

The VIC has 47 read/write registers at **$D000–$D02E** (decimal 53248+). Due to
incomplete address decoding they repeat every 64 bytes through $D000–$D3FF.
$D02F–$D03F read as $FF and ignore writes. **Unconnected ('-') bits read as 1.**

## Register map $D000–$D02E (quick table)

| Reg | Addr | Name | Meaning |
|----|------|------|---------|
| 0–15 | $D000–$D00F | M0X,M0Y … M7X,M7Y | Sprite 0–7 X/Y position (low 8 bits) |
| 16 | $D010 | M7X8…M0X8 | MSB (bit 8) of each sprite X |
| 17 | $D011 | RST8 ECM BMM DEN RSEL YSCROLL(2..0) | **Control reg 1** (see below) |
| 18 | $D012 | RASTER | Raster line, low 8 bits (bit 8 = $D011.7) |
| 19 | $D013 | LPX | Light pen X (latched) |
| 20 | $D014 | LPY | Light pen Y (latched) |
| 21 | $D015 | M7E…M0E | Sprite enable |
| 22 | $D016 | – – RES MCM CSEL XSCROLL(2..0) | **Control reg 2** (see below) |
| 23 | $D017 | M7YE…M0YE | Sprite Y expand (×2 vertical) |
| 24 | $D018 | VM13–VM10 CB13–CB11 – | Memory pointers (screen / char base) |
| 25 | $D019 | IRQ – – – ILP IMMC IMBC IRST | **Interrupt latch** (write 1 to clear) |
| 26 | $D01A | – – – – ELP EMMC EMBC ERST | **Interrupt enable** |
| 27 | $D01B | M7DP…M0DP | Sprite-vs-background priority (1=behind) |
| 28 | $D01C | M7MC…M0MC | Sprite multicolor enable |
| 29 | $D01D | M7XE…M0XE | Sprite X expand (×2 horizontal) |
| 30 | $D01E | M7M…M0M | Sprite-sprite collision (read-clears) |
| 31 | $D01F | M7D…M0D | Sprite-data collision (read-clears) |
| 32 | $D020 | EC | Border (exterior) color |
| 33–36 | $D021–$D024 | B0C–B3C | Background colors 0–3 |
| 37–38 | $D025–$D026 | MM0, MM1 | Sprite multicolor 0/1 (shared) |
| 39–46 | $D027–$D02E | M0C–M7C | Per-sprite color |

Color registers use only the low 4 bits. $D01E/$D01F can't be written and are
**cleared on read** — read once per frame to re-arm collisions.

**$D011 (control 1):** `RST8` (bit7) = raster bit 8; `ECM` (bit6); `BMM` (bit5);
`DEN` (bit4, display enable); `RSEL` (bit3, 25 vs 24 rows); `YSCROLL` (bits2–0).
**$D016 (control 2):** `RES` (bit5, no effect on 6567/6569 — stops the 6566 only);
`MCM` (bit4); `CSEL` (bit3, 40 vs 38 cols); `XSCROLL` (bits2–0).

## 16-color palette (4-bit index)

`0` black `1` white `2` red `3` cyan `4` pink/purple `5` green `6` blue
`7` yellow `8` orange `9` brown `10` light red `11` dark gray (gray 1)
`12` medium gray (gray 2) `13` light green `14` light blue `15` light gray (gray 3).
Multicolor *character* mode may only use color codes 0–7 per character.

## How a frame is built

The VIC draws a fixed grid: an unmovable **display window** in the middle, the
**display column** above/below it, and a **border** painted in EC ($D020). RSEL
and CSEL set the window edges (the graphics resolution is always 40×25 / 320×200;
RSEL/CSEL only move where the border starts/stops):

```
RSEL=1  25 rows / 200px   first line $33(51)  last $FA(250)
RSEL=0  24 rows / 192px   first line $37(55)  last $F6(246)
CSEL=1  40 cols / 320px   first X $18(24)     last $157(343)
CSEL=0  38 cols / 304px   first X $1F(31)     last $14E(334)
```

XSCROLL/YSCROLL ($D016/$D011 low 3 bits) shift the graphics 0–7 px right/down for
soft scrolling. To keep graphics aligned: 25-row/40-col uses Y=3,X=0; 24-row/38-col
uses Y=7,X=7.

**PAL vs NTSC** (exact, from the article):

| Chip | System | Lines/frame | Cycles/line | Visible lines | Visible px/line |
|------|--------|-------------|-------------|---------------|-----------------|
| 6569 | PAL-B  | 312 | **63** | 284 | 403 |
| 6567R8 | NTSC-M | 263 | **65** | 235 | 418 |
| 6567R56A | NTSC-M | 262 | **64** | 234 | 411 |

So a PAL frame is 312×63 cycles, NTSC 263×65 (or 262×64 on the old R56A). The
raster IRQ negative edge, not X=0, defines the start of a line.

## Bad Lines — the thing that breaks raster timing

To fetch the 40 character pointers (c-accesses) for a text row the VIC needs 40
extra cycles it doesn't have, so it pulls **BA low and stalls the 6510** for
~40–43 cycles on the first pixel-line of each text row. That row is a **Bad Line**.

> **Bad Line Condition:** at the negative edge of Φ0 starting a cycle,
> `RASTER >= $30 && RASTER <= $F7` **and** `(RASTER & 7) == YSCROLL` **and** the
> DEN bit was set at some point during raster line $30.

Consequences: (1) the CPU loses ~40 cycles, wrecking cycle-counted loops (disk
fastloaders, raster splits) — count cycles assuming the steal. (2) The VIC keys
the whole display off Bad Lines, so writing YSCROLL mid-line *moves* or
*suppresses* them — the basis of FLD/FLI. With YSCROLL=0 the first Bad Line is
line $30 once DEN is set; clearing DEN suppresses all Bad Lines. Sprite fetches
steal a further ~2 cycles per active sprite.

## Graphics modes — the ECM/BMM/MCM truth table

Bits: ECM ($D011.6), BMM ($D011.5), MCM ($D016.4). Three combinations are
"invalid" and force the pixel output to **black** (but still read memory):

| ECM | BMM | MCM | Mode |
|-----|-----|-----|------|
| 0 | 0 | 0 | Standard text (hi-res chars, per-char fg color, $D021 bg) |
| 0 | 0 | 1 | Multicolor text (col<8 hi-res; col≥8 → 2-bit MC pixels) |
| 0 | 1 | 0 | Standard bitmap (320×200, colors from video matrix nibbles) |
| 0 | 1 | 1 | Multicolor bitmap (160×200, +$D021 + matrix nibbles) |
| 1 | 0 | 0 | Extended Color Mode text (top 2 char bits pick bg of B0C–B3C) |
| 1 | 0 | 1 | **Invalid** text (output black) |
| 1 | 1 | 0 | **Invalid** bitmap 1 (output black) |
| 1 | 1 | 1 | **Invalid** bitmap 2 (output black) |

ECM steals the upper 2 character-code bits (only 64 chars) and forces video
address lines 9/10 low. Any combo with ECM=1 plus BMM=1 or MCM=1 is the black
"invalid" zone. Full per-mode address layouts are in the modes reference.

## Sprites (hardware summary — usage lives in c64-sprites)

8 sprites, 24×21 px (12×21 in multicolor), positioned by M*X/M*Y + the X bit-8 in
$D010. The VIC DMA-fetches sprite data (p- + s-accesses), stalling the CPU ~2
cycles per active sprite per line. **Priority:** $D01B bit set ⇒ sprite behind
foreground. **Collision:** $D01E = sprite-sprite, $D01F = sprite-background; both
latch the *first* collision and clear on read. $D017/$D01D double Y/X size.

## Interrupts ($D019 latch / $D01A enable)

Four sources, each with a latch bit ($D019) and an enable bit ($D01A):

| Bit | Latch/En | Source |
|-----|----------|--------|
| 0 | IRST/ERST | Raster line reached (compare set via $D012 + $D011.7) |
| 1 | IMBC/EMBC | Sprite-background (sprite↔graphics) collision |
| 2 | IMMC/EMMC | Sprite-sprite collision |
| 3 | ILP/ELP   | Light pen negative edge |

$D019 bit7 (IRQ) = inverted state of the VIC IRQ output. The VIC **never clears
the latch itself** — your handler must write a 1 to the latched bit *before* CLI
/ RTI or the IRQ (level-sensitive on the 6510) fires immediately again. The
raster compare is tested in cycle 0 of each line (cycle 1 for line 0).

**Setting a raster IRQ** (assembly):
```asm
        lda #$7f
        sta $dc0d        ; turn off CIA IRQs (so only VIC IRQs reach us)
        lda #<line       ; raster line low 8 bits
        sta $d012
        lda $d011
        and #$7f         ; clear RST8 (bit8) — set it for lines >= 256
        sta $d011
        lda #$01         ; enable raster IRQ (ERST)
        sta $d01a
        asl $d019        ; ack any pending VIC IRQ
        ...              ; point $0314/$0315 (or $FFFE) at your handler, CLI
```
In BASIC the same compare is `POKE 53266,line : POKE 53265,PEEK(53265)AND127`.

## DRAM refresh & light pen

The VIC does **5 refresh reads per raster line** (r-accesses) from $3FFF down,
using an 8-bit REF counter reset to $FF on line 0 — refreshing all 256 DRAM rows.
The light pen latches the current beam X→LPX ($D013) and Y→LPY ($D014) on a
falling edge of the LP input (shared with the keyboard matrix, so software-pokable).

## Gotchas / common mistakes

- **Raster bit 9:** $D012 is only bits 0–7. Lines ≥ 256 (PAL reaches 311) need
  RST8 = $D011 bit7; forgetting it puts the split 256 lines off.
- **Unused bits read as 1:** read $D011, mask the wanted bit, write back — never
  write a literal that clears RST8 by accident.
- **Acknowledge the IRQ** in the handler (`LDA #$0F : STA $D019` / `ASL $D019`) or
  it re-fires forever.
- **Collision regs clear on read** — sample $D01E/$D01F once, then process.
- **Bad Lines steal CPU cycles** in the display area; never assume 63/65 free
  cycles on a text-display line.
- **Opening the border** (Hyperscreen): upper/lower = switch RSEL so the comparator
  "misses"; left/right = single-cycle-exact CSEL switch (cycle 56 keep off, cycle 17
  keep on). Procedure in the effects reference.
- **$D016 RES bit** does nothing on the 6567/6569 (only stops the 6566).

## How to read the references

The body above is the index; open a reference only for the deep detail:

- **`references/register-map.md`** — App G bit-grid for every register
  ($D000–$D02E) + color-code table. Read for official per-bit names vs addresses.
- **`references/vic-ii-chip-spec.md`** — MOS App N: character/bitmap address
  generation (VM/CB/VC/RC formulas), per-mode color tables, sprite addressing,
  pin/electrical data. Read for the exact address-formation math.
- **`references/vic-article-architecture.md`** — Bauer §2: 6510/VIC signals
  (Φ2, BA, AEC, RDY), CPU- and VIC-side memory maps, VIC banks, the BA take-over.
- **`references/vic-article-registers.md`** — Bauer §3.1–3.3: block diagram, the
  authoritative register table, register quirks, and palette. Read first.
- **`references/vic-article-display-and-modes.md`** — Bauer §3.4–3.7: display
  window dimensions, full Bad Line treatment, cycle-exact raster-line timing
  diagrams, VC/RC counters, and all 8 graphics modes (incl. the 3 invalid). Big one.
- **`references/vic-article-sprites-border-irq.md`** — Bauer §3.8–3.13: sprite
  DMA/display/priority/collision, border flip-flops, Display Enable, light pen,
  interrupt logic, DRAM refresh.
- **`references/vic-article-effects.md`** — Bauer §3.14 + §4: Hyperscreen, FLD,
  FLI, Linecrunch, doubled text lines, DMA delay, sprite stretching, $00/$01 + $DE00.

## Cross-links

- Drawing/character/bitmap *application* + color-RAM usage → **c64-graphics**.
- Sprite *setup, animation, pointers, multiplexing* → **c64-sprites**.
- $DD00 CIA-2 VIC bank bits and CPU $00/$01 banking → **c64-memory-map**.
- CIA timers/TOD and how CIA IRQs interact with VIC IRQs → **c64-cia**.
- 6510 opcode/flag/addressing semantics for IRQ handlers → **c64-assembly** (or the
  companion repo `https://github.com/sunsided/6502-skills` for deeper generic 6502
  coverage — a suggestion, not a dependency).
