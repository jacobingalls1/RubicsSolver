from classes import Sticker

closeness = .05

def isClose(a, b):
    return (1-closeness)*a < b < (1+closeness)*a

def closestN(target, poss, n):
    for i in poss:
        i.dist[target] = math.dist(target, i.pos)
    return poss.sort(key=lambda p: p.dist[target])

def order(stickers):
    d = {closestN(i, stickers, n) for i in poss}
    for s in stickers:
        adj = d[s]
        first = adj[0].dist[s]
        if isClose(adj[3].dist[s], first):
            s.piece = 'c'
        elif isClose(adj[2].dist[s], first):
            s.piece = 'e'
        else:
            s.piece = 'c'


    






