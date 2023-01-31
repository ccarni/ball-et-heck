import pygame
import runner

#this is needed since the game stops when you die
while True:
    pygame.init()
    runner_instance = runner.Runner()

    #run the game
    while runner_instance.running:
        runner_instance.update()
        runner_instance.draw()
