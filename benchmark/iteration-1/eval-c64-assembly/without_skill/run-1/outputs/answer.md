Screen RAM `$0400`–`$07E7` = 1000 bytes. Char code 81 = ◯ ball (screen code, POKE-direct). Routine at `$C000` (49152).

## Assembly

```asm
        *=$C000          ; 49152
        LDA #$51         ; 81 = ball (screen code)
        LDX #$00
fill    STA $0400,X      ; screen page 0
        STA $0500,X      ; page 1
        STA $0600,X      ; page 2
        INX
        BNE fill         ; 3*256 = 768 bytes done
        LDX #$00
fill2   STA $0700,X      ; page 3, partial
        INX
        CPX #$E8         ; stop at 232 -> $0700..$07E7
        BNE fill2
        RTS              ; back to BASIC
```

Fills exactly 1000 bytes. No overshoot into sprite pointers (`$07F8`).

## Enter from BASIC (POKE loader)

```basic
10 FOR I=0 TO 26
20 READ B : POKE 49152+I,B
30 NEXT I
40 DATA 169,81,162,0,157,0,4,157,0,5
50 DATA 157,0,6,232,208,244,162,0,157,0
60 DATA 7,232,224,232,208,248,96
```

Raw bytes (`$C000`, 27 total):
```
A9 51 A2 00 9D 00 04 9D 00 05 9D 00 06 E8 D0 F4
A2 00 9D 00 07 E8 E0 E8 D0 F8 60
```

## Call

```basic
RUN
SYS 49152
```

Whole screen fill ball. Note: balls show in color held by color RAM `$D800`–`$DBE7` — after screen clear that's cursor color (default 14, light blue) on blue bg, so visible. Want set color too? add `STA $D800,X` etc. block (same loop shape) and `LDA #14` first.