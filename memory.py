# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def init():
    global deck,exposed,state,card,moves
    moves = 0
    state = 0
    card = [0,0]
    deck = 2*range(0,8)
    random.shuffle(deck)
    
    exposed = []
    for i in range(0,16):
        exposed.append(False)
            
     
# define event handlers
def mouseclick(pos):
    global exposed,state,card,deck,moves
    
    for i in range(0,16):
       if (pos[0] > 50*i and pos[0] < 50*(i+1)):
            if(not exposed[i]):
                if(state==0):
                    exposed[i] = True
                    card[0] = i
                    state = 1
                elif(state == 1):
                    exposed[i] = True
                    card[1] = i
                    state = 2
                else:
                    if(deck[card[0]] == deck[card[1]] ):
                        exposed[card[0]] = True
                        exposed[card[1]] = True
                        exposed[i] = True
                        card[0] = i
                        state = 1
                    else:
                        exposed[card[0]] = False
                        exposed[card[1]] = False
                        exposed[i] = True
                        card[0] = i
                        state = 1
                moves += 1
                label.set_text("Moves =" + str(moves))
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck,exposed
    space_deck = [10,75]
    for number in deck:
        canvas.draw_text(str(number),space_deck,75,"White")
        space_deck[0] += 50
        
    
    
    space_rect = [[0,0],[50,0],[50,100],[0,100]]
    for i in range(0,16):
        if(not exposed[i]):
            canvas.draw_polygon(space_rect,1,"Red","Green")
        space_rect[0] = list(space_rect[1])
        space_rect[3] = list(space_rect[2])
        space_rect[1][0] += 50
        space_rect[2][0] += 50
        
     
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric
