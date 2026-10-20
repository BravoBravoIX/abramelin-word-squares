# The Abramelin word squares: do symmetry breaks find copying slips?

The *Book of Abramelin*, or *Des Abraham von Worms Buch der wahren Praktik von der alten Magie*,
is a German book of magic written between about 1595 and 1609; it survives in many later hand
copies. Its fourth book holds about 250 squares of capital letters, each for a
magical purpose. Most are word squares like the Roman SATOR square: they read the same across
and down, and many read the same upside down too. The copies disagree in many letters.

This study asks one practical question about those copies: when a square's symmetry is broken
in one copy, does that break mark a copying slip? It tests the idea on copies that were not
used to find the breaks, and then asks which copies share the same slips.

**What is new, in one sentence.** Rick-Arne Kollatsch (2021) published W1's 257 squares and used
their symmetry by hand to correct that copy; this study tests the idea for the first time on
held-out copies and finds that where one copy breaks a symmetry, another copy usually differs
in exactly that cell and often has the letter the symmetry predicts (Leipzig against Mathers:
9 of 12 flagged cells differ, against 16 % of ordinary cells), and that the slips W1 still
carries recur in the other copies far more often than chance.

This is a study of how a text was copied. The squares are not a cipher and nothing here is a
decipherment. Where the evidence is short of proof, this README says "the evidence weighs
toward".

October 2026. CPU only; Python with numpy and scipy. The analysis reruns in about five minutes.

**Archived on Zenodo** with its paper, code, data and results: doi:10.5281/zenodo.XXXXXXXX
(to be added when the first release is archived; see How to cite at the end).

**The paper:** [`paper/abramelin-word-squares.pdf`](paper/abramelin-word-squares.pdf) (working
paper: abstract, method, results, discussion and references; built from
`paper/abramelin-word-squares.typ` by `paper/build.sh`). The README below covers the same
ground in more detail.

## In short

| Question | Answer | How firm |
|---|---|---|
| Are the squares really symmetric? | Yes, most of them. In Kollatsch's W1 text 237 of 257 squares have at least one symmetry, 227 of them reading the same across and down | None of 257,000 shuffled copies of the same squares passes the same rule. Leipzig (L): 207 of 250 (1 of 250,000 shuffles). Mathers (M): 115 of 242, because many of his squares are only partly filled |
| Where symmetry breaks in one copy, does another copy differ there? | Yes, in all four pre-registered directions | L → M: 9 of 12 flagged cells differ, against 15.8 % of ordinary cells (Holm p 2.7e-5). M → L: 4 of 5 against 17.9 % (Holm p 0.009). W1 → L: 2 of 2 against 14.0 % (Holm p 0.020) |
| Does the other copy have the letter the symmetry predicts? | Often | L → M: 5 times, against 1.00 expected (p 0.0007); M → L: 3 against 0.61 (p 0.011); W1 → L: 1 against 0.33 (not significant) |
| How much of the copying error does symmetry catch? | Little | 3–19 % of the cells where two copies differ inside symmetric squares fall in broken orbits; most differences keep the symmetry, as if letters were changed in matching pairs |
| Do copies share slips? | W1's surviving slips recur in L and in Mathers | W1–L: 8 shared, 0.91 expected (Holm p 0.0003); W1–M: 7 against 0.36 (0.0003); L–M: 3 against 0.95 (0.065, not significant) |
| Does the letter folding matter? | No | Without i/j and u/v folding (pre-registered) and with I/T folded (post hoc), every conclusion stands |
| Anything else? | L has 37 squares that keep only the half-turn symmetry, W1 has 3 | Not pre-registered; it fits a copyist who wrote half a square and filled the rest by turning it. To be tested on more copies |

## 1. The problem

**The squares.** The fourth book of the *Buch der wahren Praktik* gives letter squares from
4 × 4 to 12 × 12 (in L most are 5 × 5 or 7 × 7), in about thirty chapters by purpose (in L, for
example, "Vergangene Sachen zu wissen", to know things past, and "Mauern niederwerffen", to
throw down walls). Kollatsch (2021) counts 257 in the best copy, W1. Many read the same across
and down (row *k* equals column *k*), and many also read the same rotated by a half turn and
mirrored in the other diagonal, as the SATOR square does. The full square can then be written
from a few of its words.

**The copies.** Kollatsch (2020, 2021) lists 28 manuscript copies in 20 libraries. Their squares
disagree, and in some copies whole squares are missing or only partly filled. A copyist who did
not understand the letters (most are not words in any language) had nothing to guide him but the
letters in front of him.

**The idea.** If a square was composed to be symmetric, a cell that breaks the symmetry in one
copy is a candidate copying slip, and the symmetric partner cell suggests the original letter.
Kollatsch says the symmetries "proved a helpful means of emendation" when he edited W1
(edition, p. XV); he applied them by hand to one copy. We found no test of how well the method
works, which needs a copy that was not used to find the breaks.

**The questions**, made checkable and written down before any score was computed
([`PREREG.md`](PREREG.md)):
1. **Test A.** Which squares in each copy have which symmetries, by a fixed statistical rule
   with shuffled controls?
2. **Test B.** Where symmetry breaks in one copy, does a second copy (never used to find the
   break) differ in that cell more often than in ordinary cells (B1)? Does it have the letter
   the symmetry predicts (B2)? Where a break involves only two cells and so cannot say which is
   wrong, is the pair equal in the second copy (B3)?
3. **Test C.** Do two copies share the same wrong letter in the same cell more often than
   chance? Shared slips point to a shared ancestor below the original.

## 2. Sources

| Copy (Kollatsch's siglum) | What | Form used here | Rights |
|---|---|---|---|
| **W1** Wolfenbüttel, Herzog August Bibliothek, Cod. Guelf. 47.13 Aug. 4°, about 1609–13 | the oldest complete and best copy (Kollatsch) | Kollatsch's figures of the 257 squares (KCWorks, doi:10.17613/3hfq-9a74, 2021): an **edited** text, W1 with a few of his conjectures | CC BY-NC-ND 4.0. Fetched by `scripts/fetch_sources.sh` and read locally; **not redistributed**; no W1 letter is in this repository, only counts, labels, cell positions and symmetry types (see Licensing) |
| **L** Leipzig, Universitätsbibliothek, Cod. mag. 15, German, 17th–18th century | a second German copy | **our own transcription** (`data/L_read.json`, `data/L_corrections.json`), from the library's digitisation as mirrored on archive.org (`Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750_232`, 91 page images of the squares section) | the manuscript is in the public domain; UB Leipzig publishes its digitised public-domain holdings under the Public Domain Mark. Our transcription: CC BY 4.0 |
| **M** S. L. MacGregor Mathers, *The Book of the Sacred Magic of Abra-Melin the Mage*, 2nd ed. (London: Watkins, 1900), translated from the French copy Paris, Bibliothèque de l'Arsenal, MS 2351 | the French line of the text | the squares of Book III as typeset in a 1999 digital edition (archive.org `sacred-magic-abramelin`, `Abramelin_3.pdf`), parsed by `code/parse_mathers.py` into `data/m_squares.json` | public domain (Public Domain Mark); the parse is ours, CC BY 4.0 |

Matched across copies (same size, at least half the cells equal, one to one): W1–L 241 squares,
W1–M 209, L–M 194 (`results/census.json`, `matches`).

**How L was read.** Each of the 91 page images was read by Claude (Anthropic's API, model
`claude-opus-5-5`, seed 20261020, one page per call), told to copy every letter exactly and
never to correct anything towards a pattern or a symmetry. The prompt, the model's answer for
each page and the SHA-256 of each image are kept in `data/L_read.json`; the reading cost
3.97 US dollars. The API reader declined two pages (p069 and p070); those six squares were read
by eye. Then, as the pre-registration requires, every L cell that counted in Test B was checked
against the page image: 59 cells, of which 43 stood as read, 5 were corrected (clear misreadings)
and 11 were set to unreadable, mostly the scribe's I and T capitals, which look almost alike
(`data/L_corrections.json`, `data/eyecheck.json`). Five pages chosen at random (594 cells) were
checked cell by cell: no clear misreading, about 8 ambiguous I/T/F forms. These eye checks were
made by the AI coding assistant (Claude, in a Claude Code session) looking at the page images,
not by a palaeographer. L gives 255 squares, of which 250 are square-shaped and enter the tests
(the other 5 are not square as read, for example a first row one letter longer than the
square, and are left out).

**Mathers.** The parse of the typeset edition gives 242 squares; only 74 are fully filled, as
Mathers printed many squares partly empty. Blank cells count as missing. A few oversized squares
whose layout the parser could not resolve were left unmatched rather than forced.

## 3. Method

All random processes use the seed 20261020. Letters are lower-cased, long s is s, and i/j and
u/v are folded (one letter each) in the primary run; a run without that folding was
pre-registered as secondary.

**Symmetries.** Six symmetries of an *n* × *n* grid: T (reads the same across and down),
A (mirror in the other diagonal), R2 (half turn), R1 (quarter turn), H (left–right mirror) and
V (top–bottom mirror).

| Script | What it does |
|---|---|
| `code/sq.py` | Loading the three copies, the normalisation, the six symmetries, square matching |
| `code/parse_w1.py` | Kollatsch's figures (from `pdftotext -bbox`) into grids, written only to the git-ignored `work/` folder |
| `code/parse_mathers.py` | Mathers's squares (from `pdftotext -bbox`) into `data/m_squares.json` |
| `code/analyse.py` | Tests A, B and C; writes `results/census*.json`, `results/slips*.json`, `results/shared*.json` |
| `code/summary.py` | Prints the numbers used in this README from the results files |
| `code/run_all.sh` | The whole chain from the fetched sources |

**Test A, census.** A square *has* a symmetry when at least 85 % of the cell pairs that the
symmetry links hold equal letters, and the binomial chance of that many equal pairs, given the
square's own letter frequencies, is below 3.2 × 10⁻⁵ (Bonferroni for 6 symmetries × about 260
squares). The same rule is applied to 1,000 random shuffles of each square's own letters.

**Test B, held-out slips.** In a square with a set of symmetries, the cells that the symmetries
tie together form *orbits*; an orbit is *broken* if its letters are not all equal. Where a
broken orbit has a strict majority letter, each cell against the majority is a *predicted slip*,
with the majority letter as the predicted original. Then the matched square in another copy,
never used to find the break, is looked at:
- **B1:** is that copy's letter different at predicted slips more often than at cells of
  unbroken orbits in the same squares? One-sided Fisher exact test; Holm's correction over the
  four main directions (W1 → L, L → W1, L → M, M → L).
- **B2:** where it differs, is it the predicted letter? Chance is that letter's share in the
  held-out square (exact Poisson-binomial tail).
- **B3:** for broken two-cell orbits (no majority), is the pair equal in the held-out copy?
- Also: *precision* (predicted slips where the held-out copy has the predicted letter) and
  *recall* (share of all cells where the two copies differ, inside symmetric squares, that lie
  in broken orbits).

The pre-registration named the weak points in advance: W1 is Kollatsch's edited text, so where
he removed a slip by symmetry, it is already gone. With W1 as the held-out copy (L → W1) the
test is biased towards success; with W1 as the source (W1 → L) there are few breaks left to
test. **The clean comparison is between L and M**, two copies Kollatsch's editing never
touched.

**Test C, shared slips.** On squares matched in all three copies with a symmetry in at least two,
each orbit's reference letter is the strict majority over all its cells in all three copies; a
cell is a *slip* in a copy when it differs from the reference. Two copies *share* a slip when
both have the same wrong letter in the same cell. Control: 10,000 permutations that move each
copy's slips to random cells of the same square, keeping their number and letters; one-sided
p per pair, Holm over the three pairs.

**Pre-registration.** `PREREG.md` was written and committed before any symmetry, slip or
shared-slip score was computed on any copy (only square counts and sizes had been checked). It
was committed on 20 October 2026 at 07:12 UTC as commit `eb1d554` of the author's private
working repository, and is reproduced here unchanged (SHA-256
`ae4180297fac5288f920570f31877e07bdeca8456ed28d4ffaf9bfeb96639935`). Readers cannot check this
timing, since that repository is private. Its references to `docs/occult-plan.md`, a decision
number and `hunter/transcribe/remote.py` point into that repository (the plan of the wider
programme and the API client used to read L); neither is needed here.

## 4. Results

All numbers below come from `results/*.json` (primary, pre-registered run unless said
otherwise); `python3 code/summary.py results` prints them.

### Test A: most squares are true word squares (`results/census.json`)

| | squares | any symmetry | across = down (T) | at least T + A + R2 | none | shuffled controls passing |
|---|---|---|---|---|---|---|
| W1 (Kollatsch, edited) | 257 | 237 | 227 | 144 | 20 | 0 of 257,000 |
| L (Leipzig) | 250 | 207 | 162 | 127 | 43 | 1 of 250,000 |
| M (Mathers) | 242 | 115 | 107 | 63 | 127 | 0 of 242,000 |

- In W1, 138 squares have exactly T + A + R2 (the SATOR pattern), 80 only T, and 6 all six
  symmetries. 224 W1 squares are exact (every linked pair equal) in at least one symmetry.
- L has 37 squares with the half turn (R2) only, W1 has 3 and M 5. This was not pre-registered.
  It is what one gets if a copyist wrote the first half of a square and completed it by turning
  it, so that a slip in the first half reappears in the second and the across-and-down symmetry
  is lost while the half turn survives.
- Mathers's low count comes mostly from partly empty squares, which have too few linked pairs
  to pass the rule.

### Test B: symmetry breaks point at copying slips (`results/slips.json`)

| source → held out | matched squares | predicted slips | held-out copy differs | ordinary cells differing | B1 p (Holm) | held-out has predicted letter / chance | B2 p |
|---|---|---|---|---|---|---|---|
| W1 → L | 241 | 2 | 2 | 14.0 % | 0.020 | 1 / 0.33 | 0.30 |
| L → W1 | 241 | 37 | 32 | 12.1 % | 6.7e-24 | 26 / 3.51 | 1.2e-21 |
| L → M | 194 | 12 | 9 | 15.8 % | 2.7e-5 | 5 / 1.00 | 6.6e-4 |
| M → L | 194 | 5 | 4 | 17.9 % | 0.0089 | 3 / 0.61 | 0.011 |
| W1 → M (secondary) | 209 | 1 | 1 | 9.5 % | (0.095 raw) | 1 / 0.12 | 0.12 |
| M → W1 (secondary) | 209 | 5 | 5 | 9.3 % | (7.5e-6 raw) | 3 / 0.65 | 0.016 |

- All four pre-registered B1 tests pass after Holm's correction. In the clean pair, L → M and
  M → L, flagged cells differ in the other copy 75–80 % of the time, against 16–18 % for
  ordinary cells.
- **B3, two-cell breaks.** Where L breaks a pair of cells, W1 has the pair equal 88 of 101
  times (13.1 expected by chance; at unbroken pairs 1,681 of 1,914) and Mathers 24 of 28 (5.1
  by chance; 609 of 659). Where W1 breaks a pair, L has it equal 19 of 35 times (4.3 by chance).
- **Precision and recall.** Of the predicted slips, the held-out copy has the predicted letter
  in 42 % (L → M) to 70 % (L → W1). But symmetry finds only a small share of the differences:
  of the cells where two copies differ inside symmetric squares, 3 % (M → L) to 19 % (L → W1)
  lie in broken orbits. Most differences between the copies keep the symmetry: the copyists
  changed letters in matching pairs, or the differences go back to an ancestor that was
  already consistent.
- W1 → L is nearly empty (2 predicted slips) because Kollatsch already corrected most of W1's
  breaks; L → W1 is inflated by the same editing. Both were stated in advance.

### Test C: which copies share slips (`results/shared.json`)

196 squares are matched in all three copies; 172 have a symmetry in at least two and are used.
Slips counted: W1 71, L 561, M 283.

| pair | shared slips | expected by chance | p | Holm |
|---|---|---|---|---|
| W1–L | 8 | 0.91 | 0.0001 | 0.0003 |
| W1–M | 7 | 0.36 | 0.0001 | 0.0003 |
| L–M | 3 | 0.95 | 0.065 | 0.065 |

(0.0001 is the smallest p that 10,000 permutations can give.) The slips W1 still carries
recur in L and in the French line through Mathers; L and Mathers share no more than chance
allows. With three copies this ranks the pairs; it is not a family tree.

### The same with other letter folding (`results/*_nofold.json`, `results/*_foldit.json`)

- **No i/j, u/v folding** (pre-registered secondary): the same picture. L → M 9 of 12 against
  16.0 % (Holm p 3.0e-5); W1–L 8 shared against 0.91, W1–M 7 against 0.38, L–M 3 against 0.98.
- **I and T folded** (post hoc, added after the eye checks showed how alike L's I and T are;
  labelled as such): L → M 12 of 15 against 14.3 % (Holm p 7.4e-8), predicted letter 8 times
  against 1.71; M → L 4 of 5; W1–L 8 shared against 0.96, W1–M 7 against 0.39, L–M 4 against
  1.59 (p 0.067). The pre-registered numbers above are the primary ones.

### Other observations about L (descriptive, from the eye checks)

- L's scribe writes capital I as a J with a cross-stroke and T as a J with a top bar; they are
  often hard to tell apart. Most cells set to unreadable are such forms.
- Some letter swaps between L and W1 recur many times (h for s, f for i, n for m; noticed while
  checking, not counted in the results files). They look like an earlier copyist misreading a
  German-script exemplar. They keep the symmetry, so symmetry checks cannot see them.
- A later hand corrected letters in black ink in several squares; the final letter was
  transcribed. A reader's note on p023 says two squares stand in the wrong place.

## 5. Verdict

- **The squares were composed as symmetric word squares**, most in the SATOR pattern, and the
  symmetry survives copying well enough to be measured in every copy.
- **Symmetry breaks do mark copying slips.** Tested on copies that were not used to find them,
  a flagged cell is four to seven times as likely to differ in another copy as an ordinary cell,
  and the other copy often has the letter the symmetry predicts. The evidence weighs toward
  Kollatsch's editorial method being sound where it applies.
- **But it applies to few slips.** Symmetry flags only 3–19 % of the cells where two copies
  differ. Most changes kept the symmetry, so symmetry can correct a copy but cannot by itself
  reconstruct the original.
- **The copies are related through W1 or a close relative of it.** W1's surviving slips recur in
  both L and the French line, while L and the French share no more slips than chance. The
  evidence weighs toward L and the French copy both descending from W1 or a near relative, which
  fits Kollatsch's ranking of W1 as the best copy. A family tree needs at least four copies.

## 6. What is new, and what earlier work did

This study stands on the work of others:

- **Rick-Arne Kollatsch** edited the text from W1, showed that W1 is the oldest complete and
  best copy, dated the work to 1595–1609 from its use of the dictionary *Sylva quinquelinguis
  vocabulorum* (1595/96), listed 28 copies, and **published figures of all 257 squares of W1**, with his
  conjectures, open access (KCWorks, doi:10.17613/3hfq-9a74, 9 February 2021, CC BY-NC-ND 4.0).
  **The idea that the squares' symmetry exposes copying slips is his**: he used it by hand to
  emend W1 (edition, p. XV), and noted that "not all symmetrical errors can be corrected". His
  apparatus reports variants from three other copies (Wellcome MS 821, Leipzig Cod. mag. 15,
  Vienna Cod. 10580), as a rule only where two of the three agree against W1; it is not a full
  collation of the squares. His promised second volume, on the whole textual tradition, had not
  appeared when we searched (20 October 2026). His W1 squares are the reference text of this
  study, not a rival to it.
- **S. L. MacGregor Mathers** (1898; 2nd ed. 1900) translated the French copy, Arsenal MS 2351,
  with 242 squares, many only partly filled.
- **Georg Dehn** (*Buch Abramelin*, 2001; English translation by Steven Guth, 2006, revised
  2015) published a German text from several younger copies with all squares filled; it has no
  critical apparatus of the squares (some variants are given in endnotes). We did not use it (copyright; not read).
- **Joseph H. Peterson** (Esoteric Archives) published a digital edition of Mathers with
  variants from Dehn. It does not collate the squares.

What this study adds, as far as our search found (web, GitHub, KCWorks; Zenodo's search could
not be reached; 20 October 2026):
1. **A test of the symmetry method on held-out copies**: where one copy breaks a symmetry,
   another copy that was not used differs there far more often than at ordinary cells and often
   has the predicted letter, with the measured precision and the low recall.
2. **Shared-slip evidence for how the copies are related**: W1's surviving slips recur in L and
   in the French line; L and the French share no more than chance.
3. **A census of symmetry types copy by copy**, by a stated statistical rule with shuffled
   controls.
4. **A new transcription of the squares of Leipzig Cod. mag. 15**, published as data.
5. The **half-turn-only squares of L** (37 against 3 in W1), an observation to test on more copies.

## 7. Caveats and open checks

1. **W1 is an edited text, and assembled.** In W1 the squares are written as sequences of letter
   groups in the running text, from which Kollatsch put the 257 squares together (edition,
   p. XV; deposit description), with a few conjectures, some of them made by symmetry. We have not
   seen W1 itself (no images are online). If some cells of the figures follow from symmetry
   by construction, W1's census figures overstate the scribe's own symmetry. This is why the
   clean evidence for Test B is L against M.
2. **L was read by a model and checked by an AI assistant.** The reader was told not to correct,
   and the eye checks covered every cell that counted in Test B and five random pages, with
   corrections that made the result weaker, not stronger (before them, L → M had 14 of 17
   flagged cells differing; `results/run_records.json`).
   But no palaeographer has checked the transcription, and I/T remains uncertain in places.
3. **Mathers is a translation's printed squares, retyped.** M is a 1999 typesetting of the 1900
   edition, not the Arsenal manuscript, and many squares are partly empty. Its slips may be
   Mathers's, his printer's or the 1999 typesetter's, as well as the French copyists'.
4. **Only three copies.** Test C ranks pairs; it cannot place the copies in a tree. The
   pre-registered tree method (maximum parsimony with bootstrap and controls) waits for at least
   four transcribed copies. The candidates are the Dresden copies (SLUB Mscr.Dresd.N.111 and
   N.161), the Arsenal manuscript itself, W1's images and W3 (Wolfenbüttel Cod. Guelf. 10.1 b
   Aug. 2°, said to be the source of the French), and Wellcome MS 820 and 821 (not digitised).
5. **Deviations from the pre-registration.** The I/T-folded run was added after the eye checks
   and is labelled post hoc. The cells eye-checked were those flagged by the first, uncorrected
   run; cells that became flagged only after the corrections were not checked one by one (they
   fall under the random audit's error rate).
6. **The half-turn observation** was noticed after the results and is not a tested claim.

## 8. How to reproduce

Needs Linux or macOS with `bash`, `curl`, `sha256sum`, `pdftotext` (poppler) and
[`uv`](https://docs.astral.sh/uv/) (which supplies Python 3.13 with numpy 2.5.4 and scipy
1.18.1, the versions the results were made with; set `PYTHON` to use another interpreter that
has both).

```
scripts/fetch_sources.sh sources/downloads    # about 0.8 MB; checks SHA-256 sums
code/run_all.sh sources/downloads             # about 5 minutes on CPU (three runs in parallel)
git status --short results/ data/             # should be empty
```

`fetch_sources.sh` downloads Kollatsch's squares from KCWorks and Mathers's Book III from
archive.org and checks each against `sources/SHA256SUMS`, the copies the published results were
made from (downloaded 20 October 2026). With `WITH_L_IMAGES=1` it also fetches the 91 Leipzig
page images (JPEG 2000, 99 MB) for anyone who wants to check our transcription; image `_00NN`
is page `pNNN` in `data/L_read.json`. (The SHA-256 sums of pages in `data/L_read.json` are of the
JPEG copies the reader was sent, not of the JPEG 2000 files.)

`run_all.sh` parses Kollatsch's figures into `work/` (git-ignored; the parse equals the one
the published results were made from), rebuilds
`data/m_squares.json` from Mathers, and writes the nine results files. From a clean fetch on
20 October 2026 it rebuilt every one of them, and `data/m_squares.json`, byte for byte. The
results files hold no machine- or time-dependent fields; the commit of the original run is in
`results/run_records.json`.

**Not rerun:** the reading of L by the Claude API. Its answers are recorded data
(`data/L_read.json`), with the prompt, model, seed and per-page cost; the eye-check corrections
are applied from `data/L_corrections.json`. The reading script depended on the author's private
API client and is not included.

## Licensing

- **Code** (`code/`, `scripts/`, `paper/build.sh`): MIT, see `LICENSE`.
- **Our data, results and paper** (`data/`, `results/`, `paper/`, `PREREG.md`, this README):
  CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). `data/L_read.json` and
  `data/L_corrections.json` are our transcription of a public-domain manuscript;
  `data/m_squares.json` is our parse of Mathers's public-domain edition;
  `data/eyecheck.json` is the log of the eye checks.

**Left out, and why:**
- **Kollatsch's figures of the W1 squares** (CC BY-NC-ND 4.0): the licence does not allow
  sharing adapted material, so neither the PDF nor the parsed squares are included, and no W1
  letter is written to any published file. `scripts/fetch_sources.sh` downloads his deposit from
  KCWorks and the code reads it locally into `work/`. The results keep only counts, square labels,
  cell coordinates, the symmetry types of W1 squares and, for each predicted slip with W1 held
  out, whether W1 differs and whether it has the predicted letter.
- **Kollatsch's edition and its reading samples**: read for the prior-art check; not included.
- **Dehn's edition**: copyright; not used.
- **Page images**: none are included; the Leipzig images can be fetched (see above).
- **The API reading script**: it called the author's private client and is not needed to rerun
  the analysis; its prompt is recorded in `data/L_read.json`.

## References

- Wolfenbüttel, Herzog August Bibliothek, Cod. Guelf. 47.13 Aug. 4° (W1); Cod. Guelf. 10.1 b
  Aug. 2° (W3).
- Leipzig, Universitätsbibliothek, Cod. mag. 15. Digitised by UB Leipzig; archive.org mirror
  https://archive.org/details/Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750_232
- Paris, Bibliothèque de l'Arsenal, MS 2351.
- Rick-Arne Kollatsch, *Figures of the 257 magical letter squares from »Abraham's of Worms Book
  of the True Practice of the Old Magic«*, KCWorks (Humanities Commons), 9 February 2021,
  doi:10.17613/3hfq-9a74 (CC BY-NC-ND 4.0).
- Rick-Arne Kollatsch (ed.), *Des Abraham von Worms Buch der wahren Praktik von der alten Magie.
  Ein als jüdisch fingierter Magietext des frühen 17. Jahrhunderts. Band 1 – Edition*, Hamburg:
  tredition, 2020; 2nd revised ed. 2021, ISBN 978-3-347-26288-1. Reading samples:
  doi:10.17613/bsqa-s816 (1st ed.), doi:10.17613/8dq6-6m31 (2nd ed.).
- Rick-Arne Kollatsch, *Historische Handschriften von »Des Abraham von Worms Buch der wahren
  Praktik von der alten Magie«* (list of copies), KCWorks, 2021, doi:10.17613/kfhy-m385.
- Rick-Arne Kollatsch, "Abraham of Worms, the disciple of »Abramelin the Mage«", KCWorks, 2021,
  doi:10.17613/2mtz-ya12.
- S. L. MacGregor Mathers (tr.), *The Book of the Sacred Magic of Abra-Melin the Mage*, London:
  Watkins, 1898; 2nd ed. 1900. Digital edition https://archive.org/details/sacred-magic-abramelin
- Georg Dehn (ed.), *Buch Abramelin*, Leipzig: Edition Araki, 2001; *The Book of Abramelin: A New
  Translation*, tr. Steven Guth, Lake Worth, FL: Ibis Press, 2006 (revised 2015).
- Joseph H. Peterson (ed.), *The Book of the Sacred Magic of Abramelin the Mage*, digital
  edition with variants from Dehn, Esoteric Archives (esotericarchives.com), updated
  7 December 2025.
- Henrik Bogdan, review of Dehn, *The Book of Abramelin*, *Correspondences* 4 (2016).
- Sture Holm, "A simple sequentially rejective multiple test procedure", *Scandinavian Journal of
  Statistics* 6 (1979), 65–70.

## Versions

- **1.0** (20 October 2026): Tests A, B and C on W1, L and M; the L transcription; the paper.

## How to cite

Burford, B. (2026). The Abramelin word squares: do symmetry breaks find copying slips?
(version 1.0). Zenodo. doi:10.5281/zenodo.XXXXXXXX (to be added).
Source: https://github.com/BravoBravoIX/abramelin-word-squares
