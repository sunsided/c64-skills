Screen codes (POKE to $0400+):

| Char | Screen code |
|------|-------------|
| `@` | **0** |
| `A` | **1** |
| space | **32** |
| reverse space | **160** |

Reverse = base + 128. So `160 = 32 + 128`.

Example:
```basic
POKE 1024,0   : REM @ top-left
POKE 1025,1   : REM A
POKE 1026,32  : REM space
POKE 1027,160 : REM reverse space (solid block in fg color)
```
Note: color RAM ($D800+) also needed to see char vs background. Reverse space fills whole cell with foreground color.