import pygame
from constants import *


class Snake(object):
    """docstring for Snake."""

    def __init__(self):
        super(Snake, self).__init__()
        self.x = (GRID_SIZE // 2) * BLOCK_SIZE
        self.y = (GRID_SIZE // 2) * BLOCK_SIZE
        self.score = 0
        self.body = []
        self.dir = 1
        self.update_interval = 250
        self.last_update_time = 0
        self.can_update = False
        self.border = 4
        self.grow = False
        self.apple = None

    def update(self, apple):
        self.apple = apple
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.update_interval:
            self.can_update = True
            self.last_update_time = current_time
        else:
            self.can_update = False


        # self.key_handler()

        # if self.can_update:
        self.movment()

        self.collide_apple(apple)

        self.check_body_collide()
        self.bounds_check()






    def collide_apple(self, apple):
        if self.x == apple.x and self.y == apple.y:
            self.score += 1
            self.grow = True
            apple.new_loc()


    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
        for bod in self.body:
            pygame.draw.rect(surface, (0, 200, 0), (bod[0], bod[1], BLOCK_SIZE, BLOCK_SIZE))



    def movment(self):
        prev_pos = (self.x, self.y)
        if self.dir == 0:
            self.y -= BLOCK_SIZE
        if self.dir == 1:
            self.x += BLOCK_SIZE
        if self.dir == 2:
            self.y += BLOCK_SIZE
        if self.dir == 3:
            self.x -= BLOCK_SIZE
        self.body.insert(0, prev_pos)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()


    def check_body_collide(self):
        current_pos = (self.x, self.y)
        if current_pos in self.body:
            self.reset()



    def bounds_check(self):
        if self.x < 0 or self.x + BLOCK_SIZE > GAME_WIDTH or self.y < 0 or self.y + BLOCK_SIZE > GAME_WIDTH:
            self.reset()



    def reset(self):
        score = self.score
        self.x = (GRID_SIZE // 2) * BLOCK_SIZE
        self.y = (GRID_SIZE // 2) * BLOCK_SIZE
        self.body = []
        self.dir = 0
        self.score = 0
        return score


    def key_handler(self, input):
        print(f"input:{input}")
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or input == 0:
            if self.dir != 2:
                self.dir = 0
        if keys[pygame.K_RIGHT] or input == 1:
            if self.dir != 3:
                self.dir = 1
        if keys[pygame.K_DOWN] or input == 2:
            if self.dir != 0:
                self.dir = 2
        if keys[pygame.K_LEFT] or input == 3:
            if self.dir != 1:
                self.dir = 3

    def get_state(self):
        return {
            x: self.x,
            y: self.y,
            body: self.body,
            apple: self.apple,
            score: self.score,
        }
