import random
import pygame
from settings import *

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.radius = int(self.app.cell_width//2.3)
        self.pix_pos = self.get_pix_pos()
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.starting_pos = [pos.x, pos.y]

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2, (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2 )

    def update(self):
       self.pix_pos +=self.direction

       if self.time_to_move():
           self.move()

       self.grid_pos[0] = self. temp_position(0, self.app.cell_width)
       self.grid_pos[1] = self.temp_position(1, self.app.cell_height)

    def temp_position(self, temp_numb, temp_X):
        return (self.pix_pos[temp_numb] - TOP_BOTTOM_BUFFER + temp_X//2)//temp_X+1

    def draw(self):
       pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_colour(self):
        if self.number == 0:
            return  (43, 78, 203)

        if self.number == 1:
            return (197, 200, 27)

        if self.number == 2:
            return  (189, 29, 29)

        if self.number == 3:
            return  (215, 159, 33)

    def set_personality(self):
        if self.number == 0:
            return "second"
        elif self.number == 1:
            return "third"
        elif self.number == 2:
          return "random"
        else:
            return "last_one"

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0 or self.direction == vec(0, 0):
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()

        if self.personality == "second":
            self.direction = self.get_path_direction()

        if self.personality == "third":
            self.direction = self.get_path_direction()

        if self.personality == "last_one":
            self.direction = self.get_path_direction()

    '''def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > MAX_X//2 and self.app.player.grid_pos[1] > MAX_Y//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > MAX_X//2 and self.app.player.grid_pos[1] < MAX_Y//2:
                return vec(1, MAX_Y - 2)
            if self.app.player.grid_pos[0] < MAX_X//2 and self.app.player.grid_pos[1] > MAX_Y//2:
                return vec(MAX_X-2, 1)
            else:
                return vec(MAX_X-2, MAX_Y-2)'''

    def get_path_direction(self):
        next_cell = self.find_cell_path()
        x_dir = next_cell[0]-self.grid_pos[0]
        y_dir = next_cell[1]-self.grid_pos[1]
        return vec(x_dir, y_dir)

    def get_random_direction(self):
        while True:
            number = random.randint(-4, 4)
            if number < -2:
                x_dir, y_dir = 1, 0
            elif number > -3 and number < 0:
                x_dir, y_dir = 0, 1
            elif number > -1 and number < 2:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def find_cell_path(self):
        start_pos = [int(self.grid_pos.x), int(self.grid_pos.y)]
        target_pos = [int(self.app.player.grid_pos.x), int(self.app.player.grid_pos.y)]
        path = self.BFS(start_pos, target_pos)
        return path

    def BFS(self, start, target):
        grid = [[0 for x in range(MAX_X) ]for x in range (MAX_Y)]
        for cell in self.app.walls:
            if cell.x <MAX_X and cell.y <MAX_Y:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for temp in neighbours:
                    if temp[0]+current[0] >= 0 and temp[0] + current[0] < len(grid[0]):
                        if temp[1]+current[1] >= 0 and temp[1] + current[1] < len(grid):
                            next_cell = [temp[0]+current[0], temp[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest[1]