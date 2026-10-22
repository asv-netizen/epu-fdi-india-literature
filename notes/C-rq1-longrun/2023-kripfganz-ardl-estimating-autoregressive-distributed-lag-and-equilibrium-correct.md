# ardl: Estimating autoregressive distributed lag and equilibrium correction models

**Authors:** Sebastian Kripfganz, Daniel C. Schneider
**Year:** 2023
**Outlet:** The Stata Journal: Promoting communications on statistics and Stata
**DOI:** 10.1177/1536867x231212434
**Crossref citations:** 186
**Research questions:** RQ1
**PDF:** none. No open-access copy could be retrieved from this network. The note below is a bibliographic entry plus reviewer assessment, not a summary of results.

## Abstract

> We present a command, ardl, for the estimation of autoregressive distributed lag (ARDL) models in a time-series context. The ardl command can be used to fit an ARDL model with the optimal number of autoregressive and distributed lags based on the Akaike or Bayesian (Schwarz) information criterion. The regression results can be displayed in the ARDL levels form or in the error-correction representation of the model. The latter separates long-run and short-run effects and is available in two different parameterizations of the long-run (cointegrating) relationship. The popular bounds-testing procedure for the existence of a long-run levels relationship is implemented as a postestimation feature. Comprehensive critical values and approximate p-values obtained from response-surface regressions facilitate statistical inference.

_Source of abstract: Crossref deposit._

## Why it matters for this thesis

The Stata implementation and the small-sample critical values you plan to use. Explains why the standard Pesaran bounds are too liberal at 252 observations.

## Use

- Target section: **RQ1**.
- Check sample period, country coverage and estimator before comparing any coefficient with yours.

## Verification

- Bibliographic record resolved through Crossref (DOI, title, authors, year, outlet).
- "Why it matters" is the reviewer's judgement, not the authors' claim.
