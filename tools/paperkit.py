"""Paper acquisition helpers for the EPU-FDI literature review.

Uses OpenAlex (metadata + open-access PDF links) and Crossref (fallback metadata).
Every record is verified to exist before a note is written.
"""
import json
import os
import re
import time
import unicodedata
import urllib.parse
import requests
import pymupdf

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
MAIL = "lit-review@example.org"
OA = "https://api.openalex.org/works"
CR = "https://api.crossref.org/works"


def _get(url, params=None, timeout=40):
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 + attempt * 3)
                continue
            return r
        except requests.RequestException:
            time.sleep(2 + attempt * 2)
    return None


def reconstruct(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = s.encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return s.strip()


def search(title, rows=5, year=None):
    """Search OpenAlex by title, return candidate works sorted by title similarity."""
    params = {"filter": f"title.search:{title}", "per-page": rows, "mailto": MAIL}
    if year:
        params["filter"] += f",from_publication_date:{year-1}-01-01,to_publication_date:{year+1}-12-31"
    r = _get(OA, params)
    works = []
    if r is not None and r.status_code == 200:
        works = r.json().get("results", [])
    if len(works) < 2:
        r2 = _get(OA, {"search": title, "per-page": rows, "mailto": MAIL})
        if r2 is not None and r2.status_code == 200:
            extra = r2.json().get("results", [])
            seen = {w.get("id") for w in works}
            works += [w for w in extra if w.get("id") not in seen]
    t = norm(title)
    for w in works:
        w["_sim"] = _similarity(t, norm(w.get("title")))
    works.sort(key=lambda w: -w["_sim"])
    return works


def _similarity(a, b):
    A, B = set(a.split()), set(b.split())
    if not A or not B:
        return 0.0
    return len(A & B) / max(len(A), len(B))


def by_doi(doi):
    doi = doi.replace("https://doi.org/", "").strip()
    r = _get(f"{OA}/https://doi.org/{doi}", {"mailto": MAIL})
    if r is not None and r.status_code == 200:
        return r.json()
    r = _get(f"{CR}/{urllib.parse.quote(doi)}", None)
    if r is not None and r.status_code == 200:
        m = r.json()["message"]
        return {"doi": "https://doi.org/" + doi, "title": (m.get("title") or [""])[0],
                "publication_year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                "authorships": [{"author": {"display_name": " ".join(
                    filter(None, [a.get("given"), a.get("family")]))}} for a in m.get("author", [])],
                "primary_location": {"source": {"display_name": (m.get("container-title") or [""])[0]}},
                "abstract_inverted_index": None, "best_oa_location": None,
                "open_access": {"oa_url": None}}
    return None


def authors(w, limit=None):
    names = []
    for a in w.get("authorships", []) or []:
        n = (a.get("author") or {}).get("display_name")
        if n:
            names.append(n)
    if limit and len(names) > limit:
        return ", ".join(names[:limit]) + " et al."
    return ", ".join(names)


def venue(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return src.get("display_name") or ""


def pdf_candidates(w):
    """Ordered list of plausible PDF URLs for a work."""
    urls = []
    for loc in [w.get("best_oa_location")] + (w.get("locations") or []):
        if not loc:
            continue
        for key in ("pdf_url", "landing_page_url"):
            u = loc.get(key)
            if u and u not in urls:
                urls.append(u)
    oa = (w.get("open_access") or {}).get("oa_url")
    if oa and oa not in urls:
        urls.append(oa)
    # prefer things that look like direct pdfs
    urls.sort(key=lambda u: 0 if ("pdf" in u.lower() or u.lower().endswith(".pdf")) else 1)
    return urls


def download(url, dest, min_pages=3):
    """Download a URL and keep it only if it is a readable PDF."""
    for attempt in range(2):
        tmp = dest + ".part"
        try:
            r = requests.get(url, headers=UA, timeout=60, allow_redirects=True, stream=True)
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}"
            ct = r.headers.get("Content-Type", "")
            if "pdf" not in ct.lower() and "octet" not in ct.lower():
                return False, f"content-type {ct[:40]}"
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(65536):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(tmp) < 20000:
                os.remove(tmp)
                return False, "file too small"
            with open(tmp, "rb") as f:
                if f.read(5) != b"%PDF-":
                    os.remove(tmp)
                    return False, "not a PDF"
            try:
                d = pymupdf.open(tmp)
                n = d.page_count
                txt = d[0].get_text()[:300].lower()
                d.close()
            except Exception as e:
                os.remove(tmp)
                return False, f"unreadable: {e}"
            if n < min_pages:
                os.remove(tmp)
                return False, f"too short ({n}p)"
            if "access denied" in txt or "captcha" in txt:
                os.remove(tmp)
                return False, "blocked page"
            os.replace(tmp, dest)
            return True, f"{n} pages"
        except Exception as e:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            if attempt == 1:
                return False, str(e)[:80]
            time.sleep(2)
    return False, "failed"


def slug(text, n=70):
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].strip("-")


def pdf_abstract(path, maxlen=2600):
    """Extract the abstract paragraph from a PDF's first pages."""
    try:
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
