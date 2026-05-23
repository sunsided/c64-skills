# C64 Skills

A cluster of Claude skills for working with the **Commodore 64** — its BASIC, its
6510 machine language, the VIC-II / SID / CIA chips, I/O and peripherals, the
character set and keyboard, the hardware, and reverse-engineering existing code.
Every skill carries the relevant slices of the original Commodore manuals as its
own `references/`, with the gist authored up front in `SKILL.md`. All skills share
a `c64-` prefix so they group together once installed.

These are platform skills: self-contained, but they pair naturally with the
generic [`sunsided/6502-skills`](https://github.com/sunsided/6502-skills) (6502 /
65C02 / 65816 instruction set, addressing modes, cross-platform memory maps) when
you want CPU-level depth beyond the C64's 6510. That repo is **optional**, not a
dependency.

## The skills

| Skill | What it covers |
|-------|----------------|
| **`c64`** | Orientation & router: architecture at a glance, the memory/IO map, chip locations, and a "which skill answers this" index. Start here for broad or vague questions. |
| **`c64-basic`** | Commodore BASIC V2: programming rules, constants/variables/arrays, operators & precedence, strings, INPUT/GET, crunching, and the full alphabetical keyword/command/function reference. |
| **`c64-petscii`** | The three character-code systems — PETSCII vs screen (display) codes vs ASCII/CHR$ — cursor & color control codes, reverse video, and building text UIs with PETSCII graphics. |
| **`c64-keyboard`** | The keyboard and screen editor: every special key (Commodore/C=, CTRL, RUN/STOP, RESTORE, SHIFT, CLR/HOME, INST/DEL, cursor, f1–f8) and editor behavior (quote mode, insert mode). |
| **`c64-graphics`** | VIC-II graphics from the application view: character/bitmap modes, multicolor & ECM, custom characters, smooth scrolling, screen/color/character memory, video bank selection. |
| **`c64-sprites`** | Hardware sprites (MOBs): definition, pointers, enable, X/Y position incl. the >255 MSB, color, multicolor, X/Y expansion, priority, and collision detection. |
| **`c64-vic-ii`** | The 6566/6567/6569 video chip as a cycle-exact hardware/timing reference: full register map, palette, raster, Bad Lines, all eight graphics modes, sprite hardware, borders, light pen, interrupts, PAL vs NTSC, and demo effects (FLD/FLI/etc.). |
| **`c64-sid`** | The 6581 SID sound chip: register map, 3 voices, 4 waveforms, the ADSR envelope, pulse width, the multimode filter, master volume, ring modulation & sync, and note/frequency tables. |
| **`c64-assembly`** | Writing 6510 machine language on the C64: the `$00/$01` I/O port and banking, registers/flags, addressing modes, the instruction set, the 64MON monitor, where to put ML, and calling it from BASIC (SYS/USR). |
| **`c64-kernal`** | The KERNAL ROM jump table and user-callable routines (`$FFxx`): purpose, register I/O, the standard OPEN/CHKOUT/CHROUT/CLOSE pattern, error codes, and key BASIC ROM entry points. |
| **`c64-memory-map`** | The complete memory map and banking: zero page, stack, screen/color RAM, the `$D000-$DFFF` I/O area, the ROMs, the `$00/$01` + PLA bank logic, and VIC bank selection. |
| **`c64-cia`** | The two 6526 CIA chips (CIA1 `$DC00`, CIA2 `$DD00`): data ports, timers A/B, the TOD clock, the serial shift register, and the interrupt control register — keyboard, joysticks, serial bus, user port, IRQ/NMI. |
| **`c64-io`** | The I/O / device & file model: logical device numbers, OPEN/PRINT#/INPUT#/GET#/CLOSE, secondary addresses, the serial IEC bus, printer, modem, RS-232, the user port, the expansion (cartridge) port. |
| **`c64-disk`** | Using a Commodore disk drive (1541 family): load/save, the directory (`LOAD"$",8`), the command channel (channel 15) for format/scratch/rename, the error channel, and file types. |
| **`c64-tape`** | The Datasette: device 1, LOAD/SAVE/VERIFY, the sequential (no random-access directory) nature of tape, the tape buffer, and finding files. |
| **`c64-game-ports`** | The two control ports: reading joysticks (and which port is "player 1"), paddles (via the SID POT registers), and the light pen (via VIC). |
| **`c64-hardware`** | The physical machine and servicing: specifications, the chip complement, circuit theory, power supply, board revisions, connector pinouts, the PLA, and troubleshooting orientation. |
| **`c64-disassembly`** | A workflow for reverse-engineering `.prg`/cartridge/dump code: the load address, the BASIC stub & SYS entry, classifying every address (RAM/ROM/IO), recognizing KERNAL calls and idioms, and separating code from data. |

## Installing

Each skill is a directory with a `SKILL.md`, following the [Agent Skills](https://agentskills.io)
open standard, so the same files work across Claude Code, opencode, Kilo Code,
Codex, and any other tool that implements it. You point your agent at the skill
directories; what differs per agent is *which* directory it scans.

### Quick install — `install.sh`

`install.sh` symlinks (or copies) the `c64-*` skills into the right place:

```sh
./install.sh --claude            # Claude Code, personal      → ~/.claude/skills/
./install.sh --agents            # open standard (opencode/Kilo/Codex) → ~/.agents/skills/
./install.sh --claude --agents   # both at once
./install.sh --opencode --kilo   # each agent's own global dir
./install.sh --to PATH           # any explicit directory, e.g. a project's .claude/skills
./install.sh --agents --copy     # copy instead of symlink (Windows, or to vendor into a repo)
```

Symlink is the default, so editing a skill here updates every install. `--help`
lists all options. After installing, restart the agent; in Claude Code run
`/skills` to confirm they loaded.

### Where each agent looks

| Agent | Global (all projects) | Per project |
|-------|-----------------------|-------------|
| **Claude Code** | `~/.claude/skills/<name>/` | `<project>/.claude/skills/<name>/` |
| **opencode** | `~/.agents/skills/`, `~/.config/opencode/skills/`, `~/.claude/skills/` | `.agents/skills/`, `.opencode/skills/`, `.claude/skills/` |
| **Kilo Code** | `~/.agents/skills/`, `~/.kilo/skills/`, `~/.claude/skills/` | `.agents/skills/`, `.kilo/skills/`, `.claude/skills/` |
| **Codex** | `~/.agents/skills/` | `.agents/skills/` (cwd up to repo root) |

`.agents/skills/` is the common open-standard location read by opencode, Kilo, and
Codex; `.claude/skills/` is Claude Code's. To install into a specific project
rather than globally, use `install.sh --to PATH` pointing at that project's
`.agents/skills/` or `.claude/skills/`.

### Manual install

Without the script, copy or symlink each `c64-*` directory into one of the
locations above. For Claude Code, personal install:

```sh
for s in c64 c64-*/; do ln -s "$PWD/${s%/}" ~/.claude/skills/; done
```

## How they fit together

```
                              c64   ← orientation & router
                               │
   ── language & text ──┬───── hardware & chips ─────┬── machine code ──
   c64-basic            │   c64-vic-ii  c64-sid       │  c64-assembly
   c64-petscii          │   c64-cia     c64-memory-map│  c64-kernal
   c64-keyboard         │   c64-hardware              │
                        │                             │
   ── graphics ──       │   ── I/O & peripherals ──   │
   c64-graphics         │   c64-io   c64-disk         │
   c64-sprites          │   c64-tape c64-game-ports   │
                        │                             │
                        └────────── c64-disassembly ──┘
                              (uses all of the above to read existing code)
```

`c64-disassembly` is the integrator: it leans on `c64-assembly` for instruction
semantics and on `c64-memory-map` / `c64-kernal` / `c64-vic-ii` / `c64-sid` /
`c64-cia` to turn raw addresses into meaning.

## Layout

Each skill is a directory with a `SKILL.md` (the always-loaded gist + trigger
description) and a `references/` folder of detail files loaded only when needed
(progressive disclosure). The `references/` files are lightly-cleaned verbatim
slices of the source manuals; the master copies live untouched in `reference/`.

## Sources

The reference material is sliced from public-domain / community electronic
editions of the Commodore manuals, kept in `reference/`:

- *Commodore 64 Programmer's Reference Guide* (Project 64 etext)
- *Commodore 64 User's Guide* (Project 64 etext)
- *Commodore 64 Service Manual* (Project 64 etext)
- *The MOS 6567/6569 video controller (VIC-II) and its application in the
  Commodore 64* — Christian Bauer
- *C64 PLA logic equations* — Marko Mäkelä et al.

Originals collected from <https://www.zimmers.net/cbmpics/cbm/c64/>.

## Authoring

Built and iterated with the `skill-creator` workflow. Each `SKILL.md` gist was
written against — and cross-checked with — the sliced primary sources in its own
`references/`.
