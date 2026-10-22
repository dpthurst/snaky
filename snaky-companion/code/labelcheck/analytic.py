"""Check every free label of a drawn figure against the geometry around it.

Reads the node boxes that TikZ reported (vA.log, produced by check_labels.py)
and tests them against the grid, the envelopes, the dots and the marked cells.
The two pivot markers are drawn as boxes with their letter inside, so they are
treated as geometry, not as free labels.
"""
import re

U = 17.0706          # pt per drawing unit (6mm)
SEP = 0.19           # a node's inner separation, in units: the glyph sits this far inside
SHIFT = 11 / 0.6     # the right panel's xshift, in units

log = open('vA.log', errors='ignore').read()
order = []
boxes = {}
for line in log.splitlines():
    m = re.match(r'NODE (n\d+) (-?[\d.]+)pt (-?[\d.]+)pt (-?[\d.]+)pt (-?[\d.]+)pt', line.strip())
    if m:
        n, x1, y1, x2, y2 = m.group(1), *map(float, m.groups()[1:])
        order.append(n)
        boxes[n] = (min(x1, x2) / U, min(y1, y2) / U, max(x1, x2) / U, max(y1, y2) / U)

names = ['pivot left', 'T1', 'T2', 'T3', 'b', 'children', 'pivot right',
         'parent', 'formula', 'claim p']   # in source order
assert len(order) == len(names), (len(order), len(names))
box = dict(zip(names, (boxes[n] for n in order)))
markers = {'pivot left', 'pivot right'}
labels = [n for n in names if n not in markers]

segs, dots = [], []
for dx in (0.0, SHIFT):                                   # the grid
    for k in range(-5, 4):
        segs.append((k + .5, -3.5, k + .5, 2.5))
    for k in range(-4, 3):
        segs.append((-4.5, k + .5, 3.5, k + .5))
for (x1, y1, x2, y2) in [(-4.5, -1.5, .5, 2.5), (-1.5, -1.5, 3.5, 2.5), (-3.5, -3.5, 1.5, 1.5)]:
    segs += [(x1, y1, x2, y1), (x1, y2, x2, y2), (x1, y1, x1, y2), (x2, y1, x2, y2)]
segs += [(-.13, 1.87, .13, 2.13), (-.13, 2.13, .13, 1.87)]       # the Breaker cross
P = [(-4.5, 2.5), (-4.5, -1.5), (-3.5, -1.5), (-3.5, -3.5), (1.5, -3.5),
     (1.5, -1.5), (3.5, -1.5), (3.5, 2.5)]                       # the parent outline
for i in range(len(P)):
    a, b = P[i], P[(i + 1) % len(P)]
    segs.append((a[0] + SHIFT, a[1], b[0] + SHIFT, b[1]))
for dx, cells in [(0.0, [(-4, 0), (-4, 1), (-3, 1), (2, 0), (3, 0), (3, 1), (-3, -3), (-2, -3), (-1, -3)]),
                  (SHIFT, [(-4, 0), (-4, 1), (-3, 1), (2, 0), (3, 0), (3, 1), (-3, -3), (-2, -3), (-1, -3),
                           (-1, -1), (0, -1), (-1, 1), (0, 0), (0, 1)])]:
    dots += [(x + dx, y, 0.13) for x, y in cells]


def hits(s, box):
    x1, y1, x2, y2 = box
    ax, ay, bx, by = s
    for i in range(401):
        t = i / 400
        x, y = ax + (bx - ax) * t, ay + (by - ay) * t
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False


def boxes_meet(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


problems = []
for n in labels:
    x1, y1, x2, y2 = box[n]
    g = (x1 + SEP, y1 + SEP, x2 - SEP, y2 - SEP)
    for s in segs:
        if hits(s, g):
            problems.append('%s: line through the glyph' % n)
            break
    for (x, y, r) in dots:
        if g[0] - r < x < g[2] + r and g[1] - r < y < g[3] + r:
            problems.append('%s: dot too close' % n)
            break
    for m in markers:
        if boxes_meet(g, box[m]):
            problems.append('%s: runs into a pivot marker' % n)
for m in markers:                      # a marker must not cover a dot
    for (x, y, r) in dots:
        if box[m][0] < x < box[m][2] and box[m][1] < y < box[m][3]:
            problems.append('%s: covers a dot' % m)

print('label boxes (units):')
for n in labels:
    b = box[n]
    print('  %-9s x %6.2f..%6.2f   y %6.2f..%6.2f' % (n, b[0] + SEP, b[2] - SEP, b[1] + SEP, b[3] - SEP))
for m in markers:
    b = box[m]
    print('  %-9s x %6.2f..%6.2f   y %6.2f..%6.2f   (marker: its frame is the drawing)'
          % (m, b[0], b[2], b[1], b[3]))
print()
if problems:
    for p in problems:
        print('PROBLEM:', p)
else:
    print('no free label touches a line, a dot or a pivot marker')
