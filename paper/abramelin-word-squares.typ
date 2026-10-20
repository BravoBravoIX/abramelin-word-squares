// Working paper for the abramelin-word-squares repository. Build: paper/build.sh
#set document(title: "The Abramelin word squares: do symmetry breaks find copying slips?", author: "Brett Burford")
#set page(paper: "a4", margin: (x: 2.3cm, y: 2.4cm), numbering: "1")
#set text(font: ("Libertinus Serif", "New Computer Modern"), size: 10.5pt, lang: "en", region: "au")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#1a4f8b"))
#set table(stroke: 0.4pt + luma(150), inset: 5pt)
#show table: set text(size: 9.2pt)
#show table: set par(justify: false)

#align(center)[
  #text(size: 16pt, weight: "bold")[The Abramelin word squares: do symmetry breaks find copying slips?]
  #v(0.5em)
  #text(size: 11pt)[Brett Burford]
  #v(0.2em)
  #text(size: 9pt)[ORCID #link("https://orcid.org/0009-0003-6599-8297")[0009-0003-6599-8297] · Independent researcher, Australia]
  #v(0.2em)
  #text(size: 9pt)[Working paper, version 1.0, 20 October 2026 · not peer reviewed]
  #v(0.2em)
  #text(size: 9pt)[Code, data and results: #link("https://github.com/BravoBravoIX/abramelin-word-squares")[github.com/BravoBravoIX/abramelin-word-squares]]
]

#v(0.8em)
#block(inset: (x: 1.2cm))[
  #text(weight: "bold")[Abstract.] The fourth book of the _Book of Abramelin_ (_Des Abraham von Worms Buch der wahren Praktik von der alten Magie_, written about 1595–1609) holds about 250 letter squares, most of them symmetric word squares of the SATOR kind. Kollatsch (2021) published the 257 squares of the best copy (Wolfenbüttel, Cod. Guelf. 47.13 Aug. 4°, W1) and used their symmetry by hand to correct its slips. We test that method on copies it was not applied to. We transcribed the squares of a second German copy, Leipzig, Universitätsbibliothek, Cod. mag. 15 (L, 250 squares), with a language-model reader followed by checks against the page images, and parsed the squares of Mathers's 1900 English translation of the French copy (M, 242). The tests, controls and corrections were written down and committed before any score was computed. By a fixed binomial rule, 237 of 257 W1 squares, 207 of 250 L squares and 115 of 242 M squares have at least one symmetry, against none of 257,000, one of 250,000 and none of 242,000 shuffled controls. Where a symmetry is broken in one copy, a held-out copy differs at the flagged cell far more often than at ordinary cells, in all four pre-registered directions after Holm's correction. In the comparison untouched by Kollatsch's editing, Leipzig against Mathers, 9 of 12 flagged cells differ against 15.8 % of ordinary cells, and Mathers has the letter the symmetry predicts 5 times where 1.0 is expected. The method is precise but sees little: only 3–19 % of the cells where two copies differ lie in broken symmetries, because most changes kept the symmetry. Slips that W1 still carries recur in L (8 shared, 0.91 expected) and in Mathers (7 shared, 0.36 expected), while L and Mathers share no more than chance (3, against 0.95). The evidence weighs toward Kollatsch's symmetry method being sound where it applies, and toward L and the French line descending from W1 or a close relative of it. A family tree of the copies needs at least one more transcribed copy.
]

= Introduction

The _Buch der wahren Praktik von der alten Magie_, known in English as the _Book of Abramelin_, presents itself as the work of a fifteenth-century Jew, Abraham of Worms. Kollatsch (2020, 2021) showed that it was written in German between 1595 and about 1609, probably by a Lutheran: its Hebrew and Greek words come from a printed school dictionary of 1595/96. It survives in some 28 manuscript copies in 20 libraries, the oldest complete and best of them Wolfenbüttel, Herzog August Bibliothek, Cod. Guelf. 47.13 Aug. 4° (W1, about 1609–13).

Its fourth book gives letter squares, grouped by magical purpose. Most are word squares like the Roman SATOR square: row _k_ reads the same as column _k_, and many also read the same after a half turn and when mirrored in the other diagonal, so that a whole square can be written from a few of its words. The letters are mostly not words in any language, and the copyists could not have understood them. The copies disagree in many letters, and in some copies whole squares are missing or only partly filled.

If a square was composed to be symmetric, a cell that breaks the symmetry in one copy is a candidate copying slip, and its symmetric partner suggests the original letter. Kollatsch used this idea to correct W1 by hand. This paper tests it, which needs a copy that was not used to find the breaks, and then asks which copies share the same slips. It is a study of how a text was copied; the squares are not a cipher and nothing here is a decipherment.

= Earlier work

- *Kollatsch* edited the whole text from W1 (2020; 2nd revised ed. 2021), listed 28 copies (2021b), and published figures of all 257 squares of W1, with a few of his conjectures, open access under CC BY-NC-ND 4.0 (2021a). In W1 the squares are written as sequences of letter groups ("Polygrammfolgen") in the running text, from which he put the squares together. In his introduction he writes that the squares' symmetries "proved a helpful means of emendation" for W1's slips (2020/2021, p. XV), and in the deposit that "not all symmetrical errors can be corrected". *The idea tested here is his.* His apparatus gives variants from three other copies (Wellcome MS 821, Leipzig Cod. mag. 15 and Vienna Cod. 10580), as a rule only where two of the three agree against W1; it is not a full collation of the squares, and a promised second volume on the textual tradition had not appeared by 20 October 2026.
- *Mathers* (1898; 2nd ed. 1900) translated the French copy, Paris, Bibliothèque de l'Arsenal, MS 2351, with 242 squares, many only partly filled.
- *Dehn* (2001; English translation by Guth, 2006, revised 2015) published a text from several younger copies with every square filled, without a critical apparatus of the squares. *Peterson* published a digital edition of Mathers with variants from Dehn, and None of these collates the squares or measures the symmetry method.

= Sources and data

*W1* is used in the form of Kollatsch's figures (2021a), parsed from the PDF's word coordinates into 257 complete grids. It is an edited and assembled text. Its licence does not allow adapted material to be shared, so the parsed squares are kept out of the published repository: a script fetches the deposit and the code reads it locally, and the results keep only counts, labels, cell coordinates and symmetry types.

*L*, Leipzig UB Cod. mag. 15 (German, seventeenth or eighteenth century), was transcribed for this study from the library's digitisation of the squares section, as mirrored on archive.org (91 page images; the library publishes its public-domain holdings under the Public Domain Mark). Each page was read by Claude (Anthropic's API, model claude-opus-5-5, seed 20261020, one page per call), told to copy every letter exactly and never to correct towards a pattern or symmetry; the reading cost 3.97 US dollars. The reader declined two pages, which were read by eye. As the pre-registration requires, every L cell that counted in the slip test was then checked against the page image: of 59 cells, 43 stood, 5 were corrected and 11 were set to unreadable, mostly the scribe's capital I and T, which look almost alike. A random sample of five pages (594 cells) showed no clear misreading and about 8 ambiguous I/T/F forms. These checks were made by the AI coding assistant looking at the images, not by a palaeographer. L gives 255 squares, of which 250 are square as read.

*M* is the squares of Mathers's Book III as typeset in a 1999 digital edition of the 1900 second edition (archive.org, Public Domain Mark), parsed onto a lattice so that blank cells stay blank: 242 squares, 74 of them fully filled.

Squares are matched between copies by size and the share of equal cells, one to one, with at least half the cells equal: W1–L 241 pairs, W1–M 209, L–M 194.

= Method

All random processes use the seed 20261020. Letters are lower-cased, long s is s, and in the primary run i/j and u/v are each folded to one letter; a run without folding was pre-registered as secondary. Unreadable and blank cells are missing.

*Symmetries.* Six symmetries of an $n times n$ grid are tested: T (row _k_ = column _k_), A (mirror in the other diagonal), R2 (half turn), R1 (quarter turn), H and V (left–right and top–bottom mirrors).

*Test A, census.* A square has a symmetry when at least 85 % of the cell pairs it links hold equal letters and the binomial probability of that many equal pairs, with the square's own letter-collision rate as the chance per pair, is below $3.2 times 10^(-5)$ (Bonferroni over 6 symmetries and about 260 squares). The same rule is applied to 1,000 random shuffles of each square's own letters.

*Test B, held-out slips.* The cells that a square's symmetries tie together form orbits; an orbit is broken when its letters are not all equal. Where a broken orbit has a strict majority, each cell against the majority is a predicted slip, with the majority letter as the predicted original. The matched square in another copy, never used to find the break, is then read. B1 asks whether that copy differs at predicted slips more often than at cells of unbroken orbits of the same squares (one-sided Fisher exact test; Holm's correction over the four main directions W1 → L, L → W1, L → M and M → L). B2 asks whether, where it differs, it has the predicted letter (chance: that letter's share in the held-out square; exact Poisson-binomial tail). B3 asks whether broken two-cell orbits, which have no majority, are equal in the held-out copy. Precision is the share of predicted slips where the held-out copy has the predicted letter; recall is the share of all cells where the two copies differ, inside symmetric squares, that lie in broken orbits. Because W1 is edited, the pre-registration stated in advance that L → W1 is biased towards success and that W1 → L has few breaks left; the clean comparison is L against M.

*Test C, shared slips.* On squares matched in all three copies with a symmetry in at least two, each orbit's reference letter is the strict majority over its cells in all three copies, and a cell is a slip in a copy when it differs from the reference. Two copies share a slip when both have the same wrong letter in the same cell. Control: 10,000 permutations that move each copy's slips to random cells of the same square, keeping their number and letters; one-sided p per pair, Holm over the three pairs.

*Pre-registration.* The tests, controls, corrections, transcription rules and a stop rule were written down and committed before any symmetry, slip or shared-slip score was computed on any copy; only square counts and sizes had been checked. The file was committed on 20 October 2026 at 07:12 UTC as commit `eb1d554` of the author's private working repository and is reproduced unchanged in the public repository. Readers cannot check this timing, since that repository is private. A tree method (maximum parsimony with bootstrap and controls) was registered at the same time, to run only when four or more copies are transcribed.

= Results

== Test A: most squares are true word squares

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, 1.3fr),
    align: (left, center, center, center, center, center, center),
    table.header([*Copy*], [*Squares*], [*Any symmetry*], [*T*], [*T + A + R2*], [*None*], [*Shuffled controls passing*]),
    [W1 (Kollatsch, edited)], [257], [237], [227], [144], [20], [0 of 257,000],
    [L (Leipzig)], [250], [207], [162], [127], [43], [1 of 250,000],
    [M (Mathers)], [242], [115], [107], [63], [127], [0 of 242,000],
  ),
  caption: [Symmetry census (`results/census.json`). T: reads the same across and down. T + A + R2: at least the three symmetries of the SATOR square.],
)

In W1, 138 squares have exactly the SATOR set T + A + R2, 80 only T, and 6 all six symmetries. Mathers's low count comes mostly from his partly empty squares, which have too few linked pairs to pass the rule. One pattern was noticed after the results and was not pre-registered: L has 37 squares that keep only the half turn, where W1 has 3 and M 5. That is what one would see if a copyist wrote half a square and completed it by turning it, so that the across-and-down symmetry is lost and the half turn kept.

== Test B: symmetry breaks point at copying slips

#figure(
  table(
    columns: (1.3fr, 1fr, 1fr, 1.1fr, 1fr, 1.2fr, 0.9fr),
    align: (left, center, center, center, center, center, center),
    table.header([*Source → held out*], [*Predicted slips*], [*Held-out copy differs*], [*Ordinary cells differing*], [*B1 p (Holm)*], [*Has predicted letter (chance)*], [*B2 p*]),
    [W1 → L], [2], [2], [14.0 %], [0.020], [1 (0.33)], [0.30],
    [L → W1], [37], [32], [12.1 %], [6.7e-24], [26 (3.51)], [1.2e-21],
    [L → M], [12], [9], [15.8 %], [2.7e-5], [5 (1.00)], [6.6e-4],
    [M → L], [5], [4], [17.9 %], [0.0089], [3 (0.61)], [0.011],
  ),
  caption: [The four pre-registered directions of Test B (`results/slips.json`). Matched squares: W1–L 241, L–M 194. L → W1 is biased towards success because W1 is Kollatsch's edited text; L ↔ M is the clean comparison.],
)

All four B1 tests pass after Holm's correction. Between L and M, flagged cells differ in the other copy 75–80 % of the time, against 16–18 % for ordinary cells, and the other copy has the predicted letter well above chance. Where L breaks a two-cell orbit, W1 has the pair equal 88 of 101 times (13.1 expected by chance; 1,681 of 1,914 at unbroken pairs) and Mathers 24 of 28 (5.1 by chance). The secondary directions agree: M → W1, 5 of 5 flagged cells differ against 9.3 % (raw p $7.5 times 10^(-6)$); W1 → M has a single flagged cell.

Precision is high and recall low. Of the predicted slips, the held-out copy has the predicted letter in 42 % (L → M) to 70 % (L → W1). But of the cells where two copies differ inside symmetric squares, only 3 % (M → L) to 19 % (L → W1) lie in broken orbits. Most differences between the copies keep the symmetry.

== Test C: which copies share slips

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, center),
    table.header([*Pair*], [*Shared slips*], [*Expected by chance*], [*p*], [*Holm*]),
    [W1–L], [8], [0.91], [0.0001], [0.0003],
    [W1–M], [7], [0.36], [0.0001], [0.0003],
    [L–M], [3], [0.95], [0.065], [0.065],
  ),
  caption: [Shared slips on the 172 squares matched in all three copies with a symmetry in at least two (`results/shared.json`); 10,000 permutations, so the smallest possible p is 0.0001. Slips counted: W1 71, L 561, M 283.],
)

The slips W1 still carries recur in L and in the French line through Mathers; L and Mathers share no more slips than chance allows.

== Other letter folding

Without i/j and u/v folding (pre-registered secondary), the conclusions are unchanged: L → M 9 of 12 against 16.0 % (Holm p $3.0 times 10^(-5)$); shared slips W1–L 8 against 0.91, W1–M 7 against 0.38, L–M 3 against 0.98. With I and T folded, a run added after the eye checks showed how alike L's I and T are and labelled post hoc, L → M becomes 12 of 15 against 14.3 % (Holm p $7.4 times 10^(-8)$), with the predicted letter 8 times against 1.71, and Test C is unchanged in direction (L–M 4 against 1.59, p 0.067).

= Discussion

*What the evidence weighs toward.* The squares were composed as symmetric word squares, and the symmetry survives copying well enough to be measured in every copy. Tested on copies that were not used to find them, symmetry breaks mark copying slips: a flagged cell is four to seven times as likely to differ in another copy as an ordinary cell, and the other copy often has the predicted letter. Kollatsch's editorial use of symmetry is therefore sound where it applies. But it applies to few slips: most changes between copies kept the symmetry, either because copyists changed letters in matching pairs or because the change goes back to an ancestor that was already consistent. Symmetry can correct a copy; it cannot by itself restore the original. The shared slips weigh toward L and the French line both descending from W1 or a close relative of it, which fits Kollatsch's ranking of W1 as the best copy.

*What is new*, as far as a search of the web, GitHub and KCWorks on 20 October 2026 found (Zenodo's search could not be reached):
+ a test of the symmetry method on held-out copies, with its precision and its low recall;
+ shared-slip evidence for how three copies are related;
+ a census of symmetry types copy by copy, with a stated rule and shuffled controls;
+ a new transcription of the squares of Leipzig Cod. mag. 15, published as data;
+ the half-turn-only squares of L, as an observation for later testing.

*Limits.*
+ W1 is Kollatsch's edited text, assembled from letter-group sequences, and its images were not seen. If some cells of his figures follow from symmetry by construction, W1's census overstates the scribe's own symmetry; this is why the clean evidence for Test B is L against M.
+ L was read by a language model and checked against the images by an AI assistant, not a palaeographer. The checks covered every cell that counted in Test B and five random pages. The corrections they produced made the result weaker, not stronger: before them, L → M had 14 of 17 flagged cells differing (`results/run_records.json`).
+ M is a 1999 typesetting of Mathers's printed translation, not the Arsenal manuscript, and many of its squares are partly empty; its slips may be Mathers's, his printer's or the typesetter's.
+ With three copies, Test C ranks pairs; it is not a family tree.
+ Deviations from the pre-registration: the I/T-folded run is post hoc; cells that became flagged only after the eye-check corrections were not checked one by one.

= Data availability

Code (MIT), our transcription of L, our parse of Mathers, the eye-check log and all results (CC BY 4.0) are at #link("https://github.com/BravoBravoIX/abramelin-word-squares")[github.com/BravoBravoIX/abramelin-word-squares], with the pre-registration. Kollatsch's W1 squares are not redistributed: a script fetches his deposit from KCWorks and the Mathers edition from archive.org and checks their SHA-256 sums, and the pipeline then rebuilds every results file byte for byte (about five minutes on CPU). The language-model reading of L is not rerun; its answers, prompt and costs are published as recorded data. No manuscript image is included.

= Acknowledgements

This study rests on the work of Rick-Arne Kollatsch, whose edition and openly published figures of the W1 squares are its reference text, and whose use of the squares' symmetry to emend W1 is the idea tested here. It also uses the digitisation of Cod. mag. 15 by the Universitätsbibliothek Leipzig and the archive.org copies of it and of Mathers. The analysis code was written with the help of an AI coding assistant (Claude, Anthropic), which also made the eye checks of the Leipzig transcription; the Claude API (Anthropic) was used as a reader of the Leipzig page images. The author checked the results and is responsible for any errors.

= References

#set par(hanging-indent: 1.2em, justify: false)
#set text(size: 9.5pt)


Bogdan, H. (2016). Review of G. Dehn, _The Book of Abramelin_. _Correspondences_ 4.

Dehn, G. (ed.) (2001). _Buch Abramelin_. Leipzig: Edition Araki. English: _The Book of Abramelin: A New Translation_, tr. S. Guth. Lake Worth, FL: Ibis Press, 2006; revised 2015.

Holm, S. (1979). A simple sequentially rejective multiple test procedure. _Scandinavian Journal of Statistics_ 6, 65–70.

Kollatsch, R.-A. (ed.) (2020). _Des Abraham von Worms Buch der wahren Praktik von der alten Magie. Ein als jüdisch fingierter Magietext des frühen 17. Jahrhunderts. Band 1 – Edition_. Hamburg: tredition; 2nd revised ed. 2021, ISBN 978-3-347-26288-1. Reading samples: #link("https://doi.org/10.17613/bsqa-s816")[doi:10.17613/bsqa-s816] (1st ed.), #link("https://doi.org/10.17613/8dq6-6m31")[doi:10.17613/8dq6-6m31] (2nd ed.).

Kollatsch, R.-A. (2021a). Figures of the 257 magical letter squares from »Abraham's of Worms Book of the True Practice of the Old Magic«. KCWorks (Humanities Commons), 9 February 2021. CC BY-NC-ND 4.0. #link("https://doi.org/10.17613/3hfq-9a74")[doi:10.17613/3hfq-9a74].

Kollatsch, R.-A. (2021b). Historische Handschriften von »Des Abraham von Worms Buch der wahren Praktik von der alten Magie«. KCWorks. #link("https://doi.org/10.17613/kfhy-m385")[doi:10.17613/kfhy-m385].

Kollatsch, R.-A. (2021c). Abraham of Worms, the disciple of »Abramelin the Mage«. KCWorks. #link("https://doi.org/10.17613/2mtz-ya12")[doi:10.17613/2mtz-ya12].

Leipzig, Universitätsbibliothek, Cod. mag. 15. Archive.org mirror of the library's digitisation: #link("https://archive.org/details/Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750_232")[archive.org/details/Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750\_232].

Mathers, S. L. MacGregor (tr.) (1898; 2nd ed. 1900). _The Book of the Sacred Magic of Abra-Melin the Mage_. London: Watkins. Digital edition: #link("https://archive.org/details/sacred-magic-abramelin")[archive.org/details/sacred-magic-abramelin].

Paris, Bibliothèque de l'Arsenal, MS 2351.

Peterson, J. H. (ed.). _The Book of the Sacred Magic of Abramelin the Mage_, digital edition with variants from Dehn. Esoteric Archives, updated 7 December 2025.

Wolfenbüttel, Herzog August Bibliothek, Cod. Guelf. 47.13 Aug. 4° (W1) and Cod. Guelf. 10.1 b Aug. 2° (W3).
