"""Regenerate every figure of snaky-figures.pdf into ./out (PDF and PNG)."""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
os.chdir(here)
os.makedirs('out', exist_ok=True)

import fig0, fig1, fig2, fig3, fig4, fig5  # noqa: E402

for mod in (fig0, fig1, fig2, fig3, fig4, fig5):
    name = mod.__name__
    fig = getattr(mod, name)()
    fig.clf()
    print('wrote out/%s.pdf' % name)
