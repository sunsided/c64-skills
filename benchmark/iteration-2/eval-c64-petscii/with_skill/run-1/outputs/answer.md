Screen codes (POKE into $0400+):

| Char | Screen code |
|------|-------------|
| `@` | **0** |
| `A` | **1** |
| space | **32** |
| reverse space | **160** (32 + 128) |

Reverse space = solid block, used for color bars/backgrounds. Set color RAM too or invisible:

```basic
POKE 1024,0   : POKE 55296,1   : REM @ top-left, white
POKE 1025,1   : POKE 55297,1   : REM A next, white
POKE 1026,32  : POKE 55298,1   : REM space
POKE 1027,160 : POKE 55299,1   : REM reverse space = solid block
```

Note: these are NOT PETSCII. PETSCII `@`=64, `A`=65, space=32. Only space matches both systems.