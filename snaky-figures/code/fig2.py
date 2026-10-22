from style import *
from draw import *
import snakylib as sl

cards, trees = sl.load()

def place(ref, st):
    return sl.put(ref.s, ref.dx, ref.dy, st)

def fig2(path='out/fig2'):
    fig = plt.figure(figsize=(7.1, 3.0))

    # ---------------- (a) the combination rule -------------------------------
    ax = fig.add_axes([0.005, 0.06, 0.30, 0.80])
    cx = [(-0.9, 0.55), (0.9, 0.55), (0.0, -0.95)]
    for k, (x, y) in enumerate(cx):
        ax.add_patch(Circle((x, y), 1.5, facecolor='#d7e5f3', edgecolor=ENV_EC, lw=0.9,
                            zorder=1 + k, alpha=0.55))
    A = [(-1.55, 0.25), (1.55, 0.25), (0.0, -1.75)]
    for k, (x, y) in enumerate(A):
        ax.plot([x], [y], 'o', ms=6.5, mfc=MAKER, mec='white', mew=0.7, zorder=7)
    ax.text(-1.75, -0.30, '$A_1$', ha='center', fontsize=7.4, color=MAKER)
    ax.text(1.75, -0.30, '$A_2$', ha='center', fontsize=7.4, color=MAKER)
    ax.text(0.28, -1.95, '$A_3$', ha='left', fontsize=7.4, color=MAKER)
    ax.plot([0], [0], marker='s', ms=8, mfc='white', mec=PIVOT, mew=1.8, zorder=8)
    ax.annotate('claim $p$', xy=(0.02, 0.10), xytext=(-1.05, 1.35), fontsize=7.4,
                color=PIVOT, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-', lw=0.7, color=PIVOT, shrinkA=1, shrinkB=3))
    ax.plot([0.0], [1.35], marker='x', ms=7, mew=1.7, color=BREAKER, zorder=8)
    ax.annotate('one Breaker\nstone $b$', xy=(0.10, 1.32), xytext=(1.35, 1.75), fontsize=7.4,
                color=BREAKER, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-', lw=0.7, color=BREAKER, shrinkA=1, shrinkB=3))
    ax.annotate('$\\bigcap_i T_i$', xy=(-0.10, -0.35), xytext=(-2.05, -1.15), fontsize=7.4,
                color='#33556e', ha='center', va='center',
                arrowprops=dict(arrowstyle='-', lw=0.6, color='#33556e', shrinkA=1, shrinkB=2))
    ax.plot([0.55, 1.0], [3.0, 3.0], color='none')
    ax.text(0, -3.25, '$b$ misses some $T_i$: that child survives', ha='center',
            fontsize=7.2, color=BREAKER)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-3.6, 2.5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('(a) the combination rule', fontsize=9, loc='left', pad=2)

    # ---------------- (b) card 6: the fork ------------------------------------
    axb = fig.add_axes([0.315, 0.13, 0.29, 0.68])
    A6, T6, h6 = cards[6]
    board(axb, T6, shrink=0.04)
    required(axb, A6)
    ring(axb, (1, 4), PIVOT, 1.9)
    for c in [(1, 3), (1, 5)]:
        ring(axb, c, COMPL, 1.5, ls=(0, (2, 1.5)))
    axb.text(2.25, 5.5, '$(1,5)$ wins', fontsize=7.0, color=COMPL, ha='left', va='center')
    axb.text(2.25, 4.5, '$(1,4)$ claim', fontsize=7.0, color=PIVOT, ha='left', va='center')
    axb.text(2.25, 3.5, '$(1,3)$ wins', fontsize=7.0, color=COMPL, ha='left', va='center')
    axb.text(-0.35, 2.0, 'Maker owns\nthese five', fontsize=7.0, color=MAKER,
             ha='right', va='center')
    axb.set_xlim(-2.55, 4.75); axb.set_ylim(-0.75, 6.25)
    axb.set_aspect('equal'); axb.set_xticks([]); axb.set_yticks([])
    for sp in axb.spines.values(): sp.set_visible(False)
    axb.set_title('(b) card 6:  $h=2$', fontsize=9, loc='left', pad=2)

    # ---------------- (c) card 7: stacking two copies -------------------------
    axc = fig.add_axes([0.585, 0.11, 0.27, 0.72])
    A7, T7, h7 = cards[7]
    for k in trees[7].kids:
        outline(axc, place(k, cards[k.j][1]), '#a9b6c2', lw=0.8, ls=(0, (2.5, 2)), z=1)
    board(axc, T7, shrink=0.04)
    required(axc, A7)
    ring(axc, (0, 5), PIVOT, 1.9)
    axc.text(2.25, 5.5, '$(0,5)$ claim', fontsize=7.0, color=PIVOT, ha='left', va='center')
    axc.text(-0.35, 2.6, 'the two envelopes\nshare this column', fontsize=7.0, color=MAKER,
             ha='right', va='center')
    axc.set_xlim(-2.75, 5.6); axc.set_ylim(-0.75, 6.85)
    axc.set_aspect('equal'); axc.set_xticks([]); axc.set_yticks([])
    for sp in axc.spines.values(): sp.set_visible(False)
    axc.set_title('(c) card 7:  $h=3$', fontsize=9, loc='left', pad=2)

    fig.text(0.02, 0.985, 'Figure 2.  A card $(A,T,h)$ is a promise: if Maker owns $A$ and Breaker owns nothing in $T$, '
             'Maker wins within $h$ further moves.',
             fontsize=7.0, style='italic', va='top')
    fig.text(0.02, 0.93, 'Rule: claim the pivot $p$;  then every $A_i$ and the whole intersection $\\bigcap_i T_i$ '
             'belong to Maker, and one Breaker stone cannot enter every $T_i$.',
             fontsize=7.0, style='italic', va='top')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig2(); check_layout(f, 'fig2')
