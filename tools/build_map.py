"""Generate literature-map.md from the verified state file."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "tools", "acquired.json")
state = json.load(open(STATE, encoding="utf-8"))

ORDER = [
 ("A-theory", "A. Theory: why uncertainty stops investment"),
 ("B-measurement", "B. Measurement: building the uncertainty indices"),
 ("C-rq1-longrun", "C. RQ1 - Long-run relation and structural breaks"),
 ("D-rq2-asymmetry", "D. RQ2 - Asymmetry (increases vs decreases)"),
 ("E-rq3-horizon", "E. RQ3 - Horizon and timing"),
 ("F-rq4-regimes", "F. RQ4 - Regimes and time variation"),
 ("G-rq5-sources", "G. RQ5 - Which uncertainty matters"),
 ("H-rq6-composition", "H. RQ6 - Greenfield vs acquisition"),
 ("I-india", "I. India-specific studies"),
 ("J-empirical", "J. Cross-country EPU/GPR and FDI evidence"),
 ("K-controls", "K. FDI determinants (control variables)"),
 ("Z-existing", "Z. Papers already in your library"),
]

out = []
out.append("# Literature map\n")
out.append("Every entry below is a bibliographic record verified through Crossref, plus a note file in `notes/`.\n")
out.append("Papers with a `PDF` line have the full text in `papers/`. Papers without one are metadata-verified only.\n")

for cat, label in ORDER:
    if cat == "Z-existing":
        rows = []
        zdir = os.path.join(ROOT, "notes", "Z-existing")
        pdir = os.path.join(ROOT, "papers", "Z-existing")
        for f in sorted(os.listdir(zdir)):
            txt = open(os.path.join(zdir, f), encoding="utf-8").read()
            def field(name, default="—"):
                m = re.search(rf"^\*\*{name}:\*\*\s*(.+)$", txt, re.M)
                return m.group(1).strip() if m else default
            base = f.rsplit(".", 1)[0]
            rows.append({
                "title": txt.split("\n", 1)[0].lstrip("# ").strip(),
                "authors": field("Authors"), "year": field("Year"),
                "venue": field("Outlet"), "doi": field("DOI", ""),
                "rq": field("Research questions"), "pdf": f"papers/Z-existing/{base}.pdf",
                "note": f"notes/Z-existing/{f}", "why": "",
            })
    else:
        rows = [v for v in state.values() if v.get("cat") == cat]
    if not rows:
        continue
    rows.sort(key=lambda v: (v.get("year") if isinstance(v.get("year"), int) else 0))
    out.append(f"\n---\n\n## {label}\n")
    out.append(f"\n**{len(rows)} papers**\n")
    for v in rows:
        title = re.sub(r"\s+", " ", v.get("title") or "").strip()
        out.append(f"\n### {title}\n")
        out.append(f"- **Authors:** {v.get('authors') or '—'}")
        out.append(f"- **Year:** {v.get('year') or '—'}")
        out.append(f"- **Outlet:** {v.get('venue') or '—'}")
        if v.get("doi") and v["doi"] != "—":
            out.append(f"- **DOI:** {v['doi']}")
        out.append(f"- **Serves:** {v.get('rq') or '—'}")
        if v.get("pdf"):
            out.append(f"- **Full text:** `{v['pdf']}`")
        else:
            out.append(f"- **Full text:** not retrieved (metadata only)")
        out.append(f"- **Note:** `{v.get('note')}`")
        if v.get("why"):
            out.append(f"- **Why it matters:** {v['why']}")

txt = "\n".join(out) + "\n"
open(os.path.join(ROOT, "literature-map.md"), "w", encoding="utf-8").write(txt)

n_pdf = sum(1 for v in state.values() if v.get("ok"))
n_note = sum(1 for v in state.values() if v.get("note"))
print(f"records={len(state)} with_pdf={n_pdf} with_note={n_note}")
print("wrote literature-map.md", len(txt), "chars")
