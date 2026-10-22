"""Fix records that resolved to the wrong paper. Replaces note + PDF using a strict lookup."""
import os
import re
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import crossref as cr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "tools", "acquired.json")
state = json.load(open(STATE, encoding="utf-8"))

# key-fragment -> (exact title to look up, expected first author, expected year, new why-text)
FIXES = [
 ("Simultaneous Confidence Intervals for Impulse Responses",
  "Simultaneous confidence intervals for impulse responses", "jord", 2009,
  "The joint-band method: builds confidence sets that cover the whole impulse-response path at once. This is the reference for testing all 37 horizons of RQ3 jointly rather than one at a time."),
 ("Economic Development in Modern China Since 1949",
  "Economic Policy Uncertainty in China Since 1949", "davis", 2019,
  "Shows how a country EPU index is built when newspaper archives are incomplete. Useful precedent for describing the limits of the India EPU index."),
 ("Determinants of Foreign Direct Investment",
  "Determinants of foreign direct investment in developing countries: a meta-analysis", "faeth", 2009,
  "Meta-analysis of developing-country FDI determinants. Gives expected signs and effect-size ranges for your control variables."),
 ("Institutions and FDI Attractiveness in Developing Countries",
  "Institutional determinants of foreign direct investment", "b\u00e9nassy", 2007,
  "Institutions as an FDI determinant. Needed because RQ4 prediction A is about institutional strengthening after 2014."),
 ("Clarifying the nexus between Trade Policy Uncertainty",
  "Revisiting the nexus between economic policy uncertainty, financial development, and FDI inflows", "?", 2023,
  "Recent re-estimation of the EPU-FDI-finance nexus. Check whether it contradicts the negative-sign consensus before you claim the sign is settled."),
 ("Impact of Economic Policy Uncertainty on the Outward Foreign Direct Investment",
  "The effects of economic policy uncertainty on outward foreign direct investment", "?", 2019,
  "Mirror image of your question: how home-country EPU pushes investment abroad. Useful for the discussion of whether uncertainty delays FDI or diverts it to other hosts."),
 ("On the Sign of the Investment",
  "On the sign of the investment-uncertainty relationship", "caballero", 1991,
  "Shows the sign of the investment-uncertainty relation is not universally negative. The strongest theoretical counter-argument your H1 must answer."),
]


def clean_html(s):
    s = re.sub(r"</?scp>", "", s or "")
    s = s.replace("&amp;", "&").replace("<scp>", "").replace("</scp>", "")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def make_note(t, it, pdf_name, pages, abstract):
    title = clean_html((it.get("title") or [""])[0])
    if pdf_name:
        pdf_line = f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages)"
    else:
        pdf_line = ("**PDF:** none. No open-access copy could be retrieved from this network. "
                    "This note is a verified bibliographic entry plus reviewer assessment, not a summary of results.")
    if abstract:
        abs_block = f"> {abstract.strip()}\n\n_Source of abstract: Crossref deposit._"
    else:
        abs_block = ("_No abstract available from Crossref for this record. "
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
- "Why it matters" is the reviewer's judgement, not the authors' claim.
"""


fixed = 0
for frag, title, au, yr, why in FIXES:
    hits = [k for k in state
            if frag.lower() in (state[k].get("title") or "").lower()
            or frag.lower() in k.lower()]
    if not hits:
        print("NO STATE MATCH:", frag)
        continue
    key = hits[0]
    old = state[key]
    # delete the artefacts written for the wrong match
    for rel in (old.get("note"), old.get("pdf")):
        if rel:
            p = os.path.join(ROOT, rel)
            if os.path.exists(p):
                os.remove(p)
    it = cr.best(title, au, yr)
    if not it or it["_title_sim"] < 0.72:
        print("LOOKUP FAILED:", title, "->", (it or {}).get("title"), (it or {}).get("_title_sim"))
        continue
    t = dict(cat=old.get("cat"), rq=old.get("rq"), why=why, title=title, au=au, year=yr)
    real_title = clean_html((it.get("title") or [""])[0])
    first = (cr.authors(it).split(",")[0] or "anon").split()[-1]
    base = f"{cr.year(it) or 'nd'}-{pk.slug(first,18)}-{pk.slug(real_title,70)}"
    pdf_path = os.path.join(ROOT, "papers", t["cat"], base + ".pdf")
    note_path = os.path.join(ROOT, "notes", t["cat"], base + ".md")

    import resolve
    pdf_name, pages = None, None
    urls = []
    m = re.search(r"10\.3386/w(\d{4,5})", it.get("DOI") or "")
    if m:
        n = m.group(1)
        urls.append(f"https://www.nber.org/system/files/working_papers/w{n}/w{n}.pdf")
    urls += [u for u in resolve.unpaywall(it.get("DOI")) if u]
    for u in urls[:6]:
        ok, msg = pk.download(u, pdf_path)
        if ok:
            pdf_name = os.path.basename(pdf_path)
            pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
            break

    abstract = cr.abstract(it)
    if pdf_name and not abstract:
        abstract = pk.pdf_abstract(pdf_path)

    os.makedirs(os.path.dirname(note_path), exist_ok=True)
    open(note_path, "w", encoding="utf-8").write(make_note(t, it, pdf_name, pages, abstract))

    state[key] = {"ok": bool(pdf_name), "note": os.path.relpath(note_path, ROOT).replace("\\", "/"),
                  "pdf": (f"papers/{t['cat']}/{pdf_name}" if pdf_name else None),
                  "doi": it.get("DOI"), "year": cr.year(it), "title": real_title,
                  "authors": cr.authors(it), "venue": cr.venue(it), "cat": t["cat"],
                  "rq": t["rq"], "cites": it.get("is-referenced-by-count"),
                  "has_abstract": bool(abstract), "src": "crossref", "why": why}
    print("FIXED:", real_title[:80])
    fixed += 1

json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("fixed", fixed)
