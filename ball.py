import pygame
import math
import numpy as np
import enemy

def ball_ball_collision(ball1, ball2):
    #please dont do collisions for the same 2 balls
    if ball1 == ball2:
        return False

    #variable setup
    r1 = ball1.rect.width/2
    r2 = ball2.rect.width/2

    x1, y1 = ball1.rect.center
    x2, y2 = ball2.rect.center

    #calculate distance and compare to radii to check collision
    if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < r1 + r2:
        return True
    return False


def elastic_collision(ball1, ball2, ball_enemy=False):
    # variable setup
    m1 = ball1.mass
    m2 = ball2.mass
    v1 = ball1.v
    v2 = ball2.v
    x1 = np.array(ball1.rect.center)
    x2 = np.array(ball2.rect.center)
    n = (x1 - x2) / np.linalg.norm(x1 - x2)

    r1 = ball1.rect.width / 2
    r2 = ball2.rect.width / 2
    dist = r1 + r2 - np.linalg.norm(x1 - x2)
    v1_dir = np.dot(v1, n)
    v2_dir = np.dot(v2, n)

    # fix getting stuck inside each other
    ball1.rect.center = x1 + n * dist * abs(v1_dir) / (abs(v1_dir) * abs(v2_dir))
    ball2.rect.center = x2 - n * dist * abs(v2_dir) / (abs(v1_dir) * abs(v2_dir))

    # implementing velocities
    ball1.v = v1 + (2 * m2) / (m1 + m2) * np.dot((v2 - v1), n) * n
    ball2.v = v2 + (2 * m1) / (m1 + m2) * np.dot((v1 - v2), n) * n

    #if we know that the ball is colliding with an enemy we can treat it this way and change the hp
    if ball_enemy:
        if type(ball1) != Ball:
            ball1.hitpoints -= 1
        if type(ball2) != Ball:
            ball2.hitpoints -= 1


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, pos=(0, 0), v=(0,0), lifetime=300):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius

        #sprite stiff
        self.image = pygame.surface.Surface((2*radius, 2*radius))
        self.image.fill((0, 0, 0))
        self.color = color
        pygame.draw.ellipse(self.image, self.color, self.image.get_rect())
        self.image.set_colorkey((0,0,0))

        #yes
        self.lifetime = lifetime

        #rect stuff
        self.rect = self.image.get_rect()
        self.rect.center = pos

        #physics and mvmnt stuff
        self.v = np.array(v)
        self.density = 1
        self.mass = math.pi*radius*radius*self.density

    def update(self, bounds):
        #kill if over lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            del self
            return

        #move the ball
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        #---------- boundry check ---------------     nyoooom
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
        #botttttttom
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.v[1] *= -1
