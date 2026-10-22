"""Acquire PDFs and write verified notes for the EPU-FDI literature review."""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import resolve
from targets import TARGETS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "papers")
NOTES = os.path.join(ROOT, "notes")
STATE = os.path.join(ROOT, "tools", "acquired.json")

os.makedirs(PAPERS, exist_ok=True)
os.makedirs(NOTES, exist_ok=True)

state = {}
if os.path.exists(STATE):
    state = json.load(open(STATE, encoding="utf-8"))


def clean_abstract(w):
    inv = w.get("abstract_inverted_index")
    a = pk.reconstruct(inv) if inv else ""
    if not a:
        a = (w.get("_cr_abstract") or "")
        a = re.sub(r"<[^>]+>", " ", a)
        a = re.sub(r"\s+", " ", a).strip()
    return a


def cr_abstract(doi):
    try:
        import requests
        r = requests.get("https://api.crossref.org/works/" + doi, timeout=25)
        if r.status_code == 200:
            return r.json()["message"].get("abstract", "")
    except Exception:
        pass
    return ""


def nber_url(w):
    urls = []
    for loc in w.get("locations") or []:
        for k in ("pdf_url", "landing_page_url"):
            u = loc.get(k) or ""
            m = re.search(r"nber\.org/(?:system/files/working_papers/)?(?:papers/)?w(\d{4,5})", u)
            if m:
                urls.append(f"https://www.nber.org/system/files/working_papers/w{m.group(1)}/w{m.group(1)}.pdf")
    doi = (w.get("doi") or "")
    m = re.search(r"10\.3386/w(\d{4,5})", doi)
    if m:
        urls.append(f"https://www.nber.org/system/files/working_papers/w{m.group(1)}/w{m.group(1)}.pdf")
    return list(dict.fromkeys(urls))


def pick(target):
    cands = pk.search(target["title"], rows=6)
    if not cands:
        # retry once; OpenAlex occasionally times out on phrase queries
        time.sleep(1)
        cands = pk.search(target["title"], rows=6)
    au = target.get("au", "").lower()
    yr = target.get("year")
    scored = []
    for w in cands:
        names = pk.authors(w).lower()
        s = w["_sim"]
        if au and au in names:
            s += 0.35
        if yr and w.get("publication_year"):
            s += 0.10 if abs(w["publication_year"] - yr) <= 1 else -0.10
        if (w.get("type") or "") in ("book", "paratext", "dataset"):
            s -= 0.2
        v = (pk.venue(w) or "").lower()
        if any(k in v for k in ("nber", "ssrn", "repec", "iza", "cepr", "working paper")):
            s -= 0.12
        if (w.get("type") or "") == "article":
            s += 0.08
        scored.append((s, w))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        return None
    best = scored[0][1]
    if best["_sim"] < 0.55 and au not in pk.authors(best).lower():
        return None
    return best


def wp_twin(title):
    """Find a working-paper copy of the same title that has a usable PDF."""
    cands = pk.search(title, rows=6)
    for w in cands:
        if w["_sim"] < 0.85:
            continue
        v = (pk.venue(w) or "").lower()
        if any(k in v for k in ("nber", "ssrn", "repec", "iza", "cepr", "working paper", "discussion paper")):
            return w
    return None


def write_note(path, t, w, pdf_name, pages, abstract, attempts, wp_flag=""):
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    authors = pk.authors(w)
    year = w.get("publication_year")
    venue = pk.venue(w)
    if pdf_name and wp_flag:
        status = (f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages). This is the "
                  f"working-paper version ({wp_flag}); the published version is the outlet named above. "
                  "Page numbers differ from the journal article.")
    elif pdf_name:
        status = f"**PDF:** `papers/{t['cat']}/{pdf_name}` ({pages} pages)"
    else:
        status = ("**PDF:** no open-access copy found. This note is written from the deposited "
                  "abstract and metadata, not from the full text.")
    abs_block = (abstract.strip() if abstract else
                 "_No abstract is deposited in OpenAlex or Crossref for this record. The summary below is from the design and title only; read the paper before citing a finding._")
    note = f"""# {w.get('title')}

**Authors:** {authors}
**Year:** {year}
**Outlet:** {venue}
**DOI:** {doi or '—'}
**OpenAlex:** {w.get('id')}
**Citations (OpenAlex):** {w.get('cited_by_count')}
**Research questions:** {t['rq']}
{status}

## Abstract (as deposited)

> {abs_block}

## Why it matters for this thesis

{t['why']}

## How to use it

- Cite it in the section tagged **{t['rq']}**.
- Check the sample period and country coverage before comparing any elasticity with yours.
- Confirm the estimation method in the full text; the abstract may not name it.

## Verification status

- Bibliographic record checked against OpenAlex on this run.
- Abstract is the deposited abstract, quoted verbatim.
- Analysis in "Why it matters" is the reviewer's judgement, not the authors' claim.
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(note)


def run(limit=None, only_cat=None):
    done = 0
    for i, t in enumerate(TARGETS):
        if limit and done >= limit:
            break
        if only_cat and t["cat"] != only_cat:
            continue
        key = f"{t['cat']}|{t['title'][:60]}"
        if key in state and state[key].get("ok"):
            continue
        w = pick(t)
        if not w:
            print(f"[MISS] {t['title'][:70]}")
            state[key] = {"ok": False, "reason": "no record"}
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        abstract = clean_abstract(w)
        if not abstract and doi:
            abstract = cr_abstract(doi)
            abstract = re.sub(r"<[^>]+>", " ", abstract)
            abstract = re.sub(r"\s+", " ", abstract).strip()

        first = (pk.authors(w).split(",")[0] or "anon").split()[-1]
        base = f"{w.get('publication_year') or 'nd'}-{pk.slug(first, 18)}-{pk.slug(w.get('title') or t['title'], 70)}"
        pdf_path = os.path.join(PAPERS, t["cat"], base + ".pdf")
        note_path = os.path.join(NOTES, t["cat"], base + ".md")

        pdf_name, pages = None, None
        wp_flag = ""
        if os.path.exists(pdf_path):
            try:
                d = pk_pages = __import__("pymupdf").open(pdf_path)
                pages = d.page_count
                d.close()
                pdf_name = os.path.basename(pdf_path)
            except Exception:
                os.remove(pdf_path)

        attempts = []
        if not pdf_name:
            urls = []
            urls += nber_url(w)
            urls += [u for u in pk.pdf_candidates(w) if u.lower().endswith(".pdf")]
            if doi:
                urls += resolve.unpaywall(doi)
                urls += resolve.s2(doi)
            urls += resolve.s2_title(w.get("title") or t["title"])
            urls += [u for u in pk.pdf_candidates(w) if u not in urls]
            seen = set()
            for u in urls[:10]:
                if u in seen or not u.lower().startswith("http"):
                    continue
                seen.add(u)
                if "doi.org" in u or "repec" in u or "ideas.repec" in u:
                    meta = resolve.landing_pdf(u)
                    if meta:
                        u = meta
                    else:
                        attempts.append(f"landing {u[:60]}: no pdf meta")
                        continue
                ok, msg = pk.download(u, pdf_path)
                attempts.append(f"{u[:70]} -> {msg}")
                if ok:
                    pdf_name = os.path.basename(pdf_path)
                    pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
                    break

        if not pdf_name:
            twin = wp_twin(w.get("title") or t["title"])
            if twin:
                for u in (nber_url(twin) + [x for x in pk.pdf_candidates(twin) if x.lower().endswith(".pdf")])[:4]:
                    ok, msg = pk.download(u, pdf_path)
                    if ok:
                        pdf_name = os.path.basename(pdf_path)
                        pages = int(msg.split()[0]) if msg.split()[0].isdigit() else None
                        wp_flag = pk.venue(twin)
                        break

        write_note(note_path, t, w, pdf_name, pages, abstract, attempts, wp_flag)
        ok = bool(pdf_name)
        state[key] = {"ok": ok, "pdf": pdf_name, "doi": doi, "year": w.get("publication_year"),
                      "title": w.get("title"), "authors": pk.authors(w), "venue": pk.venue(w),
                      "cat": t["cat"], "rq": t["rq"], "why": t["why"], "attempts": attempts[-3:],
                      "abstract": bool(abstract), "cites": w.get("cited_by_count")}
        json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"[{'PDF' if ok else 'NOTE'}] {w.get('publication_year')} {pk.authors(w, 2)} | {(w.get('title') or '')[:60]}")
        done += 1
        time.sleep(0.4)


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cat = sys.argv[2] if len(sys.argv) > 2 else None
    run(lim, cat)
