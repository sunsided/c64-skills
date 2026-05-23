**ICR = two different registers behind one address.** $DC0D (56333) CIA#1, $DD0D (56589) CIA#2. Read hits DATA latch; write hits MASK register.

## READ ($DC0D PEEK)

Returns pending-interrupt flags:

| bit | source |
|-----|--------|
| 0 | Timer A underflow |
| 1 | Timer B underflow |
| 2 | TOD alarm match |
| 3 | serial shift reg full/empty |
| 4 | FLAG pin (cassette read / serial bus on CIA#1) |
| 5,6 | always 0 |
| 7 | **IR** — set if any *enabled* source latched. This is what drove the IRQ/NMI line. |

Bit 7 here = "this CIA caused the interrupt" (mask AND data ≠ 0). Test bit 7 to identify source in shared IRQ handler.

**Read = destructive.** Reading DATA clears all 5 flag bits AND bit 7 to 0, and releases the interrupt line (acknowledges it). Read once, save value, test saved copy — second read returns 0.

## WRITE ($DC0D POKE)

Writes MASK register (which sources allowed to raise interrupt). Same bit-to-source map, bits 0-4.

**Bit 7 = SET/CLEAR control, not data:**
- bit 7 = 1 → each 1-bit in value **sets** (enables) that mask bit
- bit 7 = 0 → each 1-bit in value **clears** (disables) that mask bit
- 0-bits in value → mask bit **unchanged** either way

Lets you flip individual masks without read-modify-write.

## Code

```asm
        LDA #%10000001   ; $81 bit7=1 set, bit0=1 -> enable Timer A IRQ
        STA $DC0D
        ; ...
        LDA #%01111111   ; $7F bit7=0 clear, bits0-4=1 -> disable ALL sources
        STA $DC0D

irq     LDA $DC0D        ; READ: get flags + clear/ack in one shot
        AND #%00000001   ; isolate Timer A flag (bit7 already consumed)
        BEQ notme        ; not us, chain
        ; service Timer A
notme   ...
```

BASIC:
```basic
POKE 56333,129 : REM $81 enable Timer A IRQ, CIA#1
POKE 56333,127 : REM $7F disable all sources
PRINT PEEK(56333) : REM read flags — also clears them
```

Gotcha: standard KERNAL raster setup leaves CIA#1 Timer A IRQ on (jiffy clock). Read $DC0D in your handler to ack, else interrupt never clears and machine hangs.