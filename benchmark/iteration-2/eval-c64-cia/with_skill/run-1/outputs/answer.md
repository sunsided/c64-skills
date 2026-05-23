ICR at `$DC0D` (CIA1) — same address, two different behaviors:

**READ side = flags (INT DATA):**
```
IR  0  0  FLG SP ALRM TB TA
```
- Returns which sources fired: TA=Timer A underflow, TB=Timer B, ALRM=TOD alarm, SP=serial, FLG=/FLAG pin. Bit 7 (IR)=1 means this chip raised the IRQ.
- **Read clears all flags** and releases the `/IRQ` line. Destructive. Read once, save byte, branch on copy — second read returns 0, flags lost.

**WRITE side = mask (INT MASK):**
```
S/C  x  x  FLG SP ALRM TB TA
```
- Bit 7 = **set/clear select**, NOT a flag.
  - Bit 7 = 1 → every 1-bit in low 5 bits **enables** that source.
  - Bit 7 = 0 → every 1-bit in low 5 bits **disables** that source.
  - 0-bits unaffected either way. So you flip individual sources without touching others.

Values:
```asm
LDA #%10000001 : STA $DC0D   ; bit7=1 set + TA bit -> ENABLE Timer A IRQ  ($81)
LDA #%01111111 : STA $DC0D   ; bit7=0 clear + all bits -> DISABLE all     ($7F)
```

BASIC:
```basic
POKE 56333,129 : REM $DC0D=$81, enable Timer A IRQ
POKE 56333,127 : REM $DC0D=$7F, disable all CIA1 sources
X = PEEK(56333) : REM read flags AND clear them
```

Key trap: read and write are not symmetric. Reading `$DC0D` to "check the mask" doesn't work — read gives flags + wipes them. Mask is write-only; no readback.

`#$7F` to `$DC0D` at IRQ-setup is the standard "clear all pending CIA IRQs" move.