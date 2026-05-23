# c64-skills benchmark

Reproducible benchmark + tuning harness for the `c64-*` skill set, built with the
`skill-creator` workflow. Two axes were measured: **routing** (does the right
skill fire) and **functional output quality** (is a triggered skill's answer
correct vs baseline Claude), plus a per-skill **description optimizer** pass.

Model under test: `claude-opus-4-7`. All harnesses drive `claude -p`.

## Layout

```
benchmark/
├── run_routing.py            # routing benchmark (forced-choice skill selection)
├── run_functional.py         # with-skill vs baseline answer generation
├── run_grading.py            # strict assertion grader for functional runs
├── routing_evals.json        # 62 labeled routing queries (+ acceptable alternates)
├── functional_evals.json     # 18 mainstream tasks + fact-checkable assertions
├── functional_evals_hard.json# 14 long-tail/obscure tasks + assertions
├── trigger-evals/            # per-skill should/should-not sets for run_loop
├── iteration-1/              # routing results + mainstream functional + benchmark.json
├── iteration-2/              # long-tail functional + benchmark.json
└── phase4/                   # run_loop description-optimizer logs
```

## Reproduce

```sh
# routing (reads the 18 live descriptions, routes each query 3x for stability)
python3 run_routing.py routing_evals.json iteration-1/routing_results.json

# functional: generate answers (with-skill vs baseline) then grade
python3 run_functional.py functional_evals.json iteration-1
python3 run_grading.py iteration-1
python3 functional_evals_hard.json iteration-2   # (see run_functional.py args)

# aggregate + view (from the skill-creator dir)
python3 -m scripts.aggregate_benchmark <repo>/benchmark/iteration-1 --skill-name c64
python3 <skill-creator>/eval-viewer/generate_review.py iteration-1 --benchmark iteration-1/benchmark.json
```

Scripts derive the repo path from their own location, so they read whatever the
current `SKILL.md` descriptions are — re-run after editing a description.

## Results (2026-05-23)

### Routing — 62 queries × 3 passes
**100% accuracy, zero variation across passes.** Every query routed to the
correct skill or a defensible `acceptable` alternate. Strict primary-hit
(ignoring alternates) 96.8%. The descriptions disambiguate the 18 overlapping
skills cleanly.

### Functional — with-skill vs baseline (no skill)
| Set | With skill | Baseline | Δ pass | Time | Tokens |
|-----|-----------|----------|--------|------|--------|
| iter-1 mainstream (18) | 99% | 99% | **+0.0** | 13.1s | 21.7k |
| iter-2 long-tail (14) | 100% | 100% | **+0.0** | — | — |
| baseline iter-1 | — | — | — | 21.2s | 18.7k |

**No correctness lift.** Baseline Opus 4.7 already answers C64 questions
correctly to the register-bit level — even obscure facts (SID ADSR millisecond
table, PAL/NTSC raster cycle counts, the exact Bad Line condition, `$030C–$030F`
SYS register slots, `$01` bank configs). The benchmark ceiling is 100% with or
without the skills. Measurable skill effect: **~8s lower latency** (answers from
the gist instead of deriving) at a **~3k-token** context cost.

### Triggering reality (run_loop)
The forced-choice routing test hits 100%, but `run_loop` (which tests the *real*
"should I spontaneously consult this skill?" decision in isolation) shows
**recall 0–33%**: Opus usually declines the skill because it judges it can answer
unaided — which the functional results confirm is correct. Pushier, intent-led
descriptions raise triggering, but that fights a correct self-assessment for
little correctness gain. The set keeps lean descriptions by design.

### Fact-check sweep
Cross-checking every load-bearing claim in all 18 `SKILL.md` files against their
verbatim `references/` caught **8 errors**, all fixed (commit `4c93c23`): the
worst were `$01=$33` mis-mapping `$A000` as RAM (it's BASIC ROM) and a `$DC00`
control-port number swap; plus a `SYS 64759`→`64738` cold-reset fix (an OCR error
inherited from the User's Guide etext).

## Takeaway
For the C64 — among the most thoroughly documented machines ever — Opus 4.7 is
already an expert. These skills add value as a **curated, citable, verbatim manual
corpus**, clean **routing/disambiguation**, **provenance**, and minor **latency** —
not as knowledge augmentation. The most concrete win from benchmarking was the
fact-check sweep that hardened the skills' accuracy.
