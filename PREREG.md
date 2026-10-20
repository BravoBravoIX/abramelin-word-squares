# Abramelin Book IV letter squares: pre-registration

Version 1.0, 20 October 2026. Written and committed **before any symmetry, error-location or stemma score was computed** on any witness. Only parsing checks (square counts and sizes) had been run. Occult programme project #1 (`docs/occult-plan.md`, D102). Nothing here is a cipher; nothing is called solved.

## Witnesses used in this run

| Siglum (Kollatsch) | What | Form we use | Rights |
|---|---|---|---|
| W1 | Wolfenbüttel HAB Cod. Guelf. 47.13 Aug. 4°, about 1609–13 | Kollatsch's figures of the 257 squares (KCWorks doi:10.17613/3hfq-9a74, 2021). **An edited text**: W1 plus his "few cautious conjectures" | CC BY-NC-ND 4.0: used privately for computation; the squares are not redistributed or adapted in this repository (only counts, cell coordinates and hashes) |
| L | Leipzig UB Cod. mag. 15, German, 17th–18th c. | Our transcription from the UB Leipzig digitisation (archive.org mirror `Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750_232`) | UB Leipzig open digitisation policy: public-domain holdings under the Public Domain Mark |
| M | Mathers 1898/1900 English translation of the French Arsenal MS 2351 | 1999 typeset digital edition of the 1900 second edition (archive.org `sacred-magic-abramelin`, Public Domain Mark) | Public domain |

W1 is an edited text. Where Kollatsch emended a W1 slip by symmetry, the slip is already gone from our W1. This biases any test in which W1 is the **held-out** witness towards success; tests with W1 as the **source** of breaks are not biased this way (they see only the breaks he left). This is stated with every result.

## Normalisation (fixed)

Lowercase; long s `ſ` = `s`; umlauts kept as written. Primary comparisons fold `j`→`i` and `v`→`u` (interchangeable letter forms in German hands of the period); a secondary run without folding is reported beside it. `?` (unreadable) and blank cells are missing and drop out of every comparison that needs them.

## Square matching between witnesses

Squares are matched across witnesses by size and by the highest share of equal cells in the same orientation (identity only), one-to-one (greedy, best first), with a minimum of 50 % equal cells. Unmatched squares are listed, not forced.

## Test A: symmetry census (per witness)

Symmetries of an n×n grid (cell (r,c), 0-based): T rows = columns (r,c)→(c,r); A anti-diagonal (r,c)→(n-1-c,n-1-r); R2 half turn (r,c)→(n-1-r,n-1-c); R1 quarter turn (r,c)→(c,n-1-r); H left-right mirror (r,c)→(r,n-1-c); V top-bottom mirror (r,c)→(n-1-r,c).

- **Agreement** of a square with symmetry g: share of unordered cell pairs {c, g(c)} with c ≠ g(c) whose letters are equal (both present).
- **Control**: 1,000 random permutations of the same square's own letters (seed 20261020 + square index); the control agreement for g is computed the same way.
- A square **has** symmetry g when agreement ≥ 0.85 **and** the one-sided binomial p of that many equal pairs, with the square's own letter-collision rate (sum of squared letter shares) as the per-pair chance, is below 3.2e-5 (Bonferroni for 6 symmetries × about 260 squares at family-wise 0.05). **Exact** when agreement = 1. The permutation controls are classified by the same rule.
- Reported: counts per symmetry and combination per witness; the list of squares with no symmetry; the same census on the permuted controls (expected about 0).

## Test B: do symmetry breaks locate copying slips? (held-out witness)

For a square with symmetry set S in witness X, the **orbits** are the connected components of cells linked by every g in S. An orbit is **broken** when its letters are not all equal. In a broken orbit with a unique strict-majority letter m, each minority cell is a **predicted slip** with predicted original m. Broken orbits of two cells (no majority) are **located but unresolved**.

Held-out check: the matched square in another witness Y, never used to find the break.

- **B1 (location)**: share of predicted slip cells where Y ≠ X, against the share among cells of unbroken orbits of the same squares (control cells). One-sided Fisher exact test.
- **B2 (repair)**: among predicted slips where Y ≠ X, share where Y = m; chance = frequency of m among Y's letters in that square (one-sided binomial on the summed expectation, Poisson-binomial approximated by normal if needed; exact binomial with the mean chance as fallback).
- **B3 (unresolved)**: for two-cell broken orbits, share where Y has the two cells equal (symmetric), against the same share at control two-cell orbits that are unbroken in X (expected near 1) and at random cell pairs of the same square (chance).
- Directions: W1→L, L→W1, L→M, M→L (and W1→M, M→W1 where M has the square filled). Holm correction over the B1 tests of the four main directions at family-wise α = 0.05. **The clean directions are W1→L and L→M / M→L**; L→W1 is reported with the edited-text caveat.
- Also reported (descriptive): precision (share of predicted slips confirmed by Y) and recall (share of X≠Y differences inside symmetric squares that fall in broken orbits).

## Test C: shared slips and the copy family (three witnesses)

On squares matched in W1, L and M with a symmetry found in at least two of them: in each orbit the **reference letter** is the strict majority over all cells of the orbit in all witnesses together; a cell in a witness is a **slip** when its letter differs from the reference. Two witnesses **share** a slip when both have the same wrong letter in the same cell.

- Statistic per pair: observed shared slips minus the number expected if slips fell independently (sum over cells of the product of the two witnesses' per-square slip rates, letter-matched).
- Control: 10,000 permutations that move each witness's slips to random cells of the same square (keeping its slip count and the wrong letters), seed 20261020; one-sided p per pair, Holm over the three pairs.
- Reading: a pair with excess shared slips shares an ancestor below the archetype. With three witnesses this ranks pairs only; it is not a full tree.

## Full stemma (pre-registered now; run only when four or more witnesses are transcribed)

Characters: slip cells as above (reference by orbit majority over all witnesses). Method: maximum parsimony over unrooted trees (exhaustive up to 8 witnesses), support by 1,000 bootstrap resamples of squares (seed 20261020); controls: (i) the same pipeline on slips shuffled between squares, (ii) the parsimony score distribution over 1,000 random trees. Claims tested: D2 (N 161) independent of the Wolfenbüttel group; the French (Pa1, Mathers) from Cod. Guelf. 10.1 (W3).

## Transcription rules for L (fixed before reading)

- Reader: Claude through `hunter/transcribe/remote.py` (transport `anthropic`, model `claude-opus-5-5`, seed 20261020), one page image per call, told to copy letters exactly as written and **never** to correct towards a pattern or symmetry. Batch budget 8 USD for L (project cap 15 USD).
- Eye checks (by the session, from the page image): (1) every L cell that counts as a **success** in B1/B2 with L as the held-out witness, and every L cell that is a predicted slip with L as source; (2) a random sample of 5 pages (seed 20261020) checked cell by cell, error rate reported. Corrections are logged with the image crop hash.

## Stop rule and honesty

One run of each test on the data as transcribed. No threshold, orientation or normalisation is changed after scores are seen; any later change is a new, labelled version. Negative results are kept.
