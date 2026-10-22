# A companion to *Snaky in 21 Maker moves*

`snaky-companion.pdf` (6 pages) explains the preprint of 25 September 2026 and draws the
pictures its text implies but does not contain. It **does not modify the paper**: no source
file of the paper is patched, recompiled or redistributed here, and every numbered reference in
the companion (Definition 2, Lemma 3, Proposition 5, Section 4) points at the paper as
published.

## What is in it

| section | contents | figure |
| --- | --- | --- |
| introduction | what the companion is, and a map of the paper | — |
| 1 | the game, the target, the eight orientations, the quantifier order | Figure 1 |
| 2 | cards: Definition 2 read as a promise, and why a card is portable | — |
| 3 | Lemma 3, the one-stone argument, and what a *pivot* is | Figure 2 |
| 4 | the certificate: 728 cards, the two trends, Table 1 drawn | Figures 3, 4 |
| 5 | the policy of Section 4 and one played game | Figure 5 |
| 6 | what the companion leaves out (25/35-move routes, four-in-a-row) | — |
| 7 | how the figures and the computational remarks were checked | — |

The pivot material in §3 is the one place the companion adds something the paper does not say
outright: the paper names $p$ the pivot from §3 on but only ever says "let $p\in\mathbb Z^2$".
§3 gives the definition the later usage requires — marked in the text as a reconstruction, not
as a quotation — and then the property that makes it worth having: over all 1,620 combination
nodes of the certificate, the pivot lies in every child's *required* set, not merely in every
envelope. `code/check_pivots.py` verifies that (`PASS`, 0 exceptions).

`code/check_symmetry.py` answers the question a simplification will ask: how many
distinct cases does a certificate really contain? On the printed certificate the answer is
728 of 728 --- no two cards are congruent, because symmetry is already spent as placement
(each card is proved once and referenced in up to eight orientations, 4,089 references in
all). Run it on a new certificate and it lists any classes holding more than one card;
those are the merge candidates.

## Files

```
snaky-companion.tex     the document
snaky-companion.pdf     the built document
figures/fig-*.tex       the five TikZ figures, each a complete float environment
code/gen_tikz.py        regenerates four of the figures from the certificate
code/make_figures.py    runs that, writing figures/fig-*.tex
code/check_pivots.py    the 1,620-node pivot check
code/check_symmetry.py  cards modulo the eight symmetries: how many distinct cases a certificate has
code/{snakylib,check,trace,sim}.py   certificate parser and the played game
code/certificate.txt    the file distributed with the paper (byte-identical)
preview-pages/          the six pages as grayscale PNGs
```

## Rebuilding

```sh
python3 code/make_figures.py     # rewrites figures/fig-{target,landscape,top-card,play}.tex
latexmk -pdf snaky-companion.tex # needs tikz, booktabs and float (all in TeX Live)
```

`figures/fig-combination.tex` is hand-written — it is a schematic, not data — so `make_figures.py`
leaves it alone. The other four are generated from `code/certificate.txt`, which is the paper's
own `verification/certificate.txt` (SHA-256 `3fa12d36…9e3d04`, the identity stated in §6.2).

The figures use the paper's drawing conventions — cells at integer centres, `gray!35` grid,
filled dots for Maker cells, small squares for pivots, `.13` crosses for Breaker — so they read
as part of the same family as the paper's own Figures 1–4 without touching them.

## What was checked

- The certificate matched the SHA-256 stated in §6.2 and was re-parsed independently: all 728
  cards recomputed from Definition 2 and the combination rule, reproducing $|T_{727}|=251$,
  $h_{727}=21$ and the $35,31,21,12,4,0$ column of Table 1.
- Figure 5 is a simulation of the Section 4 policy with the invariant of Definition 2 asserted
  at every step — Breaker owns nothing in the active envelope, Maker owns the whole required
  set — over 200 randomised Breaker strategies and one greedy one. Every play ended in six to
  eight claims; the figure shows a representative one, not the worst case.
- The pivot claim above, over all 1,620 combination nodes.
