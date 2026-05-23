Routine fill 1000-byte screen RAM at `$0400`. Char 81 = `$51`. Classic 4×256 loop.

## Assembly

```asm
        *=$C000
        LDA #$51        ; 81 = ball (filled circle) screen code
        LDX #$00
loop    STA $0400,X     ; screen page 0  ($0400-$04FF)
        STA $0500,X     ; page 1
        STA $0600,X     ; page 2
        STA $0700,X     ; page 3
        INX
        BNE loop        ; 256 iterations, X wraps to 0
        RTS             ; back to BASIC (SYS = JSR)
```

20 bytes. Note: loop writes `$0400-$07FF` = 1024 bytes, but screen only 1000 (`$0400-$07E7`). Extra 24 bytes hit `$07E8-$07FF`, which include sprite pointers `$07F8-$07FF`. Harmless for plain text display. Want exact 1000? See below.

## Enter + call (BASIC DATA loader)

```basic
10 FOR I=0 TO 19 : READ B : POKE 49152+I,B : NEXT
20 DATA 169,81,162,0,157,0,4,157,0,5,157,0,6,157,0,7,232,208,241,96
30 SYS 49152
```

`RUN` pokes the 20 machine code bytes into `$C000` then `SYS 49152` runs them. Screen fills with balls instantly. Re-run anytime with bare `SYS 49152`.

Byte breakdown (matches DATA):

```
C000  A9 51       LDA #$51
C002  A2 00       LDX #$00
C004  9D 00 04    STA $0400,X
C007  9D 00 05    STA $0500,X
C00A  9D 00 06    STA $0600,X
C00D  9D 00 07    STA $0700,X
C010  E8          INX
C011  D0 F1       BNE $C004
C013  60          RTS
```

## Notes

- Color unchanged. Balls use whatever color RAM (`$D800-$DBE7`) already holds — default light-blue on blue. Want them all one color too? Add a second loop storing color to `$D800,X`/`$D900,X`/`$DA00,X`/`$DB00,X`.
- Exact-1000 version (no sprite-pointer clobber): drop page 3, fill `$0400/$0500/$0600` with full 256, then `$0700,X` only while `X < 232` (`$E8`). More code; the 4-page loop is the standard idiom and the overwrite is benign unless using sprites.
- `81` poked = screen code, not PETSCII. Screen code 81 = ball. (PETSCII 81 = "Q".)