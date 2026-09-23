colors = ["Red", "Blue", "Green", "Yellow"]
draw_amounts = {
    "Draw Two": 2,
    "Draw Four": 4,
    "Wild Reverse Draw Four": 4,
    "Wild Draw Six": 6,
    "Wild Draw Ten": 10,
}

def print_card(card):
    print(card.type)
    if card.type == "Number Card":
        print(card.color)
        print(card.number)
    elif card.type == "Action Card":
        print(card.color)
        print(card.effect)
    elif card.type == "Wild Card":
        print(card.effect)

class Card():
    def __init__(self, type, color=None, number=None, effect=None):
        self.type = type
        self.color = color
        self.number = number
        self.effect = effect

class Engine():
    def __init__(self, generator, labels):
        self.generator = generator
        self.deck = []
        self.discard_pile = []
        self.hands = [[], []]
        self.current = 0
        self.labels = list(labels)
        self.plays = 0
        self.chosen_color = None
        self.skip = False
        self.pending_draw = 0
        self.penalty_turns = 0
        self.roulette_turns = 0
        self.ending = None
        self.winner = None
        self.setup()

    def setup(self):
        self.create_deck()
        self.total_cards = len(self.deck)
        self.shuffle(self.deck)
        for _ in range(7):
            self.deal_card_from_deck_to_hand(self.hands[0])
            self.deal_card_from_deck_to_hand(self.hands[1])
        self.draw_card_to_start_discard()
        self.pick_player_first_turn()    

    def summary(self):
        summary = {
            "winner": self.winner,
            "ending": self.ending,
            "plays": self.plays,
            "penalty_turns": self.penalty_turns,
            "roulette_turns": self.roulette_turns,
            "total_turns": self.plays + self.roulette_turns + self.penalty_turns,
        }
        return summary

    def is_over(self):
        for i, hand in enumerate(self.hands):
            if len(hand) >= 25:
                self.ending = "knocked out"
                self.winner = self.labels[1 - i]
                return True
            if len(hand) == 0:
                self.ending = "emptied"
                self.winner = self.labels[i]
                return True
        return False

    def list_of_stackable_cards(self, index):
        stackable = []
        top_card = self.discard_pile[-1]
        top_number = draw_amounts[top_card.effect]
        for card in self.hands[index]:
            if card.effect in draw_amounts:
                if draw_amounts[card.effect] >= top_number:
                    stackable.append(card)
        return stackable

    def take_pending_draw(self):
        self.penalty_turns += 1
        for num in range(self.pending_draw):
            self.deal_card_from_deck_to_hand(self.hands[self.current])
        self.pending_draw = 0
        self.next_players_turn()

    def count_cards(self):
        deck_len = len(self.deck)
        hand1_len = len(self.hands[0])
        hand2_len = len(self.hands[1])
        discard_len = len(self.discard_pile)
        return deck_len + hand1_len + hand2_len + discard_len

    def get_current_hand(self):
        return self.current

    def discard_all_color(self, color, hand):
        keep = []
        for card in hand:
            if card.color == color:
                self.discard_pile.insert(-1, card)
            else:
                keep.append(card)
        hand[:] = keep

    def play_card(self, card, index, wild=None, roulette=None):
        hand = self.hands[index]
        hand.remove(card)
        self.discard_pile.append(card)
        if card.type == "Action Card" or card.type == "Wild Card":
            effect = card.effect

            if effect == "Skip" or effect == "Reverse" or effect == "Skip Everyone":
                self.skip = True

            elif effect in draw_amounts:
                amount = draw_amounts[effect]
                self.pending_draw += amount

            elif effect == "Discard All":
                color = card.color
                self.discard_all_color(color, hand)

            elif effect == "Wild Color Roulette":
                self.roulette_turns += 1
                drawn_cards = []
                color_in_hand = False
                while not color_in_hand:
                    new_card = self.draw_card_from_deck()
                    drawn_cards.append(new_card)
                    if new_card.color == roulette:
                        color_in_hand = True
                        for acard in drawn_cards:
                            self.hands[1 - index].append(acard)

        if card.type != "Wild Card":
            self.chosen_color = None
        if wild is not None:
            self.chosen_color = wild
        if roulette is not None:
            self.chosen_color = roulette
        self.plays += 1
        if self.skip:
            self.skip = False
            return
        if roulette is None:
            self.next_players_turn()
        
    def list_of_playable_cards_from_hand(self, index):
        playable = []
        for card in self.hands[index]:
            if self.can_card_be_played(card):
                playable.append(card)
        while len(playable) == 0:
            new_card = self.draw_card_from_deck()
            if self.can_card_be_played(new_card):
                playable.append(new_card)
            self.hands[index].append(new_card)
        return playable

    def can_card_be_played(self, card):
        if self.chosen_color is not None:
            if card.type == "Number Card" or card.type == "Action Card":
                if card.color == self.chosen_color:
                    return True
        if card.type == "Wild Card":
            return True
        discard_card = self.discard_pile[-1]
        types = [discard_card.type, card.type]
        if "Number Card" in types and types.count("Number Card") == 2:
            if card.color == discard_card.color:
                return True
            if card.number == discard_card.number:
                return True
        elif "Number Card" in types and "Action Card" in types:
            if card.color == discard_card.color:
                return True
        elif "Action Card" in types and "Wild Card" in types:
            if card.effect == discard_card.effect:
                return True
        elif "Action Card" in types and types.count("Action Card") == 2:
            if card.effect == discard_card.effect:
                return True
            if card.color == discard_card.color:
                return True
        return False

    def next_players_turn(self):
        if self.current == 0:
            self.current = 1
        else:
            self.current = 0

    def pick_player_first_turn(self):
        players = [0, 1]
        chosen = self.generator.choice(players)
        self.current = chosen

    def draw_card_to_start_discard(self):
        card = self.draw_card_from_deck()
        self.discard_pile.append(card)
        if card.type != "Number Card":
            self.draw_card_to_start_discard()

    def reset_deck_from_discard(self):
        top = self.discard_pile.pop()
        self.shuffle(self.discard_pile)
        self.deck = self.discard_pile
        self.discard_pile = [top]

    def deal_card_from_deck_to_hand(self, hand):
        if not len(self.deck) > 0:
            self.reset_deck_from_discard()
        new_card = self.draw_card_from_deck()
        hand.append(new_card)

    def draw_card_from_deck(self):
        if not len(self.deck) > 0:
            self.reset_deck_from_discard()
        card = self.deck.pop(0)
        return card
    
    def shuffle(self, deck):
        self.generator.shuffle(deck)

    def create_deck(self):
        # Number Cards
        for num in range(10):
            for color in colors:
                for _ in range(2):
                    new_card = Card(type="Number Card", color=color, number=num)
                    self.deck.append(new_card)

        # Action Cards
        for color in colors:
            for _ in range(3):
                skip_card = Card(type="Action Card", color=color, effect="Skip")
                reverse_card = Card(type="Action Card", color=color, effect="Reverse")
                draw_two_card = Card(type="Action Card", color=color, effect="Draw Two")
                discard_all = Card(type="Action Card", color=color, effect="Discard All")

                self.deck.append(skip_card)
                self.deck.append(reverse_card)
                self.deck.append(draw_two_card)
                self.deck.append(discard_all)

            for _ in range(2):
                draw_four_card = Card(type="Action Card", color=color, effect="Draw Four")
                skip_everyone_card = Card(type="Action Card", color=color, effect="Skip Everyone")

                self.deck.append(draw_four_card)
                self.deck.append(skip_everyone_card)

        # Wild Cards
        for _ in range(8):
            wild_reverse_draw_four = Card(type="Wild Card", effect="Wild Reverse Draw Four")
            wild_color_roulette = Card(type="Wild Card", effect="Wild Color Roulette")

            self.deck.append(wild_reverse_draw_four)
            self.deck.append(wild_color_roulette)

        for _ in range(4):
            wild_draw_six = Card(type="Wild Card", effect="Wild Draw Six")
            wild_draw_ten = Card(type="Wild Card", effect="Wild Draw Ten")

            self.deck.append(wild_draw_six)
            self.deck.append(wild_draw_ten)