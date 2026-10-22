"""Reconstruct the 21-move certificate: 728 cards (A, T, h) plus the expression trees."""
SYM = '0123456789ABCDEFG'
SNAKE = [(0,0),(1,0),(2,0),(3,0),(3,1),(4,1)]

def point(w):
    return (SYM.index(w[0]), SYM.index(w[1]))

def put(s, dx, dy, P):
    Q=set()
    for x,y in P:
        if s & 2: x=-x
        if s & 4: y=-y
        if s & 1: x,y = y,x
        Q.add((x+dx, y+dy))
    return Q

class Ref:
    __slots__=('j','s','dx','dy')
    def __init__(self,j,s=0,dx=0,dy=0): self.j,self.s,self.dx,self.dy=j,s,dx,dy
class Expr:
    __slots__=('p','kids')
    def __init__(self,p,kids): self.p,self.kids=p,kids

def parse_ref(tok):
    parts=tok.split(':')
    j=int(parts[0])
    if len(parts)==1: return Ref(j)
    s=int(parts[1][0]); dx,dy=point(parts[1][1:])
    return Ref(j,s,dx,dy)

def parse_line(line):
    words=line.replace('(',' ( ').replace(')',' ) ').split()
    it=iter(words+[')'])
    num=int(next(it))
    def expr():
        p=point(next(it)); kids=[]
        while True:
            w=next(it)
            if w==')': break
            kids.append(expr() if w=='(' else parse_ref(w))
        return Expr(p,kids)
    return num, expr()

def load(path=None):
    import os
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificate.txt')
    cards=[]  # list of (A,T,h) ; 0..5 bases
    trees={}  # j -> Expr
    for T0,p in zip([set(SNAKE) for _ in SNAKE], SNAKE):
        cards.append((T0-{p}, T0, 1))
    for line in open(path):
        line=line.strip()
        if not line: continue
        num,root=parse_line(line)
        assert num==len(cards), (num,len(cards))
        a,t,h=eval_expr(root,cards)
        cards.append((a,t,h)); trees[num]=root
    return cards, trees

def eval_expr(node, cards):
    aa=[];tt=[];hh=[]
    for k in node.kids:
        if isinstance(k,Ref):
            a,t,h=cards[k.j]
            a=put(k.s,k.dx,k.dy,a); t=put(k.s,k.dx,k.dy,t)
        else:
            a,t,h=eval_expr(k,cards)
        aa.append(a);tt.append(t);hh.append(h)
    A=(set().union(*aa)|set.intersection(*tt))-{node.p}
    T=set().union({node.p},*tt)
    return A,T,1+max(hh)
