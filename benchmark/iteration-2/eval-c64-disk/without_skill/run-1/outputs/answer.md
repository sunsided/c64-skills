Command channel = channel 15 (secondary address 15). Read it with `INPUT#`.

```basic
10 OPEN 15,8,15
20 INPUT#15,EN,EM$,ET,ES
30 PRINT EN;EM$;ET;ES
40 CLOSE 15
```

Four fields: error number, error message string, track, sector.

After a command that succeeded:

```
0 OK 0 0
```

Exact bytes on channel: `00, OK,00,00` followed by CR (`$0D`). `EN=0`, `EM$="OK"`, `ET=0`, `ES=0`.

Notes:
- Reading the channel **clears** the drive's error LED (blinking light stops).
- Send DOS command first on same channel: `PRINT#15,"I0"` (init), `"S0:FILE"` (scrape/delete), etc. Then `INPUT#15` to read result.
- Field separators are commas; message field has no quotes on the wire — `INPUT#` parses commas, so `EM$` gets `OK` clean.
- One-shot status check without keeping file open: `OPEN 1,8,15,"I0":INPUT#1,...` — command goes in the OPEN string.

Example after error (e.g. file not found): `62, FILE NOT FOUND,00,00`.