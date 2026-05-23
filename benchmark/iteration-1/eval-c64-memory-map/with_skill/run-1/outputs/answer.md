## Banking

Char ROM only appears when **CHAREN = bit 2 of `$01` = 0**. Shares `$D000-$DFFF` with I/O. Clear bit 2 → char ROM swaps in, I/O chips vanish.

- Default `$01` = `$37` (%00110111) → I/O visible.
- Clear bit 2 → `$33` (%00110011) → char ROM at `$D000-$DFFF`.
- Uppercase/graphics set at `$D000`, lowercase set at `$D800`. Each set = 2K (256 chars × 8 bytes).

## Why interrupts matter

CIA1 at `$DC00` triggers IRQ 60×/sec for keyboard scan + jiffy clock. While char ROM banked in, **CIA1 gone from `$D000-$DFFF`**. If IRQ fires mid-copy:
- handler reads garbage where CIA1 used to be,
- can't clear interrupt source → lockup or crash.

So: **`SEI` before, `CLI` after**. Disable IRQ for whole bank-swap window.

(KERNAL at `$E000` stays put here — only `$D000` region changed — but IRQ handler still touches CIA1. Must block it.)

## Assembly — copy 4K (both sets) to $3000

```asm
        SEI                ; block IRQ — CIA1 about to vanish
        LDA $01
        PHA                ; save banking state
        AND #%11111011     ; CHAREN=0 -> char ROM at $D000-$DFFF
        STA $01

        LDA #$D0           ; source page = $D000
        STA $FC
        LDA #$30           ; dest page = $3000
        STA $FE
        LDX #$10           ; 16 pages = 4096 bytes (both char sets)
        LDY #$00
        STY $FB
        STY $FD

copy    LDA ($FB),Y        ; read char ROM
        STA ($FD),Y        ; write RAM
        INY
        BNE copy
        INC $FC            ; next source page
        INC $FE            ; next dest page
        DEX
        BNE copy

        PLA                ; restore banking (CHAREN=1 -> I/O back)
        STA $01
        CLI                ; IRQ on again
        RTS
```

`$FB-$FE` = the four free zero-page bytes. Copies `$D000-$DFFF` → `$3000-$3FFF`. Want just uppercase set? Use `LDX #$08` (2K → `$3000-$37FF`).

## BASIC version

```basic
10 POKE 56334,PEEK(56334)AND254 : REM stop CIA1 timer IRQ
20 POKE 1,PEEK(1)AND251        : REM CHAREN=0 -> char ROM in
30 FOR I=0 TO 4095 : POKE 12288+I,PEEK(53248+I) : NEXT
40 POKE 1,PEEK(1)OR4           : REM CHAREN=1 -> I/O back
50 POKE 56334,PEEK(56334)OR1   : REM CIA1 timer IRQ on
```

`12288` = `$3000`, `53248` = `$D000`. Line 10/50 here stop/restart the CIA1 timer instead of `SEI/CLI` since BASIC can't hold IRQ off across a `FOR` loop cleanly.

## After copy

To make VIC use font at `$3000`: set screen-memory pointer `$D018` and ensure VIC bank covers `$3000` (bank 0, default). See **c64-vic-ii** for `$D018` char-base bits.