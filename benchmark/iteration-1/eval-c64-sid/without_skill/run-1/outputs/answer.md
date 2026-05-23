SID base **$D400** (54272). Voice 1 regs:

| Reg | Addr | Purpose |
|-----|------|---------|
| $D400/$D401 | 54272/54273 | freq lo/hi |
| $D404 | 54276 | control: sawtooth=bit5 ($20), gate=bit0 ($01) → **$21** on |
| $D405 | 54277 | attack(hi nibble)/decay(lo) |
| $D406 | 54278 | sustain(hi)/release(lo) |
| $D418 | 54296 | master volume (lo nibble) |

Freq formula: `Fn = Fout * 16777216 / Fclk`. PAL Fclk=985248 → ~440 Hz = **7493** = $1D45 → hi=29, lo=69. NTSC Fclk=1022730, scale by ~0.964.

## BASIC

```basic
10 S=54272
20 FOR I=0 TO 24:POKE S+I,0:NEXT
30 POKE S+24,15:REM VOLUME 15
40 POKE S+5,9:REM ATTACK 0, DECAY 9
50 POKE S+6,249:REM SUSTAIN 15, RELEASE 9
60 POKE S+1,29:POKE S,69:REM FREQ ~440HZ
70 POKE S+4,33:REM SAWTOOTH + GATE ON
80 FOR T=1 TO 800:NEXT:REM HOLD ~1S
90 POKE S+4,32:REM GATE OFF (RELEASE)
100 FOR T=1 TO 400:NEXT
110 POKE S+24,0:REM VOLUME OFF
```

Line 80 loop ≈ 1 s. Tune count for exact timing (BASIC loop speed approximate).

## 6510 assembly

Uses KERNAL jiffy clock ($A0–$A2, low byte $A2, ~60 Hz NTSC / 50 Hz PAL). IRQ left enabled so jiffy ticks.

```asm
        sid = $d400

        lda #$00
        ldx #$18
clr     sta sid,x        ; clear $d400-$d418
        dex
        bpl clr

        lda #$0f
        sta $d418        ; volume = 15
        lda #$09
        sta $d405        ; attack=0, decay=9
        lda #$f9
        sta $d406        ; sustain=15, release=9

        lda #69
        sta $d400        ; freq lo  (~440 Hz PAL)
        lda #29
        sta $d401        ; freq hi

        lda #$21
        sta $d404        ; sawtooth + gate ON

        lda #$00         ; reset jiffy clock
        sta $a0
        sta $a1
        sta $a2
wait    lda $a2          ; low byte of jiffy
        cmp #50          ; ~1 s PAL (use 60 for NTSC)
        bcc wait

        lda #$20
        sta $d404        ; gate OFF -> release phase
        rts
```

Note: jiffy needs CIA/IRQ running — do **not** `sei` here. If you must `sei`, swap delay for a raster/`$D012` count or nested decrement loop.