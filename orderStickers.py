from classes import Sticker
import math

closeness = .4

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def isClose(a, b):
    return (1-closeness)*a < b < (1+closeness)*a

def closest(target, poss):
    return min(poss, key=lambda p: dist(p.pos, target))

def closestN(target, poss, n):
    return sorted(poss, key=lambda p: p.dist[target])[1:n+1]

def isEdge(stickers, piece):
    for ip in range(len(stickers)):
        if stickers[ip] == piece:
            continue
        i = stickers[ip]
        for j in range(ip, len(stickers)):
            if stickers[j] == piece or ip == j:
                continue
            j = stickers[j]
            mid = dist(((i.pos[0]+j.pos[0])/2, (i.pos[1]+j.pos[1])/2), piece.pos)
            tot = dist(i.pos, j.pos)
            print(mid, tot, i.pos[:2], j.pos[:2], piece.pos[:2])
            if mid < closeness*tot:
                return i, j
    return False

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
    while stickers:
        if len(stickers) == 2:
            stickers[0].piece = 'e'
            stickers[1].piece = 'e'
        for i in stickers:
            e = isEdge(stickers, i)
            if e:
                i.piece = 'e'
                e[0].piece = 'c'
                e[1].piece = 'c'
                stickers.remove(i)
                stickers.remove(e[0])
                stickers.remove(e[1])
                break
            print('couldn\'t find the edges')
            return
    return

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

