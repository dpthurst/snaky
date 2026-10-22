from style import *
import snakylib as sl

S = sl.SNAKE
FORM = ['(x,y)', '(y,x)', '(\u2212x,y)', '(y,\u2212x)',
        '(x,\u2212y)', '(\u2212y,x)', '(\u2212x,\u2212y)', '(\u2212y,\u2212x)']

def cell(ax, x, y, fc, ec=None, lw=0.8, z=2, alpha=1.0):
    ax.add_patch(Rectangle((x + 0.05, y + 0.05), 0.90, 0.90, facecolor=fc,
                           edgecolor=ec or fc, linewidth=lw, zorder=z, alpha=alpha,
                           joinstyle='round'))

def fig1(path='out/fig1'):
    fig = plt.figure(figsize=(7.0, 3.5))
    # ---------- (a) the target -------------------------------------------------
    ax = fig.add_axes([0.02, 0.14, 0.29, 0.62])
    for x, y in S:
        cell(ax, x, y, '#c9dcf0', '#17456e', 1.0, z=3)
    for i, (x, y) in enumerate(S):
        ax.text(x + 0.5, y + 0.47, '$s_{%d}$' % i, ha='center', va='center',
                fontsize=8.5, color='#0d2b45', zorder=5)
    ax.annotate('', xy=(5.5, 0), xytext=(-0.4, 0),
                arrowprops=dict(arrowstyle='-|>', lw=0.7, color='#333333'))
    ax.annotate('', xy=(0, 2.9), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle='-|>', lw=0.7, color='#333333'))
    ax.text(5.45, -0.22, '$x$', fontsize=9, ha='right', va='top')
    ax.text(-0.22, 2.85, '$y$', fontsize=9, ha='right', va='top')
    ax.text(2.4, -1.15, 'cells indexed by\ntheir lower-left corner',
            ha='center', va='center', fontsize=6.8, color=MUTED)
    ax.set_xlim(-0.55, 5.6); ax.set_ylim(-1.55, 3.1)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('(a) the target $S$', fontsize=9, loc='left', pad=2)

    # ---------- (b) the eight orientations ------------------------------------
    CW, CH = 6.6, 8.8
    ax2 = fig.add_axes([0.33, 0.02, 0.66, 0.92])
    ax2.set_xlim(-0.2, 4 * CW); ax2.set_ylim(-0.2, 2 * CH)
    ax2.set_aspect('equal'); ax2.set_anchor('C'); ax2.axis('off')
    for s in range(8):
        P = sl.put(s, 0, 0, set(S))
        mx, my = min(p[0] for p in P), min(p[1] for p in P)
        P = [(x - mx, y - my) for x, y in P]
        w = max(p[0] for p in P) + 1; h = max(p[1] for p in P) + 1
        ox = (s % 4) * CW; oy = (1 - s // 4) * CH
        bx, by = ox + (5 - w) / 2, oy + 1.3          # bottom-left of the shape
        for x, y in P:
            cell(ax2, bx + x, by + y, '#c9dcf0', '#17456e', 0.8, z=3)
        ax2.add_patch(FancyBboxPatch((bx - 0.45, by - 0.45), w + 0.9, h + 0.9,
                                     boxstyle='round,pad=0,rounding_size=0.35',
                                     fill=False, edgecolor='#c8c8c8', lw=0.5,
                                     ls=(0, (2, 2)), zorder=1))
        ax2.text(ox + 2.5, oy + 7.2, '$s=%d$' % s, ha='center', va='center', fontsize=8.2)
        ax2.text(ox + 2.5, oy + 0.25, '$R_%d\\,(x,y)=$ %s' % (s, FORM[s]),
                 ha='center', va='center', fontsize=7.4, color='#333333')
    ax2.set_title('(b) all eight orientations count:  every target is $t+R_s(S)$, $t\\in\\mathbb{Z}^2$',
                  fontsize=9, loc='left', pad=2)
    fig.text(0.5, 0.012, 'Figure 1.  The shape to be built, and the eight orientations that all count as a win.',
             fontsize=7.2, style='italic', ha='center')
    fig.savefig(path + '.pdf', bbox_inches='tight', pad_inches=0.02)
    fig.savefig(path + '.png', dpi=200, bbox_inches='tight', pad_inches=0.02)
    return fig

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    f = fig1(); check_layout(f, 'fig1')
