"""Adds PDF resolution through Unpaywall, citation_pdf_url and Semantic Scholar."""
import re
import requests


def _meta_pdf(html):
    for pat in [r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url',
                r'<link[^>]+type=["\']application/pdf["\'][^>]+href=["\']([^"\']+)']:
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1)
    return None


def unpaywall(doi, email="lit-review@example.org"):
    try:
        r = requests.get(f"https://api.unpaywall.org/v2/{doi}", params={"email": email}, timeout=30)
        if r.status_code == 200:
            d = r.json()
            out = []
            for loc in d.get("oa_locations") or []:
                for k in ("url_for_pdf", "url"):
                    if loc.get(k):
                        out.append(loc[k])
            return out
    except Exception:
        pass
    return []


def s2(doi):
    try:
        r = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}",
                         params={"fields": "openAccessPdf,externalIds"}, timeout=30)
        if r.status_code == 200:
            p = r.json().get("openAccessPdf") or {}
            return [p["url"]] if p.get("url") else []
    except Exception:
        pass
    return []


def s2_title(title):
    try:
        r = requests.get("https://api.semanticscholar.org/graph/v1/paper/search",
                         params={"query": title, "limit": 3, "fields": "title,openAccessPdf,year"},
                         timeout=30)
        if r.status_code == 200:
            out = []
            for p in r.json().get("data", []):
                oa = p.get("openAccessPdf") or {}
                if oa.get("url"):
                    out.append(oa["url"])
            return out
    except Exception:
        pass
    return []



def landing_pdf(url, session=None):
    try:
        r = requests.get(url, timeout=40, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                         allow_redirects=True)
        if r.status_code == 200 and "html" in r.headers.get("Content-Type", "").lower():
            return _meta_pdf(r.text[:400000])
    except Exception:
        pass
    return None
