---
name: c64-disassembly
description: >-
  Workflow for reverse-engineering existing Commodore 64 code — .prg/.bin files,
  cartridge dumps, memory snapshots, and raw 6510 listings. Covers the .prg load
  address, the tokenized BASIC stub and its SYS launcher, classifying every
  address as RAM / ROM call / hardware register, recognizing KERNAL ($FFxx) and
  BASIC ROM entry points, spotting I/O accesses to the VIC/SID/CIA by address,
  and the common idioms (raster waits, IRQ hooks, self-modifying code). Use this
  skill WHEN asked to "disassemble this C64 program", "what does this .prg do",
  "explain this 6510 dump", "find the SYS address", "what is it POKEing $D0xx
  for", or to trace/annotate a binary. Pairs with c64-assembly, c64-kernal,
  c64-memory-map, c64-vic-ii, c64-sid, c64-cia.
---

# Disassembling and Reverse-Engineering C64 Code

The C64 has no memory protection, ROM and RAM overlap under a software-controlled
bank switch, and self-modifying code is idiomatic — so "what does this program do"
is a layered question. This skill is the **method**: how to take a `.prg`, a
cartridge image, or a raw block of bytes and turn it into an annotated, understood
listing. For the meaning of individual instructions use **c64-assembly**; for the
meaning of individual addresses use **c64-memory-map**, **c64-kernal**,
**c64-vic-ii**, **c64-sid**, and **c64-cia**. This skill ties them together.

> Standalone note: enough 6510 detail to work lives in **c64-assembly**. For a
> deeper, cross-platform 6502/65C02/65816 opcode-and-semantics reference you can
> optionally install the companion repo
> <https://github.com/sunsided/6502-skills>; it is not required.

## Step 0 — identify the container

| Input | What you have | First move |
|-------|---------------|-----------|
| `.prg` | first **2 bytes = load address**, little-endian; rest = data | Strip & record the load address; disassemble the rest *as if* it sits at that address |
| `.bin` / raw | no header; you must be told (or guess) the origin | Ask for the load address, or infer it from absolute self-references |
| `.crt` / cartridge | a header + one or more banked ROM images mapped at `$8000`/`$A000`/`$E000` | Use the CRT header for chip/bank layout; entry via the cold/warm vectors at `$8000` (see below) |
| `.d64` | a disk image — extract the `.prg` files first | Pull files out, then treat each as a `.prg` |
| memory snapshot | full 64K (+ optionally I/O / ROM state) | Use `$00/$01` value to know which banks were live |

A `.prg` whose load address is `$0801` (2049) is almost always a **BASIC**
program (possibly a BASIC stub that `SYS`es into machine code). A load address of
`$0810`, `$C000` (49152), `$1000`, `$2000`, `$0340`, etc. is machine code.

## Step 1 — is there a BASIC stub?

If the load address is `$0801`, decode the tokenized BASIC at the front before
disassembling. BASIC line layout, repeated per line:

```
.word link      ; pointer to the NEXT line ($0000 link = end of program)
.word lineno    ; line number, binary
.byte tokens... ; keywords are single bytes >= $80 (SYS=$9E, PRINT=$99, ...)
.byte $00       ; end-of-line marker
```

The classic launcher is a single line like `10 SYS 2064`. Find the `SYS` token
(`$9E`), the digits after it are PETSCII text — that decimal number is the **entry
point** of the machine code. Common ones: `2061` ($080D), `2064` ($0810),
`49152` ($C000). Disassemble starting there. A one-line stub at `$0801` typically
occupies `$0801`–`$080C`, so code at `$080D`/`$0810` sits right after it.

To read the SYS target fast: dump bytes from `$0801`, skip the 4 link/lineno
bytes, expect `$9E`, then ASCII digits up to `$00`.

## Step 2 — classify every address

As you disassemble, tag each operand address by region. This is the single most
useful pass — it turns opaque `STA $D015` into "enable sprites".

| Range | Meaning | Skill |
|-------|---------|-------|
| `$0000`/`$0001` | 6510 I/O port — **bank switching** & datasette | c64-memory-map |
| `$0002`–`$00FF` | zero page (BASIC/KERNAL vars; `$FB-$FE`,`$22` etc. often "free") | c64-memory-map |
| `$0100`–`$01FF` | stack | c64-assembly |
| `$0200`–`$03FF` | system buffers; **`$0314/$0315`** IRQ vector, **`$0318/$0319`** NMI, `$033C-$03FB` tape buffer | c64-kernal / c64-cia |
| `$0400`–`$07FF` | default screen RAM; sprite pointers at `$07F8-$07FF` | c64-graphics |
| `$0800`–`$9FFF` | BASIC program / general RAM | — |
| `$A000`–`$BFFF` | BASIC ROM (or RAM when banked) — entry points like `$AB1E`, `$BDCD` | c64-kernal |
| `$D000`–`$D3FF` | **VIC-II** (mirrors every $40) | c64-vic-ii |
| `$D400`–`$D7FF` | **SID** | c64-sid |
| `$D800`–`$DBFF` | color RAM (low nibble only) | c64-graphics |
| `$DC00`–`$DCFF` | **CIA1** — keyboard, joysticks, IRQ timer | c64-cia / c64-game-ports |
| `$DD00`–`$DDFF` | **CIA2** — serial bus, user port, **VIC bank**, NMI timer | c64-cia / c64-io |
| `$DE00`–`$DFFF` | expansion I/O 1 / I/O 2 (cartridge registers) | c64-io |
| `$E000`–`$FFFF` | KERNAL ROM (or RAM); jump table `$FF81-$FFF3`; vectors `$FFFA-$FFFF` | c64-kernal |

Whether `$A000`/`$D000`/`$E000` reads hit ROM, RAM, or I/O depends on the live
`$01` value at that moment — see c64-memory-map. Code that `STA $01` mid-stream is
banking; track it.

## Step 3 — recognize ROM calls

`JSR`/`JMP` into `$FFxx` is almost always a KERNAL jump-table call — decode it
immediately. The high-frequency ones:

| Call | Routine | Effect |
|------|---------|--------|
| `JSR $FFD2` | CHROUT | print the char in A |
| `JSR $FFCF` | CHRIN | input a char to A |
| `JSR $FFE4` | GETIN | read keyboard/queue to A (0 = none) |
| `JSR $FFBD`/`$FFBA`/`$FFC0` | SETNAM / SETLFS / OPEN | file setup + open |
| `JSR $FFC6`/`$FFC9`/`$FFCC` | CHKIN / CHKOUT / CLRCHN | redirect I/O |
| `JSR $FFD5`/`$FFD8` | LOAD / SAVE | block load/save |
| `JSR $FFE1` | STOP | test RUN/STOP |
| `JSR $FF9F`/`$FFF0` | SCNKEY / PLOT | scan keyboard / set cursor |

Full table with register I/O: **c64-kernal**. Calls into `$A000-$BFFF` are BASIC
ROM helpers (float math, string output) — see c64-kernal's BASIC-ROM notes.

## Step 4 — read the idioms

C64 machine code has a recognizable vocabulary. Spotting these collapses big
regions into one annotation:

- **Raster wait**: `LDA $D012 / CMP #n / BNE *-5` (or `BNE` back) — busy-wait for
  scanline `n`. Precedes most screen-split / colour-bar effects.
- **IRQ hook**: `SEI`; store a new vector into `$0314/$0315` (KERNAL IRQ) — or,
  after banking ROM out via `$01`, into `$FFFE/$FFFF`; set up a raster IRQ with
  `$D012`/`$D011`/`$D01A`; `CLI`. The handler usually ends `JMP $EA31` (chain to
  KERNAL) or `JMP $EA81` (just restore & RTI). See c64-cia / c64-vic-ii.
- **Disable interrupts / take over**: `SEI` + `LDA #$7F STA $DC0D` (kill CIA1 IRQ)
  + `LDA #$01 STA $D01A` (enable raster IRQ). Signature of a demo/game taking the
  machine.
- **Sprite setup**: writes to `$D015` (enable), `$D000-$D00F`+`$D010` (position),
  `$07F8-$07FF` (pointers). See c64-sprites.
- **VIC bank select**: `LDA $DD00 / AND #$FC / ORA #n / STA $DD00` — chooses which
  16K the VIC sees (bits inverted). See c64-memory-map.
- **Self-modifying code**: a `STA addr` that targets the operand byte of a later
  instruction (e.g. patching the high byte of an absolute address to step through
  pages). Do **not** assume code bytes are constant — flag writes that land inside
  the code region.
- **Copy char ROM / under-ROM RAM**: banking `$01` to `$33`/`$34` then block-copy
  from `$D000` (char ROM) into RAM.

## Step 5 — separate code from data

The hardest part of any disassembly. Heuristics:
- Start from known entry points (the SYS target, IRQ/NMI/RESET vectors at
  `$FFFA/$FFFC/$FFFE`, cartridge `$8000` cold-start vector) and follow control
  flow; only bytes reached by flow are *certainly* code.
- Tables of `.byte`/`.word` referenced by `LDA table,X` are data — sprite
  bitmaps (64-byte aligned), char sets (`$D000`-style 8-byte cells), screen maps,
  SID note tables, colour washes.
- A run of bytes that disassembles into nonsense (long strings of `BRK`/`???`,
  implausible branches) is usually data or a packed/compressed blob.
- **Packed files**: many `.prg`s are crunched (Exomizer, ByteBoozer, pucrunch,
  etc.). Signature: a tiny decruncher at the load address that copies/expands a
  blob then `JMP`s to the real entry. Identify and (if possible) run/unpack the
  decruncher before disassembling the payload.

## Workflow summary

1. Split off the 2-byte load address; note it.
2. If `$0801`, decode the BASIC stub → find the `SYS` entry point.
3. Disassemble from every known entry/vector; mark code vs data as you go.
4. Tag every absolute operand by region (Step 2 table) and resolve `$FFxx`/ROM
   calls (Step 3) and idioms (Step 4) into plain-language annotations.
5. Track `$01` and `$DD00` writes — they change what addresses *mean*.
6. Note self-modifying writes and any decruncher; re-disassemble the real payload.

## References

- **`references/prg-and-vectors.md`** — `.prg`/`.crt` container layout, the BASIC
  stub byte format and SYS-token decoding, and the `$FFFA-$FFFF` /
  `$0314-$0319` vector set. Read it when you need exact byte offsets to parse a
  file header or stub.
- **`references/io-and-rom-cheatsheet.md`** — a one-page address→meaning table for
  the `$D000-$DFFF` I/O space and the top KERNAL/BASIC entry points, for fast
  tagging during a disassembly pass.

For instruction semantics use **c64-assembly**; for the full meaning of any
address use **c64-memory-map**, **c64-kernal**, **c64-vic-ii**, **c64-sid**,
**c64-cia**.
