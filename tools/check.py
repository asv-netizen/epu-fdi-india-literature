"""Final integrity check: every state record has a note, notes are non-empty, no orphans."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
state = json.load(open(os.path.join(ROOT, "tools", "acquired.json"), encoding="utf-8"))

problems = []
notes_on_disk = set()
pdfs_on_disk = set()

for d in os.listdir(os.path.join(ROOT, "notes")):
    for f in os.listdir(os.path.join(ROOT, "notes", d)):
        p = os.path.join(ROOT, "notes", d, f)
        notes_on_disk.add(f"{d}/{f}")
        if os.path.getsize(p) < 200:
            problems.append(f"TINY NOTE {d}/{f} ({os.path.getsize(p)} bytes)")

for d in os.listdir(os.path.join(ROOT, "papers")):
    for f in os.listdir(os.path.join(ROOT, "papers", d)):
        p = os.path.join(ROOT, "papers", d, f)
        pdfs_on_disk.add(f"{d}/{f}")
        if not f.lower().endswith(".pdf") or os.path.getsize(p) < 20000:
            problems.append(f"BAD PDF {d}/{f} ({os.path.getsize(p)} bytes)")

missing_notes, missing_pdfs = [], []
for k, v in state.items():
    n = (v.get("note") or "").replace("notes/", "", 1)
    if n and n not in notes_on_disk:
        missing_notes.append((k, n))
    if v.get("ok") and v.get("pdf"):
        p = v["pdf"].replace("papers/", "", 1)
        if p not in pdfs_on_disk:
            missing_pdfs.append((k, p))

state_notes = {(v.get("note") or "").replace("notes/", "", 1) for v in state.values()}
state_pdfs = {(v.get("pdf") or "").replace("papers/", "", 1) for v in state.values() if v.get("pdf")}
orphan_notes = sorted(n for n in notes_on_disk if n not in state_notes)
orphan_pdfs = sorted(p for p in pdfs_on_disk if p not in state_pdfs)

print(f"state records      : {len(state)}")
print(f"notes on disk      : {len(notes_on_disk)}")
print(f"pdfs on disk       : {len(pdfs_on_disk)}")
print(f"records with pdf   : {sum(1 for v in state.values() if v.get('ok'))}")
print(f"records w/ abstract: {sum(1 for v in state.values() if v.get('has_abstract'))}")
print()
print(f"missing notes      : {len(missing_notes)}")
for k, n in missing_notes[:10]:
    print("   ", k[:55], "->", n)
print(f"missing pdfs       : {len(missing_pdfs)}")
for k, p in missing_pdfs[:10]:
    print("   ", k[:55], "->", p)
print(f"orphan notes       : {len(orphan_notes)}")
for n in orphan_notes[:10]:
    print("   ", n)
print(f"orphan pdfs        : {len(orphan_pdfs)}")
for p in orphan_pdfs[:10]:
    print("   ", p)
print(f"problems           : {len(problems)}")
for p in problems[:15]:
    print("   ", p)

print("\n--- per category ---")
from collections import Counter
c = Counter(v.get("cat") for v in state.values())
for cat in sorted(c):
    rows = [v for v in state.values() if v.get("cat") == cat]
    print(f"  {cat:22} n={c[cat]:3} pdf={sum(1 for v in rows if v.get('ok')):3}")
