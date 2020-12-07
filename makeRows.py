from classes import Sticker
import math

def closest(target, poss):
    return min(poss, key=lambda p: math.dist(target.pos, p.pos))

def find_border(edges, corners):
    rows = []
    for edge in edges:
        corn1 = closest(edge, corners)
        corn2 = closest(edge, [c for c in corners if not c == corn1])
        rows.append([corn1, edge, corn2])
    return rows

def classify_rows(rows, corners, center):
    row1 = rows[0]
    for row in rows[1:]:
        skip = False
        for sticker in row:
            if sticker in row1:
                skip = True
                break
        if skip:
            continue
        row2 = row
        middleRow = []
        for corn in corners:
            if corn not in row1 and corn not in row2:
                print('a')
                middleRow.append(corn)
        middleRow.insert(1, center)
        return [row1, middleRow, row2]

def sort_pts(row, index):
    assert len(row) == 3
    max_i = max(row, key=lambda p: p.pos[index])
    min_i = min(row, key=lambda p: p.pos[index])
    for s in row:
        if s not in [max_i, min_i]:
            return [min_i, s, max_i]

def sort_rows(rows, index):
    assert len(rows) == 3
    max_i = max(rows, key=lambda r: r[0].pos[index])
    min_i = min(rows, key=lambda r: r[0].pos[index])
    for s in rows:
        if s[0] not in [max_i[0], min_i[0]]:
            return [min_i, s, max_i]

def order_row(rows):
    for i in range(len(rows)):
        rows[i] = sort_pts(rows[i], 0)
    rows = sort_rows(rows, 1)[::-1]
    return rows

def testing():
    import random
    random.seed(50)
    e = [(0, 1), (1, 0), (1, 2), (2, 1)]
    random.shuffle(e)
    edges = [Sticker(pos=p) for p in e]
    c = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(c)
    corners = [Sticker(pos=p) for p in c]
    mid = Sticker(pos=(1, 1))
    bord = find_border(edges, corners)
    print(bord)
    rows = classify_rows(bord, corners, mid)
    print(rows)
    ord_rows = order_row(rows)
    print(ord_rows)

testing()
