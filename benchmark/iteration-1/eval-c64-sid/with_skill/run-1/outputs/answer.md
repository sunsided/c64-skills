BASIC. Voice 1 sawtooth, ~1 sec note.

```basic
10 S=54272
20 FOR L=S TO S+24: POKE L,0: NEXT     : REM clear all SID registers
30 POKE S+24,15                        : REM master volume = 15
40 POKE S+5,9                          : REM attack=0 (hi nibble), decay=9 (lo)
50 POKE S+6,240                        : REM sustain=15 (hi), release=0 (lo)
60 POKE S+1,17: POKE S,37              : REM freq HI=17 LO=37 (mid note)
70 POKE S+4,33                         : REM sawtooth (32) + GATE on (1)
80 FOR T=1 TO 900: NEXT                : REM hold ~1 second
90 POKE S+4,32                         : REM GATE off -> release
```

Key points:
- `S+4 = 33` → sawtooth bit (32) + GATE (1).
- `S+5 = 9` → attack nibble 0 (2ms), decay nibble 9. `S+6 = 240` → sustain=15 (full, hi nibble), release=0. Sustain 15 holds tone at peak while gate on.
- Line 80 hold-loop ~1s wall time. BASIC loop speed varies; bump count up/down to tune.
- Line 90 clears GATE → RELEASE phase. Release=0 = fast cutoff. Want soft tail? set `S+6,249` (sustain 15, release 9 ≈ 750ms) and shorten hold loop.

Assembly equivalent:

```asm
        LDA #$0F : STA $D418      ; master volume 15
        LDA #$09 : STA $D405      ; attack 0 / decay 9
        LDA #$F0 : STA $D406      ; sustain 15 / release 0
        LDA #$25 : STA $D400      ; freq lo  (37)
        LDA #$11 : STA $D401      ; freq hi  (17)
        LDA #$21 : STA $D404      ; sawtooth + GATE on  (%00100001)
        ; ~1s delay (e.g. nested loops / raster count)
        LDA #$20 : STA $D404      ; GATE off -> release
```

Gate edge (S+4 / $D404) most common silent-SID bug — must toggle on then off.