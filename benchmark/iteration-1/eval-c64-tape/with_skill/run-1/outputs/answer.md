**Save:**

```basic
SAVE "NAME"      : REM device 1 = default, no number needed
SAVE "NAME",1,2  : REM also write EOT marker after (clean stop on later read)
```

KERNAL prompts **PRESS RECORD & PLAY ON TAPE** (waits on SENSE line, pin F-6).

**Load back:**

```basic
LOAD "NAME"      : REM scan forward for header "NAME", load it
LOAD "NAME",1    : REM device 1 explicit
LOAD "",1,1      : REM first program, to ORIGINAL address (ML/data)
```

Screen blanks to border color while searching. On hit: **FOUND NAME**, then **LOADING**. Type `RUN` after.

Verify write good: `VERIFY "NAME"`.

**Get specific program when several on tape:**

Tape = sequential, **no directory**, no random access. Options:

1. **`LOAD "NAME"`** — scans headers *forward* from current position until name matches. Only forward; rewind first if target is behind you.
2. **Step through.** Repeated `LOAD` (no name) loads NEXT program; watch each **FOUND xxxx** message to see names one by one as tape advances.
3. **Tape counter + own written log.** Manuals assume you note counter value where each file starts — spool to that number, then `LOAD`.

No way to jump backward without rewinding. No `LOAD"$"` — `$` means nothing on tape (that's disk DOS only).