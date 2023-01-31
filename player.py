import numpy as np
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, color, radius, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((2 * radius, 2 * radius))
        # rects and positions
        self.pos = np.array(list(pos))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = radius

        # physics and movement
        self.density = 1
        self.mass = math.pi * radius * radius * self.density
        self.dir = [0, 0]
        self.speed = 7

        #sprite stuff
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.ellipse(self.image, color, self.image.get_rect())

    def set_dir(self, dir):
        self.dir = dir

    def update(self, bounds):
        #move player
        self.rect.x += self.dir[0] * self.speed
        self.rect.y += self.dir[1] * self.speed

        #--------------- check boundries ------------------
        #left
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.rect.x -= self.dir[0]
        #top
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.rect.y -= self.dir[1]
        #right
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.rect.x -= self.dir[0]
        #down
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.rect.y -= self.dir[1]

        #update position
        self.pos = np.array(self.rect.center)

    def draw(self, screen):
        pygame.draw.circle(screen, (29, 218, 26), self.rect.topleft, 20)
