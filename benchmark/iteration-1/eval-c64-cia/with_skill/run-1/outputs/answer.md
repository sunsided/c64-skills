~60 Hz IRQ from CIA1 Timer A. Period = φ2 cycles per tick. Latch = φ2/60 − 1.

- **PAL** φ2 = 985248 Hz → 985248/60 ≈ 16421 = `$4025`
- **NTSC** φ2 = 1022727 Hz → 1022727/60 ≈ 17045 = `$42A5`

Code (PAL value; swap latch for NTSC):

```asm
; --- install CIA1 Timer A IRQ at ~60 Hz (PAL) ---
        SEI

        LDA #%01111111     ; bit7=0 -> clear-mask, all bits
        STA $DC0D          ; disable+ack all CIA1 IRQ sources (kills jiffy)
        LDA $DC0D          ; read ICR -> clear any pending flag, release /IRQ

        LDA #<newirq
        STA $0314          ; CINV lo  (KERNAL IRQ vector)
        LDA #>newirq
        STA $0315          ; CINV hi

        LDA #$25           ; latch = $4025 (PAL ~60 Hz). NTSC: $A5/$42
        STA $DC04          ; Timer A latch LO
        LDA #$40
        STA $DC05          ; Timer A latch HI

        LDA #%10000001     ; bit7=1 set-mask + TA bit -> enable Timer A IRQ
        STA $DC0D

        LDA #%00010001     ; CRA: bit4 LOAD latch->counter, bit0 START,
        STA $DC0E          ;      bit3=0 continuous (auto-reload)

        CLI
        RTS

newirq:
        LDA $DC0D          ; READ+CLEAR CIA1 ICR -> ack, release /IRQ
        ; ... your 60 Hz work here ...
        JMP $EA31          ; chain to KERNAL (scan keyboard, blink, jiffy)
                           ; use $EA81 instead if you want bare RTI only
```

Registers:

| Reg | Addr | Role |
|-----|------|------|
| TA LO/HI latch | `$DC04`/`$DC05` | reload value. counter underflow → IRQ. write sets latch, not counter directly |
| ICR | `$DC0D` | **write** = mask (bit7 set/clear, bit0 = Timer A). **read** = flags, and read CLEARS them + drops /IRQ |
| CRA | `$DC0E` | bit0 START, bit3 RUNMODE (0=continuous reload), bit4 LOAD strobe (force latch→counter), bit5 INMODE (0=count φ2) |
| CINV | `$0314`/`$0315` | KERNAL IRQ vector. point at your handler |

Key points:

- CIA1 `/IRQ` → CPU **IRQ**. Default KERNAL jiffy already uses this timer; `#$7F` to `$DC0D` removes its source so you own it.
- Continuous mode (CRA bit3=0): latch auto-reloads on underflow → repeating 60 Hz, no rearm needed.
- Handler **must** read `$DC0D` once to ack, else /IRQ stays low and you never fire again.
- Chain `JMP $EA31` to keep keyboard/jiffy clock alive; `$EA81` if you replaced everything.
- LOAD (CRA bit4) = strobe: reads back 0, only force-loads latch into counter when written 1.

Exact 60.000 Hz impossible — both latches give ~59.99 Hz. Standard KERNAL jiffy uses same `$4025`/`$42A5`, so TI clock stays consistent.