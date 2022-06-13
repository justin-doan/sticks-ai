import numpy as np
from player import player
import pygame
import sys

PLAYER_1 = 1    ## Format of game board is [PLAYER_2               
PLAYER_2 = 0    ##                          PLAYER_1]

BG_COLOR = (219,185,134)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Creating a game, intiialize both players and the board
def create_game_space():
    player_1 = player("Player 1")
    player_2 = player("Player 2")
    board = [player_2, player_1]
    return board

# Print game
def print_game(board):
    print("Current Game State: ")
    for player in board:
        print(str(player.left_hand.num_fingers) + ' ' + str(player.right_hand.num_fingers) + '      ' + str(player.name))
    print("-------------")

# Updates hand given a certain move and which hand to update
def attack_hands(hand_1, hand_2):
    # Attack hand, hand_1 attacks hand_2 
    hand_2.num_fingers += hand_1.num_fingers

    hand_2.num_fingers = hand_2.num_fingers % 5

# Split fingers amongst the two hands
def split(player, amount_left, amount_right):
    player.left_hand.num_fingers = amount_left
    player.right_hand.num_fingers = amount_right

# Checks for winner (both hands finger count is 0)
def is_winner(board):
    for i in range(len(board)):
        if (board[i].left_hand.num_fingers == 0 and board[i].right_hand.num_fingers == 0):
            print('Player {} has won!'.format(2 if i == 1 else 1))
            return True
    
    return False

# Makes a move
def make_move(game, choice, turn):
    
    # Make move
    # Attack
    if choice == 1:
        #self_hand_choice = int(input('Which hand would you like to use, 1 for left Hand or 2 For Right Hand: ')) - 1
        #opp_hand_choice = int(input('Which of the opponents hands to attack? 1 for Left Hand or 2 For Right Hand: ')) -1

        #TO DO implement self_hand_choice and opp_hand_choice, but instead of taking in input from command line,
        #take in input via mouse button down, 

        # Cannot use dead hand to attack
        if game[turn].hands[self_hand_choice].num_fingers==0:
            print("Cannot use dead hand to attack, using other hand to attack")
            self_hand_choice = 0 if self_hand_choice == 1 else 1

        # Cannot attack a dead hand
        if game[turn].hands[opp_hand_choice].num_fingers==0:
            print ("Can't attack a dead hand, attacking other hand")
            opp_hand_choice = 0 if opp_hand_choice == 1 else 1
        
        attack_hands(game[turn].hands[self_hand_choice], game[(turn+1)%2].hands[opp_hand_choice])
        print_game(game)

    # Choice is 2, Split.
    else:

        total_fingers = game[turn].hands[0].num_fingers + game[turn].hands[1].num_fingers 
        
        valid_split = False

        while not valid_split:
            left_hand_amt = int(input('How much do you want to put on your left hand: '))
            right_hand_amt = int(input('How much do you want to put on your right hand: '))
            # Valid split is left and right sum to the total and the new left isn't the old right (and vice versa), no mirror splits allowed
            # Doesn't check if when person "splits" theyre actually making changes: so if it's 2 and 1 and person chooses 2 and 1 it will allow it
            if left_hand_amt + right_hand_amt == total_fingers and left_hand_amt != game[turn].right_hand.num_fingers and right_hand_amt != game[turn].left_hand.num_fingers:
                split(game[turn], left_hand_amt, right_hand_amt)
                break
            else:
                print("Invalid split option, choose again")


# Gets the hand choice given where the mouse clicks
def get_hand_choice(game, mouse):
    if 0 <= mouse[0] <= 200 and 200 <= mouse[1] <= 400:
        return 0
    elif 200 <= mouse[0] <= 400 and 200 <= mouse[1] <= 400:
        return 1
    elif 0 <= mouse[0] <= 200 and 400 <= mouse[1] <= 600:
        return 2
    elif 200 <= mouse[0] <= 400 and 400 <= mouse[1] <= 600:
        return 3
    else:
        return -1
    

def draw_game(game):
    offset = SQUARESIZE

    for c in range(COLUMN_COUNT-1):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BG_COLOR, (c*SQUARESIZE, r*SQUARESIZE+offset, SQUARESIZE, SQUARESIZE))

    # Draw borders for rectangles
    pygame.draw.line(screen, BLACK, (200,200), (200,600))
    pygame.draw.line(screen, BLACK, (0,400), (400,400))

    # Draw buttons
    pygame.draw.rect(screen, BG_COLOR, (width * 2/3 + 25, height/2 - 75, button_width, button_height))
    pygame.draw.rect(screen, BG_COLOR, (width * 2/3 + 25, height/2 + 75, button_width, button_height))

    # Render labels for players
    label1 = my_font.render("Player 2", 1, BG_COLOR)
    screen.blit(label1,(25,100))
    label2 = my_font.render("Player 1", 1, BG_COLOR)
    screen.blit(label2, (25,625))

    # Render label text for buttons
    attack_button_label = my_font_small.render("Attack", 1, WHITE)
    split_button_label = my_font_small.render("Split", 1, WHITE)
    screen.blit(attack_button_label, (width * 2/3 + 37, height / 2 - 70))
    screen.blit(split_button_label, (width * 2/3 + 45, height / 2 + 80))

    #and then render all the hand values in the GUI (use images)
    # Drawing the images
    
    centers = [(25,200), (225,200), (25,450), (225,450)]
    # In range 4 => 4 hands
    for i in range(4):
        finger_number = game[i % 2].hands[i % 2].num_fingers
        image = pygame.image.load(r'C:\Users\doanjust\Desktop\sticks\images\{}.png'.format(finger_number))
        print('Image {} loaded'.format(i))
        screen.blit(image, centers[i])

    pygame.display.update()

game = create_game_space() # Game is a board of 2 players
game_over = False
turn = PLAYER_1

# Py game init block

pygame.init()
SQUARESIZE = 200
COLUMN_COUNT = 3
ROW_COUNT = 2

button_width = SQUARESIZE - 50
button_height = 50
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 2) * SQUARESIZE
size = (width,height)
screen = pygame.display.set_mode(size)
my_font = pygame.font.SysFont("monospace",75)
my_font_small = pygame.font.SysFont("monospace",35)
screen.fill(WHITE)
draw_game(game)



pygame.display.update()

# Game Loop
# It will always be game[turn]'s turn
while not game_over:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            # Attack method
            if width * 2/3 + 25 <= mouse[0] <= width * 2/3 + 175 and height / 2 - 75 <= mouse[1] <= height / 2 - 25:
                choice = 1

                

            if width * 2/3 + 25 <= mouse[0] <= width * 2/3 + 175 and height / 2 + 75 <= mouse[1] <= height / 2 + 150:
                choice = 2

            print_game(game)

            # Prompt player for move option and take in their choice
            print('Player 1' if turn else 'Player 2')

            make_move(game, choice, turn)
            game_over = is_winner(game)
            turn += 1
            turn = turn %2
    