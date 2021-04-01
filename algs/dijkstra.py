import numpy
from heapq import *
import time



def dijkstra(canvas, array, start, goal):
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: 1}
    oheap = []

    heappush(oheap, (1, start))
    
    canvas.in_search = True

    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            canvas.finish_search(path)
            canvas.in_search = False
            return path

        close_set.add(current)
        for w, h in neighbours:
            neighbour = current[0] + w, current[1] + h
            temp_g_score = gscore[current] + 1
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

            if temp_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                canvas.highlight(neighbour)
                time.sleep(canvas.get_root().options['speed']/1000)
                came_from[neighbour] = current
                gscore[neighbour] = temp_g_score
                fscore[neighbour] = temp_g_score + 1
                heappush(oheap, (fscore[neighbour], neighbour))

    canvas.in_search = False
    return False

