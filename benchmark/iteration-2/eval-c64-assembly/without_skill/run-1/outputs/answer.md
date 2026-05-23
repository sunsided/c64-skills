C64 SYS register storage = page 3, **not** zero page.

| Reg | Hex | Dec | Role |
|-----|------|-----|------|
| A | `$030C` | 780 | accumulator |
| X | `$030D` | 781 | X index |
| Y | `$030E` | 782 | Y index |
| P (SR) | `$030F` | 783 | processor status |

## How SYS uses them

On entry: BASIC `SYS` routine (ROM ~`$E12A`) loads CPU regs **from** these locations, then `JSR`s your code. On `RTS`: it stores live CPU regs **back** into same locations. So they are bidirectional — set before call, read after.

ROM logic (paraphrase):
```asm
        LDA $030C      ; A
        LDX $030D      ; X
        LDY $030E      ; Y
        ... PLP from $030F  ; status loaded
        JSR your_routine
        PHP / STA $030C / STX $030D / STY $030E ; regs saved back
        ... store status -> $030F
```

## BASIC usage

Pass A=1, X=2, Y=3, then call `$C000` (49152):
```basic
10 POKE 780,1 : POKE 781,2 : POKE 782,3 : POKE 783,0
20 SYS 49152
30 PRINT PEEK(780); PEEK(781); PEEK(782); PEEK(783)
```
Line 30 reads regs as left by your code's `RTS`.

## Notes

- `$030F` = full P byte (NV-BDIZC). Bit values matter — carry = bit 0, zero = bit 1, etc. Setting `783` lets you pass carry in / read carry out.
- These mirror the KERNAL register-save bytes; many KERNAL calls via SYS round-trip through them.
- `USR()` is different — uses floating-point accumulator (`$61`+), not these.