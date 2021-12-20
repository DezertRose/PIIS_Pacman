import pygame
from settings import *
from heapq import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, app,  pos):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.direction = vec(1, 0)
       # self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

        for_X = (self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2
        for_Y =  (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2
        self.pix_pos = vec(for_X, for_Y )

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
            # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.on_coin():
            self.eat_coin()

    def temp_position(self, temp_numb, temp_X):
        return (self.pix_pos[temp_numb] - TOP_BOTTOM_BUFFER + temp_X//2)//temp_X+1

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

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

    def move(self, direction):
        self.stored_direction = direction

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

