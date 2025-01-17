from constants import *
import pygame

import snake, apple, ai

clock = pygame.time.Clock()
surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

pygame.init()


input_shape = 20
num_actions = 4


snake = snake.Snake()
apple = apple.Apple()
ai = ai.AI(input_shape, num_actions)


train_interval = 5  # Train every 5 cycles
frame_counter = 0  # To track frames



def main():
    running = True

    while running:

        clock.tick(TICK_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_r:
                    board.reset()
                if event.key == pygame.K_q:
                    running = False

        draw()
        if frame_counter % train_interval == 0:
            update()  # AI will train only every `train_interval` cycles

    pygame.quit()



def draw():
    surface.fill((0, 0, 0))#background

    snake.draw(surface)
    apple.draw(surface)
    pygame.display.flip()



def update():
    # snake.update(apple)
    ai.train(snake, apple)


if __name__ == "__main__":
    main()
