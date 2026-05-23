PETSCII codes:

| Function | CHR$ |
|---|---|
| Lower-case set (text mode) | `CHR$(14)` |
| Cursor down | `CHR$(17)` |
| Reverse on (RVS ON) | `CHR$(18)` |
| White | `CHR$(5)` |

Example:

```basic
PRINT CHR$(14);CHR$(5);CHR$(18);CHR$(17);"hello"
```

Notes:
- `CHR$(142)` = back to upper-case/graphics set.
- `CHR$(146)` = RVS OFF.
- Lower-case `CHR$(14)` flips bit at `53272` ($D018) — POKE 53272,23 same effect.