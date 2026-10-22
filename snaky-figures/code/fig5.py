from style import *
from draw import *
import check, trace

def fig5(path='out/fig5'):
    log, M, B = check.play('greedy', 0)
    n = len(log)
    fig = plt.figure(figsize=(7.1, 3.5))
    ax = fig.add_axes([0.015, 0.06, 0.44, 0.86])
    ax.set_xlim(-0.7, 16.7); ax.set_ylim(-0.7, 16.7)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.add_patch(Rectangle((-0.5, -0.5), 17, 17, fill=False, ec='#cccccc', lw=0.5))
    # heat map of the funnel: how long a cell stays in the active envelope
    T1 = log[0]['T']
    cmap = plt.get_cmap('Blues')
    for (x, y) in T1:
        last = max(i for i, e in enumerate(log) if (x, y) in e['T'])
        ax.add_patch(Rectangle((x, y), 1, 1, fc=cmap(0.10 + 0.78 * last / max(1, n - 1)),
                               ec='none', zorder=2))
    for i, e in enumerate(log):
        outline(ax, e['T'], '#33556e', lw=0.6, z=12 + i)
    # the path of claims
    pts = [e['claim'] for e in log]
    ax.plot([p[0] + 0.5 for p in pts], [p[1] + 0.5 for p in pts],
            color='#7a7a7a', lw=0.7, ls=(0, (1.5, 1.5)), zorder=20)
    win = log[-1]['win']
    outline(ax, win, COMPL, lw=2.0, z=25)
    # stones
    for (c, e) in zip([e['claim'] for e in log], log):
        ax.plot([c[0] + 0.5], [c[1] + 0.5], 'o', ms=11, mfc=MAKER, mec='white', mew=0.9, zorder=30)
        ax.text(c[0] + 0.5, c[1] + 0.47, str(e['step']), ha='center', va='center',
                color='white', fontsize=6.2, zorder=31)
    for e in log:
        if 'reply' in e:
            b = e['reply']
            ax.plot([b[0] + 0.5], [b[1] + 0.5], marker='x', ms=8, mew=1.9,
                    color=BREAKER, zorder=32)
    # ---- ladder -------------------------------------------------------------
    cols = [cmap(0.10 + 0.78 * i / max(1, n - 1)) for i in range(n)]
    ys = 0.90
    fig.text(0.50, 0.955, 'the descent actually played', fontsize=8.5, va='top')
    fig.text(0.50, 0.885, 'level   card     $h$    $|T|$     Maker claims     Breaker replies',
             fontsize=7.0, va='top', color='#444444', family='serif')
    for i, e in enumerate(log):
        y = 0.815 - i * 0.075
        fig.patches.append(plt.Line2D([0.50, 0.545], [y + 0.012, y + 0.012],
                                      transform=fig.transFigure, color=cols[i], lw=2.4))
        fig.text(0.555, y, '%d' % (i + 1), fontsize=7.0, va='center')
        fig.text(0.585, y, ('%d' % e['card']) if isinstance(e['card'], int) else 'inline',
                 fontsize=7.0, va='center')
        fig.text(0.645, y, '%d' % e['h'], fontsize=7.0, va='center')
        fig.text(0.690, y, '%d' % e['size'], fontsize=7.0, va='center')
        fig.text(0.750, y, str(e['claim']), fontsize=7.0, va='center')
        fig.text(0.855, y, str(e.get('reply', '\u2014')), fontsize=7.0, va='center')
    fig.text(0.50, 0.19, 'Maker owns 7 cells and completes $S$ on move 7;\nthe remaining bound was never needed.',
             fontsize=7.2, va='top', color='#333333')
    fig.text(0.02, 0.015, 'Figure 5.  One legal play under the certificate policy:  nested envelopes (light $\to$ dark, '
             '251 $\\to$ 6 cells) and Maker\u2019s claims.', fontsize=7.0, style='italic', va='bottom')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig5(); check_layout(f, 'fig5')
