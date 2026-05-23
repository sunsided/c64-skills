Three statements. OPEN channel, PRINT# text, CLOSE.

```basic
10 OPEN 4,4
20 PRINT#4,"HELLO PRINTER"
30 CLOSE 4
```

- `OPEN 4,4` — logical file 4 onto device 4 (printer). No secondary = upper-case+graphics. Want upper/lower case: `OPEN 4,4,7`.
- `PRINT#4,...` — send line. Trailing RETURN ends line. Note: `PRINT#`, no space between `PRINT` and `#`.
- `CLOSE 4` — flush, release channel. Skip = data stuck in buffer, printer hangs.

Check `ST` after if want status (device-not-present etc).