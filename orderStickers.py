from classes import Sticker
import math

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def isClose(a, b):
    return (1-closeness)*a < b < (1+closeness)*a

def closest(target, poss):
    return min(poss, key=lambda p: dist(p.pos, target))

def closestN(target, poss, n):
    return sorted(poss, key=lambda p: p.dist[target])[1:n+1]

def order(stickers):
    pos = [0,0]
    for s in stickers:
        p = s.pos
        pos[0] += p[0]
        pos[1] += p[1]
    pos[0]/=9
    pos[1]/=9
    center = closest(pos, stickers)
    center.piece = 'c'
    print(center.pos, pos)
    stickers.remove(center)
    edges = [[1000], [1000], [1000], [1000]]
    def insert(insertion):
        for i in range(len(edges)):
            print(edges)
            print(edges[i][0])
            print(insertion[0])
            if edges[i][0] > insertion[0]:
                edges.insert(i, insertion)
                edges.pop()
                return

    for ip in range(len(stickers)):
        i = stickers[ip]
        for jp in range(ip, len(stickers)):
            if jp == ip:
                continue
            j = stickers[jp]
            mid = ((i.pos[0]+j.pos[0])/2, (i.pos[1]+j.pos[1])/2)
            tot = dist(i.pos, j.pos)
            for kp in range(len(stickers)):
                if kp == jp or kp == ip:
                    continue
                edgeness = dist(mid, stickers[kp].pos)/tot
                insert((edgeness, stickers[kp], i, j))
    for s in stickers:
        s.piece = 'r'

    border = []
    for e in edges:
        e[1].piece = 'e'
        border.append((e[2],e[1],e[3]))

    return border

    '''
    d = {}
    for i in range(len(stickers)):
        for j in range(i, len(stickers)):
            dis = dist(stickers[i].pos, stickers[j].pos)
            stickers[i].dist[stickers[j]] = dis
            stickers[j].dist[stickers[i]] = dis
    for s in stickers:
        d[s] = closestN(s, stickers, 4)
        adj = d[s]
        first = adj[0].dist[s]
        if isClose(adj[3].dist[s], first):
            s.piece = 'c'
        elif isClose(adj[2].dist[s], first):
            s.piece = 'e'
        else:
            s.piece = 'r'
    '''

