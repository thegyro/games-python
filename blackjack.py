# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
outcome = ""
score = 0
message = ""
in_play = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):	# return a string representation of a hand
        result="Hand contains "
        for card in self.hand:
            result += str(card) + " "
        return result
            

    def add_card(self, card): # add a card object to a hand
        self.hand.append(card)	

    def get_value(self):
        hand_value = 0
        ace_present = False
        for card in self.hand:
            hand_value = hand_value + VALUES[card.get_rank()]
            if(card.get_rank()=='A'):
               ace_present = True
        
        if not ace_present:
            return hand_value
        else:
            if(hand_value + 10 <= 21):
                return hand_value + 10
            else:
                return hand_value
            
    # draw a hand on the canvas, use the draw method for cards              
    def draw(self, canvas, pos):
        pos_shift = pos
        for card in self.hand:
            card.draw(canvas,pos_shift)
            pos_shift[0] += CARD_SIZE[0] + 20
        
                    
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in range(4):
            for j in range(13):
                card = Card(SUITS[i],RANKS[j])
                self.deck.append(card)
            

    def shuffle(self):
        self.deck = []
        for i in range(4):
            for j in range(13):
                card = Card(SUITS[i],RANKS[j])
                self.deck.append(card)
        
        random.shuffle(self.deck)        

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card
        
    def __str__(self):
        result = "Deck contains "
        for card in self.deck:
            result += str(card) + " "
        
        return result

#define event handlers for buttons
def deal():
    global outcome,in_play,deck,player,dealer,message,score
        
    deck = Deck()
    player = Hand()
    dealer = Hand()
    
    deck.shuffle()
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    
    message = "Hit or Stand?"
    outcome = ""
    
    if in_play:
        message = "New Deal?"
        outcome = "You loose"
        score -= 1
        in_play = False
        
    else:
        in_play = True
def hit():
    global player,deck,in_play,outcome,message,score,dealer
    
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card()) 
        
    # if busted, assign a message to outcome, update in_play and score
    if(player.get_value() > 21 and in_play):
        in_play = False
        outcome = "You have busted-you loose"
        message = "New Deal?"
        score -= 1        
       
def stand():
    global player,deck,in_play,dealer,outcome,score,message
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if(player.get_value() <= 21):
            while(dealer.get_value() < 17):
                dealer.add_card(deck.deal_card())
        else:
            outcome = "You have busted-you loose"
            message = "New Deal?"
            score -= 1
            in_play = False
        
        if dealer.get_value() > 21:
            outcome = "Dealer Busted-You win!"
            message = "New Deal?"
            in_play = False
            score += 1
        else:
            if(player.get_value() > dealer.get_value()):
                outcome = "You win!"
                message = "New Deal?"
                in_play = False
                score += 1
            else:
                outcome = "You loose"
                message = "New Deal?"
                in_play = False
                score -= 1
# draw handler    
def draw(canvas):
    global dealer,player,deck,outcome,message,score,in_play
    canvas.draw_text("Blackjack",[75,100],30,"Cyan")
    canvas.draw_text("Score " + str(score),[300,100],30,"Black")
    canvas.draw_text("Dealer",[50,175],25,"Black")
    canvas.draw_text("Player",[50,375],25,"Black")
    canvas.draw_text(message,[200,375],25,"Black")
    canvas.draw_text(outcome,[200,175],25,"Black")
    if in_play:
        dealer.draw(canvas,[50,200])
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[50+CARD_BACK_CENTER[0],200+CARD_BACK_CENTER[1]],CARD_BACK_SIZE)
    else:
        dealer.draw(canvas,[50,200])
        
    player.draw(canvas,[50,400])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#initialize the game
deal()

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()


# remember to review the gradic rubric
