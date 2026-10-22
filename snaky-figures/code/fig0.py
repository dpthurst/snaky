from style import *
from draw import *
import snakylib as sl, check

cards, trees = sl.load()

def mini(rect, draw_fn, xlim, ylim, fig):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    draw_fn(ax)
    return ax

def fig0(path='out/fig0'):
    FW, FH = 7.1, 2.0
    fig = plt.figure(figsize=(FW, FH))
    bx = [0.012, 0.348, 0.684]; bw = 0.304; bh = 0.66; by = 0.285
    head = ['(1)  six one-hole copies',
            '(2)  combine at a pivot',
            '(3)  play the top card']
    note = ['each leaf: one claim finishes $S$',
            'each step: one move, $h\\to h+1$',
            'nothing required: $h=21$']
    for i, bxx in enumerate(bx):
        fig.patches.append(FancyBboxPatch((bxx, by), bw, bh,
                                          boxstyle='round,pad=0.004,rounding_size=0.012',
                                          transform=fig.transFigure, facecolor='#f6f9fc',
                                          edgecolor='#c3d0dd', lw=0.7, zorder=-2))
        fig.text(bxx + bw / 2, by + bh - 0.03, head[i], fontsize=7.8, va='top',
                 ha='center', zorder=5)
        fig.text(bxx + bw / 2, by + 0.045, note[i], fontsize=6.9, va='bottom',
                 ha='center', zorder=5, color='#33556e')
    for x in (bx[0] + bw, bx[1] + bw):
        fig.patches.append(FancyArrowPatch((x + 0.006, by + bh / 2), (x + 0.028, by + bh / 2),
                                           transform=fig.transFigure, arrowstyle='-|>',
                                           mutation_scale=8, lw=0.9, color='#6d7d8c'))
    slot = 0.24
    sh = 0.45
    yy = 0.375

    def d1(ax):
        A = {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)}
        for c in A:
            ax.add_patch(Rectangle((c[0] + 0.05, c[1] + 0.05), 0.9, 0.9, fc='#b9cfe6',
                                   ec='#17456e', lw=0.7))
        ax.add_patch(Rectangle((4.15, 1.15), 0.7, 0.7, fill=False, ec=COMPL, lw=1.4,
                               ls=(0, (2, 1.5))))
        ax.text(4.5, 2.5, 'win', fontsize=6.0, color=COMPL, ha='center', va='bottom')
    mini([bx[0] + bw / 2 - slot / 2, yy, slot, sh], d1, (-0.15, 5.6), (-0.15, 2.9), fig)

    def d2(ax):
        A6, T6, _ = cards[6]
        for c in T6:
            ax.add_patch(Rectangle((c[0], c[1]), 1, 1, fc=ENV_FC, ec='#c7d6e6', lw=0.4))
        for c in A6:
            ax.plot([c[0] + 0.5], [c[1] + 0.5], 'o', ms=3.0, mfc=MAKER, mec='white', mew=0.3)
        ax.add_patch(Rectangle((1.13, 4.13), 0.74, 0.74, fill=False, ec=PIVOT, lw=1.2))
        for c in [(1, 3), (1, 5)]:
            ax.add_patch(Rectangle((c[0] + 0.16, c[1] + 0.16), 0.68, 0.68, fill=False,
                                   ec=COMPL, lw=1.0, ls=(0, (1.8, 1.2))))
    mini([bx[1] + bw / 2 - slot / 2, yy, slot, sh], d2, (-0.3, 2.3), (-0.3, 6.0), fig)

    log, M, B = check.play('greedy', 0)

    def d3(ax):
        for c in cards[727][1]:
            ax.add_patch(Rectangle((c[0], c[1]), 1, 1, fc='#e6eef7', ec='none'))
        ax.add_patch(Rectangle((-0.5, -0.5), 17, 17, fill=False, ec='#c9c9c9', lw=0.4))
        outline(ax, log[-1]['win'], COMPL, lw=1.0, z=6)
        for e in log:
            c = e['claim']
            ax.plot([c[0] + 0.5], [c[1] + 0.5], 'o', ms=2.6, mfc=MAKER, mec='white',
                    mew=0.25, zorder=8)
    mini([bx[2] + bw / 2 - slot / 2, yy, slot, sh], d3, (-0.6, 16.6), (-0.6, 16.6), fig)

    fig.text(0.012, 0.235, 'The 728 cards are built offline, bottom-up, one instance of the middle step '
             'at a time.\nThe game is the descent back down that tree; one descent step is one real '
             'Maker claim.', fontsize=7.0, va='top', color='#333333')
    fig.text(0.012, 0.02, 'Figure 0.  The strategy in one line: build a finite tree of conditional '
             'positions, then walk down it.', fontsize=7.2, style='italic', va='bottom')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig0(); check_layout(f, 'fig0')
