# Figures and a companion for *Snaky in 21 Maker moves*

Two pieces of work on OpenAI's preprint **Snaky in 21 Maker moves** (25 September 2026),
<https://github.com/openai/math/tree/main/preprints/Snaky-in-21-Maker-moves-September-25-2026>.

The paper proves that Maker can complete the Snaky hexomino within 21 Maker claims against
any Breaker play on the infinite empty board, by building a finite tree of conditional
positions and then descending it. Its own figures are local dot-and-grid diagrams for
individual tactics; neither folder here modifies the paper, recompiles it, or redistributes
a changed copy of it.

| folder | what it is |
| --- | --- |
| `snaky-companion/` | **current piece.** A six-page companion document that explains the argument and draws what the paper's text implies but does not contain: the combination rule, the certificate as a whole, the last card, one played game. Figures are TikZ in the paper's own drawing idiom. |
| `snaky-figures/` | earlier piece. A five-figure reading guide rendered with matplotlib, as PDF and PNG, with the short prose that goes with it. |

Each folder has its own README with the details, and `code/` with everything needed to
regenerate the figures.

## Building

```sh
cd snaky-companion
python3 code/make_figures.py      # regenerates the four data-driven figures as TikZ
latexmk -pdf snaky-companion.tex  # needs tikz, booktabs, float
```

```sh
cd snaky-figures
cd code && python3 make_figures.py   # writes code/out/fig*.{pdf,png}
cd .. && latexmk -pdf snaky-figures.tex
```

## Where the numbers come from

`certificate.txt`, present in both `code/` directories, is the file distributed with the
preprint (`verification/certificate.txt`, SHA-256 `3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04`,
the identity the paper states in §6.2). It is the paper authors' data, included unchanged so
that the figures can be regenerated and checked; everything else here was written for this
repository.

Both code sets re-derive all 728 cards from Definition 2 and the combination rule rather than
trusting the paper's own verifier: they reproduce `|T727| = 251`, `h727 = 21` and the
`35, 31, 21, 12, 4, 0` column of Table 1. The played game in the companion is a simulation of
the Section 4 policy with the invariant of Definition 2 asserted at every step, and
`snaky-companion/code/check_pivots.py` verifies the claim that every pivot of the certificate
lies in every child's required set — 1,620 combination nodes, no exceptions.

## Licence

The mathematical content of the preprint is the authors'. No licence is asserted here for it;
add one before publishing if you intend the repository to be reused.
