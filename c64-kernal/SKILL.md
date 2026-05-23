---
name: c64-kernal
description: >-
  The Commodore 64 KERNAL ROM jump table and its user-callable routines: the
  fixed $FFxx entry points, each routine's purpose and register inputs/outputs,
  the carry-flag error convention and error codes, and the power-up sequence. Use
  this skill WHEN calling C64 OS routines from assembly: "print a character in
  6510", "address of CHROUT/CHRIN/GETIN", "open a file with SETLFS and SETNAM",
  "the KERNAL I/O pattern", "what does set carry mean after a KERNAL call", "read
  the jiffy clock with RDTIM", "scan the STOP key". Pairs with c64-assembly,
  c64-memory-map, c64-io, c64-disk, and c64-tape.
---

# C64 KERNAL ROM Routines

The KERNAL is the C64 operating system. Its user-callable routines are reached
through a **fixed jump table at the top of the KERNAL ROM ($FF81-$FFF5)**. Each
`$FFxx` address is a `JMP` to the real (version-specific) routine deeper in ROM.

**Always call the `$FFxx` jump-table entry, never the actual ROM address.** The
jump-table addresses are guaranteed stable across KERNAL revisions; the internal
routine addresses are not. This indirection is the whole point of the KERNAL.

```asm
        JSR $FFD2          ; CHROUT — correct, version-proof
        ; JSR $E716        ; the real routine — DON'T; moves between ROM versions
```

## Most-used routines

| Name   | Addr   | Purpose | Registers (in → out) |
|--------|--------|---------|----------------------|
| SETLFS | $FFBA | Set logical file #, device #, secondary addr | A=lfn, X=dev, Y=sec |
| SETNAM | $FFBD | Set filename | A=len, X/Y=name ptr (lo/hi) |
| OPEN   | $FFC0 | Open a logical file | (after SETLFS+SETNAM); C/A=err |
| CLOSE  | $FFC3 | Close a logical file | A=lfn |
| CHKIN  | $FFC6 | Set an open file as input channel | X=lfn; C/A=err |
| CHKOUT | $FFC9 | Set an open file as output channel | X=lfn; C/A=err |
| CLRCHN | $FFCC | Restore default I/O channels | — |
| CHRIN  | $FFCF | Input a char from current input channel | → A |
| CHROUT | $FFD2 | Output the char in A to current output channel | A=char |
| LOAD   | $FFD5 | Load/verify RAM from device | A=0 load/1 verify, X/Y=addr; C/A=err |
| SAVE   | $FFD8 | Save RAM to device | A=zp ptr to start, X/Y=end; C/A=err |
| GETIN  | $FFE4 | Get a char from the keyboard queue (0 if none) | → A |
| CLALL  | $FFE7 | Close all files & channels | — |
| CHKIN/CHKOUT/CLRCHN | (above) | channel management | |
| PLOT   | $FFF0 | Read (C=1) / set (C=0) cursor X,Y | X=row, Y=col |
| SCNKEY | $FF9F | Scan the keyboard once | — |
| RDTIM  | $FFDE | Read the jiffy clock (1/60 s) | → A/X/Y |
| SETTIM | $FFDB | Set the jiffy clock | A/X/Y |
| STOP   | $FFE1 | Test the STOP key (Z=1 if pressed) | → Z, A |
| READST | $FFB7 | Read the I/O status word ST | → A |
| ACPTR  | $FFA5 | Input a byte from the serial (IEC) bus | → A |
| CIOUT  | $FFA8 | Output a byte to the serial bus | A=byte |
| TALK/LISTEN | $FFB4/$FFB1 | Command a serial device to talk/listen | A=dev |
| UNTLK/UNLSN | $FFAB/$FFAE | Untalk / unlisten the serial bus | — |
| SECOND/TKSA | $FF93/$FF96 | Send secondary address after LISTEN/TALK | A=sec |
| MEMTOP | $FF99 | Read (C=1) / set (C=0) top of memory | X/Y |
| MEMBOT | $FF9C | Read/set bottom of memory | X/Y |
| VECTOR | $FF8D | Read/set the RAM I/O vector table | C, X/Y=ptr |
| RESTOR | $FF8A | Restore default system & I/O vectors | — |

The full per-routine reference (purpose, communication registers, preparatory
routines, error returns, stack use, registers affected, description, example) is
in `references/kernal-routines.md`.

## Worked I/O example: print a character

```asm
        LDA #'H            ; PETSCII code of the character
        JSR $FFD2          ; CHROUT — to current output (default = screen)
```

## The standard file-I/O pattern

To talk to a device (disk, printer, tape), the canonical sequence is:
**SETNAM → SETLFS → OPEN → CHKIN/CHKOUT → CHRIN/CHROUT → CLRCHN → CLOSE.**

```asm
        ; OPEN 1,8,2,"FILENAME"  then write a byte, then close
        LDA #fnamelen
        LDX #<fname
        LDY #>fname
        JSR $FFBD          ; SETNAM
        LDA #1             ; logical file 1
        LDX #8             ; device 8 (disk)
        LDY #2             ; secondary address 2
        JSR $FFBA          ; SETLFS
        JSR $FFC0          ; OPEN
        LDX #1             ; logical file 1
        JSR $FFC9          ; CHKOUT — make it the output channel
        LDA #'X
        JSR $FFD2          ; CHROUT — send a byte
        JSR $FFCC          ; CLRCHN — restore default channels
        LDA #1
        JSR $FFC3          ; CLOSE
        RTS
```

Reading is symmetric: use `CHKIN` then `CHRIN`, checking `READST` ($FFB7) for
end-of-file/error after each byte. Device numbers: 0 keyboard, 1 tape, 2 RS-232,
3 screen, 4-7 printers/serial, 8+ disk drives. For the device-side usage of this
pattern see **c64-io**, **c64-disk**, **c64-tape**.

## Error convention

After a KERNAL call, **carry set (C=1) means error**, and the accumulator holds
the error code:

| Code | Meaning |
|------|---------|
| 0 | Routine terminated by the STOP key |
| 1 | Too many open files |
| 2 | File already open |
| 3 | File not open |
| 4 | File not found |
| 5 | Device not present |
| 6 | File is not an input file |
| 7 | File is not an output file |
| 8 | File name is missing |
| 9 | Illegal device number |
| 240 | Top-of-memory change (RS-232 buffer alloc/dealloc) |

```asm
        JSR $FFC0          ; OPEN
        BCS error          ; carry set => A = error code above
```

Some I/O routines (CHRIN/CHROUT/serial) do **not** return these codes — instead
you must poll `READST` ($FFB7) for the ST status word (bit 6 = EOF, bit 7 =
device-not-present/timeout, etc.). See `references/kernal-error-codes.md`.

## Power-up sequence (what runs at reset)

On reset the KERNAL: tests/sizes RAM and sets the tape buffer & screen via
RAMTAS; sets up the I/O devices and CIA timers via IOINIT; initializes the RAM
I/O vectors via RESTOR; sets the screen editor via CINT; then hands off (the
BASIC ROM cold-start). Full detail in `references/kernal-routines.md`
("KERNAL Power-Up Activities").

## Calling KERNAL from BASIC

You can drive these from BASIC with SYS plus the register-pass locations:
`POKE 780,A : POKE 781,X : POKE 782,Y : SYS addr`. See **c64-assembly** for the
SYS/USR convention and the $030C-$030F register locations.

## Gotchas

- Call the `$FFxx` vector, not the internal ROM routine.
- The KERNAL ROM must be banked in (HIRAM=1 at `$0001`) to reach `$FFxx`. If you
  bank it out for RAM, you lose the jump table — see **c64-memory-map**.
- CHROUT to the serial bus sends to **all** open serial output channels; CLRCHN
  or close the others first.
- Many routines need preparatory calls (OPEN needs SETLFS+SETNAM first); check
  the "Preparatory routines" line in each entry.
- SAVE takes a **zero-page pointer in A** to the start address (not X/Y), with
  X/Y holding the end address.

## How to read the references

- **`references/kernal-routines.md`** — the complete routine-by-routine
  reference (PRG Ch5): "The KERNAL", the power-up activities, "How to Use the
  KERNAL", and every User Callable routine with call address, communication
  registers, preparatory routines, error returns, stack use, registers affected,
  description, and an assembly example. Read for the exact contract of any
  routine.
- **`references/kernal-error-codes.md`** — the carry-flag error convention and
  the numbered error-code table. Read when interpreting a failed KERNAL call.

For the calling convention from BASIC/ML see **c64-assembly**; for where these
addresses sit and how to keep the KERNAL banked in see **c64-memory-map**; for
real file/device workflows see **c64-io**, **c64-disk**, **c64-tape**.
