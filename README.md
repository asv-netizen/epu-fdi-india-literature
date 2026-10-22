# EPU and FDI in India — literature review

Working literature folder for the thesis *"Economic Policy Uncertainty and Foreign Direct Investment in India: six research questions"*.

Sample: monthly, January 2005 – December 2025 (252 months). Dependent variable: log of real gross FDI equity inflows (DPIIT).

---

## What is in here

| Folder | Contents |
|---|---|
| `papers/` | PDFs of full texts, grouped by research question |
| `notes/` | One Markdown note per paper |
| `literature-map.md` | Every paper, grouped by theme and research question |
| `gap-statement.md` | The corrected gap statement, with the India studies you must cite |
| `data-sources.md` | Where each data series comes from, with verified links |
| `methodology-key.md` | Which paper supports which method, question by question |
| `tools/` | The scripts used to find, verify and index the papers |

**112 papers** are indexed in this folder.

- **86** were found, verified against Crossref, and given a note in this review. **18** of those have the PDF downloaded here.
- **26** were already in `C:\Users\HP\Documents\Literature-Review`. They have been copied in and indexed in `notes/Z-existing/`.
- **44 PDFs** total are in `papers/`.

---

## How a note is built

Each note in `notes/` contains:

1. The bibliographic record — title, authors, year, outlet, DOI, citation count.
2. Whether the PDF is in this repo.
3. The abstract, taken from the Crossref deposit or extracted from the first page of the PDF.
4. **Why it matters for this thesis** — the reviewer's judgement, not the authors' claim.
5. A verification line stating exactly what was checked.

Read the "Why it matters" paragraph before you read the paper. It tells you which research question the paper serves and what you need it for. Then read the paper — the note is a map, not a substitute.

---

## Two things this folder will not do for you

**It cannot tell you a finding the abstract does not state.** Where no abstract was deposited, the note says so in those words. Do not cite a result from those papers until you have read them.

**It cannot make a paywalled paper appear.** Publisher sites (Elsevier, Wiley, MDPI, Oxford, Springer) block automated access from this network. Where a repository copy exists — NBER, EconStor, RePEc, MPRA, IMF, BIS — it has been downloaded. Where none was available, the note is metadata only.

---

## The four papers that matter most

If you read only four, read these:

1. **Shin, Yu & Greenwood-Nimmo (2014)**, *Modelling Asymmetric Cointegration and Dynamic Multipliers in a Nonlinear ARDL Framework* — the method behind RQ2. `notes/D-rq2-asymmetry/`
2. **Jordà (2005)**, *Estimation and Inference of Impulse Responses by Local Projections* — the method behind RQ3. `notes/E-rq3-horizon/`
3. **Sinha & Ghosh (2021)**, *Impact of Economic Policy Uncertainty on FDI Inflows: Evidence from India* — the existing India study you must differentiate from. `notes/I-india/`
4. **Jardet, Jude & Chinn (2022)**, *Foreign direct investment under uncertainty* — the claim RQ5 tests. `notes/G-rq5-sources/`

---

## A note on what changed from your draft

Your research-questions text contained two statements that did not survive checking. Both are corrected in `gap-statement.md`:

- **H2 is written backwards.** You define EPU⁺ as the sum of monthly *increases* in EPU. "Increases cause more damage" is therefore `|β⁺| > |β⁻|`. Your draft says `|β⁻| > |β⁺|`. Fix this before your supervisor reads it.
- **The gap statement says Khan & Qamar (2023) is the only India EPU–FDI study.** It is not. Sinha & Ghosh (2021) is a second one, and it was not in your folder.

The `new-literature.md` file you referenced is **not in this folder** and was not found on this machine. The 29 sources it claims to list could not be checked.
