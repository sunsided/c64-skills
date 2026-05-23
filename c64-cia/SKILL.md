---
name: c64-cia
description: >-
  The two MOS 6526 CIA chips on the Commodore 64 — CIA1 at $DC00 (keyboard scan,
  joystick/paddle ports, the IRQ source) and CIA2 at $DD00 (serial IEC bus, user
  port, VIC bank select, the NMI source) — their data ports A/B and DDRs, the two
  16-bit interval timers, the Time-of-Day clock, the serial shift register, and
  the interrupt control register. Use this skill WHEN working with these chips:
  "set up a CIA timer IRQ", "read the TOD clock", "what's at $DC0D", "the CIA
  interrupt control register", "$DD00 VIC bank bits", "user port lines". Pairs
  with c64-keyboard, c64-game-ports, c64-io, c64-vic-ii, and c64-memory-map.
---

# C64 CIA (6526) Chips

The C64 has **two** MOS 6526 Complex Interface Adapters. Each is identical
silicon — same 16-register layout — but wired to different things:

- **CIA1 at `$DC00`** (56320): keyboard matrix scan, joystick/paddle game ports,
  and its `/IRQ` line drives the CPU **IRQ**. This is what the KERNAL's 60 Hz
  jiffy interrupt uses.
- **CIA2 at `$DD00`** (56576): serial IEC bus, RS-232, the user port, VIC bank
  select, and its `/IRQ` line is wired to the CPU **NMI**.

## Register map (offset from the chip base)

| Off | Name | Function |
|-----|------|----------|
| +0 | PRA  | Peripheral data register A |
| +1 | PRB  | Peripheral data register B |
| +2 | DDRA | Data direction register A (1=output) |
| +3 | DDRB | Data direction register B |
| +4 | TA LO | Timer A low byte |
| +5 | TA HI | Timer A high byte |
| +6 | TB LO | Timer B low byte |
| +7 | TB HI | Timer B high byte |
| +8 | TOD 10THS | Time-of-day 1/10 seconds (BCD) |
| +9 | TOD SEC | TOD seconds (BCD) |
| +A | TOD MIN | TOD minutes (BCD) |
| +B | TOD HR | TOD hours + AM/PM (bit 7) (BCD) |
| +C | SDR  | Serial data (shift) register |
| +D | ICR  | Interrupt control register (read=flags, write=mask) |
| +E | CRA  | Control register A (Timer A) |
| +F | CRB  | Control register B (Timer B) |

So CIA1 timer A low byte = `$DC04`, CIA2 ICR = `$DD0D`, etc.

## What each CIA is wired to

**CIA1 ($DC00):** PRA (`$DC00`) writes the keyboard **column** strobe (and
selects paddles, bits 6-7); PRB (`$DC01`) reads the keyboard **row** lines.
Joystick directions/fire share these same lines — joystick 2 on PRA, joystick 1
on PRB (each: bits 0-3 directions, bit 4 fire). Its interrupt goes to **IRQ**.

**CIA2 ($DD00):** PRA bits 1-0 are the **VIC bank select** (inverted: 11→bank 0);
bits 2-7 are the serial bus (ATN/CLK/DATA out, CLK/DATA in) and RS-232 TX. PRB
(`$DD01`) is the 8-bit **user port** (also RS-232 handshake lines). Its interrupt
goes to **NMI** (so RESTORE — wired to NMI — and any CIA2 timer share that line).

For the keyboard matrix detail see **c64-keyboard**; for joysticks/paddles see
**c64-game-ports**; for the serial bus and user port see **c64-io**; for VIC bank
selection in context see **c64-memory-map**.

## Interrupt control register (ICR, +$D)

The ICR has a **read** side (flags) and a **write** side (mask) at the same
address — they behave differently:

```
READ  (INT DATA):  IR  0  0  FLG SP ALRM TB TA
WRITE (INT MASK): S/C  x  x  FLG SP ALRM TB TA
```

- Bits: TA = Timer A underflow, TB = Timer B underflow, ALRM = TOD alarm,
  SP = serial port full/empty, FLG = /FLAG pin edge. Bit 7 on read (IR) = "this
  chip raised an interrupt".
- **Reading the ICR clears it** (and releases the /IRQ line). Read it once in
  your handler and act on the saved value — a second read loses the flags.
- **Writing the mask uses bit 7 as set/clear:** if bit 7 of the written byte is
  1, every 1-bit *enables* that source; if bit 7 is 0, every 1-bit *disables* it.
  Zero bits are unaffected either way.

```asm
        LDA #%10000001     ; bit7=1 (set) + TA bit -> enable Timer A interrupt
        STA $DC0D
        LDA #%01111111     ; bit7=0 (clear) + all bits -> disable all sources
        STA $DC0D          ; common at IRQ-setup time to clear pending CIA IRQs
```

## Control registers (CRA/CRB, +$E/+$F)

CRA bits: 0 START (1=run), 1 PBON (timer out on PB6), 2 OUTMODE (1=toggle/0=pulse),
3 RUNMODE (1=one-shot/0=continuous), 4 LOAD (strobe: force-load latch into
counter), 5 INMODE (1=count CNT edges/0=count φ2 cycles), 6 SPMODE (serial
out/in), 7 TODIN (1=50 Hz / 0=60 Hz TOD clock). CRB is the same for Timer B
except bit 1 = PB7, bits 5-6 select Timer B's input (φ2 / CNT / Timer A underflow
/ Timer A underflow while CNT high), and bit 7 = ALARM (1: writes set the TOD
alarm instead of the clock).

## Worked example: hook a CIA1 Timer A IRQ

```asm
        SEI
        LDA #<handler
        STA $0314          ; CINV — KERNAL IRQ vector lo
        LDA #>handler
        STA $0315          ; CINV hi
        LDA #$01           ; Timer A latch = period (low byte)...
        STA $DC04
        LDA #$00
        STA $DC05          ; ...high byte
        LDA #%10000001     ; ICR: set-mask, enable Timer A
        STA $DC0D
        LDA #%00010001     ; CRA: LOAD latch + START, continuous
        STA $DC0E
        CLI
        RTS

handler:
        LDA $DC0D          ; READ + CLEAR the CIA1 ICR (releases IRQ)
        ; ... do periodic work ...
        JMP $EA31          ; chain to the KERNAL IRQ handler (or $EA81 for RTI-only)
```

To stop scanning the keyboard/jiffy and own the IRQ entirely, you can clear the
default sources first with `LDA #$7F : STA $DC0D`, then enable just yours.

## Time-of-Day clock

The TOD is a 4-register BCD clock (10ths, sec, min, hr+AM/PM) ticking off a 50/60
Hz reference (set by CRA bit 7). Reading and writing follow a strict order:

- **Reading:** reading the **Hours** register *latches* all four; they stay
  latched until you read **10ths** — so read HR → MIN → SEC → 10THS to get a
  consistent snapshot. (To read one register on the fly, follow a HR read with a
  10THS read to clear the latch.)
- **Writing:** writing **Hours** *stops* the clock; it doesn't restart until you
  write **10ths**. So write HR last-but-one and 10THS last. With CRB bit 7 = 1,
  writes set the **alarm** (which fires the ALRM interrupt) instead of the clock.
- All values are **BCD** — `$59` means 59, not 89.

## Serial shift register (SDR, +$C)

An 8-bit synchronous shift register, MSB first. Input mode shifts SP-pin data in
on CNT rising edges, raising the SP interrupt after 8 bits. Output mode uses
Timer A as the baud generator (shift rate = ½ the Timer A underflow rate), CNT
becomes the clock output, and writing the SDR starts transmission. Used for fast
inter-chip links; the standard C64 IEC bus uses the port-A handshake lines, not
this register.

## Gotchas

- **ICR read clears the flags** — read once, save the byte, branch on the copy.
- **ICR write mask uses bit 7 as set/clear**, not as a flag bit — `#$7F` disables
  all, `#$81` enables just Timer A.
- **$DD00 VIC bank bits are inverted** — 11 = bank 0 ($0000-$3FFF). Set DDRA
  (`$DD02`) bits 0-1 to outputs first.
- CIA2 interrupts hit **NMI**, not IRQ; an NMI can't be masked by `SEI`, and the
  RESTORE key shares that line.
- TOD latching/stopping: read Hours then 10ths; write Hours then 10ths — get the
  order wrong and the clock freezes or you read a torn value.
- TOD registers are **BCD**.
- Timer LOAD (CRA/CRB bit 4) is a strobe: it always reads back 0, and writing 0
  does nothing — set it only to force-load the latch.

## How to read the references

- **`references/cia-6526-spec.md`** — Appendix M, the full 6526 chip
  specification: features, the complete register map, the functional description
  of the I/O ports, both interval timers and their modes, the Time-of-Day clock
  (with the read/write latching sequence and BCD layouts), the serial shift
  register, the interrupt control register read/write tables, and the CRA/CRB bit
  charts. Read for the exact bit meaning of any CIA register or precise timer
  behavior.

For the bit assignments of the C64's *specific* wiring of these registers ($DC00
keyboard/joystick lines, $DD00 serial/VIC-bank/RS-232 lines) see
`references/io-assignments.md` in **c64-memory-map**. Keyboard scanning →
**c64-keyboard**; joysticks/paddles → **c64-game-ports**; serial bus / user port
→ **c64-io**; raster vs timer interrupts → **c64-vic-ii**; banking → **c64-memory-map**.
