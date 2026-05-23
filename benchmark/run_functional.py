#!/usr/bin/env python3
"""Functional benchmark: with-skill vs baseline (no skill) for each c64-* skill.

For each eval, runs the same task twice via `claude -p --output-format json`:
  with_skill  -> the skill's SKILL.md body is provided as context
  without_skill -> baseline, just the task
The closing instruction is identical in both, so the only variable is the skill.
Emits the directory layout the skill-creator aggregator + eval-viewer expect.
"""
import json, re, subprocess, sys, time
from pathlib import Path
import concurrent.futures as cf

REPO = Path(__file__).resolve().parent.parent
WS = Path(__file__).resolve().parent
MODEL = "claude-opus-4-7"
EVALS_FILE = Path(sys.argv[1]) if len(sys.argv) > 1 else WS / "functional_evals.json"
ITER = WS / (sys.argv[2] if len(sys.argv) > 2 else "iteration-1")

CLOSER = ("Answer concisely and correctly, with C64-accurate specifics: exact "
          "register addresses, POKE/PEEK locations or assembly, and values. Give "
          "runnable code where the task asks for it.")

def skill_body(name):
    txt = (REPO / name / "SKILL.md").read_text()
    # drop frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", txt, count=1, flags=re.S)
    return body.strip()

def build_prompt(eval, with_skill):
    if with_skill:
        return (f"You are assisting a user with the Commodore 64. You have the following "
                f"skill available; use it to answer accurately. (Deeper reference files exist "
                f"on disk under {REPO}/{eval['skill']}/references/, but answer from the skill "
                f"content below.)\n\n===SKILL {eval['skill']}===\n{skill_body(eval['skill'])}\n"
                f"===END SKILL===\n\nUser request: {eval['prompt']}\n\n{CLOSER}")
    return f"User request: {eval['prompt']}\n\n{CLOSER}"

def run_cfg(eval, with_skill):
    cfg = "with_skill" if with_skill else "without_skill"
    rundir = ITER / f"eval-{eval['id']}" / cfg / "run-1"
    (rundir / "outputs").mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(eval, with_skill)
    t0 = time.time()
    try:
        r = subprocess.run(["claude","-p","--output-format","json","--model",MODEL,prompt],
                           capture_output=True, text=True, timeout=300)
        d = json.loads(r.stdout)
        answer = d.get("result","")
        u = d.get("usage",{})
        toks = (u.get("input_tokens",0)+u.get("output_tokens",0)
                +u.get("cache_creation_input_tokens",0)+u.get("cache_read_input_tokens",0))
        dur = d.get("duration_ms", int((time.time()-t0)*1000))
    except Exception as e:
        answer = f"<ERROR: {e}>"; toks=0; dur=int((time.time()-t0)*1000)
    (rundir / "outputs" / "answer.md").write_text(answer)
    (rundir / "timing.json").write_text(json.dumps(
        {"total_tokens": toks, "duration_ms": dur, "total_duration_seconds": round(dur/1000,1)}, indent=2))
    # eval_metadata.json at config-dir level (viewer reads run_dir.parent)
    meta = {"eval_id": eval["id"], "eval_name": f"{eval['id']} ({cfg})",
            "prompt": eval["prompt"], "assertions": eval["assertions"]}
    (ITER / f"eval-{eval['id']}" / cfg / "eval_metadata.json").write_text(json.dumps(meta, indent=2))
    return f"{eval['id']}/{cfg}: {len(answer)} chars, {toks} tok, {dur}ms"

def main():
    evals = json.loads(EVALS_FILE.read_text())["evals"]
    jobs = [(e, ws) for e in evals for ws in (True, False)]
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(run_cfg, e, ws) for e, ws in jobs]
        for f in cf.as_completed(futs):
            print("  ", f.result())
    print(f"\ndone: {len(jobs)} runs into {ITER}")

if __name__ == "__main__":
    main()
