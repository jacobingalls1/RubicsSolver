from classes import Sticker
import math

closeness = .1

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def isClose(a, b):
    return (1-closeness)*a < b < (1+closeness)*a

def closestN(target, poss, n):
    
    return sorted(poss, key=lambda p: p.dist[target])[1:n+1]

def order(stickers):
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


