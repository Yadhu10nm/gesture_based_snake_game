import pygame
import random
import sys

pygame.init()

WIDTH=900
HEIGHT=600
cell=30
display=pygame.display.set_mode((WIDTH,HEIGHT))  #for creating a screen
clock=pygame.time.Clock()
is_eaten=False
score=0
game_over=False


class Snake:
    def __init__(self):
        self.x=150
        self.y=150
        self.body=[pygame.Rect(self.x,self.y,cell,cell)]
        self.direction='none'

    def draw_snake(self):
        for block in self.body:
            pygame.draw.rect(display,'green',block,0)

    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction = 'right'

    def move_down(self):
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'

    def move(self):
        if self.direction=='right':
            self.x+=cell
        if self.direction=='left':
            self.x-=cell
        if self.direction=='up':
            self.y-=cell
        if self.direction=='down':
            self.y+=cell
        self.update_snake()

    def update_snake(self):
        self.body.append(pygame.Rect(self.x,self.y,cell,cell))
        self.head=self.body[-1]
        pygame.draw.rect(display, 'red', self.head)
        self.tail=self.body[0]
        pygame.draw.rect(display, 'white', self.tail)

    def is_dead(self):
        global game_over
        for block in self.body[1:]:
            if block.colliderect(snake.body[0]):
                game_over=True
        if self.x<0 or self.x>WIDTH:
            game_over=True
        if self.y<0 or self.y>HEIGHT:
            game_over=True



class Fruit:
    def __init__(self):
        self.x=(random.randint(0,WIDTH)//cell)*30
        self.y=(random.randint(0,HEIGHT)//cell)*30
    def draw_fruit(self):
        colors = [
            "#ADD8E6","#F08080","#E0FFFF","#F8C8DC","#FFB6C1",
            "#FFA07A", "#20B2AA","#87CEFA","#8470FF","#B0C4DE","#B39EB5","#E6E6FA",
            "#FF77FF","#FFDAB9","#FFA500","#FFCCCC","#DDA0DD","#FF7F7F",
            "#EE82EE",  "#AFEEEE", "#FF6347","#8B0000", "#8B008B", "#556B2F", "#8B4513",
            "#A52A2A", "#9932CC", "#483D8B", "#2F4F4F", "#6B8E23", "#9400D3", "#800000",
            "#B22222", "#5F9EA0", "#CD5C5C", "#8A2BE2",
            "#A0522D", "#D2691E", "#C71585", "#7B68EE", "#6A5ACD"
        ]

        self.body=pygame.Rect(self.x,self.y,cell,cell)
        pygame.draw.rect(display,random.choice(colors),self.body)

    def get_random_pos(self):
        self.x = (random.randint(0, WIDTH) // cell) * 30
        self.y = (random.randint(0, HEIGHT) // cell) * 30

snake = Snake()
fruit=Fruit()

 #size of a cell in the grid
def draw_grids():
    for x in range(0,WIDTH,cell):
        for y in range(0,HEIGHT,cell):
            rect=pygame.Rect(x,y,cell,cell)
            pygame.draw.rect(display,'black',rect,1)

def display_score():
    font=pygame.font.SysFont('Tlwg Tyist',40)
    score_font=font.render(f"SCORE {score}",True,'red')
    font_pos = score_font.get_rect(center=((WIDTH // 2) - 30, 30))
    display.blit(score_font,font_pos)

def end_screen():
     bg=pygame.image.load('game_over.png')
     display.blit(bg,(-120,-120))

game_close=False
while not game_close:
    for event in pygame.event.get():  #event is a like a user interaction like mouse click
        if event.type ==pygame.QUIT:
            game_close=True
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT and snake.direction!='right':
                snake.move_left()
            if event.key==pygame.K_RIGHT and snake.direction!='left':
                snake.move_right()
            if event.key==pygame.K_UP and snake.direction!='down':
                snake.move_up()
            if event.key==pygame.K_DOWN and snake.direction!='up':
                snake.move_down()

    display.fill((0,0,0))
    draw_grids()
    snake.draw_snake()
    snake.move()
    fruit.draw_fruit()
    display_score()

    if(snake.head.colliderect(fruit.body)):
        is_eaten=True
        score+=1
        print(score)
    else:
        snake.body.pop(0)
    if is_eaten:
        fruit.get_random_pos()
        is_eaten=False
    snake.is_dead()
    if game_over:
        end_screen()

    pygame.display.update()
    clock.tick(7)
