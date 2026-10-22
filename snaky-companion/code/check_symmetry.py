"""Count the distinct cases of a certificate, once symmetry is quotiented out.

Reads a certificate in the dialect of the 21-move construction -- numbered lines,
``j:sUV`` references, parenthesised combinations -- and groups its cards by
congruence under the eight signed permutations followed by a translation.

In the printed certificate symmetry is already spent as *placement*: a card is
proved once and referenced in up to eight orientations, which is how 722 lines
carry 4,089 references.  So the useful question is the other way round, and it is
the one that matters when simplifying: does a certificate contain two lines that
are the same case in different clothes?  Run this on a new certificate and look at
the classes with more than one member -- those are merge candidates, and the
count of orbits is the number of cases the certificate really has.

    python3 check_symmetry.py [certificate.txt]

Exit status is 0 whether or not duplicates are found; duplicates are a finding,
not an error.
"""
import sys
from collections import Counter, defaultdict

import snakylib as sl

# the eight signed permutations, as maps on cells
G = [lambda x, y: (x, y), lambda x, y: (y, x), lambda x, y: (-x, y), lambda x, y: (y, -x),
     lambda x, y: (x, -y), lambda x, y: (-y, x), lambda x, y: (-x, -y), lambda x, y: (-y, -x)]


def canon(P):
    """Least image of a pair of finite sets under the eight maps, then a translation.

    The translation normalises on the union, so it is well defined for any pair
    with at least one non-empty component.
    """
    A, T = P
    base = T or A
    if not base:
        return ()
    best = None
    for f in G:
        FA = {(f(*p)) for p in A}
        FT = {(f(*p)) for p in T}
        mx = min(p[0] for p in (FT or FA))
        my = min(p[1] for p in (FT or FA))
        key = (tuple(sorted((x - mx, y - my) for x, y in FT)),
               tuple(sorted((x - mx, y - my) for x, y in FA)))
        if best is None or key < best:
            best = key
    return best


def references(trees):
    """Every reference in every line, as (line, placement code)."""
    out = []
    for j, root in sorted(trees.items()):
        todo = [root]
        while todo:
            node = todo.pop()
            for k in node.kids:
                if isinstance(k, sl.Ref):
                    out.append((j, k.s))
                else:
                    todo.append(k)
    return out


def reachable(trees, top):
    """Line numbers that the final card actually depends on."""
    seen = set()
    stack = [top]
    while stack:
        j = stack.pop()
        if j in seen:
            continue
        seen.add(j)
        root = trees.get(j)
        if root is None:
            continue
        todo = [root]
        while todo:
            node = todo.pop()
            for k in node.kids:
                if isinstance(k, sl.Ref):
                    stack.append(k.j)
                else:
                    todo.append(k)
    return seen


def main(path=None):
    cards, trees = sl.load(path)
    keys = [canon((A, T)) for A, T, h in cards]
    classes = defaultdict(list)
    for j, k in enumerate(keys):
        classes[k].append(j)

    top = len(cards) - 1
    A, T, h = cards[top]
    refs = references(trees)
    placements = Counter(s for _, s in refs)

    print('cards                 : %d' % len(cards))
    print('final card            : %d, |A| = %d, |T| = %d, h = %d' % (top, len(A), len(T), h))
    print('references            : %d' % len(refs))
    print('distinct cases        : %d   (cards modulo the eight maps and translations)'
          % len(classes))
    print('hidden duplicates     : %d   (cards - cases)' % (len(cards) - len(classes)))
    print()

    dup = sorted((v for v in classes.values() if len(v) > 1), key=len, reverse=True)
    if dup:
        print('classes with more than one card -- merge candidates:')
        for v in dup:
            j = v[0]
            a, t, hh = cards[j]
            print('  %d cards: %s   (|A| = %d, |T| = %d, h = %d)'
                  % (len(v), v, len(a), len(t), hh))
    else:
        print('no two cards are congruent: a symmetry quotient would save nothing.')
    print()

    print('distinct envelopes up to symmetry   : %d'
          % len({canon((set(), t)) for a, t, hh in cards}))
    print('distinct requirements up to symmetry: %d'
          % len({canon((a, set())) for a, t, hh in cards}))
    print('distinct (|A|,|T|,h) triples        : %d'
          % len({(len(a), len(t), hh) for a, t, hh in cards}))
    print()

    print('placement codes used (s: references): %s'
          % dict(sorted(placements.items())))
    if refs:
        print('identity placements                 : %d (%.0f%%)'
              % (placements[0], 100.0 * placements[0] / len(refs)))
    print()

    byh = defaultdict(lambda: [set(), 0])
    for j, (a, t, hh) in enumerate(cards):
        byh[hh][0].add(keys[j])
        byh[hh][1] += 1
    print('  h   cards   cases')
    for hh in sorted(byh):
        print('%3d %7d %7d' % (hh, byh[hh][1], len(byh[hh][0])))
    print()

    if trees:
        used = reachable(trees, top)
        dead = [j for j in range(len(cards)) if j not in used]
        print('reachable from the final card: %d cards, %d cases'
              % (len(used), len({keys[j] for j in used})))
        if dead:
            print('not reachable                : %d cards, %d cases  %s'
                  % (len(dead), len({keys[j] for j in dead}), dead[:20]))


if __name__ == '__main__':
    main(*sys.argv[1:])
