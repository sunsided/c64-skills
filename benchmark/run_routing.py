#!/usr/bin/env python3
"""Routing benchmark for the c64-* skill set.

Reads each skill's name+description LIVE from its SKILL.md, then for every labeled
query asks a fresh `claude -p` instance to pick the single best skill (or 'none').
Scores predicted vs expected(+acceptable) and writes results.json + a confusion
matrix. Re-run after editing descriptions to measure improvement.
"""
import json, os, re, subprocess, sys, concurrent.futures as cf
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODEL = "claude-opus-4-7"
SKILLS = ["c64","c64-basic","c64-graphics","c64-sprites","c64-vic-ii","c64-sid",
          "c64-assembly","c64-kernal","c64-memory-map","c64-cia","c64-io","c64-disk",
          "c64-tape","c64-game-ports","c64-petscii","c64-keyboard","c64-hardware","c64-disassembly"]

def load_desc(name):
    txt = (REPO / name / "SKILL.md").read_text()
    m = re.search(r"\ndescription: >-\n(.*?)\n---", txt, re.S)
    if not m:
        m = re.search(r"\ndescription:\s*(.*?)\n[a-z_]+:", txt, re.S)
    body = m.group(1) if m else ""
    return " ".join(line.strip() for line in body.strip().splitlines())

def router_prompt(query, descs):
    lines = ["You are the skill-selection layer for a Commodore 64 assistant.",
             "Below are the available skills (name: description). Given the USER MESSAGE,",
             "decide which SINGLE skill is the best one to consult, exactly as Claude would",
             "when choosing a skill to load. If no skill is a good fit (the request is not",
             "about the C64 or no skill covers it), answer none.",
             "", "AVAILABLE SKILLS:"]
    for n in SKILLS:
        lines.append(f"- {n}: {descs[n]}")
    lines += ["", f"USER MESSAGE: {query}", "",
              "Answer with ONLY the skill name (e.g. c64-sid) or the word none. No other text."]
    return "\n".join(lines)

def parse(out):
    out = out.strip().lower()
    # exact line match first
    for n in sorted(SKILLS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(n)}\b", out):
            return n
    if "none" in out:
        return "none"
    return out.split("\n")[0][:40] if out else "<empty>"

def run_one(item, descs):
    p = router_prompt(item["query"], descs)
    try:
        r = subprocess.run(["claude","-p","--model",MODEL,p],
                           capture_output=True, text=True, timeout=120)
        pred = parse(r.stdout)
    except Exception as e:
        pred = f"<error:{e}>"
    ok = (pred == item["expected"]) or (pred in item.get("acceptable", []))
    return {"id": item["id"], "query": item["query"], "expected": item["expected"],
            "acceptable": item.get("acceptable", []), "predicted": pred, "correct": ok}

def main():
    evals = json.loads((Path(sys.argv[1])).read_text())["queries"] if len(sys.argv)>1 \
            else json.loads((Path(__file__).parent/"routing_evals.json").read_text())["queries"]
    out_path = Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).parent/"iteration-1"/"routing_results.json"
    descs = {n: load_desc(n) for n in SKILLS}
    results = [None]*len(evals)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, e, descs): i for i,e in enumerate(evals)}
        for f in cf.as_completed(futs):
            i = futs[f]; results[i] = f.result()
            r = results[i]
            print(f"  [{ 'OK ' if r['correct'] else 'XX ' }] q{r['id']:>2}: {r['expected']:<16} <- {r['predicted']}")
    # metrics
    n = len(results); ncorr = sum(r["correct"] for r in results)
    # per-skill recall (over queries whose expected == skill)
    per = {}
    for s in SKILLS+["none"]:
        rel = [r for r in results if r["expected"]==s]
        if rel:
            per[s] = {"n": len(rel), "correct": sum(x["correct"] for x in rel)}
    # confusion: expected -> predicted counts for the wrong ones
    confusion = {}
    for r in results:
        if not r["correct"]:
            confusion.setdefault(r["expected"], {}).setdefault(r["predicted"], 0)
            confusion[r["expected"]][r["predicted"]] += 1
    summary = {"total": n, "correct": ncorr, "accuracy": round(ncorr/n,3),
               "per_skill_recall": per, "confusion_misroutes": confusion, "results": results}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"\nACCURACY: {ncorr}/{n} = {ncorr/n:.1%}")
    print("MISROUTES (expected -> got):")
    for exp, gots in sorted(confusion.items()):
        for got, c in gots.items():
            print(f"  {exp:<16} -> {got}  (x{c})")
    print(f"\nwrote {out_path}")

if __name__ == "__main__":
    main()
