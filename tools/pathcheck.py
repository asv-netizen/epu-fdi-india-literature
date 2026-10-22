import os
import re

ROOT = r"C:\Users\HP\Documents\LT-2"
docs = ["README.md", "gap-statement.md", "data-sources.md", "methodology-key.md", "literature-map.md"]
bad, checked = [], 0
for d in docs:
    txt = open(os.path.join(ROOT, d), encoding="utf-8").read()
    for m in re.finditer(r"`((?:papers|notes|tools)/[^`]+)`", txt):
        rel = m.group(1).split(" (")[0]
        checked += 1
        if not os.path.exists(os.path.join(ROOT, rel)):
            bad.append((d, rel))

print(f"paths checked: {checked}, broken: {len(bad)}")
for d, rel in bad:
    print(f"  {d}: {rel}")

print()
for d in docs:
    p = os.path.join(ROOT, d)
    print(f"  {d:22} {os.path.getsize(p):7} bytes")
