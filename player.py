from hand import hand
# Player class
class player:
    # Constructor, creates a left hand, right hand, and a hands array
    def __init__(self,name):
        self.name = name
        self.left_hand = hand()
        self.right_hand = hand()
        self.hands = [self.left_hand, self.right_hand]

    