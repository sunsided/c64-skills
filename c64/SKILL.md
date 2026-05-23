---
name: c64
description: >-
  Orientation and router for Commodore 64 programming and hardware — the
  architecture at a glance, the memory/IO map, and a "which skill answers this"
  index across the focused c64-* skills (BASIC, graphics, sprites, VIC-II, SID,
  6510 assembly, KERNAL, memory map, CIA, I/O, disk, tape, game ports, PETSCII,
  keyboard, hardware, disassembly). Use this skill WHEN a C64 question is broad,
  vague, or cross-cutting ("how does the C64 work", "where do I start", "what
  chip does sound"), when you need the high-level memory map or chip locations,
  or to route a specific question to the right c64-* skill. For depth, defer to
  the specific sibling skill.
---

# Commodore 64 — overview & router

The C64 (1982, ~17M sold) is a 6510-based 8-bit home computer: 64 KB RAM, a
VIC-II video chip, a SID sound chip, two CIA I/O chips, and BASIC + KERNAL in ROM.
This skill is the **map of the territory** and a router to the focused `c64-*`
skills. Use it to orient, then open the specific skill for depth.

## The machine in one screen

| Part | Chip | Job | Lives at | Skill |
|------|------|-----|----------|-------|
| CPU | 6510 (6502 + I/O port) | runs code; `$00/$01` bank ROM/RAM | — | **c64-assembly** |
| Video | VIC-II 6567(NTSC)/6569(PAL) | screen, sprites, raster, IRQ | `$D000-$D3FF` | **c64-vic-ii**, **c64-graphics**, **c64-sprites** |
| Sound | SID 6581 | 3-voice synth + filter | `$D400-$D7FF` | **c64-sid** |
| I/O #1 | CIA1 6526 | keyboard, joysticks, timer IRQ | `$DC00-$DCFF` | **c64-cia**, **c64-keyboard**, **c64-game-ports** |
| I/O #2 | CIA2 6526 | serial bus, user port, VIC bank, NMI | `$DD00-$DDFF` | **c64-cia**, **c64-io** |
| Banking | PLA 82S100 | decodes ROM/RAM/IO/charROM | — | **c64-memory-map**, **c64-hardware** |
| Firmware | BASIC + KERNAL ROM | language + OS routines | `$A000`,`$E000` | **c64-basic**, **c64-kernal** |

## Memory map at a glance

```
$0000-$00FF  zero page    ($00/$01 = 6510 bank-switch port)
$0100-$01FF  CPU stack
$0200-$03FF  OS work area + buffers (IRQ vector $0314, tape buffer $033C)
$0400-$07FF  default screen RAM (sprite pointers $07F8-$07FF)
$0800-$9FFF  BASIC program / free RAM   (BASIC starts $0801)
$A000-$BFFF  BASIC ROM      (or RAM, switchable)
$C000-$CFFF  free RAM (4K) — favourite spot for ML
$D000-$DFFF  I/O: VIC $D000 / SID $D400 / colorRAM $D800 / CIA1 $DC00 / CIA2 $DD00
             (or character ROM, or RAM — depends on $01)
$E000-$FFFF  KERNAL ROM     (or RAM); jump table $FF81-$FFF3
```
Full detail, the `$01` banking-bit table, and the PLA logic → **c64-memory-map**.

## Which skill answers this?

| You want to… | Skill |
|--------------|-------|
| write/understand BASIC; a keyword's syntax | **c64-basic** |
| print special chars, color/cursor codes, build a text UI | **c64-petscii** |
| know what a key does (C=, RUN/STOP, RESTORE), use the editor | **c64-keyboard** |
| draw chars/bitmaps, set screen colors, scroll, custom fonts | **c64-graphics** |
| make/move/collide sprites | **c64-sprites** |
| exact raster timing, bad lines, all video modes, demo effects | **c64-vic-ii** |
| produce sound/music, program the SID | **c64-sid** |
| write 6510 machine language; call ML from BASIC | **c64-assembly** |
| call OS routines (print, load, save, input) | **c64-kernal** |
| the full memory map / banking / where things live | **c64-memory-map** |
| timers, IRQ/NMI, the chip behind keyboard/joystick/serial | **c64-cia** |
| files & devices, serial bus, printer, modem, RS-232, user/cartridge port | **c64-io** |
| disk drive: load, save, directory, DOS commands | **c64-disk** |
| cassette / Datasette load, save, "directory" | **c64-tape** |
| read joysticks, paddles, light pen | **c64-game-ports** |
| repair, pinouts, voltages, board revisions, chips | **c64-hardware** |
| reverse-engineer a .prg / dump / listing | **c64-disassembly** |

## Quick answers to common questions

- **Which control port is "player 1"?** Hardware: port 1 reads at CIA1 `$DC01`,
  port 2 at `$DC00`. By software convention most single-joystick games use
  **control port 2**. Detail → **c64-game-ports**.
- **What does the C= (Commodore) key do?** With SHIFT it toggles the
  upper-case/graphics vs upper/lower-case character set; held with a number key it
  selects one of the second set of text colors; it can also slow listings. →
  **c64-keyboard**.
- **How do I see a disk directory?** `LOAD"$",8` then `LIST`. → **c64-disk**.
- **How do I list a tape "directory"?** Tape is sequential — there is **no**
  random-access directory; you search forward for files. → **c64-tape**.
- **How do I clear the screen / where is screen RAM?** `PRINT CHR$(147)` (or
  POKE screen codes to `$0400-$07FF`, colors to `$D800`). → **c64-petscii**,
  **c64-graphics**.
- **Where do I put a machine-language routine?** `$C000` (free 4K) or the tape
  buffer `$033C`; call with `SYS`. → **c64-assembly**.
- **PAL vs NTSC?** PAL = 6569 (50 Hz, 63 cycles/line, 312 lines); NTSC = 6567
  (60 Hz, ~64–65 cycles/line, 262/263 lines). Matters for timing/music. →
  **c64-vic-ii**.

## How to use the set

Each `c64-*` skill is self-contained and carries the relevant sliced reference
docs under its own `references/`. Start here for orientation or a one-liner; jump
to the specific skill for register layouts, code, and exact behavior. For generic
6502/65C02/65816 CPU semantics beyond the C64's 6510, the optional companion repo
<https://github.com/sunsided/6502-skills> pairs well — not required.
