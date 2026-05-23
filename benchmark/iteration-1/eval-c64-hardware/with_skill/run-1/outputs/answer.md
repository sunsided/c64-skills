**Power LED on but blank = digital logic running, video chain dead or CPU not booting.**

## Check first — power supply

Old brick = #1 killer. Internal 5V regulator drifts high as it ages, overvolts logic rail, cooks RAM/PLA/chips together.
- Meter the +5V DC rail. Should be ~5.0V. >5.2V = brick bad, stop, replace before more chips die.
- Check 9V AC present too (CN7 pins 6/7).

## Most likely chips (service-manual order)

Blank-screen-on-power-up suspect list:

1. **Power supply** (above) — first.
2. **KERNAL ROM U4** — CPU resets, vectors $FFFC/$FFFD into KERNAL, finds nothing → never sets up screen.
3. **PLA U17** — bank-switch logic. Dead PLA = no ROM/RAM decode = no boot. Runs hot, notorious failure. Also prime warm-up suspect.
4. **CPU 6510 U7** — no fetch, nothing.
5. **VIC-II U19** — no border/no video. Also makes DRAM RAS/CAS + PHI0 system clock; dead VIC = no clock = whole machine stops.
6. **DRAM U9–U12 / U21–U24** — bad RAM. (Usually garbage/"OUT OF MEMORY" not full blank, but can hang boot.)
7. **U8 7406** — reset/serial buffer.

## Fast triage steps

- **Reseat socketed chips** (PLA, ROMs, CPU, VIC, CIAs). Bad socket contacts common after decades.
- **Press chips down** while powered (carefully) — intermittent = bad socket/cracked solder.
- **Feel chip temps** — PLA + VIC run warm normal; ice-cold CPU or scorching PLA = suspect.
- **Reset test** — RESTORE dead + no reset → also check **U20 (556)** reset one-shot; if /RES never releases, CPU held in reset = blank.
- **Border color clue:** truly black/no border at all = VIC not even running (clock/VIC/power). Border but no text = RAM/ROM/CPU side.

## Confirm by swap

Got a known-good board or chips? Socketed parts (PLA, ROMs, CPU, VIC) swap easy — quickest diagnosis. PLA + DRAM are the two most-replaced parts on a dead C64.

Order: **brick voltage → reseat → swap PLA → swap KERNAL → swap VIC/CPU → DRAM.**