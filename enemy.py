import pygame
import math
import numpy as np
import globals


class Enemy(pygame.sprite.Sprite):
    def __init__(self, radius, screen, player, pos=(0, 0), hitpoints = 3, score_multiplier=1):

        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pygame.surface.Surface((2 * radius, 2 * radius))
        self.image.fill((0, 0, 0))
        self.hitpoints = hitpoints

        # positions and rects
        center_x = self.image.get_rect().centerx
        center_y = self.image.get_rect().centery
        self.x = self.image.get_rect().centerx
        self.y = self.image.get_rect().centery
        self.rect = self.image.get_rect()
        self.rect.center = pos
        screen_center = np.array([screen.get_width() * 0.5, screen.get_height() * 0.5])
        position = np.array(pos)

        # physics/movement stuff
        self.speed = 8
        self.v = self.speed * (screen_center - position) / np.linalg.norm(screen_center - position)
        self.density = 1
        self.mass = math.pi * radius * radius * self.density
        self.score_multiplier = score_multiplier

        #main player circle
        pygame.draw.ellipse(self.image, (217, 2, 125), self.image.get_rect())

        #eyebrows
        pygame.draw.line(self.image, (219, 219, 72), (center_x, center_y - 10), (center_x * 2, 0), 5)
        pygame.draw.line(self.image, (219, 219, 72), (center_x, center_y - 10), (0, 0), 5)
        #eyes
        pygame.draw.circle(self.image, (219, 219, 72), (center_x - 10, center_y), 5)
        pygame.draw.circle(self.image, (219, 219, 72), (center_x + 10, center_y), 5)
        #frown
        frown_rect = pygame.rect.Rect(center_x - 10, center_y + 5, 20, 20)
        pygame.draw.arc(self.image, (219, 219, 72), frown_rect, 0, math.pi, 2)
        #colorkeying so that there's no background
        self.image.set_colorkey((0, 0, 0))

        #hello world welcome to our great game ball-et heck
        self.player = player

    def update(self, bounds):
        #update velocity to point to player
        self.v = self.speed * (self.player.pos - np.array(list(self.rect.center))) /\
                 (np.linalg.norm(self.player.pos - np.array(list(self.rect.center))))
        #move the enemy
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        #check hitpoints and die
        if self.hitpoints <= 0:
            globals.score += 10 * self.score_multiplier
            self.kill()
            del self
        else:
        #check boundry collisions ----------------------
        #left
            if self.rect.left < bounds.left:
                self.rect.left = bounds.left
                self.v[0] *= -1
        #top
            if self.rect.top < bounds.top:
                self.rect.top = bounds.top
                self.v[1] *= -1
        #right
            if self.rect.right > bounds.right:
                self.rect.right = bounds.right
                self.v[0] *= -1
        #bottom
            if self.rect.bottom > bounds.bottom:
                self.rect.bottom = bounds.bottom
                self.v[1] *= -1


