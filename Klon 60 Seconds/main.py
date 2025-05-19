import pygame
import sys
import os
from settings import *
from game import Game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("60 Seconds Clone")
clock = pygame.time.Clock()

os.makedirs("assets/data", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

def main():
    game = Game(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        game.update()
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
