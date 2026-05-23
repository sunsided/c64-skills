CIA #1 = `$DC00–$DC0F`. Timer A IRQ ~60Hz. PAL clock 985248 Hz → 985248/60 = 16421 = `$4025`. (NTSC 1022727/60 = 17045 = `$4295`.)

**Registers:**

| Addr | Reg | Role |
|------|-----|------|
| `$DC04` | TA LO | Timer A latch/counter low byte |
| `$DC05` | TA HI | Timer A latch/counter high byte. Write HI loads latch. |
| `$DC0D` | ICR | Interrupt Control. Write: bit7=set/clear mask, bit0=Timer A IRQ enable. Read: shows+clears pending source. |
| `$DC0E` | CRA | Control Reg A. bit0=start, bit3=runmode (0=continuous), bit4=force-load latch, bit5=count source (0=Ø2 clock). |
| `$0314/$0315` | CINV | KERNAL IRQ vector. Point at your handler. |

Counter counts down latch→0, fires IRQ, auto-reloads (continuous mode). 16421 cycles ≈ 1/60 s.

```asm
; --- 6510 / CIA#1 Timer A -> ~60 Hz IRQ (PAL) ---
; assemble at $C000, SYS 49152 to start

        *=$C000

        sei                 ; block IRQ while wiring up

        lda #<irq           ; install handler into KERNAL vector
        sta $0314           ; CINV low
        lda #>irq
        sta $0315           ; CINV high

        lda #$7f            ; bit7=0 -> clear; %01111111
        sta $dc0d           ; disable ALL CIA#1 IRQ sources
        lda $dc0d           ; read ICR -> ack/clear any pending

        lda #$25            ; 16421 = $4025, low byte
        sta $dc04           ; Timer A latch LO  (use $95 for NTSC)
        lda #$40            ; high byte         (use $42 for NTSC)
        sta $dc05           ; Timer A latch HI

        lda #$81            ; %10000001 bit7=set, bit0=Timer A
        sta $dc0d           ; enable Timer A interrupt

        lda $dc0e           ; CRA
        and #%10000000      ; keep TOD-50/60 bit, clear rest
        ora #%00010001      ; bit4 force-load latch, bit0 start
        sta $dc0e           ; start Timer A, continuous mode

        cli                 ; allow IRQ
        rts

; --- IRQ handler ---
irq:
        lda $dc0d           ; read ICR -> ACK Timer A, clears IRQ line
        ; ... your 60Hz code here ...

        jmp $ea31           ; chain to KERNAL IRQ (scan kbd, jiffy clock)
```

**Key points:**
- Read `$DC0D` in handler = mandatory. Acknowledges IRQ; without it line stays low, lockup.
- `jmp $ea31` chains KERNAL routine (keyboard, jiffy `TI`). Use `jmp $ea81` if you want pure return (pull regs + RTI), skip KERNAL.
- Continuous mode (CRA bit3=0) auto-reloads latch each underflow → steady 60Hz, no re-arm needed.
- KERNAL already runs CIA#1 Timer A at ~60Hz for jiffy clock. This replaces that timing with your own.

BASIC note: hardware IRQ vector `$FFFE/$FFFF` only used if KERNAL ROM banked out. With ROM in, all IRQ funnel through `$0314/$0315` — why install there.