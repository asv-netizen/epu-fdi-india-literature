import json, os
from collections import Counter
ROOT = r"C:\Users\HP\Documents\LT-2"
state = json.load(open(os.path.join(ROOT, "tools", "acquired.json"), encoding="utf-8"))
c = Counter(v.get("note") for v in state.values())
print("duplicate note paths:")
for p, n in c.items():
    if n > 1:
        print(f"  x{n}  {p}")
        for k, v in state.items():
            if v.get("note") == p:
                print(f"        <- {k}")
print()
print("records:", len(state), "unique notes:", len(c))
for d in sorted(os.listdir(os.path.join(ROOT, "notes"))):
    print(f"  notes/{d}: {len(os.listdir(os.path.join(ROOT,'notes',d)))}")
for d in sorted(os.listdir(os.path.join(ROOT, "papers"))):
    print(f"  papers/{d}: {len(os.listdir(os.path.join(ROOT,'papers',d)))}")
