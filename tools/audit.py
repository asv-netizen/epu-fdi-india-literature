import json, sys, re
sys.path.insert(0, r"C:\Users\HP\Documents\LT-2\tools")
from targets import TARGETS

state = json.load(open(r"C:\Users\HP\Documents\LT-2\tools\acquired.json", encoding="utf-8"))


def sim(a, b):
    A, B = set(re.sub(r"[^a-z0-9]+", " ", a.lower()).split()), set(re.sub(r"[^a-z0-9]+", " ", b.lower()).split())
    return len(A & B) / max(len(A | B), 1)


bad, good, missing = [], 0, []
for t in TARGETS:
    key = f"{t['cat']}|{t['title'][:60]}"
    v = state.get(key)
    if not v:
        missing.append(t["title"])
        continue
    s = sim(t["title"], v.get("title") or "")
    if s < 0.5:
        bad.append((round(s, 2), t["title"][:70], (v.get("title") or "")[:70], v.get("doi"), key))
    else:
        good += 1

print(f"good={good} bad={len(bad)} missing={len(missing)} total={len(TARGETS)}")
print("\n--- MISMATCHES ---")
for s, want, got, doi, key in sorted(bad):
    print(f"{s}  WANT: {want}")
    print(f"        GOT : {got}  [{doi}]")
    print(f"        KEY : {key}")
if missing:
    print("\n--- MISSING ---")
    for m in missing:
        print("   ", m)
