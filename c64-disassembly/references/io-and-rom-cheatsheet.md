# I/O and ROM address → meaning cheat-sheet

Authored quick-reference for tagging operands during a disassembly pass. For full
bit layouts use c64-vic-ii, c64-sid, c64-cia; for the full KERNAL table use
c64-kernal; for banking use c64-memory-map.

## VIC-II ($D000–$D02E, mirrored every $40 up to $D3FF)

| Addr | Reg | Meaning |
|------|-----|---------|
| `$D000-$D00F` | M0X..M7Y | sprite 0–7 X/Y position (pairs) |
| `$D010` | MSIGX | sprite X bit-8 (positions > 255) |
| `$D011` | control 1 | bit7=raster bit8, bit6=ECM, bit5=BMM, bit4=DEN, bit3=RSEL, bits2-0=YSCROLL |
| `$D012` | RASTER | raster line read / IRQ compare write |
| `$D015` | sprite enable | one bit per sprite |
| `$D016` | control 2 | bit4=MCM, bit3=CSEL, bits2-0=XSCROLL |
| `$D017` | MYE | sprite Y expand |
| `$D018` | memory ptr | screen RAM (bits7-4) & char/bitmap (bits3-1) base |
| `$D019` | IRQ flags | bit0=raster, bit1=spr-bg, bit2=spr-spr, bit3=lightpen |
| `$D01A` | IRQ enable | mask for the above |
| `$D01B` | sprite-bg priority | per sprite |
| `$D01C` | sprite multicolor | per sprite |
| `$D01D` | MXE | sprite X expand |
| `$D01E` | spr-spr collision | read-clears |
| `$D01F` | spr-bg collision | read-clears |
| `$D020` | border color | |
| `$D021-$D024` | background colors 0–3 | |
| `$D025-$D026` | sprite multicolor 0–1 | shared |
| `$D027-$D02E` | sprite 0–7 color | |

## SID ($D400–$D41C, mirrored to $D7FF)

| Addr | Meaning |
|------|---------|
| `$D400/$D401` | voice 1 freq lo/hi |
| `$D402/$D403` | voice 1 pulse width lo/hi |
| `$D404` | voice 1 control (bit0=gate,1=sync,2=ringmod,3=test,4=tri,5=saw,6=pulse,7=noise) |
| `$D405/$D406` | voice 1 attack/decay, sustain/release |
| `$D407-$D40D` | voice 2 (same layout, +7) |
| `$D40E-$D414` | voice 3 (same layout, +14) |
| `$D415/$D416` | filter cutoff lo/hi |
| `$D417` | resonance / filter routing |
| `$D418` | filter mode + master volume (low nibble) |
| `$D419/$D41A` | POTX / POTY (paddles, read) |
| `$D41B` | OSC3 / random (read) |
| `$D41C` | ENV3 (read) |

## Color RAM

`$D800-$DBFF` — 1000 nibbles, low 4 bits = color of the matching screen cell.

## CIA1 ($DC00) — keyboard, joysticks, IRQ

| Addr | Meaning |
|------|---------|
| `$DC00` | port A — keyboard cols / **control port 2** (joystick) |
| `$DC01` | port B — keyboard rows / **control port 1** (joystick) |
| `$DC02/$DC03` | DDRA / DDRB |
| `$DC04-$DC07` | timer A / B lo,hi |
| `$DC08-$DC0B` | TOD 10ths/sec/min/hr |
| `$DC0D` | ICR — IRQ control/status |
| `$DC0E/$DC0F` | CRA / CRB — timer control |

## CIA2 ($DD00) — serial bus, user port, VIC bank, NMI

| Addr | Meaning |
|------|---------|
| `$DD00` | port A — bits0-1 **VIC bank** (inverted), serial bus CLK/DATA/ATN, RS-232 |
| `$DD01` | port B — user port |
| `$DD0D` | ICR — NMI control/status |
| `$DD0E/$DD0F` | CRA / CRB |

## Expansion I/O

`$DE00-$DEFF` = I/O area 1, `$DF00-$DFFF` = I/O area 2 — cartridge-defined
registers (e.g. REU, GeoRAM, freezer carts).

## 6510 port

| Addr | Meaning |
|------|---------|
| `$0000` | data direction for the on-chip port (usually `$2F`) |
| `$0001` | bits0-2 = LORAM/HIRAM/CHAREN banking; bits3-5 = datasette out/sense/motor |

## Top KERNAL jump-table entries (call these, not the ROM body)

| Addr | Routine | Addr | Routine |
|------|---------|------|---------|
| `$FFB7` | READST | `$FFD2` | CHROUT |
| `$FFBA` | SETLFS | `$FFD5` | LOAD |
| `$FFBD` | SETNAM | `$FFD8` | SAVE |
| `$FFC0` | OPEN | `$FFE1` | STOP |
| `$FFC3` | CLOSE | `$FFE4` | GETIN |
| `$FFC6` | CHKIN | `$FFE7` | CLALL |
| `$FFC9` | CHKOUT | `$FFEA` | UDTIM |
| `$FFCC` | CLRCHN | `$FFF0` | PLOT |
| `$FFCF` | CHRIN | `$FF9F` | SCNKEY |
| `$FF81` | CINT (init screen/editor) | `$FFE7` | CLALL |

Common BASIC-ROM helpers seen in ML that calls into `$Axxx/$Bxxx`:
`$AB1E` print null-terminated string (A/Y = addr), `$BDCD` print 16-bit int in
A/X as decimal, `$E544` clear screen. Confirm against the running ROM version.
