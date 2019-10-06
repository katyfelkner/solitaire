# action type

# actions have card(s) (a list), a current pile, a target pile (no spot number needed since it's always spot 0), and an ID
#optional flipBonus for when a card is flipped in a turn to account for +5 reward

#ID:
#1. moveBetweenPiles
#2. movePileToBlock
#3. moveBlockToPile
#4. drawCard
#5. recycleDeck
#6. wasteToPile
#7. wasteToBlock

class Action:

    def __init__(self, cards, pile, target,id,flipBonus=False):
        self.card = cards
        self.pile = pile
        self.target = target
        self.id = id
        self.flipBonus = flipBonus