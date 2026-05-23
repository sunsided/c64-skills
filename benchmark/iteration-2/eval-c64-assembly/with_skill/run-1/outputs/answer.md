SYS save/restore registers at four page-3 locations:

| Addr | Dec | Name | Holds |
|------|-----|------|-------|
| `$030C` | 780 | SAREG | A |
| `$030D` | 781 | SXREG | X |
| `$030E` | 782 | SYREG | Y |
| `$030F` | 783 | SPREG | status P |

Flow: on SYS, KERNAL copies these four into the CPU registers **before** `JSR` to your code. On `RTS`, copies CPU registers back **out** to same locations. So PEEK after = post-call values.

BASIC — call $C000 with A=65, X=0, Y=0:
```basic
POKE 780,65 : POKE 781,0 : POKE 782,0 : SYS 49152
PRINT PEEK(780) : REM A returned by routine
```

ASM side — SYS lands here, A already =65:
```asm
        STA $0400          ; 'A' char to screen
        RTS                ; mandatory: copies regs back, returns to BASIC
```

Caveats:
- SPREG ($030F) = full P byte. Setting it before SYS forces flags (e.g. carry) into CPU. Be careful — wrong bits break things.
- Default A/X/Y values at SYS = whatever BASIC left; POKE first if you need known input.