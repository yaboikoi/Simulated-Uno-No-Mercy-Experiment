class EasyBot():
    def __init__(self):
        self.generator = None
        self.hand = None

    def set_gen(self, generator):
        self.generator = generator
        return self

    def set_hand(self, hand):
        self.hand = hand

    def choose_card_from_list(self, cards):
        if not cards:
            return None
        for card in cards:
            if card.type == "Wild Card":
                if card.effect == "Wild Color Roulette":
                    return [card, "opponent chooses color"]
                return [card, self.pick_color()]
        choice = self.generator.choice(cards)
        return [choice]

    def pick_color(self):
        colors = ["Red", "Blue", "Yellow", "Green"]
        choice = self.generator.choice(colors)
        return choice
    