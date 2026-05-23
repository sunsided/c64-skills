## Memory map problem

Char ROM lives at **$D000–$DFFF** (4KB) — same address as the I/O block (VIC-II, SID, CIAs, color RAM). Only one visible at a time. Default: I/O wins.

## $01 — CPU port (processor I/O port)

Bit that matters: **CHAREN = bit 2**.

| Bit | Name | Function |
|----|------|----------|
| 0 | LORAM | BASIC ROM at $A000 |
| 1 | HIRAM | KERNAL ROM at $E000 |
| 2 | CHAREN | 0 = char ROM at $D000, 1 = I/O at $D000 |

Default $01 = **$37** (`%00110111`). Clear bit 2 → **$33** (`%00110011`). Char ROM now readable at $D000–$DFFF; BASIC+KERNAL stay in.

- $D000–$D7FF = set 1 (uppercase/graphics)
- $D800–$DFFF = set 2 (lowercase/uppercase)

## Why interrupts matter

CHAREN=0 banks **I/O out**. While char ROM visible, $D000–$DFFF no longer reaches VIC/SID/CIA — those addresses return ROM bytes.

KERNAL IRQ fires ~60×/sec. Handler reads CIA #1 ($DC00–$DCFF) to ack timer + scan keyboard. If IRQ fires mid-copy with I/O banked out, it reads **font bytes instead of CIA registers** → keyboard breaks, timer never acked, machine hangs/crashes.

Fix: **disable IRQ before banking, re-enable after.**
- ASM: `SEI` / `CLI`
- BASIC (no SEI): stop CIA#1 Timer A — source of the IRQ — via $DC0E (56334) bit 0.

## BASIC

```basic
10 POKE 56334,PEEK(56334) AND 254 : REM stop CIA#1 timer IRQ
20 POKE 1,PEEK(1) AND 251       : REM CHAREN=0, char ROM in
30 FOR I=0 TO 4095 : POKE 12288+I,PEEK(53248+I) : NEXT : REM $D000->$3000
40 POKE 1,PEEK(1) OR 4          : REM CHAREN=1, I/O back
50 POKE 56334,PEEK(56334) OR 1  : REM restart timer IRQ
```

Copies full 4KB. Want only uppercase set? `FOR I=0 TO 2047`.

## Assembly

```asm
        sei                 ; block interrupts
        lda $01
        and #%11111011      ; CHAREN=0 -> char ROM at $D000
        sta $01

        ldx #$00
loop    lda $d000,x         ; copy 4 pages = 1KB chunks
        sta $3000,x
        lda $d100,x
        sta $3100,x
        lda $d200,x
        sta $3200,x
        lda $d300,x
        sta $3300,x
        ; ... repeat for $d400-$df00 to cover full 4KB
        inx
        bne loop

        lda $01
        ora #%00000100      ; CHAREN=1 -> I/O back
        sta $01
        cli                 ; re-enable interrupts
        rts
```

(Loop only shows first 1KB; extend blocks or use a page counter for the full $D000–$DFFF.)

## Point VIC at new font (optional)

Font now at $3000, inside VIC bank 0 ($0000–$3FFF). Set char base via $D018 (53272), bits 3–1. $3000 = unit 6 = `%110`.

```basic
POKE 53272,(PEEK(53272) AND 240) OR 12 : REM char base $3000, keep screen
```

Now edit bytes at $3000+ to reshape glyphs — 8 bytes per char, char N at $3000 + N*8.