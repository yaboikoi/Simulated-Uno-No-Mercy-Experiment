import drivers
import uno_agents
import statician

seed = 3000

driver = drivers.Driver1()
agent1 = uno_agents.EasyBot()
agent2 = uno_agents.EasyBot()
summary = driver.run_game(seed, agent1, agent2)
print(summary)

# DIFFERENT BRANCHES OF MAIN DEPENDING ON MODE 
# Driver interactive, 2_bots
# Agent1 Easy, Hard
# Agent2 Easy, Hard
# How many games
# Seed

# Wild Color Roulette is supposed to show the opponents cards as they draw them
# In the future a bot with memory that stores what cards its opponent has and then decides based on that and its own logic but this is big stretch goal

