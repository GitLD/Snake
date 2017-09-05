#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'LuDi'
# Date: 2017/9/5
# Version: 3.0

import random

import os
import pygame


class Snake(object):
    def __init__(self):
        # Check Error
        check_import = pygame.init()
        if check_import[1] != 0:
            print("Warning : Had %d initializing errors ..." % check_import[1])
            exit()
        else:
            print("Pygame initializing successfully!")
        # Create Surface
        self.MainSurface = pygame.display.set_mode((720, 480))
        pygame.display.set_caption('Snake [Version 3.0]')
        icon = pygame.image.load('贪吃蛇.ico')
        pygame.display.set_icon(icon)
        # Set Color
        self.red = pygame.Color(255, 0, 0)  # gameOver
        self.green = pygame.Color(0, 255, 0)  # Snake
        self.black = pygame.Color(0, 0, 0)  # Score
        self.white = pygame.Color(255, 255, 255)  # background
        self.brown = pygame.Color(162, 42, 42)  # food
        # FPS control
        self.fpsController = pygame.time.Clock()
        # Set initial fps
        self.fps = 10
        # Initial Snake Pos
        self.pos_snake = [100, 60]
        self.snake = [[100, 60], [90, 60], [80, 60]]
        # Initial Food Pos
        self.pos_food = []
        self.flag_food = False
        # Initialize the direction
        self.direction = 'RIGHT'
        self.changeTo = self.direction
        # Initial Score
        self.load_score()
        self.score = 0
        # Set the game over flag
        self.flag = False
        # Create food
        self.food_create()
        # Set difficulty level
        self.level = 0
        self.speed = [10, 15, 20, 25, 30]

    def food_create(self):
        while True:
            pos_food_temp = [random.randrange(1, 70) * 10, random.randrange(5, 44) * 10]
            if pos_food_temp not in self.snake:
                self.pos_food = pos_food_temp
                self.flag_food = True
                break

    def keyboard_detect(self):
        # Get Keyboard Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.changeTo = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.changeTo = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.changeTo = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.changeTo = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def direction_change(self):
        # Validate whether to change direction
        if self.changeTo == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if self.changeTo == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if self.changeTo == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if self.changeTo == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def snake_move(self):
        # Move the snake
        # 1.First move the head
        if self.direction == 'RIGHT':
            self.pos_snake[0] += 10
        if self.direction == 'LEFT':
            self.pos_snake[0] -= 10
        if self.direction == 'UP':
            self.pos_snake[1] -= 10
        if self.direction == 'DOWN':
            self.pos_snake[1] += 10
        # 2.Second move the body
        self.snake.insert(0, list(self.pos_snake))
        if self.pos_snake[0] == self.pos_food[0] and self.pos_snake[1] == self.pos_food[1]:
            self.score += 10
            self.flag_food = False
        else:
            self.snake.pop()

    def draw_main(self):
        # Draw the food, snake
        self.MainSurface.fill(self.white)
        pygame.draw.rect(self.MainSurface, self.black, pygame.Rect(10, 50, 700, 400), 0)

        self.show_description()

        self.show_score()

        self.show_level()

        for pos in self.snake:
            pygame.draw.rect(self.MainSurface, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.MainSurface, self.brown, pygame.Rect(self.pos_food[0], self.pos_food[1], 10, 10))

    def is_over(self):
        # Decide whether game is over
        # 1.Outside Judgement
        flag1 = (self.pos_snake[0] > 700) or (self.pos_snake[0] < 10) \
                or (self.pos_snake[1] > 440) or (self.pos_snake[1] < 50)
        # 2.Collision Judgement
        flag2 = self.pos_snake in self.snake[1:]
        self.flag = flag1 or flag2

    def show_score(self, choice=1):
        # Show the score
        font = pygame.font.SysFont('monaco', 24)
        surf1 = font.render('Score : {0}'.format(self.score), True, self.black)
        surf2 = font.render('Best Score : {0}'.format(self.bestScore), True, self.black)
        rect1 = surf1.get_rect()
        rect2 = surf1.get_rect()
        if choice == 1:
            rect1.topleft = (20, 10)
            rect2.topleft = (20, 10+20)
        else:
            rect1.topleft = (300, 150)
            rect2.topleft = (300, 150+20)
        self.MainSurface.blit(surf1, rect1)
        self.MainSurface.blit(surf2, rect2)

    def show_description(self):
        # Show the operation key
        font_dis = pygame.font.SysFont('monaco', 24)
        surf_dis = font_dis.render('Using the arrow to take the control.', True, self.black)
        rect_dis = surf_dis.get_rect()
        rect_dis.topleft = (400, 10)
        self.MainSurface.blit(surf_dis, rect_dis)

    def show_level(self):
        # Show the difficulty level
        font_dis = pygame.font.SysFont('monaco', 24)
        surf_dis = font_dis.render('Level : {0}'.format(self.level + 1), True, self.black)
        rect_dis = surf_dis.get_rect()
        rect_dis.topleft = (400, 10+20)
        self.MainSurface.blit(surf_dis, rect_dis)

    def game_over(self):
        self.MainSurface.fill(self.white)
        myFont1 = pygame.font.SysFont('monaco', 72)
        myFont2 = pygame.font.SysFont('monaco', 32)
        surf1 = myFont1.render('Game Over!', True, self.red)
        surf2 = myFont2.render('Key Space to Restart!', True, self.black)
        rect1 = surf1.get_rect()
        rect2 = surf2.get_rect()
        rect1.midtop = (360, 15)
        rect2.midtop = (360, 400)
        self.MainSurface.blit(surf1, rect1)
        self.MainSurface.blit(surf2, rect2)
        self.show_score(0)
        pygame.display.flip()
        self.save_score()

    def restart(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.flag = False
                    self.__init__()
                else:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def decide_level(self):
        # 判定难度级别
        if len(self.snake) < 10:
            self.level = 0
        elif len(self.snake) < 20:
            self.level = 1
        elif len(self.snake) < 40:
            self.level = 2
        elif len(self.snake) < 50:
            self.level = 3
        elif len(self.snake) > 50:
            self.level = 4

    def save_score(self):
        # Save the best score
        with open("bestscore.ini", "w") as f:
            f.write(str(self.bestScore))

    def load_score(self):
        # load the best score
        if os.path.exists("bestscore.ini"):
            with open("bestscore.ini") as f:
                self.bestScore = int(f.read())
        else:
            self.bestScore = 0

    def run(self):
        # Main Loop
        while True:
            if not self.flag:
                # Get Keyboard Event
                self.keyboard_detect()

                # Validate whether to change direction
                self.direction_change()

                # Move the snake
                self.snake_move()

                # if food None, crate food
                if not self.flag_food:
                    self.food_create()

                # Renew Score
                if self.score > self.bestScore:
                    self.bestScore = self.score

                # Draw the food, snake
                self.draw_main()

                # Refresh the window
                pygame.display.flip()
                # Cntrol FPS
                self.decide_level()
                self.fpsController.tick(self.speed[self.level])

                # Judge Over
                self.is_over()
                if self.flag:
                    self.game_over()
            else:
                # Restart the game
                self.restart()


if __name__ == '__main__':
    snake_app = Snake()
    snake_app.run()
