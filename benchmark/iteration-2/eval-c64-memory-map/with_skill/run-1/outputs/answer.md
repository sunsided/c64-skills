Decode bits 2-0 of `$01` = CHAREN(b2), HIRAM(b1), LORAM(b0). Key rule: **I/O and Char ROM only appear when HIRAM OR LORAM is high.** Both low → those regions become RAM, CHAREN inert.

**`$37` = %0011 0111 → bits 111** (CHAREN=1, HIRAM=1, LORAM=1) — default
| Region | Content |
|--------|---------|
| $A000-$BFFF | **BASIC ROM** |
| $D000-$DFFF | **I/O** (VIC/SID/color/CIA) |
| $E000-$FFFF | **KERNAL ROM** |

**`$35` = %0011 0101 → bits 101** (CHAREN=1, HIRAM=0, LORAM=1)
| Region | Content |
|--------|---------|
| $A000-$BFFF | **RAM** (HIRAM=0 kills BASIC; BASIC needs LORAM AND HIRAM) |
| $D000-$DFFF | **I/O** (CHAREN=1 + LORAM=1 → I/O wins) |
| $E000-$FFFF | **RAM** (HIRAM=0) |

60K RAM + I/O. KERNAL gone → IRQ/NMI vectors gone, write own I/O.

**`$34` = %0011 0100 → bits 100** (CHAREN=1, HIRAM=0, LORAM=0)
| Region | Content |
|--------|---------|
| $A000-$BFFF | **RAM** |
| $D000-$DFFF | **RAM** (← not I/O! both HIRAM+LORAM low, CHAREN ignored) |
| $E000-$FFFF | **RAM** |

All RAM in these regions — **identical to `$30`**. CHAREN=1 does nothing here; PLA needs HIRAM or LORAM high before CHAREN picks I/O vs Char ROM.

**Gotcha:** $35 → $34 flips LORAM 1→0. That single bit yanks I/O out of $D000 entirely, since with HIRAM already 0, LORAM was the only line keeping I/O mapped.

Set from BASIC (`$01` = decimal 1):
```basic
POKE 1, 55 : REM $37 default
POKE 1, 53 : REM $35  60K RAM + I/O
POKE 1, 52 : REM $34  all RAM (= 48)
```
ASM (IRQs off — no KERNAL/I/O for handler):
```asm
        SEI
        LDA #$35
        STA $01
```