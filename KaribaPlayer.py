
class KaribaPlayer:

    def __init__(self, name="Default Name"):
        self.name = name

    def get_name(self):
        return self.name

    def get_move(self, board, cards_in_deck, hand, scores):
        raise NotImplementedError("")