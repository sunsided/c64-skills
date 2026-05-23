C64 BASIC. Two control CHR$ codes do it:

```basic
10 PRINT CHR$(147);CHR$(5);"READY"
```

- `CHR$(147)` = clear screen + home cursor (PETSCII shift-CLR/HOME).
- `CHR$(5)` = white text color. Stays white until changed.

`READY` then prints white. Trailing `;` optional.

**Color CHR$ codes** (common): 144 black, **5 white**, 28 red, 159 cyan, 156 purple, 30 green, 31 blue, 158 yellow.

## Screen code vs PETSCII for "A"

| Thing | "A" value |
|---|---|
| PETSCII / CHR$ code | 65 ($41) |
| Screen code (POKE to screen RAM) | 1 ($01) |

**Why different:** screen RAM (`$0400`–`$07E7`, 1024–2039) holds **screen codes**, not PETSCII. VIC-II takes the screen code, ×8, adds char-ROM base → fetches the 8-byte glyph bitmap. So screen codes index the character generator ROM in its layout: `@`=0, `A`=1, `B`=2 … `Z`=26.

PETSCII (what `CHR$`, `PRINT`, keyboard, `GET` use) is the ASCII-like encoding where `A`=65. `PRINT` converts PETSCII→screen code internally before writing screen RAM. POKE bypasses that, so you supply the screen code yourself.

POKE needs a separate color byte too — screen RAM = char, color RAM = color:

```basic
POKE 1024,1 : POKE 55296,1
```

White "A" top-left. `1024`=screen RAM start, `55296`=`$D800` color RAM start, value `1`=screen code A / color white.