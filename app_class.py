import sys
from  player_class import *
import pygame
from settings import *
from enemy_class import *
import copy

pygame.init()
vec = pygame.math.Vector2


class App:
     def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.p_pos = None
        self.cell_width = FIELD_WIDTH//MAX_X
        self.cell_height = FIELD_HEIGHT//MAX_Y
        self.walls = []
        self.coints = []
        self. enemies = []
        self.e_pos = []
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

     def run(self):
         while self.running:
             if self.state == 'start':
                 self.intro_events()
                 self.intro_draw()
             elif self.state == 'playing':
                 self.playing_events()
                 self.playing_update()
                 self.playing_draw()
             elif self.state == 'game_over':
                 self.over_events()
                 self.over_draw()
             else:
                 self.running = False
             self.clock.tick(CADRES)
         pygame.quit()
         sys.exit()

     def draw_text(self, words, screen, pos,  size, colour, font_name, centered = False):
         font = pygame.font.SysFont(font_name, size)
         text = font.render(words, False, colour)
         text_size = text.get_size()
         if centered:
             pos[0] = pos[0] - text_size[0]//2
             pos[1] = pos[1] - text_size[1]//2
         screen.blit(text, pos)

     def random_field(self):
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0:
                    self.walls.append(1)
                elif x  > int(MAX_X//2 + 3) and x < int(MAX_X//2-3):
                    if y == int(MAX_Y//2 - 3) or y == int(MAX_Y//2+ 3):
                        self.walls.append(1)
                    elif x == int(MAX_X//2 + 3) or x == int(MAX_X//2-3):
                        self.walls.append(1)
                    else:
                        self.walls.append(0)
                else:
                    self.walls.append(0)

     def load(self):
        self.baground = pygame.image.load('FIELD.png')
        self.baground = pygame.transform.scale(self.baground, (FIELD_WIDTH, FIELD_HEIGHT))
        with open("walls.txt", 'r' ) as file:
            for temp_y,  line in enumerate(file):
                for temp_x, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(temp_x, temp_y))
                    elif char == 'C':
                        self.coints.append(vec(temp_x, temp_y))
                    elif char == 'P':
                        self.p_pos = [temp_x, temp_y]
                    elif char in ['2', '3', '4', '5']:
                       self.e_pos.append(copy.copy([temp_x, temp_y]))
                    elif char == "B":
                       pygame.draw.rect(self.baground, BLACK, (temp_x*self.cell_width, temp_y*self.cell_height, self.cell_width, self.cell_height))

     def make_enemies(self):
         for idx, pos in enumerate(self.e_pos):
              self.enemies.append(Enemy(self, vec(pos), idx))

     def intro_events(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.running = False
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 self.state = 'playing'

     def intro_draw(self):
         self.screen.fill(BLACK)
         self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT // 2], START_TEXT_SIZE, ORANGE, START_FONT, centered=True)
         self.draw_text('HIGH SCORE', self.screen, [4, 0], START_TEXT_SIZE, BLUE, START_FONT)
         pygame.display.update()

     def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.baground, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))

        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.baground, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))

        for wall in self.walls:
            pygame.draw.rect(self.baground, BLUE, (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))

       # for coin in self.coints:
         #   pygame.draw.rect(self.baground, ORANGE, ( coin.x * self.cell_width, coin.y * self.cell_height, self.cell_width, self.cell_height), 1)

     def playing_events(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.running = False
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT:
                     self.player.move(vec(-1, 0))
                 if event.key == pygame.K_RIGHT:
                     self.player.move(vec(1, 0))
                 if event.key == pygame.K_UP:
                     self.player.move(vec(0, -1))
                 if event.key == pygame.K_DOWN:
                     self.player.move(vec(0, 1))

     def playing_update(self):
         self.player.update()
         for enemy in self.enemies:
             enemy.update()

         for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
               self.del_live()

     def del_live(self):
        self.player.lives  -= 1
        if self.player.lives == 0:
            self.state = "game_over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                 enemy.grid_pos = vec(enemy.starting_pos)
                 enemy.pix_pos = enemy.get_pix_pos()
                 enemy.direction *= 0

     def draw_path(self, path):
        for step in path:
            pygame.draw.rect(self.screen, GREY, ((step[0] +1)* self.cell_width, (step[1]+1) * self.cell_height, self.cell_width,  self.cell_height))

     def playing_draw(self):
         self.screen.fill(BLACK)
         self.screen.blit(self.baground, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
         self.draw_coints()
         self.draw_grid()
         self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [10, 0], 18, BLUE, START_FONT,  centered = False)
         self.player.draw()

         for enemy in self.enemies:
             enemy.draw()
         pygame.display.update()

     def draw_coints(self):
        for coin in self.coints:
            pygame.draw.circle(self.screen, ORANGE, (int(coin.x * self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2, int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

     def over_events(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.running = False
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 self.reset()
             if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                 self.state = False

     def over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("Game over!", self.screen, [WIDTH//2, 100], 38, RED, "arial", centered=True)
        self.draw_text("Press the escape to QUITE", self.screen, [WIDTH//2, HEIGHT//2], 28, BLUE, "arial", centered=True)
        self.draw_text("Press SPACE to play again", self.screen, [WIDTH//2, HEIGHT//1.5], 38, BLUE, "arial", centered=True)
        pygame.display.update()

     def reset(self):
        self.player.lives = 3
        self.coints = []
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "C":
                        self.coints.append(vec(xidx, yidx))

        self.state = "playing"