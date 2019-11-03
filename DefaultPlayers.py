from KaribaPlayer import KaribaPlayer
import random

class BasicPlayer(KaribaPlayer):
    def __init__(self, name="Default Name"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):   
        return hand[0], 1

class LowestCardPlayer(KaribaPlayer):
    def __init__(self, name="LowestCardPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):  
        my_move = (hand[0], 1)  
        return my_move

class HighestCardPlayer(KaribaPlayer):
    def __init__(self, name="HighestCardPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = (hand[-1], 1)
        return my_move

class GreedyPlayer(KaribaPlayer):
    def __init__(self, name="GreedyPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        for card in hand:
            if board[card - 1] >= 2:
                my_move = (card, 1)
        if my_move is None:
            my_move = (hand[-1], 1)
        return my_move

class GreedyPlayer2(KaribaPlayer):
    def __init__(self, name="GreedyPlayer2"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        for card in hand[::-1]:
            if board[card - 1] >= 2:
                my_move = (card, 1)
        if my_move is None:
            my_move = (hand[0], 1)
        return my_move

class GreedyPlayer3(KaribaPlayer):
    def __init__(self, name="GreedyPlayer3"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        best_move_score = 0
        possible_moves = get_possible_moves(hand)
        for move in possible_moves:
            move_score = get_move_score(board, move)
            if move_score > best_move_score:
                best_move_score = move_score
                my_move = move
        if my_move is None:
            highest_index = None
            for i in hand:
                if highest_index is None or board[i - 1] > board[highest_index - 1]:
                    highest_index = i
                return highest_index, 1
            if highest_index is None:
                my_move = (hand[0], 1)
            else:
                my_move = highest_index, 1
        return my_move 
    
class RandomPlayer(KaribaPlayer):
    def __init__(self, name="RandomPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = (random.choice(hand), 1)
        return my_move
        
def get_possible_moves(hand):
    moves = []
    counter=collections.Counter(hand)
    for card in counter:
        moves += [(card, i) for i in range(1, counter[card] + 1)]
    return moves

def get_move_score(board, move):
    loc = int(move[0])
    count = int(move[1])
    if board[loc - 1] + count < 3:
        return 0
    if loc == 1:
        return board[7]
    loc -= 1
    while loc > 0:
        if board[loc] > 0:
            return board[loc]
        loc -=1
    return 0
