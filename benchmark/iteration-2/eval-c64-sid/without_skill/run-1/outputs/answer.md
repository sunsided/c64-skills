SID 6581 standard envelope table (from C64 Programmer's Reference / SID datasheet). Decay/Release = 3× Attack.

**Value 11 ($B):**
- Attack: **800 ms**
- Decay/Release: **2.4 s** (2400 ms)

**Value 0:**
- Attack: **2 ms**
- Decay/Release: **6 ms**

## Registers (SID base $D400)

| Reg | Addr | Dec | Bits |
|-----|------|-----|------|
| Voice1 ATK/DEC | $D405 | 54277 | hi nibble=attack, lo nibble=decay |
| Voice1 SUS/REL | $D406 | 54278 | hi nibble=sustain, lo nibble=release |

Attack in bits 4-7, Decay/Release in bits 0-3. Pack: `byte = (rate<<4) | other`.

## BASIC — attack=11, decay=11

```basic
10 POKE 54277, 11*16+11 : REM $BB = attack 800ms, decay 2.4s
20 POKE 54278, 0*16+11  : REM sustain 0, release 2.4s (rel value 11)
```

Attack=0, decay=0:
```basic
10 POKE 54277, 0*16+0 : REM $00 = attack 2ms, decay 6ms
```

## Assembly

```asm
        ; attack=$B, decay=$B  -> $D405 = $BB
        lda #$BB
        sta $D405
        ; sustain=0, release=$B -> $D406 = $0B
        lda #$0B
        sta $D406
```

Full table for reference (Attack ms / Dec-Rel):

```
val  attack    dec/rel
 0   2ms       6ms
 1   8ms       24ms
 2   16ms      48ms
 3   24ms      72ms
 4   38ms      114ms
 5   56ms      168ms
 6   68ms      204ms
 7   80ms      240ms
 8   100ms     300ms
 9   250ms     750ms
10   500ms     1.5s
11   800ms     2.4s   <-
12   1s        3s
13   3s        9s
14   5s        15s
15   8s        24s
```