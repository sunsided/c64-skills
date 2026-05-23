Raster IRQ line 100. Line 100 < 256, so RST8 (bit 9) = **0** — clear it.

## Registers

| Reg | Addr | Set to |
|----|------|--------|
| $D012 | 53266 | 100 — raster compare low 8 bits |
| $D011 bit7 | 53265 | 0 — RST8, raster bit 9 (line<256) |
| $D01A bit0 | 53274 | 1 — ERST, enable raster IRQ |
| $D019 | 53273 | write 1 to bit0 — ack/clear latch |
| $DC0D | 56333 | $7F — kill CIA IRQs |

## Assembly

```asm
        sei
        lda #$7f
        sta $dc0d        ; disable CIA IRQs
        lda $dc0d        ; ack pending CIA IRQ

        lda #$01
        sta $d01a        ; enable raster IRQ (ERST)

        lda #100
        sta $d012        ; raster compare = line 100
        lda $d011
        and #$7f         ; clear RST8 (bit9=0, line < 256)
        sta $d011

        lda #<irq
        sta $0314
        lda #>irq
        sta $0315        ; set IRQ vector (KERNAL ROM banked in)

        asl $d019        ; ack any pending VIC IRQ
        cli
        rts

irq:
        asl $d019        ; ACK — write 1 to $D019 bit0, clears latch
        ; ... your raster code here ...
        jmp $ea31        ; KERNAL IRQ wrap-up (or jmp $ea81 if no kbd scan)
```

## Notes

- **ACK mandatory.** VIC never clears latch itself. `asl $d019` shifts bit0→carry and writes 1 back, clearing it. Skip it → IRQ refires forever (level-sensitive on 6510).
- `$0314/$0315` = KERNAL RAM IRQ vector. Works only with KERNAL ROM mapped. For raw hardware vector use `$FFFE/$FFFF` after switching out ROM + own SEI/cycle handling.
- Raster compare tested cycle 0 each line. Negative edge defines line start.
- Read-modify-write `$D011` (`lda/and/sta`) — never write literal, unused bits read 1.

## BASIC equivalent (compare setup only)

```basic
POKE 53266,100 : POKE 53265,PEEK(53265)AND127 : POKE 53274,1
```

For line **≥256** instead: `ora #$80` on $D011 to set RST8. Line 100 here, so clear it.