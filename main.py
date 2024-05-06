import pygame, sys
from settings import *
from player import Player
from car import Car


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(0, 0)
        self.bg = pygame.image.load('graphics/main/map.png').convert()
        self.fg = pygame.image.load('graphics/main/overlay.png').convert_alpha()

    def customize_draw(self):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)

        display_surface.blit(self.fg, -self.offset)

pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cross the road")

clock = pygame.time.Clock()

# Groups
all_sprites = AllSprites()

# Sprites
player = Player((600, 400), all_sprites)
car = Car((700, 200), all_sprites)

# car timer


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         print("W")

    dt = clock.tick() / 1000

    # draw bg
    display_surface.fill('black')

    all_sprites.update(dt)

    # draw
    # all_sprites.draw(display_surface)
    all_sprites.customize_draw()

    # update surface
    pygame.display.update()


