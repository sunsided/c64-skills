---
name: c64-io
description: >-
  The Commodore 64 input/output system and its device/file model: logical
  device numbers, OPEN/CLOSE/PRINT#/INPUT#/GET#/CMD, secondary addresses, and
  the ports behind them — output to TV/printer/modem, the RS-232 interface, the
  serial IEC bus, the user port, the expansion (cartridge) port, and the Z-80
  cartridge. Use this skill WHEN a user asks "how do I OPEN a channel", "what
  device number is the printer/screen/RS-232", "what does the secondary address
  mean", "how does the serial bus work", "what's on the user port or expansion
  port", "how do I set up RS-232 / a modem", or works with EXROM/GAME, ATN/CLK/
  DATA, $DD00, $DE00. Pairs with c64-disk, c64-tape, c64-game-ports, c64-cia,
  c64-kernal, and c64-memory-map.
---

# C64 Input/Output System

Every peripheral on the C64 is reached through one model: you OPEN a *logical
file* onto a *device number* (optionally with a *secondary address* and a name),
then use PRINT#/CMD to send and INPUT#/GET# to receive, and CLOSE when done. The
screen, keyboard, tape, RS-232, printer, and disk are all the same machinery
from BASIC's point of view — only the device number and the meaning of the
secondary address change.

## Logical device numbers

| Dev | Device | Notes |
|-----|--------|-------|
| 0 | Keyboard | default input |
| 1 | Cassette (Datassette) | default for LOAD/SAVE with no device — see **c64-tape** |
| 2 | RS-232 | built-in serial interface, runs on CIA2 |
| 3 | Screen | default output |
| 4, 5 | Printer | on the serial bus |
| 6, 7 | (plotter / extra serial devices) | |
| 8–11 | Disk drives | 8 is the usual 1541 — see **c64-disk** |

Devices 4–11 live on the **serial IEC bus**; 1 (tape), 2 (RS-232), 3 (screen),
0 (keyboard) do not.

## The OPEN model

```
OPEN logical#, device#, secondary#, "name"
```

- **logical#** (1–255): the handle you pass to PRINT#/INPUT#/GET#/CMD/CLOSE. Use
  1–127; numbers >127 add a line feed after each carriage return.
- **device#**: from the table above.
- **secondary#** (a.k.a. sa / channel): a per-device setup code (see below).
- **"name"**: filename, or device-specific setup bytes (printer mode, RS-232
  control/command bytes, disk "drive:name,type,mode").

```basic
100 OPEN 4,4: PRINT#4,"WRITING ON PRINTER"        : REM printer, dev 4
110 OPEN 3,8,3,"0:DISK-FILE,S,W": PRINT#3,"HI"     : REM disk seq write
120 OPEN 1,1,1,"TAPE-FILE": PRINT#1,"WRITE ON TAPE": REM tape write
130 OPEN 2,2,0,CHR$(10): PRINT#2,"SEND TO MODEM"   : REM RS-232
```

Companion statements: `PRINT#lf,...` writes; `INPUT#lf,var` / `GET#lf,var$` read;
`CMD lf` redirects normal PRINT output to that file (e.g. `CMD` to a printer then
`LIST`); `CLOSE lf` finishes. Read the **reserved variable ST** after I/O for
status (end-of-file, errors). Pitfall: after `CMD`, you must `PRINT#lf` then
`CLOSE lf` to flush and unhook output, or the channel stays redirected.

## Secondary address meaning (per device)

| Device | sa | Meaning |
|--------|-----|---------|
| Cassette | 0 / 1 / 2 | read / write / write-with-EOT marker |
| Printer | 0 / 7 | upper-case+graphics / upper+lower case |
| RS-232 | 0 | always 0; the name field carries control/command bytes |
| Disk | 2–14 | data channel; **15** = command channel (DOS commands) |

The secondary address is how the C64 hands *setup* to a device — e.g.
`OPEN 1,4,7` tells printer 4 to switch to upper/lower case.

## Output to screen, printer, modem

- **Screen (dev 3):** plain `PRINT`. `;` joins with no space, `,` tabs to the
  next 10-column field, both suppress the trailing RETURN when last on the line.
  `TAB`/`SPC` position the cursor. For colors, sprites, raster: see **c64-vic-ii**.
- **Printer (dev 4/5):** like the screen, but `TAB` is wrong (it uses the screen
  cursor, not the paper) — use `SPC`. Control via PETSCII codes you simply PRINT:
  14/15 double-width on/off, 18/146 reverse on/off, 17/145 switch case set, 8 dot
  graphics. Full table in `references/io-guide.md`.
- **Modem (dev 2):** OPEN with control/command bytes selects baud/parity; you
  must translate PETSCII↔ASCII yourself. The modem *is* the RS-232 interface —
  see below.

## RS-232 interface

The C64 has a built-in RS-232 at **TTL levels (0–5V)**, not true ±12V — you need
a level-converting cable/cartridge. It runs as a software UART driven by **CIA2**
NMIs in the background. OPEN allocates two 256-byte FIFO buffers at the top of
memory (512 bytes total).

```basic
OPEN 2,2,0, CHR$(<control>)+CHR$(<command>)
```

- **control byte** sets baud/word-length/stop-bits (e.g. `CHR$(6)` = 300 baud).
- **command byte** sets parity/duplex/handshake (3-line vs x-line).
- Read **ST** for status: parity/framing/overrun/break errors, buffer-empty,
  CTS/DSR missing. Prefer `GET#` over `INPUT#` (INPUT# can hang the system).

Critical gotcha: **OPEN an RS-232 channel before creating variables/arrays** —
the OPEN does an automatic CLR to allocate buffers, and if 512 free bytes aren't
available your program gets corrupted with no error. Only one RS-232 channel at a
time. Full register maps, status bits, buffer pointers ($F7/$F9), and zero-page
usage live in `references/rs232.md`.

## The serial IEC bus

A daisy-chained 6-pin DIN bus (up to 5 devices). The C64 is always the
**controller**; it commands devices to **TALK** (put data on the bus) or
**LISTEN** (receive). Each device has a bus address (4–31); common ones: 4/5
printer, 8 disk. Only one talker at a time; many listeners. Lines:

| Pin | Signal | |
|-----|--------|-|
| 1 | /SERIAL SRQ IN | device requests attention |
| 2 | GND | |
| 3 | SERIAL ATN OUT | C64 pulls low to start a command (all devices listen for the address) |
| 4 | SERIAL CLK IN/OUT | bit timing |
| 5 | SERIAL DATA IN/OUT | one bit at a time |
| 6 | /RESET | |

If an addressed device doesn't answer in time, you get a device-not-present
error in the status word. Disk and printer details: **c64-disk**, plus the
KERNAL talk/listen routines in **c64-kernal**.

## The user port

A 12+12-pin edge connector wired straight to **CIA2**. It exposes CIA2 Port B
(PB0–PB7) as 8 general-purpose I/O lines plus FLAG2/PA2 handshake lines, and the
RS-232 signals (Sin/Sout/RTS/CTS/DSR/DCD) ride here too. From BASIC you POKE/PEEK
the port through CIA2:

| Register | Addr | Use |
|----------|------|-----|
| Port B (data) | 56577 / $DD01 | PEEK to read inputs, POKE to drive outputs |
| Port B DDR | 56579 / $DD03 | 1 bit = output, 0 bit = input |
| Port A | 56576 / $DD00 | PA2 is a handshake line |
| Port A DDR | 56578 / $DD02 | |

```basic
POKE 56579,255 : REM all 8 PB lines = outputs
POKE 56577,56  : REM drive bits 5,4,3 high (32+16+8)
```

```asm
        LDA #$FF
        STA $DD03   ; DDR: PB all outputs
        LDA #56
        STA $DD01   ; write the lines
```

For the CIA2 register set, timers, FLAG/PC handshaking, and the SP/CNT serial
lines also brought out here, see **c64-cia**.

## The expansion (cartridge) port

A 44-pin edge connector exposing the full address bus, data bus, R/W, clocks,
/IRQ, /NMI, /DMA, and four decode lines:

- **/ROML** ($8000) and **/ROMH** ($E000): cartridge ROM banks.
- **/I/O1** ($DE00–$DEFF) and **/I/O2** ($DF00–$DFFF): cartridge I/O windows.
- **/EXROM** and **/GAME**: the two control inputs that tell the PLA how to bank
  the cartridge in. Pulling these (with the cart ROM at $8000 containing the
  autostart "CBM80" signature) makes a cartridge **autostart** on power-up.
- Total user-port + cartridge draw ≤ 450 mA; /DMA should only be pulled when φ2
  is low and the device must respect VIC-II bus timing.

The exact RAM/ROM/IO banking that /EXROM and /GAME drive is in
**c64-memory-map**.

## Z-80 cartridge (Commodore CP/M)

A cartridge that drops a Z-80 onto the expansion bus so the C64 can run CP/M
software. The 6510 and Z-80 share the buses but run one at a time. Z-80 addresses
are offset by +$1000 from 6510 addresses. The sample turn-on program first
disables 6510 IRQs (`POKE 56333,127`, the CIA1 ICR), then writes the cartridge
I/O location (`POKE 56832,0` = $DE00, the /I/O1 window) to hand control to the
Z-80; the Z-80 self-disables to hand control back. See `references/io-guide.md`
for the full address-translation table and turn-on program.

## Quick answers

- **"What device number is the printer / screen / disk / RS-232?"** Printer 4 (or
  5), screen 3, disk 8, RS-232 2, tape 1, keyboard 0.
- **"How do I open a printer channel and print?"** `OPEN 4,4: PRINT#4,"TEXT": CLOSE 4`.
- **"How do I redirect LIST to the printer?"** `OPEN 4,4: CMD 4: LIST: PRINT#4: CLOSE 4`.
- **"How many devices on the serial bus?"** Up to 5, addresses 4–31.

## How to read the references

- **`references/io-guide.md`** — the verbatim Ch6 text: TV/printer/modem output,
  the OPEN parameter table, full printer control-code table, the user port pin
  list + DDR explanation, the serial bus (talk/listen, addresses, timing table),
  the expansion port pinout, and the Z-80 cartridge. Read this for any pin,
  control code, or bus-timing detail.
- **`references/rs232.md`** — everything RS-232: control/command register bit
  maps (Figures 6-1/6-2), opening/getting/sending/closing a channel, the status
  register bits (Figure 6-3), two complete sample terminal programs, the
  receiver/transmitter buffer base pointers ($F7/$F9), and the zero-page +
  $0293-area working storage. Read this when setting baud/parity or debugging
  RS-232 timing/buffers.
- **`references/io-pinouts.md`** — App I connector pinouts (control ports,
  cartridge slot, audio/video, serial I/O, cassette, user port) with the
  physical connector diagrams. Read this when wiring a cable or identifying a pin.

## Cross-links

- Disk drives (LOAD/SAVE, directory, command channel) → **c64-disk**
- Cassette tape (LOAD/SAVE/VERIFY, data files) → **c64-tape**
- Joysticks, paddles, light pen on the control ports → **c64-game-ports**
- The CIA chips behind the user port and serial bus → **c64-cia**
- KERNAL I/O routines (OPEN/CHKIN/CHKOUT/CHRIN/CHROUT/CLOSE) → **c64-kernal**
- RAM/ROM/IO banking driven by /EXROM and /GAME → **c64-memory-map**
