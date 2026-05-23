---
name: c64-disk
description: >-
  Using a Commodore disk drive (1541 and family) from the Commodore 64: device
  8, LOAD/SAVE, listing the directory, the command channel (channel 15) for DOS
  commands (NEW/format, SCRATCH, RENAME, COPY, INITIALIZE, VALIDATE), reading the
  error/status channel, and file types (PRG/SEQ/REL/USR). Use this skill WHEN a
  user asks "how do I show a disk directory", "LOAD a program from disk",
  "what's the difference between LOAD\"NAME\",8 and ,8,1", "how do I format/scratch/
  rename a disk file", "what is OPEN 15,8,15", "how do I read the disk error
  channel", or mentions device 8, the 1541, or a .d64. Pairs with c64-io,
  c64-tape, and c64-kernal.
---

# C64 Disk Drives (1541 and family)

The disk drive is serial-bus **device 8** (8–11 for multiple drives). It is an
*intelligent* peripheral with its own 6502 and DOS, so the C64 talks to it with
high-level commands rather than driving the medium directly. Two things you do
constantly: read/write program and data files, and send DOS commands down the
**command channel**.

> Honesty note: the Commodore 64 Programmer's Reference and User's Guide are
> thin on 1541 internals. They cover LOAD/SAVE, sequential files, and point you
> at the *disk drive manual* for DOS specifics. Track/sector layout, GCR
> encoding, BAM, and the full DOS command syntax are **not** in these manuals —
> the command syntax below is the well-known standard 1541 DOS set, included so
> the skill is useful, but for authoritative detail use the 1541 User's Manual /
> "Inside Commodore DOS".

## Loading and saving programs

```basic
LOAD "NAME",8        : REM load a BASIC/PRG file (relocates to BASIC start, $0801)
LOAD "NAME",8,1      : REM load to the address it was SAVEd from (ML, data, hi-res)
SAVE "NAME",8        : REM save the current BASIC program
VERIFY "NAME",8      : REM compare disk file against memory
LOAD "*",8           : REM load the first file in the directory
LOAD "PART*",8       : REM pattern match: first file starting "PART"
```

The **secondary address is the load-vs-relocate switch**, and it's the single
most common confusion:
- `,8` (sa 0, the default) → BASIC **relocates** the program to the start of
  BASIC ($0801). Use for BASIC programs.
- `,8,1` (sa 1) → loads to the **original address** the file was saved from. Use
  for machine-language routines, sprite/character data, hi-res screens — anything
  that must land at a fixed address.

A missing or non-program file gives `?FILE NOT FOUND`. SAVE over an existing name
fails on disk (`FILE EXISTS`) — see SCRATCH below.

## How do I show a disk directory?

The directory is itself a (pseudo) PROGRAM file named `$`:

```basic
LOAD "$",8           (then)   LIST
```

`LOAD"$",8` reads the directory into memory **as if it were a BASIC program**,
overwriting whatever program you had; `LIST` then displays it. Each "line number"
is the file's block count; the text is the filename and type. To peek at a subset
use a pattern, e.g. `LOAD"$0:A*",8` then `LIST`. To list the directory *without*
clobbering your program, read it through a channel with GET#:

```basic
10 OPEN 1,8,0,"$"
20 GET#1,A$,B$           : REM skip load address
30 GET#1,A$,B$           : REM line-link / block low/high
40 ...                    : REM read & print each entry, then CLOSE 1
```

(The full byte-walk is fiddly; the simple `LOAD"$",8 : LIST` is what most users
want.)

## The command channel (channel 15) — DOS commands

Open secondary address **15** to talk to the drive's DOS. Send commands with
PRINT#; read results/errors with INPUT#.

```basic
OPEN 15,8,15                 : REM open the command channel
PRINT#15,"<command>"
INPUT#15,EN,EM$,ET,ES        : REM read error channel: number, message, track, sector
CLOSE 15
```

Standard 1541 DOS commands (sent as the PRINT# string):

| Command | String | Effect |
|---------|--------|--------|
| NEW (format) | `"N0:label,id"` | format the disk: name `label`, 2-char `id`. `"N0:label"` (no id) does a quick clear of an already-formatted disk |
| SCRATCH (delete) | `"S0:name"` | delete file(s); pattern allowed (`S0:TEMP*`) |
| RENAME | `"R0:new=old"` | rename `old` to `new` |
| COPY | `"C0:new=0:old"` | copy a file on the same disk |
| INITIALIZE | `"I0"` | re-read the BAM / reset the drive |
| VALIDATE | `"V0"` | reclaim free blocks, fix the BAM (like a "collect") |

The `0:` is the drive number within the unit (always 0 on a single-drive 1541).
You can also abbreviate the open: `OPEN 15,8,15,"N0:GAMES,01"` formats at OPEN time.

## Reading the error/status channel

After any DOS operation, read channel 15 to find out what happened. A reset/OK
status is **00, OK, 00, 00**. The drive light blinking means an uncleared error.

```basic
10 OPEN 15,8,15
20 PRINT#15,"S0:OLDFILE"
30 INPUT#15,EN,EM$,ET,ES
40 PRINT EN;EM$;ET;ES        : REM e.g.  62 FILE NOT FOUND 00 00
50 CLOSE 15
```

`EN` = error number, `EM$` = message text, `ET`/`ES` = track/sector. Reading the
channel also clears the error and stops the blinking light.

## Sequential data files

For your own data (not programs), use a data channel (sa 2–14) with a file type
and mode in the name:

```basic
OPEN 2,8,2,"NAME,S,W"   : REM open SEQ file for Write
PRINT#2,"DATA";CHR$(13);"MORE"
CLOSE 2
OPEN 2,8,2,"NAME,S,R"   : REM re-open for Read
INPUT#2,A$
CLOSE 2
```

Separator pitfall (same as tape): `PRINT#` to disk needs RETURN (`CHR$(13)`) or
comma between items, or `INPUT#` reads them back as one merged string. See
**c64-tape** for the worked DOG/CAT/TREE example — the formatting rules are
identical.

## File types

| Type | In name | Meaning |
|------|---------|---------|
| PRG | `,P` | program (BASIC or ML); the default for LOAD/SAVE |
| SEQ | `,S` | sequential data file (read start-to-end, like tape) |
| REL | `,L` / `REL` | relative file: fixed-length records, random access by record # |
| USR | `,U` | user file (rare; app-defined) |

Relative and random files use a separate data channel and command channel; the
PRG manual leaves the REL record protocol to the disk drive manual.

## Quick answers

- **"How do I list a disk directory?"** `LOAD"$",8` then `LIST`.
- **"LOAD\"NAME\",8 vs ,8,1?"** `,8` relocates to BASIC start; `,8,1` loads to the
  saved address (use for ML/data).
- **"How do I delete a file?"** `OPEN 15,8,15: PRINT#15,"S0:NAME": CLOSE 15`.
- **"How do I format a disk?"** `OPEN 15,8,15,"N0:MYDISK,42": CLOSE 15`.
- **"Why is the drive light blinking?"** An error is set — read channel 15 with
  `INPUT#15,EN,EM$,ET,ES` to see and clear it.

## How to read the references

- **`references/disk-storage.md`** — the verbatim PRG Ch6 "Data Storage on Floppy
  Diskettes" text (sequential/relative/random files, the data+command channel
  concept) plus the disk-relevant slices of the LOAD and OPEN keyword entries
  (secondary-address rules, file type/mode syntax, error conditions). Read this
  for the exact wording on relocation, channels, and OPEN syntax.

## Cross-links

- The general device/file model and the serial bus the drive sits on → **c64-io**
- KERNAL LOAD/SAVE routines (LOAD $FFD5, SAVE $FFD8, SETLFS, SETNAM) → **c64-kernal**
- Cassette storage and the shared PRINT#/INPUT# separator rules → **c64-tape**
