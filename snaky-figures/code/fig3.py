from style import *
import snakylib as sl
import numpy as np

cards, trees = sl.load()
H = np.array([h for _, _, h in cards])
NT = np.array([len(t) for _, t, _ in cards])
NA = np.array([len(a) for a, _, _ in cards])
rng = np.random.default_rng(7)

def panel(ax, key, colour, ylab, note=None):
    for h in range(1, 22):
        m = H == h
        if not m.any(): continue
        jit = rng.uniform(-0.28, 0.28, m.sum())
        ax.plot(h + jit, key[m], 'o', ms=2.0, mfc=colour, mec='none', alpha=0.45, zorder=2)
        ax.plot([h - 0.36, h + 0.36], [key[m].mean()] * 2, '-', color='#333333', lw=1.0, zorder=4)
    ax.set_xlim(0.3, 21.7)
    ax.set_xlabel('height $h$', fontsize=7.5)
    ax.set_ylabel(ylab, fontsize=7.5)
    ax.tick_params(labelsize=6.5, length=2, width=0.5)
    ax.grid(axis='y', color='#eeeeee', lw=0.5, zorder=0)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.set_xticks([1, 5, 10, 15, 20, 21])
    if note: ax.text(*note[0], note[1], fontsize=6.8, color=MUTED)

def fig3(path='out/fig3'):
    fig = plt.figure(figsize=(7.1, 2.45))
    ax1 = fig.add_axes([0.055, 0.20, 0.255, 0.63])
    ax2 = fig.add_axes([0.395, 0.20, 0.255, 0.63])
    ax3 = fig.add_axes([0.735, 0.20, 0.245, 0.63])
    panel(ax1, NT, '#2b6ea8', 'envelope size $|T|$')
    ax1.set_ylim(0, 262)
    ax1.annotate('card 727: 251 cells', xy=(21, 251), xytext=(11.5, 235), fontsize=6.8,
                 color=MAKER, arrowprops=dict(arrowstyle='-', lw=0.6, color=MAKER))
    ax1.annotate('six base cards', xy=(1, 6), xytext=(2.6, 30), fontsize=6.8,
                 color=MAKER, arrowprops=dict(arrowstyle='-', lw=0.6, color=MAKER))
    ax1.set_title('(a) envelopes grow as the bound grows', fontsize=8, loc='left', pad=3)

    panel(ax2, NA, '#a5562b', 'required set $|A|$')
    ax2.set_ylim(-0.6, 11)
    ax2.annotate('nothing required', xy=(21, 0), xytext=(12.5, 1.6), fontsize=6.8,
                 color='#a5562b', arrowprops=dict(arrowstyle='-', lw=0.6, color='#a5562b'))
    ax2.set_title('(b) requirements shrink', fontsize=8, loc='left', pad=3)

    cnt = [int((H == h).sum()) for h in range(1, 22)]
    ax3.bar(range(1, 22), cnt, color='#7f9db5', width=0.72, zorder=3)
    ax3.set_xlim(0.3, 21.7)
    ax3.set_ylim(0, 112)
    ax3.set_xlabel('height $h$', fontsize=7.5)
    ax3.set_ylabel('cards', fontsize=7.5)
    ax3.tick_params(labelsize=6.5, length=2, width=0.5)
    ax3.grid(axis='y', color='#eeeeee', lw=0.5, zorder=0)
    for s in ('top', 'right'): ax3.spines[s].set_visible(False)
    ax3.set_xticks([1, 5, 10, 15, 20, 21])
    ax3.set_title('(c) 728 cards in all', fontsize=8, loc='left', pad=3)

    fig.text(0.02, 0.955, 'The certificate is one finite object: 6 base cards, 722 numbered lines, '
             '1,620 combination nodes.  Each point is a card $(A,T,h)$;  the bar over a column is its mean.',
             fontsize=7.3, va='top')
    fig.text(0.02, 0.015, 'Figure 3.  Reading the whole construction at once.', fontsize=7.0,
             style='italic')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig3(); check_layout(f, 'fig3')
