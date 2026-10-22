"""Check the pivot property claimed in the Pivot definition: in every combination
node of the 21-move certificate, the pivot belongs to every child's envelope and
to every child's required set.

Reads certificate.txt (the file distributed with the paper, SHA-256
3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04) and applies
the combination rule of Lemma 3 exactly as the paper states it.

    python3 check_pivots.py [certificate.txt]
"""
import hashlib
import sys

SYMBOLS = '0123456789ABCDEFG'
SNAKE = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
EXPECTED = '3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04'


def point(word):
    return tuple(SYMBOLS.index(c) for c in word)


def place(s, dx, dy, P):
    out = set()
    for x, y in P:
        if s & 2:
            x = -x
        if s & 4:
            y = -y
        if s & 1:
            x, y = y, x
        out.add((x + dx, y + dy))
    return out


class Ref:
    __slots__ = ('j', 's', 'dx', 'dy')

    def __init__(self, token):
        parts = token.split(':')
        self.j = int(parts[0])
        if len(parts) == 1:
            self.s = self.dx = self.dy = 0
        else:
            self.s = int(parts[1][0])
            self.dx, self.dy = point(parts[1][1:])


class Expr:
    __slots__ = ('p', 'kids')

    def __init__(self, p, kids):
        self.p = p
        self.kids = kids


def parse_line(line):
    words = line.replace('(', ' ( ').replace(')', ' ) ').split()
    it = iter(words + [')'])
    number = int(next(it))

    def expr():
        p = point(next(it))
        kids = []
        while True:
            w = next(it)
            if w == ')':
                return Expr(p, kids)
            kids.append(expr() if w == '(' else Ref(w))

    return number, expr()


def combine(node, cards):
    aa, tt, hh = [], [], []
    for k in node.kids:
        if isinstance(k, Ref):
            a = place(k.s, k.dx, k.dy, cards[k.j][0])
            t = place(k.s, k.dx, k.dy, cards[k.j][1])
            h = cards[k.j][2]
        else:
            a, t, h = combine(k, cards)
        aa.append(a)
        tt.append(t)
        hh.append(h)
    A = (set().union(*aa) | set.intersection(*tt)) - {node.p}
    T = set().union({node.p}, *tt)
    return A, T, 1 + max(hh)


def main(path=None):
    if path is None:
        import os
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificate.txt')
    payload = open(path, 'rb').read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED:
        print('warning: unexpected SHA-256', digest)

    cards = [(set(SNAKE) - {p}, set(SNAKE), 1) for p in SNAKE]
    roots = {}
    for line in payload.decode('ascii').strip().splitlines():
        if not line.strip():
            continue
        number, root = parse_line(line)
        assert number == len(cards), (number, len(cards))
        cards.append(combine(root, cards))
        roots[number] = root

    nodes = envelope_bad = required_bad = 0
    for j, root in sorted(roots.items()):
        stack = [root]
        while stack:
            node = stack.pop()
            nodes += 1
            envelopes, required = [], []
            for k in node.kids:
                if isinstance(k, Ref):
                    envelopes.append(place(k.s, k.dx, k.dy, cards[k.j][1]))
                    required.append(place(k.s, k.dx, k.dy, cards[k.j][0]))
                else:
                    a, t, _ = combine(k, cards)
                    envelopes.append(t)
                    required.append(a)
            if node.p not in set.intersection(*envelopes):
                envelope_bad += 1
                print('  pivot outside the common envelope: line', j, 'pivot', node.p)
            if node.p not in set.intersection(*required):
                required_bad += 1
                print('  pivot outside a child requirement: line', j, 'pivot', node.p)
            stack.extend(k for k in node.kids if isinstance(k, Expr))

    assert len(cards) == 728
    print('combination nodes: %d' % nodes)
    print('pivot outside every child envelope: %d' % envelope_bad)
    print('pivot outside some child required set: %d' % required_bad)
    assert nodes == 1620 and envelope_bad == 0 and required_bad == 0
    print('PASS')


if __name__ == '__main__':
    main(*sys.argv[1:])
