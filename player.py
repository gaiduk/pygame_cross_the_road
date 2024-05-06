import pygame
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.import_assets()

        self.frame_index = 0
        self.status = 'up'
        self.image = self.animationss[self.status][self.frame_index]

        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 205

    def import_assets(self):
        # self.animations = [pygame.image.load(f'graphics/player/right/{frame}.png').convert_alpha() for frame in
        #                    range(4)]
        # for frame in range(4):
        #     surf = pygame.image.load(f'graphics/player/right/{frame}.png').convert_alpha()
        #     self.animations.append(surf)

        # better import
        self.animationss = {}
        for index, folder in enumerate(walk("graphics/player")):
            if index == 0:
                for name in folder[1]:
                    self.animationss[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animationss[key].append(surf)
        print(self.animationss)

    def move(self, dt):
        # normalize vector (по діагоналі без цього швидкість бідьша ніж по прямій)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def animate(self, dt):
        current_animation = self.animationss[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 7 * dt
            if self.frame_index > len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        elif keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
