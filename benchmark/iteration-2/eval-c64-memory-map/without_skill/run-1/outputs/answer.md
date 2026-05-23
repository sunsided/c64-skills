C64 $01 = 6510 processor port. Low 3 bits drive PLA banking (with cartridge lines GAME=EXROM=1, i.e. no cart):

- bit0 LORAM, bit1 HIRAM, bit2 CHAREN.
- BASIC ROM at $A000 needs **LORAM=1 AND HIRAM=1**.
- KERNAL ROM at $E000 needs **HIRAM=1**.
- $D000 = I/O when CHAREN=1 (and BASIC/KERNAL not all-RAM), CHAR ROM when CHAREN=0, RAM when all banking bits low.

## $37 = %00110111 (default, bits 210 = 111)
- **$A000–$BFFF:** BASIC ROM (8K)
- **$D000–$DFFF:** I/O — VIC-II, SID, color RAM, CIA1, CIA2
- **$E000–$FFFF:** KERNAL ROM (8K)

## $35 = %00110101 (bits 210 = 101 → LORAM=1, HIRAM=0, CHAREN=1)
- **$A000–$BFFF:** RAM (HIRAM=0 → no BASIC)
- **$D000–$DFFF:** I/O (CHAREN=1, still visible)
- **$E000–$FFFF:** RAM (HIRAM=0 → no KERNAL)

Common ML config: BASIC+KERNAL gone, max RAM, but I/O still reachable.

## $34 = %00110100 (bits 210 = 100 → LORAM=0, HIRAM=0, CHAREN=1)
- **$A000–$BFFF:** RAM
- **$D000–$DFFF:** RAM (no I/O, no CHAR ROM)
- **$E000–$FFFF:** RAM

Full RAM in all three regions. I/O hidden — VIC/SID/CIA unreachable until you restore. Note: even though CHAREN=1, when both LORAM=HIRAM=0 the PLA forces RAM at $D000.

## Code

Read/set port. $00 = DDR (default $2F), $01 = port:

```basic
PRINT PEEK(1)        : REM read current, default 55 ($37)
POKE 1,53            : REM $35
POKE 1,52            : REM $34
POKE 1,55            : REM back to $37
```

Warning: `POKE 1,52` from BASIC kills BASIC/KERNAL — machine crashes. Do bank switching only from ML with interrupts disabled.

Assembly (e.g. peek hidden RAM under KERNAL, then restore I/O):

```asm
        sei
        lda #$35        ; KERNAL+BASIC out, I/O in
        sta $01
        ; ... access RAM at $A000/$E000 ...
        lda #$37        ; restore default
        sta $01
        cli
```

For $34 (kill I/O too) you must also stash/restore around it since IRQ handler lives in KERNAL — keep `sei` set and restore $37 before `cli`.