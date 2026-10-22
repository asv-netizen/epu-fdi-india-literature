"""Acquire PDFs and write notes using Crossref + Unpaywall + open repositories."""
import json
import math
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import resolve
import crossref as cr
from targets import TARGETS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "papers")
NOTES = os.path.join(ROOT, "notes")
STATE = os.path.join(ROOT, "tools", "acquired.json")
os.makedirs(PAPERS, exist_ok=True)
os.makedirs(NOTES, exist_ok=True)

state = {}
if os.path.exists(STATE):
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        state = {}
state = {k: v for k, v in state.items() if v.get("src") == "crossref"}


def nber(doi):
    m = re.search(r"10\.3386/w(\d{4,5})", doi or "")
    if m:
        n = m.group(1)
        return [f"https://www.nber.org/system/files/working_papers/w{n}/w{n}.pdf"]
    return []


def pdf_abstract(path, maxlen=2600):
    """Pull the abstract out of a downloaded PDF, if it has one."""
    try:
        import pymupdf
        d = pymupdf.open(path)
        txt = ""
        for i in range(min(2, d.page_count)):
            txt += d[i].get_text()
        d.close()
    except Exception:
        return ""
    t = re.sub(r"-\n", "", txt)
    t = re.sub(r"\s+", " ", t)
    m = re.search(r"\b(?:Abstract|ABSTRACT|Summary)\b[\s:.\-–]*(.{200,%d}?)(?:\b(?:Keywords?|JEL|1\.?\s*Introduction|Introduction|I\.\s+INTRODUCTION)\b)" % maxlen, t)
    if m:
        return m.group(1).strip()[:maxlen]
    return ""


def note_text(t, it, doi, pdf_name, pages, abstract, abs_source, wp_flag):
    title = (it.get("title") or [t["title"]])[0]
    authors = cr.authors(it)
    year = cr.year(it)
    venue = cr.venue(it)
    if pdf_name and wp_flag:
        pdf_line = (f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages). "
                    f"Note: this file is the {wp_flag} version; the published version is the outlet above.")
    elif pdf_name:
        pdf_line = f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages)"
    else:
        pdf_line = ("**PDF:** none. No open-access copy could be retrieved from this network. "
                    "The note below is a bibliographic entry plus reviewer assessment, not a summary of results.")
    if abstract:
        abs_block = f"> {abstract.strip()}"
        abs_note = f"_Source of abstract: {abs_source}._"
    else:
        abs_block = ("_No abstract available from Crossref, Unpaywall or the PDF for this record. "
                     "Do not attribute a finding to this paper until you have read it._")
        abs_note = ""
    return f"""# {title}

**Authors:** {authors}
**Year:** {year}
**Outlet:** {venue}
**DOI:** {doi or '—'}
**Crossref citations:** {it.get('is-referenced-by-count')}
**Research questions:** {t['rq']}
{pdf_line}

## Abstract

{abs_block}

{abs_note}

## Why it matters for this thesis

{t['why']}

## Use

- Target section: **{t['rq']}**.
- Check sample period, country coverage and estimator before comparing any coefficient with yours.

## Verification

- Bibliographic record resolved through Crossref (DOI, title, authors, year, outlet).
- "Why it matters" is the reviewer's judgement, not the authors' claim.
"""


def run(limit=None, only_cat=None):
    done = 0
    for t in TARGETS:
        if limit and done >= limit:
            break
        if only_cat and t["cat"] != only_cat:
            continue
        key = f"{t['cat']}|{t['title'][:60]}"
        if key in state and state[key].get("ok") is not None and state[key].get("note"):
            continue
        it = cr.best(t["title"], t.get("au", ""), t.get("year"))
        if not it:
            print(f"[MISS] {t['title'][:72]}")
            state[key] = {"ok": False, "reason": "no crossref record", "src": "crossref",
                          "cat": t["cat"], "rq": t["rq"]}
            json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            continue
        doi = it.get("DOI")
        title = (it.get("title") or [t["title"]])[0]
        abstract = cr.abstract(it)
        abs_source = "Crossref deposit" if abstract else ""

        first = (cr.authors(it).split(",")[0] or "anon").split()[-1]
        base = f"{cr.year(it) or 'nd'}-{pk.slug(first,18)}-{pk.slug(title,70)}"
        pdf_path = os.path.join(PAPERS, t["cat"], base + ".pdf")
        note_path = os.path.join(NOTES, t["cat"], base + ".md")

        pdf_name, pages, wp_flag = None, None, ""
        if os.path.exists(pdf_path):
            try:
                import pymupdf
                d = pymupdf.open(pdf_path)
                pages = d.page_count
                d.close()
                pdf_name = os.path.basename(pdf_path)
            except Exception:
                os.remove(pdf_path)

        if not pdf_name:
            urls = nber(doi)
            urls += [u for u in resolve.unpaywall(doi) if u]
            for u in urls[:10]:
                ok, msg = pk.download(u, pdf_path)
                if ok:
                    pdf_name = os.path.basename(pdf_path)
                    pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
                    if "nber.org" in u and not (doi or "").startswith("10.3386"):
                        wp_flag = "NBER working-paper"
                    break

        if pdf_name and not abstract:
            a = pdf_abstract(pdf_path)
            if a:
                abstract, abs_source = a, "first page of the downloaded PDF, machine-extracted"

        os.makedirs(os.path.dirname(note_path), exist_ok=True)
        open(note_path, "w", encoding="utf-8").write(
            note_text(t, it, doi, pdf_name, pages, abstract, abs_source, wp_flag))

        state[key] = {"ok": bool(pdf_name), "note": os.path.relpath(note_path, ROOT).replace("\\", "/"),
                      "pdf": (f"papers/{t['cat']}/{pdf_name}" if pdf_name else None),
                      "doi": doi, "year": cr.year(it), "title": title,
                      "authors": cr.authors(it), "venue": cr.venue(it), "cat": t["cat"],
                      "rq": t["rq"], "cites": it.get("is-referenced-by-count"),
                      "has_abstract": bool(abstract), "src": "crossref"}
        json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"[{'PDF' if pdf_name else 'NOTE'}] {cr.year(it)} {cr.authors(it,2)} | {title[:62]}")
        done += 1
        time.sleep(0.5)


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cat = sys.argv[2] if len(sys.argv) > 2 else None
    run(lim, cat)
