C64 tape = Datasette, **device 1** (default — no device number needed).

## Save
```basic
SAVE "MYPROG"
```
Saves to tape. Prompts `PRESS RECORD & PLAY ON TAPE`. Writes header + program to current tape position. No name OK too (`SAVE` alone) but naming required to find later.

## Load back
```basic
LOAD "MYPROG"
```
Then `RUN`. `PRESS PLAY ON TAPE` → `SEARCHING` → `FOUND MYPROG` → `LOADING`.

Bare `LOAD` (no name) = loads **next** program from current position.

## Verify (optional, after save)
```basic
VERIFY "MYPROG"
```
`OK` = good. `VERIFY ERROR` = bad write, redo.

## Several programs — reach specific one

Two ways:

**By name (easy):** `LOAD "MYPROG"` scans forward from current tape position, checks each header. Prints `FOUND <name>` for each. If name ≠ target, keeps searching; matches → loads. Tape only moves forward, so rewind first if target is behind current position.

**Skip manually:** When `FOUND <name>` appears and it's NOT the one you want, press **C= (Commodore key)** to skip it and continue searching next header.

**Tape counter (fast):** Note Datasette counter number where each program starts. Rewind/FF to that count, then `LOAD ""` (or `LOAD`) to grab next program at that spot. Faster than scanning whole tape.

## Specifics
- Device 1 = cassette. Kernal: `SETLFS` `$FFBA`, `SETNAM` `$FFBD`, `LOAD` `$FFD5`, `SAVE` `$FFD8`, `VERIFY` via LOAD with A=1.
- Tape buffer: `$033C–$03FB` (828–1019).
- SAVE secondary address: 0=relocatable, bit `$02` set = write End-of-Tape marker after.
- Tape speed fixed ~300 baud (slow — turbo loaders speed up but need extra software).