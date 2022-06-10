import numpy as np
from player import player
import pygame
import sys

PLAYER_1 = 1    ## Format of game board is [PLAYER_2               
PLAYER_2 = 0    ##                          PLAYER_1]

BG_COLOR = (219,185,134)

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
        self_hand_choice = int(input('Which hand would you like to use, 1 for left Hand or 2 For Right Hand: ')) - 1
        opp_hand_choice = int(input('Which of the opponents hands to attack? 1 for Left Hand or 2 For Right Hand: ')) -1

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
            if left_hand_amt + right_hand_amt == total_fingers and left_hand_amt != game[turn].right_hand.num_fingers and right_hand_amt != game[turn].left_hand.num_fingers:
                split(game[turn], left_hand_amt, right_hand_amt)
                break
            else:
                print("Invalid split option, choose again")

# Draw board block
# SQUARESIZE = 200
# COLUMN_COUNT = 2
# ROW_COUNT = 2
# def draw_game(game):
#     offset = SQUARESIZE
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT):
#             pygame.draw.rect(screen, BG_COLOR, (c*SQUARESIZE, r*SQUARESIZE+offset, SQUARESIZE, SQUARESIZE))

#     pygame.display.update()
# Initialize Game
game = create_game_space() # Game is a board of 2 players
game_over = False
turn = PLAYER_1

# Py game init block

# pygame.init()
# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT + 2) * SQUARESIZE
# size = (width,height)
# screen = pygame.display.set_mode(size)
# draw_game(game)
# pygame.display.update()

# Game Loop
# It will always be game[turn]'s turn
while not game_over:

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()
        
    #     if event.type== pygame.MOUSEBUTTONDOWN:
    #         print ('')
        print_game(game)

        # Prompt player for move option and take in their choice
        print('Player 1' if turn else 'Player 2')
        choice = int(input('Enter 1 for attack or 2 for split: '))

        make_move(game, choice, turn)
        game_over = is_winner(game)
        turn += 1
        turn = turn %2
    