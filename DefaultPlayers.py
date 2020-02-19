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
        possible_moves = KaribaPlayer.get_possible_moves(hand)
        for move in possible_moves:
            move_score = KaribaPlayer.get_move_score(board, move)
            if move_score > best_move_score:
                best_move_score = move_score
                my_move = move
        if my_move is None:
            highest_index = None
            for i in hand:
                if highest_index is None or board[i - 1] > board[highest_index - 1]:
                    highest_index = i
                #return highest_index, 1
            if highest_index is None:
                my_move = (hand[0], 1)
            else:
                my_move = highest_index, 1
        return my_move 
    
class GreedyPlayer4(KaribaPlayer):
    def __init__(self, name="GreedyPlayer4"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        best_move_score = 0
        possible_moves = KaribaPlayer.get_possible_moves(hand)
        for move in possible_moves:
            move_score = KaribaPlayer.get_move_score(board, move)
            if move_score > best_move_score:
                best_move_score = move_score
                my_move = move

        if my_move is None:
            lowest_index = None
            for i in hand:
                if lowest_index is None or board[i - 1] < board[lowest_index - 1]:
                    lowest_index = i
                #return lowest_index, 1
            if lowest_index is None:
                my_move = (hand[-1], 1)
            else:
                my_move = lowest_index, 1
        return my_move 
    
def get_move_effect(board, move):
    loc = int(move[0])
    count = int(move[1])
    if board[loc - 1] + count < 3:
        return None
    if loc == 1:
        if board[7] > 0:
            return 7
        else:
            return None
    loc -= 2
    while loc >= 0:
        if board[loc] > 0:
            return loc
        loc -=1
    return None
    
def get_move_simulated_score(board, hand, move, discount_factor=0.5):
    loc = int(move[0])
    count = int(move[1])
    effect_loc = get_move_effect(board, move)
    board_next = board[:]
    hand_next = hand[:]
    for _ in range(count):
        hand_next.remove(loc)
    score = 0
    board_next[loc-1] += count
    if effect_loc is not None:
        score += board_next[effect_loc]
        board_next[effect_loc] = 0
    if hand_next:
        score += discount_factor*max(
            KaribaPlayer.get_move_score(board_next, move_next)
            for move_next in KaribaPlayer.get_possible_moves(hand_next))
    return score
    
class SimulationPlayer(KaribaPlayer):
    def __init__(self, name="SimulationPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        best_move_score = 0
        possible_moves = self.get_possible_moves(hand)
        for move in possible_moves:
            move_score = get_move_simulated_score(board, hand, move)
            if move_score == 0:
                continue
            if move_score > best_move_score:
                best_move_score = move_score
                my_move = move

        if my_move is None:
            lowest_index = None
            for i in hand:
                if lowest_index is None or board[i - 1] < board[lowest_index - 1]:
                    lowest_index = i
                #return lowest_index, 1
            if lowest_index is None:
                my_move = (hand[-1], 1)
            else:
                my_move = lowest_index, 1
        return my_move 
    
def get_move_opponent(board, hand):
    # This is the baseline opponent the simulation will be carried against.
    my_move = None
    best_move_score = 0
    possible_moves = KaribaPlayer.get_possible_moves(hand)
    for move in possible_moves:
        # move_score = get_move_simulated_score(board, hand, move)
        move_score = KaribaPlayer.get_move_score(board, move)
        if move_score == 0:
            continue
        if move_score > best_move_score:
            best_move_score = move_score
            my_move = move

    if my_move is None:
        lowest_index = None
        for i in hand:
            if lowest_index is None or board[i - 1] < board[lowest_index - 1]:
                lowest_index = i
            #return lowest_index, 1
        if lowest_index is None:
            my_move = (hand[-1], 1)
        else:
            my_move = lowest_index, 1
    return my_move 
    
def simulated_score_recursive(board, hand, move, opponent_hand, deck, remaining_turns, is_opponent=False):
    loc = int(move[0])
    count = int(move[1])
    effect_loc = get_move_effect(board, move)
    board_next = board[:]
    hand_next = hand[:]
    deck_next = deck[:]
    for _ in range(count):
        hand_next.remove(loc)
        if deck_next:
            hand_next.append(deck_next.pop())
    score = 0
    board_next[loc-1] += count
    if effect_loc is not None:
        score += board_next[effect_loc]
        board_next[effect_loc] = 0
    is_opponent = not is_opponent
    if opponent_hand and remaining_turns:
        remaining_turns -= 1
        if is_opponent:
            moves = [get_move_opponent(board_next, opponent_hand)]
        else:
            moves = KaribaPlayer.get_possible_moves(opponent_hand)
        score -= max(
            simulated_score_recursive(
                board_next, opponent_hand, move_next, hand_next, deck_next, remaining_turns, is_opponent) 
            for move_next in moves)
    return score
    
def averaged_simulated_score(board, hand, move, states, num_turns):
    score = sum(
        simulated_score_recursive(
            board, hand, move, opponent_hand, deck, num_turns)
        for deck, opponent_hand in states)
    return score / len(states)
    
class RecursiveSimulationPlayer(KaribaPlayer):

    NUM_SIMULATIONS = 50
    SIMULATION_LENGTH = 4
    
    def __init__(self, name="RecursiveSimulationPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = None
        best_move_score = 0
        possible_moves = KaribaPlayer.get_possible_moves(hand)
        states = []
        for _ in range(self.NUM_SIMULATIONS):
            all_cards = list(range(1, 9)) * 8
            for card in hand:
                all_cards.remove(card)
            for card, count in enumerate(board):
                for _ in range(count):
                    all_cards.remove(card+1)
            random.shuffle(all_cards)
            # Last five cards are used for the opponent_hand.
            opponent_hand = all_cards[-5:]
            deck = all_cards[:-5][:cards_in_deck]
            states.append((deck, opponent_hand))
        for move in possible_moves:
            move_score = averaged_simulated_score(
                board, hand, move, states, self.SIMULATION_LENGTH)
            if move_score == 0:
                continue
            if move_score > best_move_score:
                best_move_score = move_score
                my_move = move
        
        if my_move is None:
            lowest_index = None
            for i in hand:
                if lowest_index is None or board[i - 1] < board[lowest_index - 1]:
                    lowest_index = i
                #return lowest_index, 1
            if lowest_index is None:
                my_move = (hand[-1], 1)
            else:
                my_move = lowest_index, 1
        return my_move 
    
class RandomPlayer(KaribaPlayer):
    def __init__(self, name="RandomPlayer"):
        super().__init__(name)
        
    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        my_move = (random.choice(hand), 1)
        return my_move
        

