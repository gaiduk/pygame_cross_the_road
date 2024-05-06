import pygame, sys
from settings import *
from player import Player
from car import Car
from random import choice, randint
from sprites_assets import SimpleSprite, LongSprite


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
is_game_over = False

# Groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# Sprites
player = Player((2063, 3420), all_sprites, obstacle_sprites)

# car timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 70)
pos_list = []

font = pygame.font.Font(None, 47)
text_surf = font.render("*** YOU WIN ***", True, "white")
text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

lose_text_surf = font.render("*** GAME OVER ***", True, "white")
lose_text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

music = pygame.mixer.Sound("audio/music.mp3")
music.play(loops=-1)

# setup aditional sprites
for file_name, position_list in SIMPLE_OBJECTS.items():
    path = f'graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()

    for pos in position_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

for file_name, position_list in LONG_OBJECTS.items():
    path = f'graphics/objects/long/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()

    for pos in position_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-7, 7))
                Car(pos, [all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         print("W")

    dt = clock.tick() / 1000

    # draw bg
    display_surface.fill('black')

    if player.is_game_over:
        display_surface.fill('gray')
        display_surface.blit(lose_text_surf, lose_text_rect)

    # Win logic
    elif player.pos.y > 1180:

        all_sprites.update(dt)

        # draw
        # all_sprites.draw(display_surface)
        all_sprites.customize_draw()
    else:
        display_surface.fill('teal')
        display_surface.blit(text_surf, text_rect)

    # update surface
    pygame.display.update()


