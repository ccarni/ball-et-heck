import pygame
import math
import numpy as np
import globals


class Springy_Enemy(pygame.sprite.Sprite):
    def __init__(self, radius, screen, player, pos=(0, 0), hitpoints=3, score_multiplier=1):
        pygame.sprite.Sprite.__init__(self)
        #sprite stuff
        self.radius = radius
        self.image = pygame.surface.Surface((2 * radius, 2 * radius))
        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, (217, 2, 125), self.image.get_rect())

        #other
        self.hitpoints = hitpoints
        center_x = self.image.get_rect().centerx
        center_y = self.image.get_rect().centery

        #eyebrows
        pygame.draw.line(self.image, (255,255, 255), (center_x, center_y - 10), (center_x * 2, 0), 5)
        pygame.draw.line(self.image, (255, 255, 255), (center_x, center_y - 10), (0, 0), 5)

        #eyes
        pygame.draw.circle(self.image, (255, 255, 255), (center_x - 10, center_y), 5)
        pygame.draw.circle(self.image, (255, 255, 255), (center_x + 10, center_y), 5)

        #frown
        frown_rect = pygame.rect.Rect(center_x - 10, center_y + 5, 20, 20)
        pygame.draw.arc(self.image, (255, 255, 255), frown_rect, 0, math.pi, 2)
        #colorkey so there's no background box
        self.image.set_colorkey((0, 0, 0))

        #position stuff
        self.x = self.image.get_rect().centerx
        self.y = self.image.get_rect().centery
        self.original_position = (pos[0] + 50, pos[1] + 50)



        #hello world welcome to our great game ball-et heck

        self.rect = self.image.get_rect()
        self.rect.center = pos
        screen_center = np.array([screen.get_width() * 0.5, screen.get_height() * 0.5])
        position = np.array(pos)

        #------------ physics stuff --------------
        # spring force
        self.k = 10
        self.rest_length = 500
        #velocity
        self.v = 10 * (screen_center - position) / np.linalg.norm(screen_center - position)
        self.density = 1
        self.mass = math.pi * radius * radius * self.density
        self.score_multiplier = score_multiplier

    def update(self, bounds):
        #distance to spring using pythagorean theorem
        distance = math.sqrt((self.rect.center[0] - self.original_position[0]) ** 2 + (
                    self.rect.center[1] - self.original_position[1]) ** 2)
        #how far spring has been stretched
        displacement = self.rest_length - distance
        spring_force = -self.k * displacement / self.mass

        #make the velocity in the right direction (should be different if enemy is on different side of spring
        if displacement < 0:
            # make a vector from the enemy to the spring based off spring force and other fancy math
            to_spring = -(np.array(self.rect.center) - np.array(self.original_position)) / (
                    np.linalg.norm(np.array(self.rect.center)
                                   - np.array(self.original_position))) * spring_force
        else:
            # make a vector from the enemy to the spring based off spring force and other fancy math
            to_spring = (np.array(self.rect.center) - np.array(self.original_position)) / (
                np.linalg.norm(np.array(self.rect.center)
                               - np.array(self.original_position))) * spring_force

        #add acceleration to velocity
        self.v[0] += to_spring[0]
        self.v[1] += to_spring[1]

        #add velocity to position (move the enemy)
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        #check hp and delete
        if self.hitpoints <= 0:
            globals.score += 10 * self.score_multiplier
            self.kill()
            del self
        else:
        #check boundries
            #left
            if self.rect.left < bounds.left:
                self.rect.left = bounds.left
                self.v[0] *= -1
            # top
            if self.rect.top < bounds.top:
                self.rect.top = bounds.top
                self.v[1] *= -1
            # right
            if self.rect.right > bounds.right:
                self.rect.right = bounds.right
                self.v[0] *= -1
            # bottom
            if self.rect.bottom > bounds.bottom:
                self.rect.bottom = bounds.bottom
                self.v[1] *= -1



