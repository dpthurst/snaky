from style import *
from draw import *
import snakylib as sl

cards, trees = sl.load()
E = trees[727]

def groups():
    out = []
    for k in E.kids:
        if out and out[-1][0] == k.j:
            out[-1][1].append(k)
        else:
            out.append((k.j, [k]))
    return out

G = groups()
placed = [[sl.put(k.s, k.dx, k.dy, cards[k.j][1]) for k in ks] for _, ks in G]
running, cur = [], None
for Ts in placed:
    cur = Ts[0].copy() if cur is None else cur
    for t in Ts:
        cur &= t
    running.append(set(cur))
assert [len(r) - 1 for r in running] == [35, 31, 21, 12, 4, 0]

def small_board(fig, rect, light, dark, title=None, sub=None, pivot=(8, 8),
                edge='#c9c9c9'):
    ax = fig.add_axes(rect)
    ax.set_xlim(-0.55, 16.55); ax.set_ylim(-0.55, 16.55)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.add_patch(Rectangle((-0.5, -0.5), 17, 17, fill=False, ec=edge, lw=0.5, zorder=1))
    for x, y in light:
        ax.add_patch(Rectangle((x, y), 1, 1, fc='#dbe7f3', ec='none', zorder=2))
    for x, y in dark:
        ax.add_patch(Rectangle((x + 0.04, y + 0.04), 0.92, 0.92, fc=MAKER, ec='none', zorder=3))
    if pivot is not None:
        ax.add_patch(Rectangle((pivot[0] + 0.10, pivot[1] + 0.10), 0.80, 0.80,
                               fill=False, ec=PIVOT, lw=1.4, zorder=5))
    if title:
        ax.set_title(title, fontsize=7.4, pad=3)
    if sub:
        ax.text(8, -1.3, sub, ha='center', va='top', fontsize=6.4, color=MUTED)
    return ax

def fig4(path='out/fig4'):
    FW, FH = 7.1, 2.55
    fig = plt.figure(figsize=(FW, FH))
    W = 0.105
    H = W * FW / FH
    x0, y0, gap = 0.022, 0.40, 0.0175
    for i, ((j, ks), Ts) in enumerate(zip(G, placed)):
        sub = ('%d cells still common' % (len(running[i]) - 1)) if i < 5 else 'only $(8,8)$ left'
        small_board(fig, [x0 + i * (W + gap), y0, W, H], Ts[0], running[i] - {(8, 8)},
                    'card %d' % j, sub)
    xr = x0 + 6 * (W + gap)
    fig.patches.append(FancyArrowPatch((xr - 0.004, y0 + H / 2), (xr + 0.032, y0 + H / 2),
                                       transform=fig.transFigure, arrowstyle='-|>',
                                       mutation_scale=7, lw=0.8, color='#666666'))
    Wf = 0.155
    Hf = Wf * FW / FH
    small_board(fig, [0.80, 0.34, Wf, Hf], cards[727][1], set(), 'card 727', None,
                edge='#8a8a8a')
    fig.text(0.80 + Wf / 2, 0.245, '$A=\\varnothing$', ha='center', fontsize=8)
    fig.text(0.02, 0.975, 'The 32 children of card 727, grouped by card number.  '
             'Light: one placed envelope $T$ of the group.  Dark: cells still common to '
             'every envelope listed so far.', fontsize=7.4, va='top')
    fig.text(0.02, 0.885, 'Maker claims the pivot $(8,8)$, which every child requires;  '
             'one Breaker stone meets at most one group, so some child stays untouched.',
             fontsize=7.4, va='top', color='#333333')
    fig.text(0.02, 0.115, 'card 727:  $|T_{727}|=251$ cells inside $\\{0,\\ldots,16\\}^2$,  '
             '$h_{727}=21$', fontsize=7.6)
    fig.text(0.02, 0.045, 'Figure 4.  How the last card closes: the 32 children share exactly one cell, '
             'and one of them always survives.', fontsize=7.0, style='italic', va='top')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig4(); check_layout(f, 'fig4')
