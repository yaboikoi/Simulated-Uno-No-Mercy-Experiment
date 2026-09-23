import uno_engine
import random

class Driver1():
    def __init__(self):
        pass

    def run_game_n(self, n, seed, agent1, agent2):
        summaries = []
        for _ in range(n):
            seed += 1
            summary = self.run_game(seed, agent1, agent2)
            summaries.append(summary)
        return summaries

    def run_game(self, seed, agent1, agent2):
        generator1 = random.Random(seed)
        game_seed = generator1.randrange(2**32)
        splitter = random.Random(game_seed)

        engine_seed = splitter.randrange(2**32)
        bot1_seed = splitter.randrange(2**32)
        bot2_seed = splitter.randrange(2**32)

        engine_generator = random.Random(engine_seed)
        bot1_generator = random.Random(bot1_seed)
        bot2_generator = random.Random(bot2_seed)

        agents = [agent1.set_gen(bot1_generator), agent2.set_gen(bot2_generator)]
        labels = ["easy-0", "easy-1"]
        engine = uno_engine.Engine(engine_generator, labels)
        
        while not engine.is_over():
            hand = engine.get_current_hand()
            chosen_agent = agents[hand]

            if engine.pending_draw > 0:
                options = engine.list_of_stackable_cards(hand)
                chosen = chosen_agent.choose_stack(options)
                if chosen[0] == "penalty":
                    engine.take_pending_draw()
                    continue
            else:
                options = engine.list_of_playable_cards_from_hand(hand)
                chosen = chosen_agent.choose_card_from_list(options)

            if len(chosen) == 1:
                engine.play_card(chosen[0], hand)
            else:
                if chosen[1] == "opponent chooses color":
                    chosen_agent = agents[1 - hand]
                    color = chosen_agent.pick_color()
                    engine.play_card(chosen[0], hand, roulette=color)
                else:
                    engine.play_card(chosen[0], hand, wild=chosen[1])
            if engine.count_cards() != engine.total_cards:
                raise RuntimeError(f"Count of Cards != Total Cards | Turn: {engine.turn} Count: {engine.count_cards()} Target: {engine.total_cards}")
        summary = engine.summary()
        return summary
        


