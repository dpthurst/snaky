"""Emit TikZ figures in the paper's own idiom from the certificate data."""
import snakylib as sl, check, trace

cards, trees = sl.load()

def segments(cells):
    """axis-parallel boundary segments of a set of cells centred at integer points"""
    cells = set(cells)
    segs = []
    for (x, y) in sorted(cells):
        if (x, y + 1) not in cells: segs.append(((x - .5, y + .5), (x + .5, y + .5)))
        if (x, y - 1) not in cells: segs.append(((x - .5, y - .5), (x + .5, y - .5)))
        if (x - 1, y) not in cells: segs.append(((x - .5, y - .5), (x - .5, y + .5)))
        if (x + 1, y) not in cells: segs.append(((x + .5, y - .5), (x + .5, y + .5)))
    total = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in segs)
    return segs, total

def fmt(v):
    s = ('%g' % v)
    return s

def path(loop):
    parts = ['(%s,%s)' % (fmt(round(x, 1)), fmt(round(y, 1))) for x, y in loop[:-1]]
    return '--'.join(parts) + '--cycle'

def cells_foreach(cells, style, cmd='\\fill'):
    cells = sorted(cells, key=lambda c: (c[1], c[0]))
    toks = ','.join('%d/%d' % (x, y) for x, y in cells)
    return '%s[%s] \\foreach \\x/\\y in {%s}{\\fill (\\x,\\y) circle (2pt);}' % (cmd, style, toks)

# --------------------------------------------------------------- the play
STYLES = ['gray!30', 'gray!42', 'gray!54', 'gray!66', 'gray!78', 'gray!90', 'black']

def fig_play(path_out='fig-play.tex'):
    log, M, B = check.play('greedy', 0)
    assert len(log) == 7
    L = []
    L.append(r"""% ---------------------------------------------------------------------------
%  Suggestion: place in Section 4, where the descent is described
%  ("Proof of Theorem 1"), with \ref{fig:descent} in the text.
%  Generated from the certificate by gen_tikz.py; edit that, not this.
% ---------------------------------------------------------------------------
\begin{figure}[H]
\centering
\begin{tikzpicture}[x=4.5mm,y=4.5mm,font=\small]
\draw[gray!30,step=1] (-.5,-.5) grid (16.5,16.5);""")
    for i, e in enumerate(log):
        segs, _ = segments(e['T'])
        L.append('\\draw[%s] %s;' % (STYLES[i],
                 ' '.join('(%s,%s)--(%s,%s)' % (fmt(round(a[0], 1)), fmt(round(a[1], 1)),
                                                fmt(round(b[0], 1)), fmt(round(b[1], 1)))
                          for a, b in segs)))
    L.append('\\draw[very thick] (7.5,8.5)--(8.5,8.5)--(8.5,11.5)--(9.5,11.5)--(9.5,12.5)'
             '--(10.5,12.5)--(10.5,13.5)--(8.5,13.5)--(8.5,12.5)--(7.5,12.5)--cycle;')
    for e in log:
        c = e['claim']
        L.append('\\node[circle,fill=black,text=white,inner sep=0pt,minimum size=3.2mm,'
                 'font=\\scriptsize,draw=white,line width=.4pt] at (%d,%d) {%d};'
                 % (c[0], c[1], e['step']))
    for e in log:
        if 'reply' in e:
            x, y = e['reply']
            L.append('\\draw[thick] (%d.14,%d.14)--(%d.86,%d.86) (%d.14,%d.86)--(%d.86,%d.14);'
                     % (x, y, x, y, x, y, x, y))
    # legend to the right (picture coordinates, so it scales with x/y)
    L.append(r"""\node[anchor=south west,font=\footnotesize] at (18.0,16.6) {the active envelope};
\node[anchor=south west,font=\footnotesize] at (18.0,15.3) {after each claim,};""")
    y0 = 14.0
    pitch = 1.15      # legend rows: 4.5mm unit, 8pt text
    for i, e in enumerate(log):
        y = y0 - i * pitch
        L.append('\\draw[%s,line width=.7pt] (18.0,%s)--(19.4,%s);'
                 '\\node[right,font=\\footnotesize] at (19.6,%s) {$h=%d$, %d cells};'
                 % (STYLES[i], fmt(y), fmt(y), fmt(y), e['h'], e['size']))
    L.append(r"""\node[anchor=north west,font=\footnotesize,align=left] at (18.0,5.6)
 {$\bullet$\ Maker's claim, in order\\[3pt]$\times$\ Breaker's reply\\[3pt]
  heavy: the copy of $S$\\[3pt] completed on claim $7$};""")
    L.append('\\end{tikzpicture}')
    L.append(r"""\caption{One play of the policy of Section~\ref{sec:strategy}, against a Breaker
that always blocks as many child envelopes as possible. The numbered dots are Maker's
claims, each the pivot of the card then active; the crosses are Breaker's replies.
The outlines, progressively darker, are the active envelope after each claim ---
$251,169,40,25,11,8$ and $6$ cells, with heights $21,20,10,9,3,2$ and $1$. Each reply
misses one of them and play descends into it. The heaviest outline is the copy of $S$ completed on claim $7$; the
remaining bound was never needed. No cell outside these regions influences the play.}""")
    L.append('\\label{fig:descent}\n\\end{figure}')
    open(path_out, 'w').write('\n'.join(L) + '\n')
    print('wrote', path_out)

if __name__ == '__main__':
    fig_play()

# ------------------------------------------------------------ the top card
def fig_topcard(path_out='fig-top-card.tex'):
    E = trees[727]
    groups = []
    for k in E.kids:
        if groups and groups[-1][0] == k.j:
            groups[-1][1].append(k)
        else:
            groups.append((k.j, [k]))
    placed = [[sl.put(k.s, k.dx, k.dy, cards[k.j][1]) for k in ks] for _, ks in groups]
    running, cur = [], None
    for Ts in placed:
        cur = Ts[0].copy() if cur is None else cur
        for t in Ts:
            cur &= t
        running.append(set(cur))
    remaining = [len(r) - 1 for r in running]
    assert remaining == [35, 31, 21, 12, 4, 0]

    def dotfill(cells):
        cells = sorted(cells, key=lambda c: (c[1], c[0]))
        if not cells:
            return '% no cell other than $(8,8)$ is still common'
        toks = ','.join('%d/%d' % (x, y) for x, y in cells)
        return ('\\fill \\foreach \\x/\\y in {%s}'
                '{(\\x,\\y) circle (.58mm)};' % toks)

    def cellfill(cells, style):
        cells = sorted(cells, key=lambda c: (c[1], c[0]))
        toks = ','.join('%d/%d' % (x, y) for x, y in cells)
        return ('\\fill[%s] \\foreach \\x/\\y in {%s}'
                '{(\\x-.5,\\y-.5) rectangle (\\x+.5,\\y+.5)};' % (style, toks))

    L = [r"""% ---------------------------------------------------------------------------
%  Suggestion: place in Section 3, beside Table 1 (the six groups of children
%  of card 727), with \ref{fig:topcard} in the paragraph before it.
%  Generated from the certificate by gen_tikz.py; edit that, not this.
% ---------------------------------------------------------------------------
\begin{figure}[H]
\centering
\begin{tikzpicture}[x=1.9mm,y=1.9mm,font=\small]"""]
    for i, (j, ks) in enumerate(groups):
        ox = (i % 3) * 21.5
        oy = -(i // 3) * 22.0
        L.append('\\begin{scope}[xshift=%.1fcm,yshift=%.1fcm]' % (ox * 0.19, oy * 0.19))
        L.append('\\draw[gray!35,step=1] (-.5,-.5) grid (16.5,16.5);')
        L.append(cellfill(placed[i][0], 'gray!22'))
        L.append(dotfill(running[i] - {(8, 8)}))
        L.append('\\filldraw[fill=gray!60] (7.72,7.72) rectangle (8.28,8.28);')
        note = ('$%d$ cells still common' % remaining[i]) if i < 5 else 'only $(8,8)$ remains'
        L.append('\\node[below,font=\\footnotesize,align=center] at (8,-.9) '
                 '{card %d \\ (%d placements)\\\\[-1pt] %s};' % (j, len(ks), note))
        L.append('\\end{scope}')
    L.append(r"""\end{tikzpicture}
\caption{The $32$ children of card $727$, grouped by the card they come from;
the card number and the number of its placements are printed below each panel.
Light cells are one placed envelope of the group. The black dots are the cells
still common to every envelope listed up to and including that group, apart from
the pivot $(8,8)$ itself, which is drawn as a grey square throughout: $35,31,21,
12,4$ and finally $0$ of them. So the intersection of all $32$ envelopes is
exactly $\{(8,8)\}$, and Maker's claim there leaves nothing to require ---
$A_{727}=\varnothing$.}""")
    L.append('\\label{fig:topcard}\n\\end{figure}')
    open(path_out, 'w').write('\n'.join(L) + '\n')
    print('wrote', path_out)


# ------------------------------------------------------------ the landscape
def fig_landscape(path_out='fig-landscape.tex'):
    hs = list(range(1, 22))
    cnt = [sum(1 for a, t, h in cards if h == k) for k in hs]
    mx = [max([len(t) for a, t, h in cards if h == k] or [1]) for k in hs]
    CA, CB = 0.75, 0.28          # vertical scale, in the common unit (y=1pt)
    L = [r"""% ---------------------------------------------------------------------------
%  Suggestion: place in Section 3, just before Proposition 5, with
%  \ref{fig:landscape} in the text.
%  Generated from the certificate by gen_tikz.py; edit that, not this.
% ---------------------------------------------------------------------------
\begin{figure}[H]
\centering
\begin{tikzpicture}[x=2.05mm,y=1pt,font=\small]"""]
    # ---- (a) cards per height
    L.append('\\begin{scope}')
    for k, c in zip(hs, cnt):
        L.append('\\fill[gray!45] (%.2f,0) rectangle (%.2f,%.2f);' % (k - .33, k + .33, c * CA))
    L.append('\\draw (-.1,0)--(22,0);')
    L.append('\\draw (0,-.5)--(0,%.2f);' % (106 * CA))
    for val in (0, 50, 100):
        L.append('\\draw (-.2,%.2f)--(.2,%.2f) node[left,font=\\scriptsize] {%d};'
                 % (val * CA, val * CA, val))
    for k in (1, 5, 10, 15, 20, 21):
        L.append('\\draw (%.1f,-.8)--(%.1f,-2.2) node[below,font=\\scriptsize] {%d};' % (k, k, k))
    L.append('\\node[below,font=\\footnotesize] at (11,-11) {height $h$};')
    L.append('\\node[font=\\footnotesize] at (11,%.2f) {cards};' % (106 * CA + 8))
    L.append('\\end{scope}')
    # ---- (b) largest envelope per height
    L.append('\\begin{scope}[xshift=6.1cm]')
    pts = '--'.join('(%.1f,%.2f)' % (k, v * CB) for k, v in zip(hs, mx))
    L.append('\\draw[thick] %s;' % pts)
    for k, v in zip(hs, mx):
        L.append('\\fill (%.1f,%.2f) circle (1.2pt);' % (k, v * CB))
    L.append('\\draw (-.1,0)--(22,0);')
    L.append('\\draw (0,-.5)--(0,%.2f);' % (265 * CB))
    for val in (0, 100, 200):
        L.append('\\draw (-.2,%.2f)--(.2,%.2f) node[left,font=\\scriptsize] {%d};'
                 % (val * CB, val * CB, val))
    for k in (1, 5, 10, 15, 20, 21):
        L.append('\\draw (%.1f,-.8)--(%.1f,-2.2) node[below,font=\\scriptsize] {%d};' % (k, k, k))
    L.append('\\node[below,font=\\footnotesize] at (11,-11) {height $h$};')
    L.append('\\node[font=\\footnotesize] at (11,%.2f) {cells};' % (265 * CB + 8))
    L.append('\\node[font=\\scriptsize,below right] at (1.1,%.2f) {$6$};' % (6 * CB))
    L.append('\\node[font=\\scriptsize,above] at (21,%.2f) {$251$};' % (251 * CB + 3))
    L.append('\\end{scope}')
    L.append(r"""\end{tikzpicture}
\caption{The certificate as a whole. Left, the number of cards at each height: a
pyramid from the six one-hole copies to the single card $727$. Right, the largest
envelope at each height. The two trends are the reason the construction works:
the higher a card reaches, the more cells it must keep free of Breaker
($251$ at the top), while the required sets move the other way and end empty.}""")
    L.append('\\label{fig:landscape}\n\\end{figure}')
    open(path_out, 'w').write('\n'.join(L) + '\n')
    print('wrote', path_out)


# ---------------------------------------------------------------- the target
FORM = ['(x,y)', '(y,x)', '(-x,y)', '(y,-x)', '(x,-y)', '(-y,x)', '(-x,-y)', '(-y,-x)']


def fig_target(path_out='fig-target.tex'):
    """The target in its eight allowed orientations."""
    S = sl.SNAKE
    L = [r"""% ---------------------------------------------------------------------------
%  Generated by gen_tikz.py; edit that, not this.
% ---------------------------------------------------------------------------
\begin{figure}[H]
\centering
\begin{tikzpicture}[x=4.2mm,y=4.2mm,font=\small]"""]
    for s in range(8):
        P = sorted(sl.put(s, 0, 0, set(S)))
        mx = min(x for x, y in P)
        my = min(y for x, y in P)
        P = [(x - mx, y - my) for x, y in P]
        w = max(x for x, y in P) + 1
        h = max(y for x, y in P) + 1
        ox = (s % 4) * 6.6
        oy = -(s // 4) * 7.4
        L.append('\\begin{scope}[xshift=%.1fcm,yshift=%.1fcm]' % (ox * 0.42, oy * 0.42))
        L.append('\\draw[gray!30] (0,0) rectangle (5.6,5.6);')
        dx, dy = (5.6 - w) / 2, (5.6 - h) / 2
        for (x, y) in P:
            L.append('\\filldraw[fill=gray!18] (%.2f,%.2f) rectangle +(1,1);'
                     % (x + dx, y + dy))
        L.append('\\node[below,font=\\footnotesize] at (2.8,-.15) {$s=%d$};' % s)
        L.append('\\end{scope}')
    L.append(r"""\end{tikzpicture}
\caption{The target in its eight allowed orientations, in the codes
$s=0,\dots,7$ that the certificate data use: $s=0$ is $(x,y)$, then $s=1,2,3,4,5,
6,7$ apply $(y,x)$, $(-x,y)$, $(y,-x)$, $(x,-y)$, $(-y,x)$, $(-x,-y)$, $(-y,-x)$.
Every translate of any one of them is a win, so a Maker policy may choose its
orientation in advance and change it later.}""")
    L.append('\\label{fig:target}\n\\end{figure}')
    open(path_out, 'w').write('\n'.join(L) + '\n')
    print('wrote', path_out)
