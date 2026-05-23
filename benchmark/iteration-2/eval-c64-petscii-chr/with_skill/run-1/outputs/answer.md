PETSCII CHR$ codes:

| Effect | CHR$ |
|--------|------|
| Lower-case charset | **14** |
| Cursor down | **17** |
| RVS ON | **18** |
| White | **5** |

```basic
PRINT CHR$(14);CHR$(5);CHR$(18);CHR$(17);"white reversed text, lowercase, one down"
```

Note: CHR$(14) = lower/upper set. Upper/graphics back = CHR$(142). RVS OFF = CHR$(146).