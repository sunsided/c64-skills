C64 BASIC printer I/O. Three commands:

```basic
10 OPEN 4,4
20 PRINT#4,"HELLO PRINTER"
30 CLOSE 4
```

Breakdown:
- `OPEN 4,4` — open logical file 4 (first arg, your choice 1-255) on device 4 (printer). Form: `OPEN lfn, device`. KERNAL routine at `$FFC0`.
- `PRINT#4,"..."` — send text to logical file 4. Note `PRINT#`, no space before `#` (tokenizes as `PRINT#`). Adds CR (`$0D`) at end → line feed on printer.
- `CLOSE 4` — close logical file 4. Flushes, frees buffer. KERNAL `$FFC3`.

Optional secondary address selects mode:
- `OPEN 4,4,0` — uppercase/graphics (default)
- `OPEN 4,4,7` — lowercase/business

Suppress trailing CR with `;`:
```basic
20 PRINT#4,"NO NEWLINE";
```