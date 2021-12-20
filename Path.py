import time
from settings import *
import pygame
vec = pygame.math.Vector2
from queue import PriorityQueue


class PathCalc:

    def __init__(self, app):
        self.x_len = MAX_X+4
        self.y_len = MAX_Y+8
        self.app = app
        self.start_time = 0
        self.end_time = 0
        self.time = 0
        self.used = []
        self.way = []


    def start_dfs(self, pos, target):
        pos_n = [pos[0], pos[1]]
        self.way = []
        self.start_time = time.time()

        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]

        pos_n, parents = self.step_dfs(pos_n, pos_n, parents, target)
        h_arr = self.find_way(parents, pos, pos_n)

        if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
            for j in range(1, len(h_arr)):
                self.used[h_arr[j][1]][h_arr[j][0]] = 1
                self.way.append(h_arr[j])

        self.end_time = time.time()
        self.time = (-self.start_time+self.end_time)*1000
        print("DFS time is " + str(self.time) + "ms")
        return self.way

    def step_dfs(self, pos, new_pos, parents, target):
        self.used[pos[1]][pos[0]] = 1

        list_of_near = self.find_near(pos, target)

        if pos[1] == target[1] and pos[0] == target[0]:

            new_pos = [pos[0], pos[1]]
            return new_pos, parents
        else:

            for i in list_of_near:
                parents[i[1]][i[0]] = pos
                new_pos, parents = self.step_dfs(i, new_pos, parents, target)
                if new_pos[1] == target[1] and new_pos[0] == target[0]:
                    return new_pos, parents
        self.used[pos[1]][pos[0]] = 0
        return new_pos, parents

    def find_near(self, pos, target):
        list_of_near = []
        all_pos = [[pos[0] + 1, pos[1]], [pos[0], pos[1] - 1], [pos[0] - 1, pos[1]], [pos[0], pos[1] + 1]]

        for i in range(len(all_pos)):
            if self.y_len > all_pos[i][1] >= 0 <= all_pos[i][0] < self.x_len:
                list_of_near = self.is_free([all_pos[i][0], all_pos[i][1]], list_of_near)

        for i in list_of_near:
            if i[0] == target[0] and i[1] == target[1]:
                list_of_near = [i]

        return list_of_near

    def is_free(self, pos, list_n):
        if self.used[pos[1]][pos[0]] == 0 and vec(pos[0], pos[1]) not in self.app.walls :
            list_n.append(pos)
        return list_n

    def find_way(self, parents, start, end):
        a = [end[0], end[1]]
        h = [a]
        count = 0
        while (a[0] != start[0] or a[1] != start[1]) and count < self.x_len * self.y_len:
            a = parents[a[1]][a[0]]
            h.append(a)
            count += 1
        h.append(start)
        h.reverse()
        return h

    def start_uniform_cost_search(self, pos, target):
        self.way = []
        self.start_time = time.time()

        self.used = [[0] * int(self.x_len) for j in range(self.y_len)]
        parents = [[0, 0] * int(self.x_len) for j in range(self.y_len)]
        dist = [[0] * int(self.x_len) for j in range(self.y_len)]
        pos_n = [pos[0], pos[1]]

        pos_n, parents = self.step_ucs(pos_n, pos_n, PriorityQueue(), parents, dist, target)

        if pos_n[0] != pos[0] or pos[1] != pos_n[1]:
            h_arr = self.find_way(parents, pos, pos_n)

            for j in range(1, len(h_arr)):
                self.way.append(h_arr[j])

        self.end_time = time.time()
        self.time = (-self.start_time + self.end_time) * 1000

        print("UCS time is " + str(self.time) + "ms")
        return self.way

    def step_ucs(self, pos, new_pos, stack_h, parents, dist, target):
        used_h = [[0] * int(self.x_len) for j in range(self.y_len)]
        used_h[pos[1]][pos[0]] = 1
        dist[pos[1]][pos[0]] = 0

        stack_h.put((dist[pos[1]][pos[0]], pos))

        while not stack_h.empty():
            h_pos = (stack_h.get())[1]

            list_of_near = self.find_near(h_pos, target)
            if h_pos[0] == target[0] and h_pos[1] == target[1]:
                new_pos = [h_pos[0], h_pos[1]]
                return new_pos, parents
            else:
                for el in list_of_near:
                    h_dist = dist[h_pos[1]][h_pos[0]] + 1

                    if used_h[el[1]][el[0]] != 0:
                        if dist[el[1]][el[0]] > h_dist:
                            parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                            dist[el[1]][el[0]] = h_dist
                            stack_h, dist = self.retouch_dist(stack_h, el, dist)
                    else:
                        parents[el[1]][el[0]] = [h_pos[0], h_pos[1]]
                        dist[el[1]][el[0]] = h_dist
                        stack_h.put((dist[el[1]][el[0]], el))
                        used_h[el[1]][el[0]] = 1
        return new_pos, parents

    @staticmethod
    def retouch_dist(stack_h, pos, dist):
        el = stack_h.get()
        h_list = [el]
        while not stack_h.empty() and (el[1] != pos[1] or el[0] != pos[0]):
            el = stack_h.get()
            h_list.append(el)
        stack_h.put((dist[pos[1]][pos[0]], pos))
        for el in h_list:
            stack_h.put((dist[el[1]][el[0]], el))
        return stack_h, dist