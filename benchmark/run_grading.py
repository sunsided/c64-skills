#!/usr/bin/env python3
"""Grade each functional run's answer against its assertions via claude -p.

Writes grading.json (schema: expectations[{text,passed,evidence}] + summary) into
each run-1 dir. Assertions are objective C64 facts; grade strictly (a wrong
register address or value = fail).
"""
import json, re, subprocess, sys
from pathlib import Path
import concurrent.futures as cf

WS = Path(__file__).resolve().parent
ITER = WS / (sys.argv[1] if len(sys.argv) > 1 else "iteration-1")
MODEL = "claude-opus-4-7"

GRADER = """You are a strict grader for Commodore 64 technical answers. Given an ANSWER and a list of ASSERTIONS, decide for EACH assertion whether the answer satisfies it.

Rules:
- Judge only what the answer actually says. Do not give credit for things it omits.
- C64 facts must be CORRECT to pass: a wrong register address, POKE location, bit, or value means that assertion FAILS even if the answer is confident.
- Accept equivalent forms (hex $D015 == decimal 53269; "location 53280" == "$D020").
- Be fair: if the assertion's substance is present and correct, pass it.

Return ONLY a JSON object, no other text:
{"expectations":[{"text":"<assertion>","passed":true|false,"evidence":"<short quote or reason>"}]}

ASSERTIONS:
%s

ANSWER:
%s
"""

def grade(rundir):
    meta = json.loads((rundir.parent / "eval_metadata.json").read_text())
    assertions = meta["assertions"]
    answer = (rundir / "outputs" / "answer.md").read_text()
    prompt = GRADER % (json.dumps(assertions, indent=2), answer[:14000])
    try:
        r = subprocess.run(["claude","-p","--output-format","json","--model",MODEL,prompt],
                           capture_output=True, text=True, timeout=180)
        content = json.loads(r.stdout).get("result","")
        m = re.search(r"\{.*\}", content, re.S)
        exps = json.loads(m.group(0))["expectations"]
    except Exception as e:
        exps = [{"text": a, "passed": False, "evidence": f"<grader error: {e}>"} for a in assertions]
    # normalize: ensure all assertions present
    passed = sum(1 for e in exps if e.get("passed"))
    total = len(exps)
    grading = {"expectations": exps,
               "summary": {"passed": passed, "failed": total-passed, "total": total,
                           "pass_rate": round(passed/total,3) if total else 0.0}}
    (rundir / "grading.json").write_text(json.dumps(grading, indent=2))
    return f"{rundir.parent.parent.name}/{rundir.parent.name}: {passed}/{total}"

def main():
    rundirs = sorted(ITER.glob("eval-*/*/run-1"))
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for f in cf.as_completed([ex.submit(grade, rd) for rd in rundirs]):
            print("  ", f.result())
    print(f"\ngraded {len(rundirs)} runs")

if __name__ == "__main__":
    main()
