**SETLFS — $FFBA**

Inputs:
- A = logical file number (1–255)
- X = device number (0 keyboard, 1 tape, 2 RS-232, 3 screen, 4–7 printer/serial, 8+ disk)
- Y = secondary address (command/channel; $FF = none)

Returns: nothing. No carry error. Stores params for next OPEN.

```asm
        LDA #1             ; logical file 1
        LDX #8             ; device 8 (disk)
        LDY #2             ; secondary address 2
        JSR $FFBA          ; SETLFS
```

**GETIN — $FFE4**

Inputs: none (preparatory: keyboard is default, so no CHKIN needed for keyboard).

Returns:
- A = PETSCII char from keyboard queue, or **A=0 if queue empty** (non-blocking — does not wait).
- X, Y corrupted.

```asm
loop    JSR $FFE4          ; GETIN
        BEQ loop           ; A=0 => no key yet, poll again
        ; A now holds the key
```

Note: GETIN on keyboard returns 0 when empty; on other (serial/RS-232) channels it returns a byte and you poll READST ($FFB7) for status. Keyboard queue max 10 chars at $0277.

BASIC: `POKE 781,8 : POKE 782,2 : POKE 780,1 : SYS 65466` (SETLFS, A/X/Y via 780/781/782).