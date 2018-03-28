import geopandas as gp
import gdal
import matplotlib.pyplot as plt
import os
from scipy.spatial import distance
import numpy
import collections

''' Set path
'''
tl_path = r'C:\Users\tnauss\permanent\edu\msc-phygeo-if-error-continue'
data_path = tl_path + os.sep + "data"
dgm_filepath = data_path + os.sep + r"KU_DGM10\KU_DGM10.tif"
summit_filepath = data_path + os.sep + r"gipfelliste\brandenberger_alpen.shp"


''' Functions
'''
def coord2array(gt, x, y):
    col = int((x - gt[0]) / gt[1])
    row = int((gt[3] - y) / gt[1])
    return(row, col)

def array2coord(gt, row, col):
    x = int(col * gt[1] + gt[0])
    y = int(row * -gt[1] + gt[3])
    return(x, y)

def dominance_positions(peak, dem_array, gt):
    pot_coords = []
    distance = 1
    x, y = coord2array(gt, peak.geometry.x, peak.geometry.y)
    while len(pot_coords) == 0:
        for x2 in range(x-distance, x+(distance+1)):
            if float(peak['height']) <= dem_array[x2, y-distance]:
                pot_coords.append([x2, y-distance])
            if float(peak['height']) <= dem_array[x2, y+distance]:
                pot_coords.append([x2, y+distance])
        for y2 in range(y-(distance-1), y+(distance)):
            if float(peak['height']) <= dem_array[x-distance, y2]:
                pot_coords.append([x-distance, y2])
            if float(peak['height']) <= dem_array[x+distance, y2]:
                pot_coords.append([x+distance, y2])
        distance = distance + 1
    return(pot_coords)


''' Load datasets
'''
dem = gdal.Open(dgm_filepath)
dem_a = dem.ReadAsArray()
gt = dem.GetGeoTransform()


summits= gp.read_file(summit_filepath)

# peaks.columns = ['cat', 'value', 'label', 'height', 'geometry']
# peaks = peaks.drop(['value','label'], axis=1)


summit = summits.iloc[[0]]
summit['height'] = 1632.1579999999999

pot_dominance = dominance_positions(summit, dem_a, gt)
potx, poty = array2coord(gt, pot_dominance[0][0], pot_dominance[0][1])
dominance = distance.euclidean([potx, poty], [summit.geometry.x, summit.geometry.y])
print(dominance)

x,y = coord2array(gt, summit.geometry.x, summit.geometry.y)
plt.figure()
dem_plot = plt.imshow(dem_a)
plt.xlim(1000, 2000)
plt.ylim(2000, 3000)
plt.scatter(pot_dominance[0][0], pot_dominance[0][1])
plt.scatter(x,y, c = 'red')
plt.show()






def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not maze[row][col + 1]:
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph


from collections import deque


def find_path_bfs(maze):
    start, goal = (1, 1), (len(maze) - 2, len(maze[0]) - 2)
    queue = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while queue:
        path, current = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!"



dem = gdal.Open(dgm_filepath)
dem_a = dem.ReadAsArray()
gt = dem.GetGeoTransform()

summit = summits.iloc[[0]]
summit['height'] = 1632.1579999999999
r, c = coord2array(gt, summit.geometry.x, summit.geometry.y)

dem_ar = numpy.copy(dem_a)
dem_ar[r,c]

level = 1500.0

dem_ar[dem_ar < level] = 0
dem_ar[dem_ar >= level] = 1

plt.figure()
dem_plot = plt.imshow(dem_ar)

dem_ar[r+5, c+5] = 2

height, width = dem_ar.shape


# https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-python
def bfs(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
                

wall, clear, goal = "0", "1", "2"
path = bfs(dem_ar, (r, c))
path


wall, clear, goal = "#", ".", "*"
width, height = 10, 5
grid = ["..........",
        "..*#...##.",
        "..##...#*.",
        ".....###..",
        "......*..."]
path = bfs(grid, (5, 2))
# [(5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]                








import numpy
from heapq import *


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

print(bfs(graph, '1', '11'))