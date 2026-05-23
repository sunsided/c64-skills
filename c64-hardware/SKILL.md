---
name: c64-hardware
description: >-
  The physical Commodore 64 and its servicing: system specs, the chip complement
  (6510, VIC-II, SID, two CIAs, PLA, ROMs, DRAM) and each chip's role, the
  circuit theory (power, reset, clock, video/audio, ports), board revisions and
  how to ID them, connector pinouts, and troubleshooting. Use this skill WHEN a
  question is about C64 hardware, a board, or repair — "what chip is U17", "why
  won't my C64 boot", "blank screen on power-up", "power-brick voltage", "which
  board revision", "5-pin vs 8-pin video", "expansion port pinout", "PLA
  failure". Pairs with c64-memory-map, c64-vic-ii / c64-sid / c64-cia, and c64-io
  / c64-game-ports.
---

# C64 Hardware & Servicing

This is the repair / hardware-internals skill: the physical machine, its chips,
its circuit blocks, its connectors, and how it fails. For *programming* a chip's
registers go to the per-chip skill instead (**c64-vic-ii**, **c64-sid**,
**c64-cia**); for the ROM/RAM/IO banking the PLA implements go to
**c64-memory-map**; for using the ports from BASIC/assembly go to **c64-io**,
**c64-game-ports**, **c64-disk**, **c64-tape**.

> Schematics in this skill's sources are the 1985 Commodore Service Manual, whose
> figures were too complex to render as ASCII in the etext and are marked
> `[Figure: ...]`. For trace-level work (component placement, exact net routing)
> you need the original scanned schematics (#326106, #251138, #251469).

## System at a glance

| Spec | Value |
|------|-------|
| CPU | 6510 (6502 core + 6-bit I/O port at $0000/$0001), ~1.02 MHz NTSC / ~0.985 MHz PAL |
| RAM | 64 KB DRAM (8× 4164) + 0.5 KB color RAM (2114, only 4 bits used) |
| ROM | 20 KB: 8 KB BASIC ($A000–$BFFF), 8 KB KERNAL ($E000–$FFFF), 4 KB character ($D000–$DFFF) |
| Video | VIC-II: 40×25 text, 320×200 hires, 16 colors, 8 sprites |
| Sound | SID 6581: 3 voices, ADSR, filters, two paddle A/D inputs |
| Power in | external brick: regulated **+5V DC** and **9V AC** |

## Chip complement (what each chip is and where it sits)

Board positions are the `Un` designators silk-screened on the PCB. Detailed
pinouts are in `references/board-identification.md`; per-board parts lists there
map every `Un` to its exact part number.

| Pos | Part | Role |
|-----|------|------|
| U7  | 6510 (906107-01) | CPU; its on-chip port $00/$01 banks ROM/RAM and runs the cassette motor/sense/write |
| U19 | 6567 (NTSC) / 6569 (PAL) VIC-II (906109) | video; also generates DRAM RAS/CAS/refresh and the system PHI0 clock |
| U18 | 6581 SID (906112-01) | sound; also the A/D for paddles |
| U1, U2 | 6526 CIA (906108-01) | U1 = keyboard matrix + joysticks + cassette read (FLAG); U2 = serial bus + user port + RS-232 |
| U17 | 82S100 PLA (906114-01) | address-decode / bank-switch logic (the ROM/RAM/IO selector) |
| U3  | 2364 BASIC ROM (901226-01) | BASIC 2.0 interpreter |
| U4  | 2364 KERNAL ROM (901227-03) | OS / KERNAL |
| U5  | 2364 character ROM (901225-01) | character generator font |
| U6  | 2114 RAM (901453-01) | 0.5 KB color/nybble RAM |
| U9–U12, U21–U24 | 4164 DRAM | the 64 KB main memory (eight chips) |
| U8  | 7406 (or 7416) | inverting buffer — drives the serial bus (ATN/CLK/DATA) and reset |
| U13, U25 | 74LS257 | address multiplexers feeding the DRAM |
| U14 | 74LS258 | address mux |
| U15 | 74LS139 | I/O device decode ($D000-block chip selects) |
| U16, U28 | 4066 | analog switches (color RAM gating; paddle routing to SID) |
| U20 | 556 (LM556) | reset one-shot **and** RESTORE-key NMI generator |
| U26 | 74LS373 | data/address latch |
| U29–U32 | 74LS74 / 193 / 629 / MC4044 | the discrete clock-generator/PLL (original & A boards); the B board folds this into one clock IC (8701) |

## Power supply (read this before you suspect a chip)

The external brick supplies a **regulated +5V DC** and **9V AC**. Inside the C64:

- 5V DC (via CN7 pins 5/1, filtered, switched by S1) runs all the digital logic.
- 9V AC (CN7 pins 6/7) is rectified on-board into **+12V DC** (VR1 = 7812, feeds
  VIC, SID, audio amps), a separate **+5V CAN** (VR2 = 7805, split into Vvid for
  video and Vc for the clock), and **9V DC unregulated** (cassette motor, RF
  modulator on the B board). The raw 9V AC is also exposed on user-port pins
  10/11.

**The classic killer:** as the original brick ages, its internal 5V regulator
can drift high. Because that regulated 5V goes straight to the logic rails, an
overvolting brick can take out the RAM, PLA, and other chips at once. A
"60 Hz hum" white band scrolling down the screen points at the supply or VR2;
a black band on warm-up points at the supply / C90 / C88 / CR4 / VR2. Suspect
the power supply first on multi-chip or intermittent failures.

## Connectors / ports

Full pin tables (with the physical connector drawings) are in
`references/connector-pinouts.md`. Roster:

| Connector | What | Notes |
|-----------|------|-------|
| Power (CN7) | 7-pin DIN | +5V DC + 9V AC from the brick |
| Audio/Video (CN5) | 5-pin DIN (orig board) or 8-pin DIN (A/B boards) | 8-pin breaks out separate luma + chroma (S-Video) + composite + audio out + audio in; 5-pin only carries composite + audio |
| RF out | coax | channel-switched TV signal from the modulator |
| Serial bus (CN4) | 6-pin DIN | Commodore IEC: ATN/CLK/DATA/SRQ/RESET — disk & printer |
| Cassette (CN3) | 6-pin edge | MOTOR/READ/WRITE/SENSE + 5V + GND |
| Control Port 1 / 2 | 9-pin D | joystick (4 dir + button) + paddle pots; **port 1 = player 2 joystick on CIA1 PB, port 2 = player 1 joystick on CIA1 PA** per the service manual wiring |
| User port (CN2) | 24-pin (12+12) edge | CIA2 port B (PB0–7), serial SP/CNT, /FLAG2, /PC2, 9V AC, RESET |
| Expansion / cartridge (CN6) | 44-pin edge | full CPU bus: A0–A15, D0–D7, R/W, PHI2, dot clock, /IRQ, /NMI, /DMA, BA, /ROML, /ROMH, I/O1, I/O2, /GAME, /EXROM, /RESET |

Quick answers:
- *Which video pins are S-Video?* On the 8-pin DIN, pin 1 = LUMINANCE, pin 6 =
  CHROMINANCE (pin 2 GND). The 5-pin board does not break chroma out.
- *Does the user port have power?* Yes — +5V (pin 2, max 100 mA) and raw 9V AC
  (pins 10/11).
- *What resets the machine from the bus?* /RESET is on serial pin 6, user-port
  pin 3, and expansion pin C — pulling it low resets the whole machine.

## Reset, RESTORE, NMI (hardware level)

- **Power-on reset:** U20 (a 556) is a one-shot; pulse width ≈ 1.1 × R34 × C24 ≈
  0.5 s. Its active-high output is inverted (U8) to the active-low /RES that
  hits the 6510 (pin 40), which then vectors through **$FFFC/$FFFD** into the
  KERNAL. If the machine won't reset and RESTORE is dead, suspect U20.
- **RESTORE key:** wired straight to hardware, *not* through the keyboard
  matrix. Pressing it triggers U20 → U8 pulls **/NMI** (6510 pin 4) low; the CPU
  vectors through **$FFFA/$FFFB**. RUN/STOP+RESTORE additionally re-inits I/O and
  BASIC pointers (the KERNAL NMI handler checks STOP).
- **NMI vector $FFFA/$FFFB, IRQ vector $FFFE/$FFFF, RESET vector $FFFC/$FFFD.**

## Clock / dot clock

Original & A boards: crystal **Y1 = 14.31818 MHz** (NTSC color-clock fundamental)
feeds a discrete VCO/PLL (U29–U32) that produces the 8.18 MHz **dot clock**; the
VIC-II divides the dot clock by 8 to make **PHI0**, the ~1 MHz system clock, and
locks the loop. The **C64B** board replaces all that with a single clock IC
(crystal becomes 16 MHz, the 8701 outputs dot + color clocks). PAL machines use
the 6569 VIC-II and a 17.734472 MHz crystal; the divide-by-8 gives the ~0.985 MHz
PAL system clock. "Wavy screen on warm-up" → clock chain (U30/U31); "wrong
frequency" → C70.

## Board revisions and how to ID one

`references/board-identification.md` has the per-board parts lists; the quick
identification:

| Version | Tell | PCB assy # | Schematic # |
|---------|------|-----------|-------------|
| Original | **5-pin** A/V DIN | 326298-01 | 326106 |
| A (CR) | **8-pin** A/V DIN | 250407-04 | 251138 |
| B | 8-pin DIN, reduced/single-IC oscillator | 250425 | 251469 |
| B-2 | 8-pin DIN; R28/29/30/36/48 collapsed into RP5, diodes CR100-105 relocated to CR9/12-16 | 250441-01 | 251469 |

So the fastest field ID is **count the pins on the video DIN** (5 = original,
8 = A or later) and then look at the clock section (discrete logic = original/A,
single clock IC = B). Boards are mechanically interchangeable, but match the
**modulator and A/V cable** to the board — modulators differ between revisions.

## Common failure modes (from the service-manual symptom table)

The full symptom→suspect table is in `references/troubleshooting.md`. Highest-yield
patterns:

- **Blank screen on power-up** → power supply first, then KERNAL ROM (U4), PLA
  (U17), CPU (U7), VIC (U19), the DRAMs (U9-12/U21-24), U8.
- **"OUT OF MEMORY" / garbage characters / locked cursor at boot** → bad DRAM
  (U9-12, U21-24); run the diagnostic disk.
- **Random crashes, wrong colors, fails only when warm** → very often the **PLA
  (U17)** or a marginal DRAM; PLAs (especially Commodore's HMOS replacement)
  run hot and are a notorious failure point. Power supply is the other prime
  warm-up suspect.
- **Characters show as solid blocks** → U26 (74LS373); **graphics chars instead
  of letters** → VIC (U19); **abnormal colors in letters** → color RAM U6 / U16.
- **Cassette motor never stops, TIP29 gets hot, fuse blows** → cassette port
  short / R4 open; check U7's port lines.
- **DEVICE NOT PRESENT on disk** → CIA U1/U2, U7, the serial bus resistors
  R28/29/30 and the U8 buffer.

The single most-replaced parts on a dead C64 are, in rough order: the **PLA
(U17)**, the **DRAM chips**, the failing **power brick / 5V regulator**, and the
**CIAs** (U1/U2, killed by hot-plugging joysticks/user-port devices).

## How to read the references

- **`references/specifications.md`** — read for the official spec sheet, the
  product parts list (case/keyboard/accessories), and the block-diagram intro.
- **`references/circuit-theory.md`** — read when you need *how a block works*:
  power supply rails, reset one-shot, clock/PLL, I/O & ROM address decode and
  the expansion port, RAM control / refresh, the 5-pin vs 8-pin video & audio
  output stages, cassette, keyboard/joystick/paddle, serial + user port. This is
  the prose behind every schematic block.
- **`references/troubleshooting.md`** — read when diagnosing: the full
  SYMPTOM → POSSIBLE SOLUTION table mapping a fault to the chips/parts to check.
- **`references/board-identification.md`** — read to identify a board revision,
  for the per-board parts lists (every Un → part number, plus all R/C/CN/misc
  values), and for the **chip pinouts** (CIA, SID, 6510, PLA, VIC-II, DRAM).
- **`references/connector-pinouts.md`** — read for the *external* port pin tables
  and connector drawings: control ports 1/2, cartridge/expansion slot, A/V,
  serial, cassette, user port.
- **`references/pla-82s100-datasheet.md`** — read for the 82S100 part itself
  (the programmable-logic-array datasheet) and the provenance of the dumped C64
  PLA. The actual banking equations live in **c64-memory-map**.

## Cross-links

- Register-level programming of each chip → **c64-vic-ii**, **c64-sid**,
  **c64-cia**.
- The ROM/RAM/IO banking the PLA implements (the $00/$01 port bits LORAM/HIRAM/
  CHAREN, GAME/EXROM) → **c64-memory-map**.
- Driving the ports from software (joystick/paddle reads, user-port I/O, serial,
  cassette) → **c64-io**, **c64-game-ports**, **c64-disk**, **c64-tape**.
- For deeper generic 6510/6502 CPU semantics you may optionally consult the
  companion repo `https://github.com/sunsided/6502-skills` (a suggestion, not a
  dependency).
