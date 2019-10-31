import random
from DefaultPlayers import *
import itertools

class Kariba:
    def __init__(self):
        pass

    def create_cards(self):
        cards = []
        for i in range(8):
            cards.extend(8 * [i+1])
        random.shuffle(cards)
        return cards

    def start_game(self, players):
        self.cards = self.create_cards()
        self.players = players
        self.players_dic = {}
        for p in players:
            self.players_dic[p] = {'taken':[]}
            self.players_dic[p]['taken'] = []
            self.players_dic[p]['hand'] = self.take_cards(5)
            self.players_dic[p]['hand'].sort()
        self.board = []
        for i in range(8):
            self.board.append([])
        self.current_player = 0
        self.last_to_play = -1

    def take_cards(self, n):
        if len(self.cards) > n:
            out = self.cards[:n]
            self.cards = self.cards[n:]
        else:
            out = self.cards[:]
            self.cards = []
        return out
          
    def handle_play(self, player, position, cards_num):
        if player not in self.players_dic.keys():
            print("Player does not exist")
            return False
        if position < 1 or position > 8:
            print("Invalid position")
            return False
        if position not in self.players_dic[player]['hand']:
            print("You don't have that card.")
            return False
        if self.players_dic[player]['hand'].count(position) < cards_num:
            print("You don't have enough %d cards." % (position))
            return False

        hand = []
        count = 0
        for c in self.players_dic[player]['hand']:
            if c != position:
                hand.append(c)
            else:
                if count>= cards_num:
                    hand.append(c)
                else:
                    count = count + 1
        self.players_dic[player]['hand'] = hand

        self.board[position-1].extend(cards_num * [position])

        if len(self.board[position-1]) > 2:
            if position == 1:
                self.players_dic[player]['taken'].extend(self.board[7])
                self.board[7] = []
            else:
                for i in range(position-2, -1, -1):
                    if self.board[i]:
                        self.players_dic[player]['taken'].extend(self.board[i])
                        self.board[i] = []
                        break
        if self.last_to_play == -1:
            self.players_dic[player]['hand'].extend(self.take_cards(cards_num))
        self.players_dic[player]['hand'].sort()
        return True

    def display_current_status(self):
        print("+-"*8+"+") 
        header = []
        data = []
        for i in range(8):
            header.append(str(i+1))
            data.append(str(len(self.board[i])))
        print("|"+"|".join(header)+"|")
        print("+-"*8+"+") 
        print("|"+"|".join(data)+"|")
        print("+-"*8+"+") 
        print(len(self.cards), "cards left.")
        print()
        for p in self.players:
            print(p, "Hand:", self.players_dic[p]['hand'], "Taken:", len(self.players_dic[p]['taken']))

    def get_current_board(self):
        return [len(x) for x in self.board]

    def get_cards_in_deck(self):
        return len(self.cards)

    def get_player_hand(self, player):
        if player not in self.players:
            return "Not a Player"
        return self.players_dic[player]['hand']

    def get_player_scores(self):
        return [(p, self.players_dic[p]['taken']) for p in self.players]

    def switch_player(self):
        self.current_player = self.current_player+1
        if self.current_player == len(self.players):
            self.current_player = 0

    def identify_winner(self):
        winner = ""
        best_score = 0
        for p in self.players_dic.keys():
            if len(self.players_dic[p]['taken']) > best_score:
                winner = p
                best_score = len(self.players_dic[p]['taken'])
        return winner, best_score


    def game_on(self):
        if self.cards:
            return True
        elif self.last_to_play == -1:
            self.last_to_play = self.current_player
            return True
        elif self.last_to_play == self.current_player:
            return False
        return True


def game_manager(player1, player2):
    kariba = Kariba()
    kariba.start_game([player1.get_name(), player2.get_name()])
    players = {player1.get_name(): player1, player2.get_name(): player2}
    while kariba.game_on():
        # kariba.display_current_status()
        player = kariba.players[kariba.current_player]
        # print("Your turn", player)
        position, n_cards = players[player].get_move(kariba.get_current_board(), kariba.get_cards_in_deck(), kariba.get_player_hand(player), kariba.get_player_scores())
        play_is_good = kariba.handle_play(player, position, n_cards)
        
        if play_is_good:
            kariba.switch_player()
    
    # kariba.display_current_status()

    winner, score = kariba.identify_winner()
    # print("The winner is", winner, "with", score, "points.")
    return winner

def interactive_player():
    kariba = Kariba()
    kariba.start_game(["A","B"])
    while kariba.game_on():
        kariba.display_current_status()
        player = kariba.players[kariba.current_player]
        print("Your turn", player)
        #print("Your hand:", kariba.players_dic[player]['hand'])
        position = int(input("Where would you like to play? "))
        n_cards = int(input("How many cards would you like to play? "))
        play_is_good = kariba.handle_play(player, int(position), int(n_cards))
        if play_is_good:
            kariba.switch_player()

    kariba.display_current_status()

    winner, score = kariba.identify_winner()
    print("The winner is", winner, "with", score, "points.")

if __name__ == "__main__":
    GAMES_TO_PLAY = 1000
    players = [LowestCardPlayer(), HighestCardPlayer(), GreedyPlayer(), RandomPlayer(), GreedyPlayer2()]
    
    print("Final score after %s games: " % GAMES_TO_PLAY)
    
    for couple in list(itertools.permutations(players, 2)):
        player1 = couple[0]
        player2 = couple[1]
        score = {player1.get_name():0, player2.get_name():0}
        for i in range(GAMES_TO_PLAY):
            winner = game_manager(player1, player2)
            score[winner] += 1
        print(score)

