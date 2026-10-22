"""Measure every \\node of a TikZ figure and report overlaps with other labels
and with the drawn geometry (rendered with the labels made invisible)."""
import json
import re
import subprocess
import sys

import numpy as np
from PIL import Image

figure = sys.argv[1] if len(sys.argv) > 1 else '../figures/fig-combination.tex'
src = open(figure).read()
a = src.index(r'\begin{tikzpicture}')
b = src.index(r'\end{tikzpicture}') + len(r'\end{tikzpicture}')
body = src[a:b]

names = []


def name_it(m):
    names.append('n%d' % (len(names) + 1))
    return r'\node (%s)' % names[-1]


bodyA = re.sub(r'\\node(?=[\s\[])', name_it, body)
assert len(names) == body.count(r'\node'), (len(names), body.count(r'\node'))

tail = '\n'.join(
    r'\path (%s.north west); \pgfgetlastxy{\ax}{\ay}'
    r'\path (%s.south east); \pgfgetlastxy{\bx}{\by}'
    r'\typeout{NODE %s \ax\space\ay\space\bx\space\by}' % (n, n, n) for n in names)
tail += (r'\path (current bounding box.south west); \pgfgetlastxy{\px}{\py}'
         r'\typeout{PIC \px\space\py}')
bodyA = bodyA.replace(r'\end{tikzpicture}', tail + '\n' + r'\end{tikzpicture}')


bodyB = re.sub(r'\\node(?:\s*\[([^\]]*)\])?',
                lambda m: r'\node[opacity=0' + (',' + m.group(1) if m.group(1) else '') + ']',
                body)

pre = (r'\documentclass[border=2pt]{standalone}' '\n'
       r'\usepackage[T1]{fontenc}\usepackage{lmodern}' '\n'
       r'\usepackage{amsmath,amssymb}\usepackage{tikz}' '\n'
       r'\begin{document}' '\n')
for tag, text in [('A', bodyA), ('B', bodyB)]:
    open('v%s.tex' % tag, 'w').write(pre + text + '\n\\end{document}\n')
    subprocess.run(['pdflatex', '-interaction=nonstopmode', 'v%s.tex' % tag],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['pdftoppm', '-png', '-r', '600', 'v%s.pdf' % tag, 'v%s' % tag],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

boxes = {}
log = open('vA.log', errors='ignore').read()
for line in log.splitlines():
    m = re.match(r'NODE (n\d+) (-?[\d.]+)pt (-?[\d.]+)pt (-?[\d.]+)pt (-?[\d.]+)pt', line.strip())
    if m:
        n, x1, y1, x2, y2 = m.group(1), *map(float, m.groups()[1:])
        boxes[n] = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
assert len(boxes) == len(names), (len(boxes), len(names))
px, py = [float(v[:-2]) for v in re.search(r'^PIC (-?[\d.]+)pt (-?[\d.]+)pt', log, re.M).groups()]

DPI = 600.0
im = np.asarray(Image.open('vB-1.png').convert('L'), dtype=int)
H = im.shape[0]


def to_px(x, y):
    return ((x - px + 2.0) * DPI / 72.0, (H - (y - py + 2.0) * DPI / 72.0))


label = {n: (re.sub(r'\s+', ' ', src.split('{%s}' % n)[0][-40:]) if False else n) for n in names}
fails = 0
for thr in (220, 200):
    ink = im < thr
    bad = []
    for n in names:
        x1, y1, x2, y2 = boxes[n]
        c1, r1 = to_px(x1, y2)
        c2, r2 = to_px(x2, y1)
        frac = ink[int(r1) + 1:int(r2) - 1, int(c1) + 1:int(c2) - 1].mean()
        if frac > 0.002:
            bad.append((n, round(100 * frac, 1)))
    print('threshold %d: %s' % (thr, bad if bad else 'every label clear of the drawing'))
    fails += len(bad)
ov = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        A, B = boxes[names[i]], boxes[names[j]]
        ox = min(A[2], B[2]) - max(A[0], B[0])
        oy = min(A[3], B[3]) - max(A[1], B[1])
        if ox > 0 and oy > 0:
            ov.append((names[i], names[j], round(ox, 1), round(oy, 1)))
print('label-label overlaps:', ov if ov else 'none')
print('%d nodes measured' % len(names))
sys.exit(1 if (fails or ov) else 0)
