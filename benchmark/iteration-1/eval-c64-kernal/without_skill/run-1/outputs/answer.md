KERNAL `CHROUT` = `$FFD2`. Char in **A**. Print, repeat for each char.

```asm
        LDA #72      ; 'H' PETSCII
        JSR $FFD2    ; CHROUT - prints char in A
        LDA #73      ; 'I'
        JSR $FFD2
        RTS
```

Registers:
- **A** — char code to print (`$FFD2` reads it from A).
- X, Y — untouched by your code; CHROUT may clobber them internally but caller need not set.

Notes:
- `$FFD2` prints to current output device (screen by default).
- PETSCII uppercase: H=72 ($48), I=73 ($49) — same as ASCII for letters.
- CHROUT preserves A on return; advances cursor.