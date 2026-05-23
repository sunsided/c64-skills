---
name: c64-assembly
description: >-
  Writing 6510 machine language on the Commodore 64: the CPU (a 6502 plus the
  on-chip $0000/$0001 I/O port that banks ROM/RAM), registers and status flags,
  the 13 addressing modes, the full 56-instruction opcode set, hexadecimal, the
  64MON monitor, where to place ML routines, and calling ML from BASIC. Use this
  skill WHEN writing or reasoning about C64 assembly: "write a 6510 routine",
  "what does LDA #$01 do", "how do I SYS to my code", "pass A/X/Y from BASIC",
  "where do I put machine code", "what's the USR vector", "RTS back to BASIC".
  Pairs with c64-kernal, c64-memory-map, and c64-disassembly.
---

# C64 Assembly (6510 Machine Language)

Writing and reasoning about 6510 machine language on the Commodore 64. The 6510
is a **6502 with one addition**: an on-chip 6-bit I/O port at `$0000` (data
direction) / `$0001` (the port) that banks ROM, RAM, I/O, and character ROM in
and out of the address space. The instruction set, registers, and addressing
modes are 100% identical to the NMOS 6502 — everything you know about 6502 code
applies, plus the banking port.

## 6510 vs 6502 — the only difference

```
$0000  D6510  Data Direction Register for the on-chip port (default $2F = %101111)
$0001  R6510  The 6-bit I/O port itself
```

| Bit | Name   | Controls                                      |
|-----|--------|-----------------------------------------------|
| 0   | LORAM  | $A000-$BFFF: 1=BASIC ROM, 0=RAM               |
| 1   | HIRAM  | $E000-$FFFF: 1=KERNAL ROM, 0=RAM              |
| 2   | CHAREN | $D000-$DFFF: 1=I/O visible, 0=character ROM   |
| 3   | —      | Cassette write line                           |
| 4   | —      | Cassette switch sense (input; 0=play down)    |
| 5   | —      | Cassette motor control (0=motor on)           |

Default value at `$0001` is `$37` (LORAM/HIRAM/CHAREN all 1 → BASIC + KERNAL +
I/O all visible). To read character ROM, clear CHAREN; to run code under the
KERNAL, clear HIRAM. Writing through ROM always hits the **hidden RAM** beneath
it; reading returns ROM. This is a summary — for the full bank-configuration
table, the PLA logic, and VIC bank selection see **c64-memory-map**.

## Register / flag model

```
A   8-bit  Accumulator      — the only register with full ALU + math
X   8-bit  Index register X  — indexing, loop counters, TSX/TXS for stack
Y   8-bit  Index register Y  — indexing (only Y works with (zp),Y)
S   8-bit  Stack pointer     — stack at $0100+S, grows downward
PC  16-bit Program counter
P   8-bit  Processor status  — flags below
```

Status `P`, bit 7 → 0: `N V - B D I Z C`

| Flag | Bit | Meaning |
|------|-----|---------|
| N | 7 | Negative — bit 7 of last result |
| V | 6 | Overflow — signed overflow from ADC/SBC; bit 6 of operand for BIT |
| - | 5 | unused, reads as 1 |
| B | 4 | Break — set in the P pushed by BRK/PHP; not a real bit |
| D | 3 | Decimal — when set, ADC/SBC do BCD arithmetic |
| I | 2 | IRQ disable — set ⇒ maskable interrupts ignored |
| Z | 1 | Zero — last result was $00 |
| C | 0 | Carry — carry out of ADC / inverted borrow for SBC / shifted bit / compare |

Two flags people get wrong: **carry on subtraction/compare is inverted borrow** —
`SEC` before a standalone `SBC`; after `CMP`, C=1 means A ≥ operand (unsigned).
And **`BIT` loads nothing** — it sets Z from `A AND M` but copies bit 7 of memory
into N and bit 6 into V.

## Addressing modes (13)

| Mode | Example | Notes |
|------|---------|-------|
| Immediate | `LDA #$01` | operand is the literal byte |
| Zero page | `LDA $FB` | 1-byte address $0000-$00FF; faster, smaller |
| Zero page,X / ,Y | `LDA $FB,X` | wraps within zero page |
| Absolute | `LDA $0400` | full 16-bit address |
| Absolute,X / ,Y | `STA $0400,X` | +1 cycle on page cross (reads only) |
| Indirect | `JMP ($0314)` | only JMP; NMOS page-wrap bug at $xxFF |
| Indexed indirect | `LDA ($FB,X)` | (zp+X) → pointer; X added before deref |
| Indirect indexed | `LDA ($FB),Y` | (zp) → pointer, then +Y; the workhorse |
| Implied | `INX`, `RTS` | no operand |
| Accumulator | `LSR`, `ROL A` | operates on A |
| Relative | `BNE $1402` | branch ±127 from the byte after the operand |

Full per-opcode byte/cycle table is in `references/instruction-set-6510.md`.

## Opcode summary (the 56 mnemonics)

- **Load/store:** LDA LDX LDY / STA STX STY
- **Transfer:** TAX TAY TXA TYA TSX TXS
- **Stack:** PHA PLA PHP PLP
- **Arithmetic/logic:** ADC SBC AND ORA EOR / CMP CPX CPY / INC INX INY DEC DEX DEY
- **Shift/rotate:** ASL LSR ROL ROR
- **Bit test:** BIT
- **Branch:** BCC BCS BEQ BNE BMI BPL BVC BVS
- **Jump/sub:** JMP JSR RTS / BRK RTI
- **Flags:** CLC SEC CLD SED CLI SEI CLV
- **NOP**

Branch cheat-sheet after `CMP A,M`: `BEQ`/`BNE` = `==`/`!=`; `BCS`/`BCC` = `>=`/`<`
unsigned; `BMI`/`BPL` = result bit7 set/clear; `BVS`/`BVC` = signed overflow.
For exact flag effects, bytes, and cycle counts per addressing mode, read
`references/instruction-set-6510.md`.

## Hexadecimal

Addresses 0-65535 = `$0000`-`$FFFF`. Prefix hex with `$`. A 16-bit value is split
low-byte/high-byte: `$1400` = lo `$00`, hi `$14`. `SYS 49152` and `SYS $C000` and
`SYS 12*4096` all target the same address.

## 64MON monitor

64MON is Commodore's ML monitor cartridge (assembler/disassembler/memory editor).
Manual examples use its syntax. Common commands:

| Cmd | Action |
|-----|--------|
| `.R` | display registers (PC SR AC XR YR SP) |
| `.M 0000 0020` | display memory (rows of 8 bytes after the address) |
| `.A 1400 LDA #$01` | assemble at $1400 |
| `.D 1400 1410` | disassemble |
| `.G 1400` | go (run) from $1400 — ends when it hits BRK, returning to 64MON |
| `BRK` | in your code, returns control to the monitor |

## Calling ML from BASIC

Five routes; SYS and USR are the everyday ones.

**SYS addr** — `JSR`s to your routine; end it with `RTS` to return to BASIC.
Pass parameters with PEEK/POKE, or load A/X/Y/status from these locations, which
SYS copies into the registers before the call and copies back after:

```
$030C  780  SAREG  .A register
$030D  781  SXREG  .X register
$030E  782  SYREG  .Y register
$030F  783  SPREG  status (P)
```

```basic
POKE 780,65 : POKE 781,0 : POKE 782,0 : SYS 49152 : REM call $C000 with A=65
```
```asm
        ; the routine SYS lands on:
        STA $0400          ; do work
        RTS                ; <-- mandatory: returns to BASIC
```

**USR(x)** — `JMP`s through the vector at `$0311/$0312` (785/786; `$0310`=784 holds
the JMP opcode $4C). The argument `x` arrives in floating-point accumulator #1 at
`$61`, and your return value goes back the same way. You must set the vector
first:

```basic
POKE 785,0 : POKE 786,192 : REM USR vector -> $C000
```

Other routes (deeper): replacing a **page-3 I/O vector** (e.g. CHROUT at $0326),
hooking the **IRQ vector** `CINV $0314/$0315` (disable interrupts first; end with
`RTI` if you serviced the CIA — see **c64-cia**), and the **CHRGET wedge** for
adding BASIC commands. The RTS-to-BASIC convention applies to SYS and USR; an IRQ
handler ends with RTI instead.

## Where to put ML code

- **`$C000-$CFFF`** (49152-53247) — 4K of free RAM BASIC never touches. The
  default home for ML routines.
- **Cassette buffer `$033C-$03FB`** (828-1019, `TBUFFR`) — 192 bytes, fine for
  small routines if you aren't using tape.
- **Top of BASIC RAM** — for larger routines, lower BASIC's top and `CLR`:
  ```basic
  10 POKE 51,L : POKE 52,H : POKE 55,L : POKE 56,H : CLR : REM reserve from H/L up
  ```
  (e.g. reserve $9000-$9FFF: `POKE 51,0:POKE 52,144:POKE 55,0:POKE 56,144:CLR`).

Entry methods: READ/DATA + POKE (easiest, small routines), 64MON or an
editor/assembler (faster, debuggable, save to disk/tape).

## Gotchas

- Forgetting the final `RTS` — your SYS never returns and the C64 hangs/crashes.
- `(zp),Y` only takes Y; `(zp,X)` only takes X. They are not interchangeable.
- The pointer for `(zp),Y` is two bytes in **zero page** — a 16-bit address there.
- After `CMP`, carry is the *unsigned* comparison; signed needs N⊕V.
- `JMP ($xxFF)` on NMOS fetches the high byte from `$xx00`, not the next page.
- Touching `$0001` mid-routine can bank out the KERNAL/IRQ — keep `SEI` around it
  and restore the previous value.

## How to read the references

- **`references/machine-language-guide.md`** — the PRG Ch5 tutorial: registers,
  hex, every addressing mode worked out, indexing, the stack, branches,
  subroutines, 64MON walkthroughs, "Using Machine Language From BASIC" (SYS/USR/
  vectors/wedges), and "Where to put ML". Read for narrative depth and examples.
- **`references/instruction-set-6510.md`** — the alphabetical MCS6510 instruction
  list with descriptions, plus the addressing-modes-and-execution-times table
  (opcode bytes, byte counts, cycle counts). Read when disassembling raw bytes,
  checking an exact opcode, or counting cycles.
- **`references/6510-chip-spec.md`** — Appendix L: 6510 pin configuration,
  electrical/timing specs, and the on-chip I/O port hardware description. Read for
  hardware-level detail.

For deeper *generic* 6502/65C02/65816 semantics (CMOS additions, the 16-bit
65816, undocumented opcodes) the companion repo
`https://github.com/sunsided/6502-skills` is an optional suggestion — not
required; this skill carries the 6510 detail you need standalone. For ROM calls
see **c64-kernal**; for addresses, banking, and the memory map see
**c64-memory-map**; for reading existing binaries see **c64-disassembly**.
