from style import *

def cell(ax, x, y, fc, ec=None, lw=0.8, z=2, alpha=1.0, shrink=0.06):
    ax.add_patch(Rectangle((x + shrink, y + shrink), 1 - 2*shrink, 1 - 2*shrink,
                           facecolor=fc, edgecolor=ec or fc, linewidth=lw,
                           zorder=z, alpha=alpha, joinstyle='round'))

def board(ax, cells, fc=ENV_FC, ec=ENV_EC, lw=0.5, z=2, shrink=0.03):
    for x, y in cells:
        cell(ax, x, y, fc, ec, lw, z, shrink=shrink)

def frame(ax, xs, ys, pad=0.7, grid=True):
    ax.set_xlim(min(xs) - pad, max(xs) + 1 + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + 1 + pad)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

def required(ax, A, color=MAKER, z=4, s=0.30, marker='o'):
    for x, y in A:
        ax.plot([x + 0.5], [y + 0.5], marker=marker, ms=7.5, mfc=color, mec='white',
                mew=0.8, zorder=z)

def ring(ax, p, color, lw=1.8, z=5, size=0.80, label=None, ls='-'):
    x, y = p
    ax.add_patch(Rectangle((x + 0.5 - size/2, y + 0.5 - size/2), size, size,
                           fill=False, edgecolor=color, linewidth=lw, zorder=z, ls=ls,
                           joinstyle='round'))

def cross(ax, p, color=BREAKER, z=6, ms=8):
    x, y = p
    ax.plot([x + 0.5], [y + 0.5], marker='x', ms=ms, mew=1.6, color=color, zorder=z)

def outline(ax, cells, color, lw=1.2, z=6, ls='-', fc=None, alpha=1.0):
    """outline the union of unit cells given as a set"""
    from matplotlib.path import Path
    import matplotlib.patches as mp
    cells = set(cells)
    segs = []
    for (x, y) in cells:
        if (x, y + 1) not in cells: segs.append(((x, y + 1), (x + 1, y + 1)))
        if (x, y - 1) not in cells: segs.append(((x, y), (x + 1, y)))
        if (x - 1, y) not in cells: segs.append(((x, y), (x, y + 1)))
        if (x + 1, y) not in cells: segs.append(((x + 1, y), (x + 1, y + 1)))
    # chain segments into loops
    from collections import defaultdict
    adj = defaultdict(list)
    for a, b in segs:
        adj[a].append(b)
    used = set()
    for a, b in segs:
        if (a, b) in used: continue
        loop = [a, b]; used.add((a, b))
        cur = b
        while cur != a:
            nxt = None
            for c in adj[cur]:
                if (cur, c) not in used:
                    nxt = c; break
            if nxt is None: break
            used.add((cur, nxt)); loop.append(nxt); cur = nxt
        if len(loop) > 2:
            xs = [p[0] for p in loop]; ys = [p[1] for p in loop]
            ax.add_patch(Polygon(list(zip(xs, ys)), closed=True, fill=fc is not None,
                                 facecolor=fc if fc is not None else 'none',
                                 alpha=alpha if fc is not None else 1.0,
                                 edgecolor=color, lw=lw, zorder=z, ls=ls,
                                 joinstyle='round'))
