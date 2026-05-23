# .prg / cartridge containers, the BASIC stub, and the vectors

Authored cheat-sheet (synthesised for the disassembly workflow). Address facts
are cross-checked against c64-memory-map and c64-kernal.

## .prg file layout

```
offset 0  : load address low byte
offset 1  : load address high byte   (little-endian => addr = lo + 256*hi)
offset 2+ : program bytes, loaded starting at that address
```

`LOAD"name",8`  loads to the embedded address only after relocation for BASIC;
`LOAD"name",8,1` (secondary address 1) forces load to the **embedded** address —
that is how ML/data files land where they expect to be. When disassembling, always
honour the embedded address as the origin.

Typical load addresses:

| Load addr | Decimal | Usual meaning |
|-----------|---------|---------------|
| `$0801` | 2049 | BASIC program (or BASIC stub + ML) |
| `$080D` | 2061 | ML right after a minimal stub |
| `$0810` | 2064 | ML after a `10 SYS 2064` stub |
| `$1000`,`$2000`,`$4000` | — | ML, often demos/games |
| `$C000` | 49152 | ML in the free RAM block under I/O |
| `$0340`,`$033C` | 832,828 | small ML in the tape/cassette buffer |

## Tokenized BASIC line format (at `$0801`)

Each line, in order:

```
.word next_line_addr   ; absolute pointer to the next line's first byte
.word line_number      ; 16-bit binary line number
... body ...           ; PETSCII bytes; tokens are single bytes $80..$FF
.byte $00              ; end of this line
```

The program ends with a **`next_line_addr` of `$0000`** (two zero bytes where the
next link pointer would be).

Common token bytes you will meet decoding a launcher:

| Byte | Token |
|------|-------|
| `$9E` | `SYS` |
| `$99` | `PRINT` |
| `$8F` | `REM` |
| `$97` | `POKE` |
| `$94` | `CLR` |
| `$A2` | `NEW` |

### Decoding `10 SYS 2064`

Bytes at `$0801` for that exact line:

```
$0801: 0B 08      ; link -> $080B (next line)
$0803: 0A 00      ; line number 10
$0805: 9E         ; SYS token
$0806: 20         ; space (PETSCII)
$0807: 32 30 36 34 ; "2064"  (PETSCII digits)
$080B: 00         ; end of line
$080C: 00 00      ; link = 0000 -> end of program
$080D / $0810: ... machine code ...
```

To extract the SYS target programmatically: from `$0801`, skip 4 bytes
(link+lineno), confirm `$9E`, skip any spaces, then read PETSCII digit bytes
(`$30`-`$39`) until a non-digit/`$00`; that decimal value is the entry point.

## CPU hardware vectors (top of memory)

When ROM is mapped at `$E000`, these read from KERNAL ROM; when RAM is banked in
there, they are whatever the program wrote. The CPU fetches:

| Vector | Address | Fired on |
|--------|---------|----------|
| NMI | `$FFFA/$FFFB` | RESTORE key, CIA2 timer/NMI |
| RESET | `$FFFC/$FFFD` | power-on / reset line |
| IRQ/BRK | `$FFFE/$FFFF` | maskable IRQ (CIA1 timer, VIC raster) and `BRK` |

In the **default** (KERNAL-mapped) machine you do not patch `$FFFE` directly;
instead the KERNAL IRQ handler reads a RAM vector:

| RAM vector | Address | Used by KERNAL for |
|------------|---------|--------------------|
| CINV (IRQ) | `$0314/$0315` | the IRQ service routine |
| CBINV (BRK) | `$0316/$0317` | the BRK service routine |
| NMINV (NMI) | `$0318/$0319` | the NMI service routine |

So "hook the IRQ" usually means: `SEI`, write your handler addr to `$0314/$0315`,
`CLI`. A handler that ends `JMP $EA31` chains to the normal KERNAL IRQ (keyboard
scan, jiffy clock); ending `JMP $EA81` just pulls registers and `RTI`.

## Cartridge (`.crt`) entry

A cartridge maps ROM at `$8000` (8K, `$8000-$9FFF`) and optionally `$A000-$BFFF`
(16K), controlled by the `EXROM`/`GAME` lines (see c64-memory-map). An autostart
cartridge is recognised by the KERNAL via the signature bytes `CBM80` (PETSCII
`C` `B` `M` plus `$80 $30`) at `$8004`, and the cold-/warm-start vectors at:

```
$8000/$8001 : cold start (RESET) entry
$8002/$8003 : warm start (NMI)  entry
$8004..$8008: $C3 $C2 $CD $38 $30  = "CBM80" signature
```

Disassemble a cartridge from the cold-start vector at `$8000`.
