All four commands:

```basic
LOAD "$",8 : LIST              REM (1) directory — clobbers BASIC program
LOAD "GAME",8                  REM (2) load BASIC prog GAME (relocates to $0801)
OPEN 15,8,15,"N0:MYDISK,42" : CLOSE 15   REM (3) format: label MYDISK, id 42
```

(4) read error channel:

```basic
10 OPEN 15,8,15
20 INPUT#15,EN,EM$,ET,ES
30 PRINT EN;EM$;ET;ES          REM e.g. 00 OK 00 00
40 CLOSE 15
```

Notes:
- (2) If GAME is ML/data needing fixed address, use `LOAD "GAME",8,1` instead — `,8` relocates to BASIC start, `,8,1` loads to saved address.
- (3) `"N0:MYDISK,42"` full format with 2-char id `42`. Drop id (`"N0:MYDISK"`) for quick clear of already-formatted disk.
- (4) `EN`=error num, `EM$`=message, `ET`/`ES`=track/sector. Reading also clears blinking drive light. OK status = `00, OK, 00, 00`.