## SID combined-waveform noise lockup

**What happens.** SID combines selected waveforms by digital **AND** of the waveform generator outputs. Noise (bit 7) taps 8 bits off the 23-bit LFSR. AND with pulse/saw/tri pulls those tapped bits to 0. Those zeros feed back into the LFSR as it shifts → register progressively fills with zeros → LFSR = all-0. XOR feedback on all-0 stays 0 forever. Result: noise generator **stuck, output silent/DC** until reseeded. Not a crash — just dead noise channel.

**Control register addresses** (one per voice):

| Voice | Addr | Hex |
|---|---|---|
| 1 | 54276 | $D404 |
| 2 | 54283 | $D40B |
| 3 | 54290 | $D412 |

**Control bits** (value to combine = OR them):

| Bit | Val | Function |
|---|---|---|
| 0 | $01 | Gate |
| 1 | $02 | Sync |
| 2 | $04 | Ring mod |
| 3 | $08 | **Test** |
| 4 | $10 | Triangle |
| 5 | $20 | Sawtooth |
| 6 | $40 | Pulse |
| 7 | $80 | Noise |

Noise+pulse = $C0 = 192. That combo triggers lockup.

**How to recover.** Reseed the LFSR. Two ways: set **TEST bit** ($08), or full SID reset. Setting TEST resets the oscillator and reloads the shift register with non-zero bits; clearing TEST lets noise run clean again.

BASIC — reseed voice 1:
```basic
10 POKE 54276,8 : REM set TEST bit, reseeds LFSR
20 POKE 54276,0 : REM clear (gate off — sound stops)
```

Keep noise playing after reseed (noise+gate = $81 = 129):
```basic
10 POKE 54276,8   : REM TEST, reseed
20 POKE 54276,129 : REM noise + gate, clean single waveform
```

Assembly — voice 1:
```asm
        LDA #$08        ; TEST bit only -> reseed noise LFSR
        STA $D404
        LDA #$81        ; noise + gate, single waveform = no lockup
        STA $D404
```

Full SID reset (clears all 29 regs $D400–$D41C, unlocks all voices):
```asm
        LDX #$1C
        LDA #$00
loop    STA $D400,X
        DEX
        BPL loop
```

**Avoid it:** never leave noise (bit 7) set together with tri/saw/pulse. Use noise alone ($80/$81). If you must morph, switch waveforms via separate POKEs, not overlapping noise.

Note: 8580 (newer SID) less prone, 6581 locks reliably. Lockup speed depends on frequency — higher freq, faster zero-fill.