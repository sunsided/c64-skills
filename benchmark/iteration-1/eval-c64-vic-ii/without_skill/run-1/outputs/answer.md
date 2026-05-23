C64 raster IRQ at line 100. Knowledge answer, no tools.

## Registers

| Addr | Dec | Purpose |
|------|-----|---------|
| `$D012` | 53266 | RASTER — low 8 bits of compare line (write) |
| `$D011` | 53265 | bit 7 = 9th raster bit (line ≥256). Line 100 → bit 7 = 0 |
| `$D01A` | 53274 | VIC IRQ enable. bit 0 = raster IRQ |
| `$D019` | 53273 | VIC IRQ flag. Write set bit back to **acknowledge** |
| `$DC0D` | 56333 | CIA#1 IRQ control. Disable timer IRQ so only raster fires |
| `$0314/$0315` | 788/789 | KERNAL IRQ vector (ROM mapped in, default) |

Line 100 < 256 → 9th bit clears.

## Setup code

```asm
        sei                 ; block IRQ during setup

        lda #<irq           ; new IRQ vector -> our handler
        sta $0314
        lda #>irq
        sta $0315

        lda #$7f            ; disable all CIA#1 IRQ sources (timers)
        sta $dc0d
        lda $dc0d           ; ack/clear any pending CIA IRQ

        lda #100            ; raster compare line = 100
        sta $d012
        lda $d011           ; clear bit 7 (9th raster bit) -> line < 256
        and #$7f
        sta $d011

        lda #$01            ; enable raster IRQ
        sta $d01a
        sta $d019           ; ack any pending VIC IRQ

        cli                 ; re-enable IRQ
        rts

irq:
        lda #$01
        sta $d019           ; ACKNOWLEDGE raster IRQ (write set bit)

        ; --- your code here ---

        jmp $ea31           ; chain to KERNAL IRQ (timer, keyscan)
                            ; use jmp $ea81 instead if you skip KERNAL work
```

## Acknowledge — why

`$D019` flag bit stays set after fire. Write a **1** to set bit clears it (`STA $D019` with `#$01`). Skip ack → IRQ re-fires forever, machine hangs.

## Notes

- `jmp $ea31` chains KERNAL handler (keyboard, jiffy clock keep working). `jmp $ea81` = just restore regs + `rti`, skips KERNAL.
- `$0314/$0315` valid only with KERNAL ROM mapped (default `$01` = `$37`). If you bank out ROM, set hardware vector `$FFFE/$FFFF` instead.
- BASIC start: `SYS` to setup routine. Stays armed until you `SEI` + restore vector.