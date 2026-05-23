---
name: c64-tape
description: >-
  The Commodore 64 Datassette / cassette tape: device 1, LOAD/SAVE/VERIFY, how
  tape files are found (sequential, no random-access directory), the tape buffer,
  headers, and the PRESS PLAY/RECORD prompts. Use this skill WHEN a user asks
  "how do I load/save from tape", "LOAD with no name", "how do I list a tape
  directory", "what's on this cassette", "why does it say PRESS PLAY ON TAPE",
  "what is the tape buffer at $033C", "how do I write data files to tape", or
  mentions the Datassette, device 1, or .tap/.t64 files. Pairs with c64-io,
  c64-kernal, and c64-assembly.
---

# C64 Cassette Tape (Datassette)

The Datassette is serial device **1**, and it's the **default** for LOAD/SAVE
when you give no device number. Tape is *sequential* magnetic storage: files sit
one after another along the tape and you reach a file by spooling past everything
before it. There is no in-place rewrite and **no random-access directory** — that
distinction drives almost everything below.

## Loading, saving, verifying programs

```basic
LOAD             : REM load the NEXT program on the tape (from current position)
LOAD "NAME"      : REM search FORWARD for program "NAME", then load it
LOAD "NAME",1    : REM same, device 1 explicit
LOAD "",1,1      : REM first program on tape, loaded to its ORIGINAL address
SAVE "NAME"      : REM save current BASIC program to tape
SAVE "NAME",1,2  : REM save and write an end-of-tape (EOT) marker after it
VERIFY "NAME"    : REM compare the tape file against memory
```

- `LOAD` with **no name** reads whatever program comes next from where the tape is
  parked. `LOAD"NAME"` scans forward until it finds a header matching `NAME`.
- The secondary address on LOAD works like disk: `,1,1` loads to the address the
  program was saved from (for ML/data), versus the default relocate to BASIC
  start. On SAVE, sa `2` appends an EOT marker so a later read stops cleanly.
- Prompts the KERNAL prints: **PRESS PLAY ON TAPE** (for read), **PRESS RECORD &
  PLAY ON TAPE** (for write). On LOAD the screen blanks to the border color while
  searching; on a hit it shows **FOUND NAME**, clears, and (after you press C=,
  CTRL, ←, or SPACE — or it just continues) shows **LOADING**.

## There is NO tape directory

A cassette has no catalog the way a disk does. `LOAD"$",8` works on disk because
the drive's DOS builds a directory; **the Datassette has no DOS and `$` means
nothing on tape.** So the honest answer to "list a tape directory" is: you can't,
not as a single listing. Practical alternatives the manuals describe:

1. **Use the tape counter + your own log.** Note the counter value where each
   file begins (the manuals assume you write down what's on each tape).
2. **Walk the headers.** Each file is preceded by a header containing its name.
   `LOAD"NAME"` searches these headers forward; repeatedly issuing `LOAD` (no
   name) and watching each **FOUND xxxx** message lets you see file names one by
   one as the tape advances. There's no way to jump backward to an earlier file
   without rewinding.
3. **EOT markers** (written with SAVE sa 2) tell a sequential read when to stop,
   so you don't run off the end into `?DEVICE NOT PRESENT`.

Because tape is sequential, the common workflow is: read the whole file into RAM,
process it, then rewrite the whole file — there's no editing in place.

## Data files on tape

For your own data (not programs), use OPEN/PRINT#/INPUT#/GET#:

```basic
OPEN 1,1,0,"NAME"   : REM sa 0 = read
OPEN 1,1,1,"NAME"   : REM sa 1 = write
OPEN 1,1,2,"NAME"   : REM sa 2 = write, and write an EOT marker on CLOSE
```

The **secondary address picks the mode**: 0 read, 1 write, 2 write-with-EOT.
Worked write/read pair (from the User's Guide):

```basic
10 OPEN 1,1,1,"DATA FILE"           20 OPEN 1,1,0,"DATA FILE"
20 INPUT "DATA";A$                  50 INPUT#1,A$
30 PRINT#1,A$                       60 PRINT A$
40 IF A$<>"STOP" THEN 20            70 IF A$<>"STOP" THEN 50
50 CLOSE 1                          80 CLOSE 1
```

**Separator pitfall:** `PRINT#1,A$,B$,C$` with commas adds 1–10 padding spaces
(like screen columns), and `INPUT#1,A$,B$,C$` then reads all three into A$ because
there's no separator between them — only a RETURN after the last. Put a RETURN
(`CHR$(13)`) or comma *between* items: `R$=",":PRINT#1,A$ R$ B$ R$ C$`. Also,
`GET#` returns `CHR$(0)` as an empty string `""`, so `ASC(A$)` on it errors — use
`A=ASC(A$+CHR$(0))`. Read `references/cassette-tape.md` for the full DOG/CAT/TREE
illustration; check the reserved variable **ST** for tape markers / end of file.

## The tape buffer

The cassette I/O buffer is **$033C–$03FB** (828–1019 decimal), 192 bytes. It holds
the header and a data block during tape operations. When you're not using tape it
is a favorite spot for short machine-language routines — but it will be
overwritten the moment any tape I/O runs. For loading/parking ML there, see
**c64-assembly**.

## Cassette port pins (edge connector)

| Pin | Signal |
|-----|--------|
| A-1 | GND |
| B-2 | +5V |
| C-3 | CASSETTE MOTOR |
| D-4 | CASSETTE READ |
| E-5 | CASSETTE WRITE |
| F-6 | CASSETTE SENSE (PLAY/RECORD pressed) |

## Quick answers

- **"How do I list a tape directory?"** You can't — tape has no directory. Use
  the tape counter, your own written log, or step through with repeated `LOAD`
  (no name) watching each `FOUND name` message.
- **"What does LOAD with no name do?"** Loads the next program on the tape.
- **"How do I save to tape?"** `SAVE "NAME"` (device 1 is the default).
- **"Why PRESS PLAY ON TAPE?"** The KERNAL is waiting on the SENSE line; press the
  Datassette's PLAY (or RECORD+PLAY for writing).
- **"Where's the tape buffer?"** $033C–$03FB.

## How to read the references

- **`references/cassette-tape.md`** — verbatim PRG Ch6 "Working With Cassette
  Tape" (the PRINT#/INPUT# separator problem with the DOG/CAT/TREE byte layout,
  the GET#/CHR$(0) trap) plus the tape-relevant slices of the LOAD and OPEN
  keyword entries (the FOUND/PRESS PLAY behavior, the sa 0/1/2 read/write/EOT
  rules). Read this for the exact wording on file formatting and load behavior.
- **`references/advanced-cassette.md`** — verbatim User's Guide App B with the
  complete write-to-tape and read-from-tape data-file programs and the GET#
  variant. Read this for runnable data-file examples.

## Cross-links

- The general device/file model (OPEN/PRINT#/INPUT#/GET#/CLOSE, device numbers,
  secondary addresses) → **c64-io**
- KERNAL LOAD/SAVE/tape routines → **c64-kernal**
- Stashing machine-language code in the tape buffer at $033C → **c64-assembly**
