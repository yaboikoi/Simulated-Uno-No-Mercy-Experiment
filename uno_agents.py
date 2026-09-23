class EasyBot():
    def __init__(self):
        self.generator = None
        self.hand = None

    def set_gen(self, generator):
        self.generator = generator
        return self

    def set_hand(self, hand):
        self.hand = hand

    def choose_stack(self, cards):
        options = cards + ["penalty"]
        chosen = self.generator.choice(options)
        if chosen != "penalty":
            if chosen.type == "Wild Card":
                return [chosen, self.pick_color()]
        return [chosen]

    def choose_card_from_list(self, cards):
        if cards is None:
            raise ValueError("choose_card_from_list got an empty list") 
        card = self.generator.choice(cards)
        if card.type == "Wild Card":
            if card.effect == "Wild Color Roulette":
                return [card, "opponent chooses color"]
            else:
                return [card, self.pick_color()]
        return [card]

    def pick_color(self):
        colors = ["Red", "Blue", "Yellow", "Green"]
        choice = self.generator.choice(colors)
        return choice
    