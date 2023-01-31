import pygame
import random
import sys
import ball
import enemy
import springy_enemy
import numpy as np
import player
import globals
import math
import time


class Runner():
    def __init__(self):
        # screen and stuff
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.background_color = (40, 40, 40)
        self.img = pygame.transform.smoothscale(pygame.image.load('title.png').convert_alpha(), self.screen.get_size())
        self.dead = False
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # setup enemies, players, and balls
        self.balls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_instance = player.Player((255, 255, 255), 10, pos=(self.screen_width / 2, self.screen_height / 2))
        self.enemy_timer = 0
        self.boss_timer = 0
        self.enemy_req = 20
        self.players = pygame.sprite.Group()
        self.players.add(self.player_instance)

        self.font = pygame.font.Font(None, 40)

        # list of bosses I guess
        self.boss_list = [self.create_boss_big, self.create_boss_small, self.create_boss_springy]
        self.running = True

        #setting up auto shooting timer
        self.shot_cooldown = 0
        self.auto_shoot_frames = 2

        # backstory
        text_array = ['once upon a time there was a old dragon who built itself a tomb.',
                      'to protect his remains and his vast treasure hoard he summoned four balls to guard his tomb.',
                      'once he was laid to rest three of the balls decided to betrayed the old dragon and began summoning more balls.',
                      'but one ball decided to learn the dragons magic and began learning to cast energy balls.',
                      'one day a foolish adventurer opened the tomb and the balls began to escape the three balls rejoiced.',
                      'but the last ball cast a spell blocking the gate and funneling all escapees to  it.',
                      'then it began its final stand.',
                      'you are that ball.']
        self.text = random.choice(text_array)

        # frames per second
        self.FPS = 30
        # clock
        self.clock = pygame.time.Clock()

    def create_boss_big(self, pos=None):
        color = [random.randint(0, 255) for j in range(3)]
        radius = random.randint(50, 50)
        p = np.array(pos)
        b = enemy.Enemy(radius, self.screen, list(self.players)[0], p, 25, 5)
        self.enemies.add(b)

    def create_boss_small(self, pos=None):
        color = [random.randint(0, 255) for j in range(3)]
        radius = random.randint(5, 5)
        p = np.array(pos)
        b = enemy.Enemy(radius, self.screen, list(self.players)[0], p, 3, 5)
        self.enemies.add(b)

    def create_boss_springy(self, pos=None):
        color = [random.randint(0, 255) for j in range(3)]
        radius = random.randint(30, 30)
        p = np.array(pos)
        b = springy_enemy.Springy_Enemy(radius, self.screen, list(self.players)[0], p, 55, 5)
        self.enemies.add(b)

    def create_ball(self, mouse_pos=None, player_pos=[0,0]):
        # use this for random color
        # color = [random.randint(0, 255) for j in range(3)]
        color = [0, 175, 0]
        radius = random.randint(10, 10)
        p = np.array(mouse_pos)
        position = np.array(player_pos)
        velocity = 10 * (p - position) / np.linalg.norm(p - position)
        b = ball.Ball(color, radius, position, velocity, lifetime=200)
        self.balls.add(b)

    def create_enemy(self, pos=None):
        color = [random.randint(0, 255) for j in range(3)]
        radius = random.randint(20, 20)
        p = np.array(pos)
        e = enemy.Enemy(radius, self.screen, list(self.players)[0], p, 5, 1)
        self.enemies.add(e)

    def update_score(self):
        surf = self.font.render(f'Score: {str(globals.score)}', True, (255, 255, 255))
        x = 20
        y = 20
        self.screen.blit(surf, (x, y))

    def update(self):
        # inputs + check before returning so game no crash :)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    globals.score = 0
                    self.running = False

        if self.dead: return
        self.clock.tick(self.FPS)
        space_down = False
        mouse_pos = pygame.mouse.get_pos()
        player_dir = [0, 0]

        # input stuff
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_e] or mouse[0]:
            space_down = True
        if keys[pygame.K_w]:
            player_dir[1] -= 1
        if keys[pygame.K_s]:
            player_dir[1] += 1
        if keys[pygame.K_a]:
            player_dir[0] -= 1
        if keys[pygame.K_d]:
            player_dir[0] += 1

        for player_ in self.players:
            player_.set_dir(player_dir)

        #auto shooting timer
        self.shot_cooldown += 1
        if space_down and self.shot_cooldown > 2:
            self.create_ball(mouse_pos, list(self.players)[0].pos)
            self.shot_cooldown = 0

        # boss/enemy timer
        self.enemy_timer += 1
        self.boss_timer += 1

        #check the timers
        if self.enemy_timer > self.enemy_req:
            self.enemy_timer = 0
            self.enemy_req -= 0.05
            if self.enemy_req < 5: self.enemy_req = 5

            #if the enemy timer is done randomly spawn an enemy
            random_x = random.randint(0, self.screen_width)
            random_y = random.randint(0, self.screen_height)

            #check if pos is good
            distance = math.dist((random_x, random_y), self.player_instance.pos)
            while not(300 < distance < 500):
                random_x = random.randint(0, self.screen_width)
                random_y = random.randint(0, self.screen_height)
                distance = math.dist((random_x, random_y), self.player_instance.pos)


            #if the boss tier is done spawn a boss
            if self.boss_timer > 100:
                random_boss = random.choice(self.boss_list)
                random_boss((random_x, random_y))
                self.boss_timer = 0
            else:
                self.create_enemy((random_x, random_y))

        #update balls
        self.balls.update(bounds=self.screen.get_rect())
        self.players.update(bounds=self.screen.get_rect())

        # ------------------------------------------ ball-ball collision ---------------------------------------

        collided = pygame.sprite.groupcollide(self.balls, self.balls, False, False, ball.ball_ball_collision)

        for collide1 in collided.keys():
            for collide2 in collided[collide1]:
                ball.elastic_collision(collide1, collide2)
                collided[collide2].remove(collide1)

        self.enemies.update(self.screen.get_rect())

        # --------------------------------------- enemy-enemy collision =--------------------------------------

        collided = pygame.sprite.groupcollide(self.enemies, self.enemies, False, False, ball.ball_ball_collision)

        for collide1 in collided.keys():
            for collide2 in collided[collide1]:
                ball.elastic_collision(collide1, collide2)
                collided[collide2].remove(collide1)

        # --------------------------------------------- ball-enemy collision -------------------------------------

        collided = pygame.sprite.groupcollide(self.enemies, self.balls, False, False, ball.ball_ball_collision)

        for collide1 in collided.keys():
            for collide2 in collided[collide1]:
                ball.elastic_collision(collide1, collide2, True)

        # ------------------------------------------------player-enemy collision ----------------------
        collided = pygame.sprite.groupcollide(self.players, self.enemies, False, False, ball.ball_ball_collision)
        for collide1 in collided.keys():
            for collide2 in collided[collide1]:
                self.dead = True

    def draw(self):
        if self.dead:
            #draw dead screen
            self.screen.fill((0, 0, 0))
            surf = self.font.render('NO', True, (255, 255, 255))
            surf2 = self.font.render('R to Reset', True, (255, 255, 255))
            score = self.font.render(f'Score: {str(globals.score)}', True, (255, 255, 255))
            big_size = self.screen.get_size()
            text_size = surf.get_size()
            x = big_size[0] / 2 - text_size[0] / 2
            y = big_size[1] / 2 - text_size[1] / 2
            self.screen.blit(surf, (x, y))
            self.screen.blit(surf2, (x, y - text_size[1]))
            self.screen.blit(score, (x, y - text_size[1] * 2))
            self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (100, 0))
        else:
            #draw the normal game
            self.screen.fill(self.background_color)
            self.screen.blit(self.img, (0, 0))
            self.update_score()
            self.balls.draw(self.screen)
            self.enemies.draw(self.screen)
            self.player_instance.draw(self.screen)

        pygame.display.update()
