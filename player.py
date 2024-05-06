import pygame
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.import_assets()

        self.frame_index = 0
        self.status = 'up'
        self.image = self.animationss[self.status][self.frame_index]

        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 205
        self.is_game_over = False

        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)

    def collision(self, direction):
        # pygame.sprite.spritecollide(self, self.collision_sprites, True)
        if direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        self.is_game_over = True
                    if self.direction.x > 0:  # we moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                else:
                    pass
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        self.is_game_over = True
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                else:
                    pass

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

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

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

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560

        if self.rect.bottom > 3499:
            self.pos.y = 3499 - self.rect.height /2
            self.rect.bottom = 3499
            self.hitbox.centery = self.rect.centery



    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
