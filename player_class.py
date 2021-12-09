import random

import pygame
from settings import *
from heapq import *
from random import randint
vec = pygame.math.Vector2

class Player:
    def __init__(self, app,  pos):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

        for_X = (self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2
        for_Y =  (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2
        self.pix_pos = vec(for_X, for_Y )

    def update(self):
        self.pix_pos += self.direction

        if self.time_to_move():
            self.direction =  self.get_path_direction()

        self.grid_pos[0] = self.temp_position(0, self.app.cell_width)
        self.grid_pos[1] = self.temp_position(1, self.app.cell_height)

        if self.on_coin():
            self.eat_coin()

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0 or self.direction == vec(0, 0):
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

        return False
    def temp_position(self, temp_numb, temp_X):
        return (self.pix_pos[temp_numb] - TOP_BOTTOM_BUFFER + temp_X // 2) // temp_X + 1


    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def  draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)),  self.app.cell_width//2-2)

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (31 + 23*x, HEIGHT - 12), 7)

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

   # def move(self, direction):
    #    self.stored_direction = direction

    def on_coin(self):
        if self.grid_pos in self.app.coints:
            return True
        return False

    def eat_coin(self):
        self.app.coints.remove(self.grid_pos)
        self.current_score += 1

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < MAX_X and 0 <= y < MAX_Y and vec(x, y) not in self.app.walls else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(1, (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def A_star(self, start, target):

        graph = {}
        for y in range(MAX_Y):
            for x in range(MAX_X):
                graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y)

        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}
        path = []
        while True:
            if queue:
                current_cost, current_node = heappop(queue)
                if current_node == target:
                    path.append(current_node)
                    return path

                next_nodes = graph[current_node]
                for next_node in next_nodes:
                    neigh_cost, neigh_node = next_node
                    new_cost = cost_visited[current_node] + neigh_cost

                    if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                        priority = new_cost + self.heuristic(neigh_node, target)
                        heappush(queue, (priority, neigh_node))
                        cost_visited[neigh_node] = new_cost
                        visited[neigh_node] = current_node

                path.append(current_node)


    def find_cell_path(self):
        start = (int(self.grid_pos.x), int(self.grid_pos.y))
        temp_goal = random.choice(self.app.coints)
        #print(self.app.coints, "c")
        #print(temp_goal, "1")
        target = (int(temp_goal[0]), int(temp_goal[1]))
        path = self.A_star(start, target)
        print(path)
        return path[1]

    def get_path_direction(self):
        next_cell = self.find_cell_path()
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vec(x_dir, y_dir)
