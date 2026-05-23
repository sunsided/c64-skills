CHROUT = `$FFD2`. A holds PETSCII char. Two calls, one per char.

```asm
        LDA #$48        ; 'H'  (PETSCII 72)
        JSR $FFD2       ; CHROUT — output A to screen (default channel)
        LDA #$49        ; 'I'  (PETSCII 73)
        JSR $FFD2       ; CHROUT
        RTS
```

Register: **A = char to print**. No SETLFS/OPEN/CHKOUT needed — default output channel is screen (device 3) at startup.

Note: `#'H` literal works in many assemblers; raw bytes `$48`/`$49` shown for clarity. PETSCII uppercase letters match ASCII here.