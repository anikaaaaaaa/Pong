import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Set up Pygame
pygame.init()
WIDTH, HEIGHT = 700,  700
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

# Set up OpenGL
glOrtho(0, 700, 700, 0, -1, 1)

# Paddle properties
paddle_width = 300
paddle_height = 60
paddle_x = 0
paddle_y = HEIGHT - paddle_height
paddle_speed = 2

# Ball properties are defined here
ball_size = 10
ball_x = 0
ball_y = 2
ball_speed = float(input("Enter the ball speed: "))
ball_direction = [2, 2]

def draw_line(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    dx = x2 - x1
    dy = y2 - y1
    x, y = x1, y1
    p = 2*dy - dx
    for i in range(dx):
        glVertex2f(x, y)
        if p < 0:
            x += 1
            p += 2 * dy
        else:
            x += 1
            y += 1
            p = p + 2 * (dy - dx)
    glEnd()


def draw_ball(radius, xc, yc):
    x, y = 0, radius
    p = 1 - radius

    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)

        if p < 0:
            x += 1
            p += 2 * x + 3
        else:
            x += 1
            y -= 1
            p += 2 * (x - y) + 5
    glEnd()


desired_value = 5
current_value = 0

# Game loop
while current_value < desired_value:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:

           pygame.quit()
           sys.exit()


   glClear(GL_COLOR_BUFFER_BIT)


   keys = pygame.key.get_pressed()
   if keys[K_LEFT] and paddle_x > 0:
       paddle_x -= paddle_speed
   if keys[K_RIGHT] and paddle_x < WIDTH - paddle_width:
       paddle_x += paddle_speed


   ball_x += ball_speed * ball_direction[0]
   ball_y += ball_speed * ball_direction[1]



   if ball_x <= 0 or ball_x >= WIDTH - ball_size:
       ball_direction[0] *= -1
   if ball_y <= 0:
       ball_direction[1] *= -1


   if (ball_y + ball_size >= paddle_y and ball_x + ball_size >= paddle_x and ball_x <= paddle_x + paddle_width):
       ball_direction[1] *= -1
       current_value += 1
   # Draw paddle
   glColor3f(1.0, 1.0, 1.0)
   glPointSize(2.0)
   glColor3f(0.5, 0.5, 0.5)

   p_x_w = paddle_x + paddle_width
   p_y_h = paddle_y + paddle_height
   draw_line(paddle_x, paddle_y, p_x_w, paddle_y)
   draw_line(paddle_x, p_y_h, p_x_w, p_y_h)
   glBegin(GL_LINES)
   glVertex2f(paddle_x, paddle_y)
   glVertex2f(paddle_x, p_y_h)
   glVertex2f(p_x_w, paddle_y)
   glVertex2f(p_x_w, p_y_h)
   glEnd()

   # Draw ball
   glColor3f(1.0, 1.0, 1.0)
   draw_ball(ball_size, ball_x,ball_y)
   pygame.display.flip()