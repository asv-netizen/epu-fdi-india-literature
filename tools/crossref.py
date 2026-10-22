"""Crossref metadata client (OpenAlex replacement while rate-limited)."""
import re
import time
import urllib.parse
import requests

UA = {"User-Agent": "LitReview/1.0 (mailto:lit-review@example.org)"}
CR = "https://api.crossref.org/works"
MAIL = "lit-review@example.org"


def _sim(a, b):
    A, B = set(a.split()), set(b.split())
    if not A or not B:
        return 0.0
    return len(A & B) / max(len(A), len(B))


def norm(s):
    s = (s or "").lower()
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def _get(params):
    for i in range(3):
        try:
            r = requests.get(CR, params=params, headers=UA, timeout=45)
            if r.status_code == 200:
                return r.json()["message"]["items"]
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 + 3 * i)
                continue
            return []
        except requests.RequestException:
            time.sleep(2 + 2 * i)
    return []


def find(title, author="", year=None, rows=6):
    items = _get({"query.bibliographic": title, "rows": rows, "mailto": MAIL,
                  "select": "DOI,title,author,issued,container-title,abstract,type,"
                            "is-referenced-by-count,publisher,link,URL"})
    t = norm(title)
    scored = []
    for it in items:
        ti = (it.get("title") or [""])[0]
        s = _sim(t, norm(ti))
        fams = norm(" ".join((a.get("family") or "") for a in it.get("author", []) or []))
        if author and norm(author) and norm(author) in fams:
            s += 0.35
        yr = None
        dp = (it.get("issued") or {}).get("date-parts") or [[None]]
        if dp and dp[0]:
            yr = dp[0][0]
        if year and yr:
            s += 0.12 if abs(yr - year) <= 1 else (-0.15 if abs(yr - year) > 3 else 0)
        if (it.get("type") or "") in ("book", "component", "dataset", "peer-review"):
            s -= 0.3
        if it.get("type") == "journal-article":
            s += 0.08
        if it.get("type") == "posted-content":
            s -= 0.12
        import math
        s += min(0.08, math.log10((it.get("is-referenced-by-count") or 0) + 1) * 0.02)
        if yr:
            it["_year"] = yr
        it["_sim"] = s
        it["_title_sim"] = _sim(t, norm(ti))
        scored.append(it)
    scored.sort(key=lambda x: -x["_sim"])
    return scored


def best(title, author="", year=None):
    c = find(title, author, year)
    if not c:
        return None
    b = c[0]
    if b["_title_sim"] < 0.5 and (not author or norm(author) not in norm(
            " ".join((a.get("family") or "") for a in b.get("author", []) or []))):
        return None
    return b


def authors(it, limit=None):
    out = []
    for a in it.get("author", []) or []:
        n = a.get("name") or " ".join(filter(None, [a.get("given"), a.get("family")]))
        if n:
            out.append(n)
    if limit and len(out) > limit:
        return ", ".join(out[:limit]) + " et al."
    return ", ".join(out)


def abstract(it):
    a = it.get("abstract") or ""
    a = re.sub(r"<[^>]+>", " ", a)
    a = re.sub(r"\s+", " ", a).strip()
    return a


def venue(it):
    ct = it.get("container-title") or []
    return ct[0] if ct else (it.get("publisher") or "")


def year(it):
    return it.get("_year")


def by_doi(doi):
    """Exact record lookup by DOI."""
    if not doi:
        return None
    doi = doi.replace("https://doi.org/", "").strip().rstrip(".,;")
    try:
        r = requests.get(CR + "/" + doi, headers=UA, timeout=40)
        if r.status_code != 200:
            return None
        it = r.json()["message"]
        dp = (it.get("issued") or {}).get("date-parts") or [[None]]
        it["_year"] = dp[0][0] if dp and dp[0] else None
        it["_sim"] = 1.0
        it["_title_sim"] = 1.0
        return it
    except Exception:
        return None
