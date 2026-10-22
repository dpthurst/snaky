"""Run the Section-4 policy against many breakers, checking the Definition-2 invariant."""
import random, trace

w = trace.World()

def play(mode, seed=0, cap=30):
    rnd = random.Random(seed)
    M, B = set(), set()
    node = ('card', 727, trace.ID)
    log = []
    for step in range(1, cap+1):
        A, T, h = w.data(node)
        assert not (B & T), 'envelope invariant broken at step %d' % step
        assert A <= M, 'required set not owned at step %d' % step
        assert h >= 1
        p = w.pivot(node)
        assert p not in B
        claim = p if p not in M and p not in B else trace.first_free(M, B)
        assert claim not in M and claim not in B
        M.add(claim)
        log.append(dict(step=step, card=(node[1] if node[0] == 'card' else 'expr'),
                        h=h, size=len(T), T=set(T), pivot=p, claim=claim, A=set(A)))
        win = trace.has_target(M)
        if win:
            log[-1]['win'] = win
            return log, M, B
        kids = w.children(node); ds = [w.data(k) for k in kids]
        cand = sorted(b for b in set().union(*[d[1] for d in ds]) if b not in M and b not in B)
        if mode == 'greedy':
            b = max(cand, key=lambda z: (sum(1 for d in ds if z in d[1]),
                                         -max(abs(z[0] - 8), abs(z[1] - 8)), tuple(-c for c in z)))
        elif mode == 'rand':
            b = rnd.choice(cand)
        B.add(b)
        log[-1]['reply'] = b
        surv = None
        for k, d in zip(kids, ds):
            if b not in d[1]:
                surv = k; break
        assert surv is not None, 'no surviving child at step %d' % step
        node = surv
    raise RuntimeError('no win in %d moves' % cap)

if __name__ == '__main__':
    from collections import Counter
    lengths = Counter()
    worst = 0
    for seed in range(200):
        log, M, B = play('rand', seed)
        lengths[len(log)] += 1
        worst = max(worst, len(log))
        assert len(log) <= 21
    print('random breakers, game lengths:', dict(sorted(lengths.items())), 'worst', worst)
    log, M, B = play('greedy', 0)
    print('greedy breaker: win in', len(log), 'moves')
    for e in log:
        print(' ', e['step'], e['card'], 'h=%2d' % e['h'], '|T|=%3d' % e['size'],
              'pivot', e['pivot'], 'claim', e['claim'], 'reply', e['reply'])
    print('  winning copy:', sorted(log[-1]['win']))
