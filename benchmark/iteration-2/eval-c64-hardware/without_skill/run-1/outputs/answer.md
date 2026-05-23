## C64 Power Supply ("Brick")

**Outputs two rails:**

- **+5V DC regulated** — powers all digital logic (CPU 6510, RAM, ROM, CIA 6526, VIC-II, PLA, etc.). ~1.5A.
- **9V AC** (unregulated) — feeds onboard circuits: SID audio section, the 9V→raw DC for the 5V VIC supply path, and the TOD (time-of-day) clock timing reference in the CIAs. ~1A.

7-pin DIN connector. The 9V AC is two pins; 5V DC + GND the rest.

**Failure mode — the killer:**

Original brick is **epoxy-potted, sealed, non-repairable, no overvoltage protection**. The 7805-style **5V regulator fails shorted**. When it dies it stops regulating and dumps the **raw rectified input (~9–12V+ DC)** straight onto the 5V rail.

Result: every chip on the 5V rail sees overvoltage. **RAM (4164s) and the CPU/PLA/CIA cook.** Classic dead-C64 symptom: black screen, blinking screen, or garbage — replaced parts die again until the PSU is tossed.

Why it's nasty: potting **traps heat** → accelerates regulator degradation, and the sealed case means you can't inspect or fix it.

**Mitigation (real-world):**
- Toss the brick. Use a modern regulated replacement (e.g. modern "C64 PSU" with crowbar/overvoltage cutoff).
- Or fit a **"Computer Saver"** dongle inline on the DIN — monitors 5V rail, cuts power if it exceeds ~5.3–5.5V before chips fry.

**Software cannot detect or prevent this** — overvoltage hits hardware directly, no register reports it. No PEEK/POKE defense exists. The 9V AC *is* readable indirectly via CIA TOD behavior, but that's unrelated to the failure.