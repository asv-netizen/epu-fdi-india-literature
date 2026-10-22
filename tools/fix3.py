"""Resolve the K-controls collision: give the institutions slot its own verified record."""
import os
import re
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import crossref as cr
import resolve

ROOT = r"C:\Users\HP\Documents\LT-2"
STATE = os.path.join(ROOT, "tools", "acquired.json")
state = json.load(open(STATE, encoding="utf-8"))

TARGET_KEY = "K-controls|Institutional Determinants of Foreign Direct Investment"
DOI = "10.31857/s042473880007982-9"
WHY = ("Institutions as a determinant of bilateral FDI flows. This is the reference behind RQ4 "
       "prediction A: if Indian institutions strengthened after 2014, the sensitivity of FDI to "
       "policy uncertainty should fall, and the Akbakay (2026) result in your library is the "
       "panel-level version of the same claim.")

it = cr.by_doi(DOI)
if not it:
    print("DOI NOT VERIFIED - aborting, nothing changed")
    sys.exit(1)
print("verified:", (it.get("title") or [""])[0], "|", cr.authors(it), "|", cr.year(it), "|", cr.venue(it))

t = dict(cat="K-controls", rq="RQ1, RQ4", why=WHY)
real_title = re.sub(r"<[^>]+>", "", (it.get("title") or [""])[0]).strip()
first = (cr.authors(it).split(",")[0] or "anon").split()[-1]
base = f"{cr.year(it) or 'nd'}-{pk.slug(first,18)}-{pk.slug(real_title,70)}"
pdf_path = os.path.join(ROOT, "papers", "K-controls", base + ".pdf")
note_path = os.path.join(ROOT, "notes", "K-controls", base + ".md")

pdf_name, pages = None, None
for u in [x for x in resolve.unpaywall(DOI) if x]:
    ok, msg = pk.download(u, pdf_path)
    if ok:
        pdf_name = os.path.basename(pdf_path)
        pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
        break

abstract = cr.abstract(it)
if pdf_name and not abstract:
    abstract = pk.pdf_abstract(pdf_path)

note = f"""# {real_title}

**Authors:** {cr.authors(it)}
**Year:** {cr.year(it)}
**Outlet:** {cr.venue(it)}
**DOI:** {it.get('DOI') or '—'}
**Crossref citations:** {it.get('is-referenced-by-count')}
**Research questions:** {t['rq']}
{f"**PDF:** `papers/K-controls/{pdf_name}` ({pages} pages)" if pdf_name else
 "**PDF:** none. No open-access copy could be retrieved from this network. "
 "This note is a verified bibliographic entry plus reviewer assessment, not a summary of results."}

## Abstract

{f"> {abstract.strip()}" + chr(10) + chr(10) + "_Source of abstract: Crossref deposit._" if abstract else
 "_No abstract available from Crossref for this record. Do not attribute a finding to this paper until you have read it._"}

## Why it matters for this thesis

{WHY}

## Use

- Target section: **{t['rq']}**.
- Check sample period, country coverage and estimator before comparing any coefficient with yours.

## Verification

- Bibliographic record resolved through Crossref by exact DOI.
- "Why it matters" is the reviewer's judgement, not the authors' claim.

## Related references not retrievable here

Two standard references for this topic could not be verified in Crossref and are **not** in this
folder. Add them manually from the published journal references and confirm the DOIs yourself:

- Bénassy-Quéré, A., Coupet, M. and Mayer, T. (2007), "Institutional Determinants of Foreign Direct Investment", *The World Economy*, 30(5), 764-782.
- Faeth, I. (2009), "Determinants of Foreign Direct Investment in Developing Countries: A Meta-Analysis", *The World Economy*, 32(8), 1137-1161.
"""

os.makedirs(os.path.dirname(note_path), exist_ok=True)
open(note_path, "w", encoding="utf-8").write(note)

state[TARGET_KEY] = {
    "ok": bool(pdf_name), "note": f"notes/K-controls/{os.path.basename(note_path)}",
    "pdf": (f"papers/K-controls/{pdf_name}" if pdf_name else None),
    "doi": DOI, "year": cr.year(it), "title": real_title, "authors": cr.authors(it),
    "venue": cr.venue(it), "cat": "K-controls", "rq": t["rq"],
    "cites": it.get("is-referenced-by-count"), "has_abstract": bool(abstract),
    "src": "crossref", "why": WHY}

json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", note_path)
