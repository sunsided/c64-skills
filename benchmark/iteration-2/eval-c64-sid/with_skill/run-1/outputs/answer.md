From SID Table 2 (envelope rates):

- Attack rate **11 ($B)** → **800 ms**
- Decay/Release rate **11 ($B)** → **2.4 s** (2400 ms)
- Attack rate **0** → **2 ms**
- Decay/Release rate **0** → **6 ms**

Registers: attack/decay = `$D405` (S+5), sustain/release = `$D406` (S+6). Hi nibble = attack (or sustain), lo nibble = decay (or release).

Attack 11 + decay 11 → nibble `$BB = 187`. Decay/release share same time column, so release 11 also = 2.4 s.

BASIC:
```basic
10 S=54272
20 POKE S+5,11*16+11 : REM attack=11(800ms) decay=11(2.4s) -> 187
30 POKE S+6,0*16+11  : REM sustain=0 release=11(2.4s)
```

Asm:
```asm
        LDA #$BB : STA $D405      ; attack 11 / decay 11
        LDA #$0B : STA $D406      ; sustain 0 / release 11
```

Note: write-only regs, no PEEK. Sustain is level (0–15), not time.