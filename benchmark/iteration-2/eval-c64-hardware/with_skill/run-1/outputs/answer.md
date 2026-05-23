**Brick output:** two rails into C64.
- **+5V DC regulated** — direct to all digital logic.
- **9V AC** — rectified on-board to +12V (VR1 7812 → VIC/SID/audio), +5V CAN (VR2 7805 → video + clock), and 9V DC unregulated (cassette motor, RF mod).

Connector = 7-pin DIN (CN7). 5V on pins 5/1, 9V AC on pins 6/7.

**Killer failure:** brick's internal 5V regulator drifts **high** as it ages. That overvolted 5V feeds logic rails direct — fries RAM, PLA (U17), and other chips at once. No protection between brick and chips.

Suspect brick first on multi-chip or warm-up/intermittent deaths. Fix: replace with modern regulated supply (or add overvoltage crowbar). Test 5V rail under load before trusting old brick.