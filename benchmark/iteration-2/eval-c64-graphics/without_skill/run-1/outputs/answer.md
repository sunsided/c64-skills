$D018 = 53272 = VIC-II memory-pointer register. 8 bits, three fields:

```
bit:   7    6    5    4    3    2    1    0
      VM13 VM12 VM11 VM10 CB13 CB12 CB11  -
      └──── screen base ───┘ └─ char base ─┘ unused
```

**Bits 7-4 (VM13–VM10): video matrix / screen base.**
Granularity 1 KB ($0400). 16 positions in bank.
`screen_offset = (D018 >> 4) * 1024`

**Bits 3-1 (CB13–CB11): character generator base (text mode).**
Granularity 2 KB ($0800). 8 positions in bank.
`char_offset = ((D018 >> 1) & 7) * 2048`

**Bit 0: unused.** Reads back 1 on real VIC-II.

**Bitmap mode (ECM/BMM):** only bit 3 (CB13) matters. Bitmap is 8 KB, base = `bit3 * 8192` → offset $0000 or $2000. CB12/CB11 ignored.

All offsets are **within the 16K VIC bank**. Bank set by CIA2 $DD00 (56576) bits 0-1, inverted:
`bank_base = (3 - (PEEK(56576) AND 3)) * 16384`
Final hardware address = `bank_base + offset`.

**Default stock C64:** $D018 = 21 ($15) = `%0001 0101`. VM=0001 → screen $0400. CB=010 → charset $1000 (char ROM image in bank 0). Bit0 reads 1 → 21 not 20.

Char base caveat: in bank 0/2, offsets $1000 ($D018 CB=010) and $1800 (CB=011) show **character ROM**, not RAM — VIC sees ROM mirrored there.

**BASIC — read current bases:**
```basic
10 V=PEEK(53272)
20 SB=(V AND 240)/16*1024 : REM screen offset
30 CB=(V AND 14)/2*2048   : REM char offset
40 PRINT "SCREEN OFFS";SB;"  CHAR OFFS";CB
```

**BASIC — set screen=$0400 (offs 1024), charset=$2000 (offs 8192):**
```basic
10 POKE 53272,(1024/1024)*16 + (8192/2048)*2
20 REM = 1*16 + 4*2 = 24
```

**Assembly — same:**
```asm
        ; screen base = $0400 -> VM = %0001
        ; char base   = $2000 -> CB = %100
        lda #%00011000   ; $18 = 24
        sta $d018
```

**Assembly — bitmap base $2000:**
```asm
        lda $d011
        ora #%00100000   ; set BMM (bit5)
        sta $d011
        lda $d018
        ora #%00001000   ; CB13=1 -> bitmap at $2000
        sta $d018
```

Note: writing $D018 directly does not update KERNAL's screen pointers ($0288 hi-byte of screen). Pure-VIC display fine; for KERNAL text output also fix $0288.