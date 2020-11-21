# faces will be passed in two at a time,
# they will be contiguous
# face[x][y]
opposites = {'R':'O', 'O':'R', 'B':'G', 'G':'B', 'W':'Y', 'Y':'W'}
starts = {  'Y': 0,
            'B': 9,
            'R': 18,
            'G': 27,
            'O': 36,
            'W': 45}

settings = {'O': {'B': [0, 0], 'W': [1, 3], 'Y': [3, 1], 'G': [2, 2]},
            'B': {'O': [2, 2], 'R': [0, 0], 'W': [1, 0], 'Y': [3, 0]},
            'R': {'B': [2, 2], 'W': [1, 1], 'Y': [3, 3], 'G': [0, 0]},
            'W': {'O': [3, 1], 'B': [3, 2], 'R': [3, 3], 'G': [3, 0]},
            'Y': {'O': [1, 3], 'B': [2, 3], 'R': [1, 1], 'G': [1, 0]},
            'G': {'O': [0, 0], 'R': [2, 2], 'W': [1, 0], 'Y': [3, 2]}}


def setFaces(stickers, faces): 
    print(faces)
    colors = [faces[0][1][1], faces[1][1][1]]
    print(colors)
    start = [starts[i] for i in colors]
    if colors[0] in opposites[colors[1]]:
        print("ERROR: INVALID CUBE")
        return False
    rotations = settings[colors[0]][colors[1]] #in clockwise direction
    
    print(rotations)
    for f in range(2):
        counter = start[f]
        for i in range(3):
            for j in range(3):
                poss = [[i,j], [j, 2-i], [2-i, 2-j], [2-j, i]][rotations[f]]
                stickers[counter] = faces[f][poss[0]][poss[1]]
                counter += 1


    

