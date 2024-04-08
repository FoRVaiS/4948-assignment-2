import json
import random


class Card:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit
        self._soft_ace = False

    def rank(self):
        if self._rank in ('J', 'Q', 'K'):
            return 10
        elif self._rank == 'A':
            return 11
        else:
            return int(self._rank)

    @property
    def soft_ace(self):
        return self.soft_ace

    @soft_ace.setter
    def soft_ace(self, value):
        if self._rank == 'A':
            self._soft_ace = value
            return True

        return False

    def __str__(self):
        return f"{self._rank} of {self._suit}"


class Deck:
    def __init__(self, num_decks=1):
        ranks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        self.cards = [
            Card(rank, suit)
            for _ in range(num_decks)
            for rank in ranks
            for suit in suits
        ]

        self.total = len(self.cards)

        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def __str__(self):
        return str([str(card) for card in self.cards])


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def total(self):
        total_value = sum(card.rank() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while total_value > 21 and num_aces:
            total_value -= 10
            num_aces -= 1
        return total_value


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = Hand()
        self.isPlaying = True

    def hit(self, card, soft_ace=False):
        card.soft_ace = soft_ace
        self._hand.add_card(card)

    def stay(self):
        self.isPlaying = False

    # def doubleDown(self, card):
    #     self._hand.add_card(card)
    #
    # def split(self, card):
    #     self.hand.add_card(card)
    #
    # def surrender(self, card):
    #     self.hand.add_card(card)

    def name(self):
        return self._name

    def getCards(self):
        return [str(card) for card in self._hand.cards]

    def getTotalHand(self):
        return self._hand.total()


class Turn:
    def __init__(self, player: Player, opponent: Player, total_cards, cards_remaining):
        self.player = player
        self.opponent = opponent
        self.total = player.getTotalHand()
        self.opponent_total = opponent.getTotalHand()
        self.composition = player.getCards()
        self.total_cards = total_cards
        self.cards_remaining = cards_remaining
        self.result = None

    def set_result(self, result):
        self.result = result

    def report(self):
        report_dict = {
            "total": self.total,
            "opponent_total": self.opponent_total,
            "composition": self.composition,
            "total_cards": self.total_cards,
            "cards_remaining": self.cards_remaining,
            "result": self.result
        }
        return report_dict


class Game:
    def __init__(self, num_decks=1):
        self.deck = Deck(num_decks)
        self.turns = []
        self.player = Player('Player 1')
        self.dealer = Player('Dealer')
        self.players = [
            self.player,
            self.dealer
        ]

    def deal(self):
        return self.deck.deal()

    def deal_initial(self):
        for _ in range(2):
            for player in self.players:
                self.hit(player)

    def prompt(self, player):
        actions = [
            self.hit,
        ]

        action = random.sample(actions, k=1)[0]
        action(player)

    def hit(self, player):
        card = self.deal()
        player.hit(card)

        return card

    def stay(self, player: Player):
        player.stay()

    def doubleDown(self, player):
        card = self.hit(player)
        print(f"{player.name()} got {str(card)}")

    def split(self, player):
        # Register split event
        pass

    def surrender(self, player):
        # Register surrender event
        pass

    def start(self):
        self.deal_initial()
        self.in_progress = True

        while (self.progress()):
            for player in self.players:
                if not player.isPlaying:
                    pass

                opponent = self.dealer if player is self.player else self.player

                total_cards = self.deck.total
                remaining_cards = total_cards - len(self.deck.cards)

                self.turns.append(Turn(player, opponent, total_cards, remaining_cards))

                # print(f"{player.name()}: {player.getTotalHand()} {player.getCards()}")
                # print(player.name())
                self.prompt(player)

                # Check limits
                if player.getTotalHand() > 21:
                    # print(f"BROKE - {player.name()}: {player.getTotalHand()} {player.getCards()}")
                    current_turn = self.turns[-1:][0]
                    current_turn.set_result(-1)
                    self.end()
                    break

    def end(self):
        self.in_progress = False

    def progress(self):
        return self.in_progress

    def report(self):
        return [turn.report() for turn in self.turns]


if __name__ == "__main__":
    game = Game(num_decks=1)
    game.start()

    print(json.dumps(game.report()))
