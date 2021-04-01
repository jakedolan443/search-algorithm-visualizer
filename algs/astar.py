import numpy
from heapq import *
import time

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(canvas, array, start, goal):
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    heap_lst = []

    heappush(heap_lst, (fscore[start], start))

    canvas.in_search = True

    while heap_lst:
        current = heappop(heap_lst)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            canvas.finish_search(path)
            canvas.in_search = False
            return path

        close_set.add(current)
        for w,h in neighbours:
            neighbour = current[0] + w, current[1] + h
            temp_g_score = gscore[current] + heuristic(current, neighbour)
            if 0 <= neighbour[0] < array.shape[0]:
                if 0 <= neighbour[1] < array.shape[1]:
                    if array[neighbour[0]][neighbour[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbour in close_set and temp_g_score >= gscore.get(neighbour, 0):
                continue

            if temp_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in heap_lst]:
                canvas.highlight(neighbour)
                time.sleep(canvas.get_root().options['speed']/1000)
                came_from[neighbour] = current
                gscore[neighbour] = temp_g_score
                fscore[neighbour] = temp_g_score + heuristic(neighbour, goal)
                heappush(heap_lst, (fscore[neighbour], neighbour))

    canvas.in_search = False
    return False

