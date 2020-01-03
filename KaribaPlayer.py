import collections

class KaribaPlayer:

    def __init__(self, name="Default Name"):
        self.name = name

    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        raise NotImplementedError("")

    @staticmethod
    def get_possible_moves(hand):
        moves = []
        counter=collections.Counter(hand)
        for card in counter:
            moves += [(card, i) for i in range(1, counter[card] + 1)]
        return moves

    @staticmethod
    def get_move_score(board, move):
        loc = int(move[0])
        count = int(move[1])
        if board[loc - 1] + count < 3:
            return 0
        if loc == 1:
            return board[7]
        loc -= 2
        while loc >= 0:
            if board[loc] > 0:
                return board[loc]
            loc -=1
        return 0
