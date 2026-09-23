What counts as one unit of game length in my engine?

The game is counted in turns. A turn gets incremented whenever a player acts: playing a card, drawing an accumulated draw card penalty, or drawing cards as the taret of a Wild Color Roulette. Drawing until a playable card is found and then playing it counts as one turn. Turns skipped by a skip, reverse, or skip everyone are not counted since the skipped player takes no action. The engine records plays, penalty turns, and roulette turns seperatly. The total turns is the sum of all 3.

When a player reaches 25 cards are they out the instant they hit 25 mid draw or after the draw finishes?

A player is out the instant they hit 25 mid draw.

What happens if one move triggers both endings at once? You play your last card and its a draw card that pushes your opponent to 25. Which ending does the engine record?

The player emptying their hand would be the ending the engine records. The engine is constantly checking both end conditions. If I play my last card and its a draw card that pushes my opponent to 25 I get the win for emptying my hand because my hand got emptied first before the card is played. In the play card function the card is removed from the hand before the effects of the card are carried out so the game would end with an empty hand ending.

How does stacking work in this engine?

When you play a car