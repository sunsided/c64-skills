**PAL 6569:** 63 cycles/raster line, 312 raster lines/frame.
- Frame total: 63 × 312 = **19656 cycles**
- Dot clock 7.881984 MHz, CPU 0.985248 MHz → ~50.12 Hz refresh.

**NTSC 6567R8:** 65 cycles/raster line, 263 raster lines/frame.
- Frame total: 65 × 263 = **17095 cycles**
- Dot clock 8.181816 MHz, CPU 1.022727 MHz → ~59.83 Hz refresh.

Note: old NTSC **6567R56A** differs — 64 cycles/line, 262 lines. Question asked R8, above correct.

Detect chip at runtime via raster line count. Read high bit of raster from `$D011` bit 7 + `$D012`. Max raster line: PAL = 311 ($137), NTSC = 262 ($106).

```asm
; returns A=0 PAL, A=1 NTSC, by max raster reached
        sei
wait1:  lda $d012        ; spin to find largest raster value
        cmp max
        bcc store
        sta max
store:  ...              ; loop one full frame, track max in zp
```

Simpler BASIC sniff (count cycles indirectly not possible in BASIC; use raster):
```basic
10 P=0:FORI=0TO20000:R=PEEK(53266):IFR>PTHENP=R
20 NEXT:IFP>=255THENPRINT"PAL":END
30 PRINT"NTSC"
```
`53266` = `$D012`. PAL raster exceeds 255 (needs bit8 in `$D011`=53265), NTSC tops 262 but low byte wraps — better read bit 7 of `$D011` too for full 9-bit value.