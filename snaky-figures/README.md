# Figures for *Snaky in 21 Maker moves*

Companion figures to OpenAI, *Snaky in 21 Maker moves* (25 September 2026),
<https://github.com/openai/math/tree/main/preprints/Snaky-in-21-Maker-moves-September-25-2026>.

`snaky-figures.pdf` is a four-page reading guide: six figures plus short prose that
follows the paper's own order — the target, the card, the combination rule, the
certificate, the top card, the play.

| file | what it shows |
| --- | --- |
| `figures/fig0.pdf` | the strategy in one line: one-hole copies → the pivot rule → the top card → a play |
| `figures/fig1.pdf` | the target and its eight orientations, in the paper's `s = 0…7` encoding |
| `figures/fig2.pdf` | (a) the combination rule; (b) card 6, the fork; (c) card 7, two copies stacked |
| `figures/fig3.pdf` | all 728 cards: envelope size, required-set size and count against height |
| `figures/fig4.pdf` | the 32 children of card 727 and the intersection shrinking to `(8,8)` |
| `figures/fig5.pdf` | one play: nested envelopes, seven claims, the copy completed on move 7 |

Each figure is a vector PDF (for print) and a 200 dpi PNG (for screens).

## Where the geometry comes from

None of the geometry is drawn by hand. `code/certificate.txt` is the paper's
`verification/certificate.txt`, byte-identical (SHA-256 `3fa12d36…9fe3d04`, the identity
stated in §6.2). `code/snakylib.py` re-parses it and recomputes all 728 cards from
Definition 2 and the combination rule, independently of the paper's verifier; the two
agree, including `|T727| = 251`, `h727 = 21` and Table 1.

Figures 2(b), 2(c), 4 and 5 are drawn from those recomputed sets. Figure 5 comes from
`code/check.py`, which plays the Section 4 policy: claim the pivot (or the first free cell
if it is already owned), let Breaker move, follow the first child whose placed envelope
avoids the reply. At every step it asserts the invariant of Definition 2 — Breaker owns
nothing in the active envelope, and Maker owns the whole required set — over 200 randomised
Breaker strategies and one greedy one. All of those plays ended in six to eight Maker
claims; the figure shows a representative one.

## Rebuilding

```sh
python3 code/make_figures.py      # writes figures/fig{0..5}.{pdf,png}
latexmk -pdf snaky-figures.tex
```

The rendered figures and the built guide are not tracked; this regenerates them.

Requires Python 3 with matplotlib and Pillow, and a LaTeX installation with `latexmk`.
The certificate file is needed only by the figure scripts, never by the PDF.

## What is not drawn

The paper's 25-move and 35-move constructions and the four-in-a-row proposition of
Section 5 are not illustrated; they reuse the rule of Figure 2 with different data.
The figures are a reading aid, not a substitute for Definitions 2, Lemma 3 and the
certificate.
