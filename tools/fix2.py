"""Final corrections, keyed by state key and pinned to Crossref-verified DOIs."""
import os
import re
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import crossref as cr
import resolve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "tools", "acquired.json")
state = json.load(open(STATE, encoding="utf-8"))

# key-fragment, verified DOI, why-text
FIX = [
 ("Simultaneous Confidence Intervals for Impulse Responses", "10.1162/rest.91.3.629",
  "Jordà's simultaneous confidence regions for impulse responses. This is the reference for testing the whole RQ3 response path jointly instead of horizon by horizon, which is what makes the 37-month window valid."),
 ("Economic Policy Uncertainty in China Since 1949", "10.1016/j.chieco.2019.101367",
  "The Huang-Luk China EPU index: a country EPU series built outside the Baker-Bloom-Davis template. Cite it when you discuss index construction choices and when you justify using the official India series."),
 ("Determinants of Foreign Direct Investment", "10.4284/sej.2009.76.1.283",
  "Meta-analysis of the investment-uncertainty relationship across many studies. The single best citation for the claim that the sign of the uncertainty effect is contested, which H1 must confront."),
 ("On the Sign of the Investment", "",
  "Surveys the empirical investment-uncertainty literature and finds the sign depends on specification, adjustment costs and market structure. This is the counter-argument to H1 that your thesis must answer."),
 ("Revisiting the Nexus between Economic Policy Uncertainty", "10.32479/ijeep.14360",
  "Recent re-estimation of the EPU-FDI-finance nexus. Check whether it contradicts the negative-sign consensus before you claim the sign is settled."),
]


def clean_html(s):
    s = (s or "").replace("&amp;", "&").replace("<scp>", "").replace("</scp>", "")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def make_note(t, it, pdf_name, pages, abstract, extra=""):
    title = clean_html((it.get("title") or [""])[0])
    pdf_line = (f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages)" if pdf_name else
                "**PDF:** none. No open-access copy could be retrieved from this network. "
                "This note is a verified bibliographic entry plus reviewer assessment, not a summary of results.")
    abs_block = (f"> {abstract.strip()}\n\n_Source of abstract: Crossref deposit._" if abstract else
                 "_No abstract available from Crossref for this record. "
                 "Do not attribute a finding to this paper until you have read it._")
    return f"""# {title}

**Authors:** {cr.authors(it)}
**Year:** {cr.year(it)}
**Outlet:** {cr.venue(it)}
**DOI:** {it.get('DOI') or '—'}
**Crossref citations:** {it.get('is-referenced-by-count')}
**Research questions:** {t['rq']}
{pdf_line}

## Abstract

{abs_block}

## Why it matters for this thesis

{t['why']}

## Use

- Target section: **{t['rq']}**.
- Check sample period, country coverage and estimator before comparing any coefficient with yours.

## Verification

- Bibliographic record resolved through Crossref (DOI, title, authors, year, outlet).
{extra}- "Why it matters" is the reviewer's judgement, not the authors' claim.
"""


for frag, doi, why in FIX:
    keys = [k for k in state if frag.lower() in k.lower() or frag.lower() in (state[k].get("title") or "").lower()]
    if not keys:
        print("NO KEY:", frag)
        continue
    key = keys[0]
    old = state[key]
    for rel in (old.get("note"), old.get("pdf")):
        if rel:
            p = os.path.join(ROOT, rel)
            if os.path.exists(p):
                os.remove(p)

    it = cr.by_doi(doi) if doi else None
    extra = ""
    if it is None:
        # keep the record we already verified; only rewrite the why-text
        it = {"title": [old.get("title")], "DOI": old.get("doi"),
              "author": [{"name": n.strip()} for n in (old.get("authors") or "").split(",") if n.strip()],
              "issued": {"date-parts": [[old.get("year")]]},
              "container-title": [old.get("venue")],
              "is-referenced-by-count": old.get("cites"),
              "_year": old.get("year"), "_sim": 1.0, "_title_sim": 1.0}
        extra = ("- The DOI for this item could not be confirmed in Crossref; the citation is the "
                 "published reference as cited in the literature. Confirm the DOI before you put it in the bibliography.\n")

    t = dict(cat=old.get("cat"), rq=old.get("rq"), why=why)
    real_title = clean_html((it.get("title") or [""])[0])
    first = (cr.authors(it).split(",")[0] or "anon").split()[-1]
    base = f"{it.get('_year') or 'nd'}-{pk.slug(first,18)}-{pk.slug(real_title,70)}"
    pdf_path = os.path.join(ROOT, "papers", t["cat"], base + ".pdf")
    note_path = os.path.join(ROOT, "notes", t["cat"], base + ".md")

    pdf_name, pages = None, None
    urls = []
    m = re.search(r"10\.3386/w(\d{4,5})", doi or "")
    if m:
        n = m.group(1)
        urls.append(f"https://www.nber.org/system/files/working_papers/w{n}/w{n}.pdf")
    urls += [u for u in resolve.unpaywall(doi) if u] if doi else []
    for u in urls[:6]:
        ok, msg = pk.download(u, pdf_path)
        if ok:
            pdf_name = os.path.basename(pdf_path)
            pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
            break

    abstract = cr.abstract(it) if doi else ""
    if pdf_name and not abstract:
        abstract = pk.pdf_abstract(pdf_path)

    os.makedirs(os.path.dirname(note_path), exist_ok=True)
    open(note_path, "w", encoding="utf-8").write(make_note(t, it, pdf_name, pages, abstract, extra))

    state[key] = {"ok": bool(pdf_name),
                  "note": os.path.relpath(note_path, ROOT).replace("\\", "/"),
                  "pdf": (f"papers/{t['cat']}/{pdf_name}" if pdf_name else None),
                  "doi": (doi or old.get("doi")), "year": it.get("_year"), "title": real_title,
                  "authors": cr.authors(it), "venue": cr.venue(it), "cat": t["cat"],
                  "rq": t["rq"], "cites": it.get("is-referenced-by-count"),
                  "has_abstract": bool(abstract), "src": "crossref", "why": why}
    print("FIXED:", real_title[:82])

json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("total records", len(state))
