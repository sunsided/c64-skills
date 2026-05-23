**Noise + other waveform = noise locks silent.** SID ANDs waveform outputs together. When NOISE (bit7) combined with PULSE/SAW/TRI, the AND feeds back into noise shift register, clearing its bits to 0. Register empties → noise output stuck at 0 (silence). Permanent until reset, even after you reselect noise alone.

Voice 1 control = `$D404` (54276). Voice 2 `$D40B`, voice 3 `$D412`.

**Recovery: pulse the TEST bit (bit3, value 8).** TEST resets the oscillator and reloads the shift register with bits, unlocking noise.

BASIC (voice 1):
```basic
10 S=54272
20 POKE S+4,8        : REM TEST bit on -> reset/reload shift register
30 POKE S+4,0        : REM TEST off
40 POKE S+4,129      : REM noise (128) + gate (1), clean again
```

Assembly:
```asm
        LDA #$08 : STA $D404      ; TEST on  -> reload noise shift reg
        LDA #$00 : STA $D404      ; TEST off
        LDA #$81 : STA $D404      ; NOISE (128) + GATE (1)
```

**Avoid it:** pick one waveform bit + GATE. Noise alone on = `128+1 = 129`. Never set noise bit alongside pulse/saw/tri.

Note: gate off (`$D404` bit0=0) does not refill the register — only TEST bit reload (or full SID reset) recovers it.