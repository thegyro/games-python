# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0,0]

paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2]
paddle2_pos = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2]

paddle1_vel = [0,0]
paddle2_vel = [0,0]

score1 = 0
score2 = 0

key_pressed = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2,HEIGHT/2]
    
    if(right):
        ball_vel[0] = random.randrange(120/60,240/60)
        ball_vel[1] = -random.randrange(60/60,180/60)
    else:
        ball_vel[0] = -random.randrange(120/60,240/60)
        ball_vel[1] = -random.randrange(60/60,180/60)
   
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2]
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2]
    
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]
    
    score1 = 0
    score2 = 0
    
    true_false = random.randrange(0,2)
    
    if(true_false==0):
        ball_init(False)
    else:
        ball_init(True)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos,paddle1_vel,paddle2_vel
    global ball_pos,ball_vel,count
 
    # update paddle's vertical position, keep paddle on the screen 
                     
    if(paddle1_pos[1] < HALF_PAD_HEIGHT):
       if(chr(key_pressed) == 'S'):
            paddle1_vel = [0,2]
       else:
            paddle1_vel = [0,0]
        
    if(paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT):  
        if(chr(key_pressed)=='W'):
            paddle1_vel = [0,-2]
        else:
            paddle1_vel = [0,0]
    
    if(paddle2_pos[1] < HALF_PAD_HEIGHT):
        if(key_pressed == simplegui.KEY_MAP["down"]):
            paddle2_vel = [0,2]
        else:
            paddle2_vel = [0,0]
        
    if(paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT):
        if(key_pressed == simplegui.KEY_MAP["up"]):
            paddle2_vel = [0,-2]
        else:
            paddle2_vel = [0,0]
    
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    pad1_y1 = paddle1_pos[1] - HALF_PAD_HEIGHT
    pad1_y2 = paddle1_pos[1] + HALF_PAD_HEIGHT
    
    pad2_y1 = paddle2_pos[1] - HALF_PAD_HEIGHT
    pad2_y2 = paddle2_pos[1] + HALF_PAD_HEIGHT
    
    
    c.draw_line([paddle1_pos[0],pad1_y1],[paddle1_pos[0],pad1_y2],PAD_WIDTH,"White")
    c.draw_line([paddle2_pos[0],pad2_y1],[paddle2_pos[0],pad2_y2],PAD_WIDTH,"White")
    
    # update ball
    
    if(ball_pos[0] < (BALL_RADIUS + PAD_WIDTH)):
        
        if(ball_pos[1]>=pad1_y1 and ball_pos[1]<=pad1_y2):            
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            score2 += 1
            ball_init(True)
        
        
    if(ball_pos[0] > (WIDTH-(BALL_RADIUS + PAD_WIDTH))):
        
        if(ball_pos[1]>=pad2_y1 and ball_pos[1]<=pad2_y2):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
            
            
        else:
            score1 += 1
            ball_init(False)
               
    if(ball_pos[1] < BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    if(ball_pos[1] > (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball and scores     
    c.draw_circle(ball_pos,BALL_RADIUS,2,"White","White")
    c.draw_text(str(score1),[WIDTH/4,30],24,"White")
    c.draw_text(str(score2),[3*WIDTH/4,30],24,"White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel,key_pressed
    
    if(chr(key)== 'W'):
        paddle1_vel = [0,-2]
                           
    if(chr(key)== 'S'):
        paddle1_vel = [0,2]
        
    if(key == simplegui.KEY_MAP["up"]): 
        paddle2_vel = [0,-2]
            
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = [0,2]
        
    key_pressed = key
                       
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",new_game,100)


# start frame
frame.start()
new_game()

