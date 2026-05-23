---
name: c64-memory-map
description: >-
  The complete Commodore 64 memory map and banking: zero page, stack, the BASIC
  program area and pointers, screen and color RAM, the $D000-$DFFF I/O area, the
  BASIC/KERNAL/character ROMs, the $0000/$0001 6510 port plus the 82S100 PLA that
  switches ROM/RAM/I/O/char-ROM, and VIC bank select via CIA2 $DD00. Use this
  skill WHEN asking where something lives or how to switch banks: "what's at
  $D000", "bank out the KERNAL", "C64 memory map", "where is screen/color RAM",
  "read the character ROM", "what do LORAM/HIRAM/CHAREN do", "which VIC bank am
  I in", "zero-page usage". Pairs with c64-assembly, c64-vic-ii, c64-sid,
  c64-cia, and c64-kernal.
---

# C64 Memory Map & Banking

The C64 has 64K RAM, 20K ROM (BASIC + KERNAL + character generator), and a 4K
I/O block — overlapping the same 16-bit address space. What appears at a given
address depends on the **6510 port at `$0001`**, the cartridge lines, and the
**82S100 PLA** that decodes them.

## The big picture

```
$0000-$00FF  Zero page        — 6510 port, BASIC/KERNAL system variables, ptrs
$0100-$01FF  Processor stack   — $0100 + S, grows downward
$0200-$03FF  System buffers    — input buffer, file tables, vectors, tape buffer
$0400-$07FF  Default screen RAM (1024 bytes, 1000 used)
$0800-$9FFF  BASIC program RAM (38K free under default banking)
$A000-$BFFF  BASIC ROM  (or RAM, or cartridge ROMH)
$C000-$CFFF  4K free RAM       — always RAM; the usual home for ML routines
$D000-$DFFF  I/O  (or character ROM, or RAM)
$E000-$FFFF  KERNAL ROM (or RAM, or cartridge ROMH)
```

I/O block breakdown ($D000-$DFFF, when I/O is banked in):

| Range | Chip | Skill |
|-------|------|-------|
| $D000-$D3FF | VIC-II (video) | **c64-vic-ii** |
| $D400-$D7FF | SID (sound) | **c64-sid** |
| $D800-$DBFF | Color RAM (1K nybbles) | (low 4 bits only) |
| $DC00-$DCFF | CIA1 (keyboard, joysticks, IRQ) | **c64-cia** |
| $DD00-$DDFF | CIA2 (serial bus, user port, VIC bank, NMI) | **c64-cia** |
| $DE00-$DFFF | Reserved I/O expansion (cartridge) | |

## The 6510 port at $0000/$0001

`$0000` is the data direction register (default `$2F` = %101111), `$0001` is the
port. Bits 0-2 do the banking:

| Bit | Name   | 1 (default) | 0 |
|-----|--------|-------------|---|
| 0 | LORAM  | BASIC ROM at $A000-$BFFF | RAM there |
| 1 | HIRAM  | KERNAL ROM at $E000-$FFFF | RAM there |
| 2 | CHAREN | I/O visible at $D000-$DFFF | character ROM there |
| 3 | — | cassette write line | |
| 4 | — | cassette switch sense (input) | |
| 5 | — | cassette motor control (0 = on) | |

Default `$0001` = `$37` → BASIC + KERNAL + I/O all visible (38K free BASIC RAM).

```asm
        ; bank in all RAM ($0000-$FFFF) — kills ROM + I/O; do it with IRQs off
        SEI
        LDA #$30           ; LORAM=0 HIRAM=0 CHAREN=0... value $34/$30 per need
        STA $01
```

```basic
POKE 1, PEEK(1) AND 254 : REM clear LORAM -> swap BASIC ROM for RAM
```

**Note:** a write (POKE) to a ROM address always lands in the **RAM underneath**;
a read returns the ROM. So you can keep e.g. a hi-res bitmap under the BASIC ROM
and edit it without banking.

## Bank configurations

The PRG bank table is indexed by `/LORAM /HIRAM /GAME /EXROM` (cartridge lines
GAME/EXROM are high when no cartridge). The everyday configurations:

| $0001 bits 2-0 | $A000-$BFFF | $D000-$DFFF | $E000-$FFFF | Use |
|----------------|-------------|-------------|-------------|-----|
| 111 ($37) | BASIC ROM | I/O | KERNAL ROM | default; 38K BASIC |
| 110 ($36) | RAM | I/O | KERNAL ROM | RAM under BASIC, KERNAL+I/O up |
| 101 ($35) | RAM | I/O | RAM | 60K RAM + I/O; write your own I/O |
| 011 ($33) | BASIC ROM | char ROM | KERNAL ROM | char ROM visible, no I/O |
| 000 ($30) | RAM | RAM | RAM | all 64K RAM |

The full nine-column table (including the Ultimax cartridge configuration and the
ROMH/ROML cartridge maps) is in `references/memory-map.md`.

### Reading character ROM

The 4K character generator ROM only appears when **CHAREN = 0**, and it shares
$D000-$DFFF with I/O, so banking it in removes the I/O chips. Do it with
interrupts disabled (the IRQ handler needs the CIA), copy the chars, restore:

```asm
        SEI
        LDA $01
        AND #%11111011     ; CHAREN = 0 -> char ROM at $D000-$DFFF
        STA $01
        ; ... copy from $D000 (uppercase set) / $D800 (lowercase) ...
        LDA $01
        ORA #%00000100     ; CHAREN = 1 -> I/O back
        STA $01
        CLI
```

(See **c64-vic-ii** for using a custom character set once copied to RAM.)

## VIC bank selection (CIA2 $DD00)

The VIC-II only sees **16K at a time**. Which 16K is chosen by **CIA2 $DD00 bits
1-0**, and these bits are **inverted** (00 → bank 3, 11 → bank 0):

| $DD00 bits 1-0 | VIC bank | VIC sees |
|----------------|----------|----------|
| 11 (default) | 0 | $0000-$3FFF |
| 10 | 1 | $4000-$7FFF |
| 01 | 2 | $8000-$BFFF |
| 00 | 3 | $C000-$FFFF |

```basic
POKE 56578, PEEK(56578) OR 3 : REM make DD00 bits 0-1 outputs (DDRA)
POKE 56576, (PEEK(56576) AND 252) OR (3 - BANK) : REM select bank
```

Set the DDR (`$DD02`) bits 0-1 to outputs first. In banks 0 and 2 the VIC also
sees the character ROM (at $1000-$1FFF / $9000-$9FFF) regardless of CHAREN, which
is why the default character set works in bank 0.

## Important zero-page / system locations

| Addr | Label | Meaning |
|------|-------|---------|
| $0000/$0001 | D6510/R6510 | 6510 data-direction / I/O port (banking) |
| $002B-$002C | TXTTAB | start of BASIC program text |
| $002D-$002E | VARTAB | start of BASIC variables |
| $0037-$0038 | MEMSIZ | highest address used by BASIC |
| $00FB-$00FE | — | four free zero-page bytes for the user |
| $0061-      | FAC#1 | floating-point accumulator (USR arg/return) |
| $0100-$01FF | stack | processor stack |
| $0277-$0280 | KEYD | keyboard buffer (10 chars) |
| $0286 | COLOR | current character color |
| $0288 | HIBASE | top-of-screen-memory page (default $04) |
| $02A7-$02FF | — | unused, free for the user |
| $0314-$0315 | CINV | hardware IRQ vector |
| $0318-$0319 | NMINV | NMI vector |
| $033C-$03FB | TBUFFR | tape buffer (free if not using tape) |
| $0400-$07FF | VICSCN | default screen RAM |
| $D800-$DBFF | — | color RAM (low nybble per cell) |

Full location-by-location map (every BASIC/KERNAL system variable and vector) is
in `references/memory-map.md`.

## Gotchas

- $DD00 VIC-bank bits are **inverted** — 11 = bank 0, not bank 3.
- Banking out the KERNAL ($E000-$FFFF) removes the IRQ/NMI vectors at $FFFA-$FFFF
  and the jump table — disable interrupts (or supply your own vectors in the
  underlying RAM) first.
- Color RAM at $D800 is only 4 bits wide; the high nybble reads as garbage.
- POKEing a ROM address writes the hidden RAM, not the ROM — easy to confuse when
  a later RAM-bank read returns "unexpected" values.
- CHAREN affects $D000-$DFFF only in configurations that *have* I/O; in all-RAM
  maps that range is just RAM.

## How to read the references

- **`references/memory-map.md`** — "Memory Management on the Commodore 64" (the
  $0001 port, the fundamental map, the full nine-configuration bank table with
  legend and notes) plus the complete location-by-location "Commodore 64 Memory
  Map" (every labeled zero-page/system variable and vector with hex + decimal).
  Read for the exact bank table or any specific address.
- **`references/io-assignments.md`** — the bit-by-bit "Commodore 64 Input/Output
  Assignments": every register of the VIC, SID, color RAM, CIA1, and CIA2 in the
  $D000-$DFFF block. Read when you need the meaning of a specific I/O register
  bit (e.g. $DD00 VIC bank bits, $D011 control register).
- **`references/screen-color-memory-map.md`** — Appendix D: the screen-memory and
  color-memory address grids and the character color codes. Read when mapping a
  row/column to a screen or color-RAM address.
- **`references/pla-banking-logic.md`** — the 82S100 PLA datasheet, JEDEC fuse
  map, and the Abel logic equations (ROMH/ROML/I_O/CHAROM/KERNAL/BASIC/CASRAM as
  functions of LORAM/HIRAM/CHAREN/GAME/EXROM/AEC/address lines). Read for the
  authoritative gate-level banking logic.

For switching banks from machine language see **c64-assembly**; for the chips
living in $D000-$DFFF see **c64-vic-ii** ($D000), **c64-sid** ($D400), and
**c64-cia** ($DC00/$DD00); for the ROM routines in $E000-$FFFF see **c64-kernal**.
