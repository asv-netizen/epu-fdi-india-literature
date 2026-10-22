import json, os
ROOT = r"C:\Users\HP\Documents\LT-2"
state = json.load(open(os.path.join(ROOT, "tools", "acquired.json"), encoding="utf-8"))
state_notes = {(v.get("note") or "").replace("notes/", "", 1) for v in state.values()}

for cat in ["A-theory", "B-measurement", "C-rq1-longrun", "E-rq3-horizon"]:
    disk = sorted(os.listdir(os.path.join(ROOT, "notes", cat)))
    print("=" * 80)
    print(cat, f"({len(disk)} files)")
    for f in disk:
        mark = "  " if f in state_notes else "ST"
        print(f"  {mark} {f}")
