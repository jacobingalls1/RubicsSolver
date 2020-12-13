from classes import Sticker
import math

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def closest(target, poss):
    return min(poss, key=lambda p: dist(target.pos, p.pos))
    # return min(poss, key=lambda p: math.dist(target.pos, p.pos))    # REQUIRES PY3.8

# find the 4 borders of a face
def find_border(edges, corners):
    rows = []
    for edge in edges:
        # find the closest sticker (a corner)
        corn1 = closest(edge, corners)
        # find the next closest sticker (another corner)
        corn2 = closest(edge, [c for c in corners if not c == corn1])
        rows.append([corn1, edge, corn2])

    return rows

# find 3 parallel rows from 4 borders
def classify_rows(rows, edges, center):
    import numpy as np
    import cv2
    import random
    bl = np.zeros((640, 480, 3))
    for r in rows:
        for p in r:
            cv2.putText(bl, str((int(p.pos[0]), int(p.pos[1]))), (int(p.pos[0]), int(p.pos[1])), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=0.5, color=(255,0,0))
        for i in range(1,3):
            cv2.line(bl, (int(r[i-1].pos[0]), int(r[i-1].pos[1])), (int(r[i].pos[0]), int( r[i].pos[1])), color=(0,255,0))
    for e in edges:
        cv2.drawMarker(bl, (int(e.pos[0]), int(e.pos[1])), color=(0,0,255))
    cv2.imwrite(str(int(random.uniform(100,999)))+'a.jpg', bl)
    row1 = rows[0]  # establish the first row
    print(row1)
    # find a row parallel to row1
    for row in rows[1:]:
        print(row)
        skip = False
        for sticker in row:
            if sticker in row1: # this row is not parallel, skip
                skip = True
                print('\t', sticker)
                break
        if skip:
            continue
        # row is parallel, classify as row2
        row2 = row
        # create middle row
        middleRow = []
        # find the two edges stickers that are a part of the middle row
        for edge in edges:
            if edge not in row1 and edge not in row2:
                middleRow.append(edge)
        middleRow.insert(1, center)
        return [row1, middleRow, row2]

# order row left to right
def sort_pts(row):
    assert len(row) == 3
    index=1 if row[0].pos[0] == row[1].pos[0] and row[0].pos[0] == row[1].pos[0] else 0
    max_i = max(row, key=lambda p: p.pos[index])
    min_i = min(row, key=lambda p: p.pos[index])
    for s in row:
        if s not in [max_i, min_i]:
            return [min_i, s, max_i], index

# order rows up to down
def sort_rows(rows, index):
    assert len(rows) == 3
    max_i = max(rows, key=lambda r: r[0].pos[index])
    min_i = min(rows, key=lambda r: r[0].pos[index])
    for s in rows:
        if s[0] not in [max_i[0], min_i[0]]:
            return [min_i, s, max_i]

# order left to right, up to down
def order_row(rows):
    # probably be better to use closest with a target of (0,0)
    for i in range(len(rows)):
        rows[i], ind = sort_pts(rows[i])
    ind = 0 if ind == 0 else 1
    rows = sort_rows(rows, ind)[::-1]
    return rows

def bordToRows(bord, center):
    row1 = bord[0]
    bord.remove(bord[0])
    row2 = [None, center, None]
    row3 = [None, None, None]
    used = []
    for i in bord:
        if row1[0] in i:
            row2[0] = i[1]
            row3[0] = [j for j in i if j.piece=='r' and j!=row1[0]][0]
            used.append(i)
        elif row1[2] in i:
            row2[2] = i[1]
            row3[2] = [j for j in i if j.piece=='r' and j!=row1[0]][0]
            used.append(i)
    print(used)
    [print(i) for i in used]
    print(bord)
    [print(i) for i in bord]
    for i in used:
        print(i)
        bord.remove(used)
    row3[1] = bord[0][1]
    return [row1, row2, row3]

'''def testing():
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
    rows = classify_rows(bord, edges, mid)
    print(rows)
    ord_rows = order_row(rows)
    print(ord_rows)'''

# MAIN FUNCTION FOR THIS FILE; ALL YOU NEED TO CALL
def make_rows(face, bord):
    edges = [s for s in face if s.piece == 'e']
    corners = [s for s in face if s.piece == 'r']
    print("edges", edges)
    print("corners", corners)
    for s in face:
        if s.piece == 'c':
            mid = s
    print(mid)
#    bord = find_border(edges, corners)
#    return bordToRows(bord, mid)
    rows = classify_rows(bord, edges, mid)
    ord_rows = order_row(rows)
    print("ord_rows")
    [print(i) for i in ord_rows]
    return ord_rows
