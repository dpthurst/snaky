import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle, FancyArrowPatch
import numpy as np

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['STIXGeneral', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'font.size': 8,
    'axes.linewidth': 0.6,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'figure.dpi': 110,
})

ENV_FC   = '#e9f1f9'
ENV_EC   = '#8fb3d9'
MAKER    = '#17456e'
PIVOT    = '#d95f02'
COMPL    = '#2e7d4f'
BREAKER  = '#a5182a'
GRID     = '#dcdcdc'
MUTED    = '#6b6b6b'
ACCENT   = '#9e2f5a'

def check_layout(fig, name, verbose=True):
    """Report text artists outside the figure and overlapping text pairs."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.canvas.get_width_height()
    boxes = []
    for ax in fig.axes:
        for t in ax.texts + [ax.title, ax.xaxis.label, ax.yaxis.label]:
            if not t.get_text():
                continue
            bb = t.get_window_extent(renderer=r)
            boxes.append((t.get_text()[:28], bb))
        leg = ax.get_legend()
        if leg is not None:
            for t in leg.get_texts():
                boxes.append((t.get_text()[:28], t.get_window_extent(renderer=r)))
    for t in fig.texts:
        boxes.append((t.get_text()[:28], t.get_window_extent(renderer=r)))
    problems = []
    for txt, bb in boxes:
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > W + 1 or bb.y1 > H + 1:
            problems.append('OUT OF FIGURE: %r' % txt)
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 1.0 and oy > 1.0:
                problems.append('OVERLAP: %r / %r (%.1f x %.1f px)' % (boxes[i][0], boxes[j][0], ox, oy))
    if verbose:
        print('[%s] %d text boxes, %d problems' % (name, len(boxes), len(problems)))
        for p in problems[:25]:
            print('   ', p)
    return problems
