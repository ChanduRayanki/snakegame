import pygame as pg
from pygame.math import Vector2
import random
import sys

pg.init()
title_font = pg.font.Font(None,60)
score_font = pg.font.Font(None, 50)
GREEN = (255, 192, 203)
DARK_GREEN = (43,51,24)
cell_size = 30
number_of_cells = 25
OFFSET = 75
screen = pg.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET+cell_size*number_of_cells))
class Food:
    def __init__(self,snake_body):
        self.position = self.genrandom_pos(snake_body)
    def draw(self,color):
        food_rect = pg.Rect(OFFSET+self.position.x * cell_size, OFFSET+self.position.y * cell_size,cell_size,cell_size)
        pg.draw.rect(screen,color,food_rect,0,7)
        #screen.blit(food_surface,food_rect)
    def genrandom_cell(self):
        x = random.randint(0,number_of_cells-1)
        y= random.randint(0,number_of_cells-1)
        return Vector2(x,y)
    def genrandom_pos(self,snake_body):
        position = self.genrandom_cell()
        while position in snake_body:
            position = self.genrandom_cell()
        return position


class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False
    def draw(self,color):
        for segment in self.body:
            segment_rect = (OFFSET+segment.x * cell_size, OFFSET+segment.y*cell_size, cell_size, cell_size)
            pg.draw.rect(screen,color, segment_rect,0,7)
    def update(self):
        self.body.insert(0,self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]  
    def edge_x(self):
        if self.body[0].x < 0:
            self.body[0] = Vector2(number_of_cells-1, self.body[0].y)
        elif self.body[0].x > number_of_cells-1:
            self.body[0] = Vector2(0, self.body[0].y)

    def edge_y(self):
        if self.body[0].y < 0:
            self.body[0] = Vector2(self.body[0].x, number_of_cells-1)
        elif self.body[0].y > number_of_cells-1:
            self.body[0] = Vector2(self.body[0].x, 0)
    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
    def draw(self):
        self.food.draw(DARK_GREEN)
        self.snake.draw(DARK_GREEN)
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_body()
    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.score = self.score +1
            self.snake.add_segment= True
            self.food.position = self.food.genrandom_pos(self.snake.body)
    
    def check_collision_with_edges(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x > number_of_cells-1:
            self.snake.edge_x()
        if self.snake.body[0].y < 0 or self.snake.body[0].y > number_of_cells-1:
            self.snake.edge_y()
    
    def check_collision_with_body(self):
        body = self.snake.body[1:]
        if self.snake.body[0] in body:
            self.gameover()
    
    def flash(self):
       flashcolor = (173,204,96)
       original_food = DARK_GREEN
       original_snake = DARK_GREEN
       for i in range(3):
        self.food.draw(flashcolor)
        self.snake.draw(flashcolor)
        pg.display.update()
        pg.time.wait(100)
        self.snake.draw(original_snake)
        self.food.draw(original_food)

        # Update the display again
        pg.display.update()

        # Wait for a short period of time
        pg.time.wait(100)


    def gameover(self):
        #self.flash()
        self.food.position = self.food.genrandom_pos(self.snake.body)
        self.state = "STOPPED"
        self.flash()
        self.score = 0
        self.snake.reset()
pg.display.set_caption("Retro Snake")
clock = pg.time.Clock()
game = Game()
food_surface = pg.image.load('graphics/plus_30.png')
SNAKE_UPDATE = pg.USEREVENT
pg.time.set_timer(SNAKE_UPDATE,100)

while True:
    for event in pg.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pg.K_UP and game.snake.direction!=Vector2(0,1):
                game.snake.direction= Vector2(0,-1)
            if event.key == pg.K_DOWN and game.snake.direction!=Vector2(0,-1):
                game.snake.direction= Vector2(0,1)
            if event.key == pg.K_RIGHT and game.snake.direction!=Vector2(-1,0):
                game.snake.direction= Vector2(1,0)
            if event.key == pg.K_LEFT and game.snake.direction!=Vector2(1,0):
                game.snake.direction= Vector2(-1,0)
    
    screen.fill(GREEN)
    pg.draw.rect(screen, DARK_GREEN,(OFFSET-5,OFFSET-5,cell_size*number_of_cells+10,cell_size*number_of_cells+10),5)
    game.draw()
    title_surface = title_font.render("Snake Game",True,DARK_GREEN)
    score_surface = score_font.render(str(game.score),True,DARK_GREEN)
    screen.blit(title_surface,(OFFSET-5,20))
    screen.blit(score_surface,((cell_size*number_of_cells), 20))
    pg.display.update()
    clock.tick(60)