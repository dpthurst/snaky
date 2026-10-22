"""Regenerate the figures of the companion as TikZ, from the certificate data.

fig-combination.tex is hand-written; the other four are generated here.
Run from anywhere:  python3 code/make_figures.py
"""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
os.chdir(os.path.dirname(here))

import gen_tikz  # noqa: E402

for name, fn in [('fig-target', gen_tikz.fig_target),
                 ('fig-landscape', gen_tikz.fig_landscape),
                 ('fig-top-card', gen_tikz.fig_topcard),
                 ('fig-play', gen_tikz.fig_play)]:
    fn('figures/%s.tex' % name)
