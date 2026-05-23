## SETLFS — $FFBA (65466)

Sets logical file number, device, secondary address. Call before OPEN.

**Inputs:**
| Reg | Holds |
|-----|-------|
| A | logical file number (1–255) |
| X | device number (0=keyboard, 1=tape, 2=RS232, 3=screen, 4–7=printer/plotter, 8–11=disk) |
| Y | secondary address (command). $FF / 255 = none |

**Returns:** nothing. No output regs. Stores values to `$B8` (LA, logical file), `$BA` (FA, device), `$B9` (SA, secondary).

## GETIN — $FFE4 (65508)

Get one char from current input channel. Default = keyboard buffer. Use CHKIN ($FFC6) first to switch input to opened file.

**Inputs:** none in regs. Channel set prior (default keyboard).

**Returns:**
| Reg/flag | Holds |
|----------|-------|
| A | PETSCII byte read. **Keyboard: A=0 if buffer empty** (non-blocking — pulls from queue `$0277`, count `$C6`) |
| Carry | set = error (RS232/serial paths). Keyboard: carry clear |

**Caveat:** X and Y destroyed for serial/RS232/tape. Keyboard path also corrupts X,Y on some ROM revs — save them if needed.

## Runnable: open disk file, read byte

```asm
; SETLFS: file#1, device 8, secondary 2
        LDA #$01        ; logical file number
        LDX #$08        ; device 8 (disk)
        LDY #$02        ; secondary addr
        JSR $FFBA       ; SETLFS
        ; ... SETNAM + OPEN + CHKIN here ...
loop    JSR $FFE4       ; GETIN -> A
        ; (use A)
        JMP loop
```

## Runnable: poll keyboard (BASIC)

```basic
10 GET A$: IF A$="" THEN 10
20 PRINT ASC(A$)
```
`GET` is the BASIC wrapper over GETIN; empty string = A returned 0.

Wait one keypress in asm:
```asm
wait    JSR $FFE4       ; GETIN
        BEQ wait        ; A=0 -> no key, loop
        ; A = key PETSCII
```