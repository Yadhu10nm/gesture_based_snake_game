import cv2
import pygame
import random
import cv2 as cv
import mediapipe.python.solutions.hands as mpHands
import mediapipe.python.solutions.drawing_utils as drawing
import numpy as np

# -------------------- INIT --------------------
pygame.init()
pygame.display.set_mode((1, 1))  # hidden pygame window (important)

WIDTH, HEIGHT = 1200, 1200
cell = 30
display = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

score = 0
game_over = False

# -------------------- CLASSES --------------------
class Snake:
    def __init__(self):
        self.x = 150
        self.y = 150
        self.body = [pygame.Rect(self.x, self.y, cell, cell)]
        self.direction = 'right'

    def draw(self):
        for block in self.body:
            pygame.draw.rect(display, (0, 255, 0), block)

    def move(self):
        if self.direction == 'right': self.x += cell
        if self.direction == 'left': self.x -= cell
        if self.direction == 'up': self.y -= cell
        if self.direction == 'down': self.y += cell

        self.body.append(pygame.Rect(self.x, self.y, cell, cell))
        self.head = self.body[-1]

    def check_dead(self):
        global game_over
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            game_over = True
        for block in self.body[:-1]:
            if block.colliderect(self.head):
                game_over = True


class Fruit:
    def __init__(self):
        self.random_pos()

    def random_pos(self):
        self.x = random.randrange(0, WIDTH, cell)
        self.y = random.randrange(0, HEIGHT, cell)

    def draw(self):
        self.body = pygame.Rect(self.x, self.y, cell, cell)
        pygame.draw.rect(display, (255, 0, 0), self.body)

# -------------------- FUNCTIONS --------------------
def draw_grid():
    for x in range(0, WIDTH, cell):
        for y in range(0, HEIGHT, cell):
            pygame.draw.rect(display, (40, 40, 40), (x, y, cell, cell), 1)

def draw_score():
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render(f"SCORE : {score}", True, (255, 255, 255))
    display.blit(txt, (WIDTH // 2 - 100, 10))

def draw_wait_text():
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("Show your hand to start", True, (255, 255, 0))
    display.blit(txt, (WIDTH // 2 - 220, HEIGHT // 2))

# -------------------- OBJECTS --------------------
snake = Snake()
fruit = Fruit()

# -------------------- HAND TRACKING --------------------
hands = mpHands.Hands(max_num_hands=1)
cam = cv.VideoCapture(0)
prev_x, prev_y = 0, 0

# -------------------- MAIN LOOP --------------------
while True:
    success, frame = cam.read()
    if not success:
        break

    frame = cv.flip(frame, 1)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb)

    hand_detected = False
    cx, cy = prev_x, prev_y

    if result.multi_hand_landmarks:
        hand_detected = True
        for hand in result.multi_hand_landmarks:
            drawing.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            tip = hand.landmark[8]
            cx, cy = int(tip.x * w), int(tip.y * h)
            cv2.circle(frame , (cx,cy) , 3 , (255, 0 ,) , 2)

    if hand_detected:
        dx, dy = cx - prev_x, cy - prev_y

        if abs(dx) > abs(dy):
            if dx > 20 and snake.direction != 'left':
                snake.direction = 'right'
            elif dx < -20 and snake.direction != 'right':
                snake.direction = 'left'
        else:
            if dy > 20 and snake.direction != 'up':
                snake.direction = 'down'
            elif dy < -20 and snake.direction != 'down':
                snake.direction = 'up'

        prev_x, prev_y = cx, cy

    # -------- GAME DRAW --------
    display.fill((0, 0, 0))
    draw_grid()
    snake.draw()
    fruit.draw()
    draw_score()

    if hand_detected:
        snake.move()

        if snake.head.colliderect(fruit.body):
            score += 1
            fruit.random_pos()
        else:
            snake.body.pop(0)

        snake.check_dead()
        if game_over:
            break
    else:
        draw_wait_text()

    # -------- PYGAME → OPENCV (CORRECT ORIENTATION) --------
    game_frame = pygame.surfarray.array3d(display)
    game_frame = np.transpose(game_frame, (1, 0, 2))
    game_frame = cv.cvtColor(game_frame, cv.COLOR_RGB2BGR)

    frame = cv.resize(frame, (WIDTH, HEIGHT))
    final = np.hstack((frame, game_frame))
    final = cv.resize(final, (1400, 700))

    cv.imshow("Hand Controlled Snake", final)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    clock.tick(6)

# -------------------- CLEANUP --------------------
cam.release()
cv.destroyAllWindows()
pygame.quit()
