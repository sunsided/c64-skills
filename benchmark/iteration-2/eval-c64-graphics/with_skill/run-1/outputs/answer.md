`$D018` = **53272**. One byte, two fields + dead bit.

```
bit:  7  6  5  4 | 3  2  1 | 0
     VM13 12 11 10|CB13 12 11|unused
     screen base  | char/bitmap base
```

## Screen (video matrix) base — bits 7-4
- 4 bits = VM13–VM10. Value × `$0400` (1K granularity) within 16K bank.
- 16 possible spots, 0..$3C00 in bank.
- Default nibble = 1 → `$0400` (1024).

```
POKE 53272,(PEEK(53272)AND15)OR(A*16)   : REM A=0..15, screen base = A*$400
```

## Char generator base — bits 3-1
- 3 bits = CB13–CB11. Value field × `$0800` (2K granularity) within bank.
- 8 spots. Bit 0 ignored (charset must sit on 2K boundary, so low bit meaningless).
- Field values (the low nibble you POKE): 0=$0000, 2=$0800, **4=$1000 ROM image (default)**, 6=$1800, 8=$2000, 10=$2800, **12=$3000**, 14=$3800.

```
POKE 53272,(PEEK(53272)AND240)OR A      : REM A picks char base (even val)
POKE 53272,(PEEK(53272)AND240)+12       : REM charset at 12288 ($3000)
```

## Bitmap mode — bit 3 alone
- Char field collapses: only **bit 3** matters as bitmap select.
- bit3=0 → bitmap at `$0000`; bit3=1 → bitmap at `$2000` (8K granularity).

```
POKE 53272,PEEK(53272)OR 8              : REM bitmap base $2000 in bank
```

## Granularity summary
| Field | Bits | Step | Range in bank |
|-------|------|------|---------------|
| Screen base | 7-4 | `$0400` (1K) | $0000–$3C00 |
| Char base | 3-1 | `$0800` (2K) | $0000–$3800 |
| Bitmap base | 3 only | `$2000` (8K) | $0000 or $2000 |

All addresses **relative to selected 16K VIC bank** (CIA2 `$DD00`), not absolute. Bit 0 = unused. Default `$D018`=21 ($15) → screen $0400, char $1000 ROM image.

Assembly, set char base $3000 keep screen nibble:
```asm
    LDA $D018
    AND #$F0        ; keep screen base bits
    ORA #$0C        ; CB field = 12 -> $3000
    STA $D018
```