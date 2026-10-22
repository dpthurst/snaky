"""Play the Section-4 policy; trace the descent. Placements = signed permutation + translation."""
import snakylib as sl

# --- placements: x |-> R_s x + t -------------------------------------------------
def Rmap(s, v):
    x, y = v
    if s & 2: x = -x
    if s & 4: y = -y
    if s & 1: x, y = y, x
    return (x, y)

_IMG = {(Rmap(s, (1, 0)), Rmap(s, (0, 1))): s for s in range(8)}

def comp(f, g):
    """placement f applied after g"""
    (sf, dxf, dyf), (sg, dxg, dyg) = f, g
    e1 = Rmap(sf, Rmap(sg, (1, 0)))
    e2 = Rmap(sf, Rmap(sg, (0, 1)))
    s = _IMG[(e1, e2)]
    tx, ty = Rmap(sf, (dxg, dyg))
    return (s, tx + dxf, ty + dyf)

def apply(F, P):
    s, dx, dy = F
    return sl.put(s, dx, dy, P)

def apply1(F, p):
    s, dx, dy = F
    x, y = p
    if s & 2: x = -x
    if s & 4: y = -y
    if s & 1: x, y = y, x
    return (x + dx, y + dy)

ID = (0, 0, 0)

class Card:
    __slots__ = ('j',)
    def __init__(self, j): self.j = j

class Game:
    def __init__(self, cards, trees):
        self.cards, self.trees = cards, trees
        self.M, self.B = set(), set()
        self.moves = []          # (maker_cell, breaker_cell_after)
        self.claims = []         # maker cells in order
        self.breakers = []
        self.done = False

    def enum_key(self, c):
        x, y = c
        return (max(abs(x), abs(y)), x, y)

    def free_cell(self):
        L = 0
        while True:
            for x in range(-L, L + 1):
                for y in range(-L, L + 1):
                    if max(abs(x), abs(y)) == L and (x, y) not in self.M and (x, y) not in self.B:
                        # enumeration: increasing max-norm, then lexicographic
                        pass
            cand = [(x, y) for x in range(-L, L + 1) for y in range(-L, L + 1)
                    if max(abs(x), abs(y)) == L and (x, y) not in self.M and (x, y) not in self.B]
            if cand:
                return sorted(cand)[0]
            L += 1

    def won(self):
        for a, b, c, d, e, f in [(0,0,1,0,2,0)]:
            pass
        return any(all((x + dx, y + dy) in self.M for dx, dy in S) for x, y in self.M)

S = [(x, y) for x, y in sl.SNAKE]
SHAPES = [sl.put(s, 0, 0, set(S)) for s in range(8)]

def has_target(M):
    for sh in SHAPES:
        pts = sorted(sh)
        for (x, y) in list(M):
            # translate shape so that pts[0] matches a cell
            for (px, py) in pts:
                dx, dy = x - px, y - py
                if set((a + dx, b + dy) for a, b in pts) <= M:
                    return set((a + dx, b + dy) for a, b in pts)
    return None

