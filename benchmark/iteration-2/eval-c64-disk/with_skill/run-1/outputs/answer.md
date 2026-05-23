Read channel 15 with `INPUT#`:

```basic
10 OPEN 15,8,15
20 PRINT#15,"<your DOS command>"
30 INPUT#15,EN,EM$,ET,ES
40 PRINT EN;EM$;ET;ES
50 CLOSE 15
```

- `EN` = error number
- `EM$` = message text
- `ET` = track
- `ES` = sector

After success, exact response:

```
00 OK 00 00
```

So `EN=0`, `EM$="OK"`, `ET=0`, `ES=0`. Reading channel 15 also clears the error and stops drive light blinking. Blinking light = uncleared error waiting to be read.