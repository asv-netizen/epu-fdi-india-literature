"""Delete files not referenced by the state file. Keeps Z-existing (indexed separately)."""
import json
import os

ROOT = r"C:\Users\HP\Documents\LT-2"
state = json.load(open(os.path.join(ROOT, "tools", "acquired.json"), encoding="utf-8"))
keep = set()
for v in state.values():
    for k in ("note", "pdf"):
        if v.get(k):
            keep.add(v[k].replace("notes/", "").replace("papers/", ""))

removed = []
for top in ("notes", "papers"):
    base = os.path.join(ROOT, top)
    for cat in os.listdir(base):
        if cat == "Z-existing":
            continue
        cdir = os.path.join(base, cat)
        if not os.path.isdir(cdir):
            continue
        for f in os.listdir(cdir):
            rel = f"{cat}/{f}"
            if rel not in keep:
                os.remove(os.path.join(cdir, f))
                removed.append(rel)

print(f"removed {len(removed)} stale files")
for r in removed:
    print("  ", r)

n_note = sum(len(os.listdir(os.path.join(ROOT, "notes", c)))
             for c in os.listdir(os.path.join(ROOT, "notes")))
n_pdf = sum(len(os.listdir(os.path.join(ROOT, "papers", c)))
            for c in os.listdir(os.path.join(ROOT, "papers")))
print(f"\nnotes on disk now: {n_note}")
print(f"pdfs  on disk now: {n_pdf}")
