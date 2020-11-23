# faces will be passed in two at a time,
# they will be contiguous
# face[x][y]
opposites = {'r':'o', 'o':'r', 'b':'g', 'g':'b', 'w':'y', 'y':'w'}
starts = {  'y': 0,
            'b': 9,
            'r': 18,
            'g': 27,
            'o': 36,
            'w': 45}
#THIS IS CORRECT AND TOOK A WHILE TO TEST, DO NOT CHANGE
settings = {'o': {'b': [0, 0], 'w': [3, 1], 'y': [1, 3], 'g': [2, 2]},
            'b': {'o': [2, 2], 'r': [0, 0], 'w': [3, 0], 'y': [1, 0]},
            'r': {'b': [2, 2], 'w': [3, 3], 'y': [1, 1], 'g': [0, 0]},
            'w': {'o': [3, 1], 'b': [2, 1], 'r': [1, 1], 'g': [0, 1]},
            'y': {'o': [1, 3], 'b': [2, 3], 'r': [3, 3], 'g': [0, 3]},
            'g': {'o': [0, 0], 'r': [2, 2], 'w': [3, 2], 'y': [1, 2]}}


def setFaces(stickers, faces): 
    colors = [faces[0][1][1], faces[1][1][1]]
    start = [starts[i] for i in colors]
    if colors[0] in opposites[colors[1]]:
        print("ERROR: INVALID CUBE")
        return False
    rotations = settings[colors[0]][colors[1]] #in counterclockwise direction
    
    for f in range(2):
        counter = start[f]
        for i in range(3):
            for j in range(3):
                poss = [[i,j], [j, 2-i], [2-i, 2-j], [2-j, i]][rotations[f]]
                stickers[counter] = faces[f][poss[0]][poss[1]]
                counter += 1


    

