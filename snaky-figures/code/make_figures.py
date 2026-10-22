"""Regenerate every figure of snaky-figures.pdf into figures/ (PDF and PNG)."""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)

import fig0, fig1, fig2, fig3, fig4, fig5  # noqa: E402

out = os.path.join(here, os.pardir, 'figures')
os.makedirs(out, exist_ok=True)

for mod in (fig0, fig1, fig2, fig3, fig4, fig5):
    name = mod.__name__
    fn = getattr(mod, name)
    fn(os.path.join(out, name))
    print('wrote figures/%s.pdf and figures/%s.png' % (name, name))
