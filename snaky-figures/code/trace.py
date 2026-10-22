import snakylib as sl
from sim import comp, apply, apply1, ID, has_target, SHAPES

class World:
    def __init__(self, path='certificate.txt'):
        self.cards, self.trees = sl.load(path)

    # --- node data -------------------------------------------------------
    def children(self, node):
        kind = node[0]
        if kind == 'card':
            _, j, F = node
            if j not in self.trees:
                return []
            return self.children(('expr', self.trees[j], F))
        _, E, F = node
        out = []
        for k in E.kids:
            if isinstance(k, sl.Ref):
                out.append(('card', k.j, comp(F, (k.s, k.dx, k.dy))))
            else:
                out.append(('expr', k, F))
        return out

    def data(self, node):
        if node[0] == 'card':
            _, j, F = node
            A, T, h = self.cards[j]
            return apply(F, A), apply(F, T), h
        _, E, F = node
        kids = self.children(node)
        ds = [self.data(k) for k in kids]
        A = (set().union(*[d[0] for d in ds]) | set.intersection(*[d[1] for d in ds])) - {apply1(F, E.p)}
        T = set().union({apply1(F, E.p)}, *[d[1] for d in ds])
        return A, T, 1 + max(d[2] for d in ds)

    def pivot(self, node):
        if node[0] == 'card':
            _, j, F = node
            if j not in self.trees:
                return apply1(F, sl.SNAKE[j])
            return apply1(F, self.trees[j].p)
        _, E, F = node
        return apply1(F, E.p)

def first_free(M, B):
    L = 0
    while True:
        cand = [(x, y) for x in range(-L, L + 1) for y in range(-L, L + 1)
                if (x, y) not in M and (x, y) not in B]
        if cand:
            return sorted(cand)[0]
        L += 1

def play(world, breaker='greedy', verbose=False):
    M, B = set(), set()
    node = ('card', 727, ID)
    log = []
    for step in range(1, 30):
        A, T, h = world.data(node)
        pivot = world.pivot(node)
        claim = pivot if pivot not in M and pivot not in B else first_free(M, B)
        M.add(claim)
        log.append(dict(step=step, card=(node[1] if node[0] == 'card' else 'expr'),
                        h=h, size=len(T), pivot=pivot, claim=claim, T=T, A=set(A)))
        win = has_target(M)
        if win:
            log[-1]['win'] = win
            return M, B, log
        kids = world.children(node)
        # greedy breaker: maximise number of child envelopes covered
        kd = [world.data(k) for k in kids]
        best, bcov = None, -1
        cand = [b for b in set().union(*[d[1] for d in kd]) if b not in M and b not in B]
        for b in sorted(cand, key=lambda c: (max(abs(c[0]), abs(c[1])), c)):
            cov = sum(1 for d in kd if b in d[1])
            if cov > bcov:
                best, bcov = b, cov
        b = best
        B.add(b)
        log[-1]['reply'] = b
        surv = None
        for k, d in zip(kids, kd):
            if b not in d[1] and not (d[1] & B):
                surv = k
                break
        assert surv is not None, step
        node = surv
    raise RuntimeError('no win')

if __name__ == '__main__':
    w = World()
    M, B, log = play(w)
    for e in log:
        print(e['step'], 'card', e['card'], 'h', e['h'], '|T|', e['size'],
              'pivot', e['pivot'], 'claim', e['claim'], 'reply', e.get('reply'),
              'WIN' if 'win' in e else '')
    print('maker stones', len(M))
    print('winning snake', sorted(log[-1]['win']))
