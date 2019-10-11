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

import solitaire
class Action:

    def __init__(self, cards, pile, target,id,flipBonus=False):
        self.card = cards
        self.pile = pile
        self.target = target
        self.id = id
        self.flipBonus = flipBonus

    def __str__(self):
        if isinstance(self.target, solitaire.Pile) and self.card is not None:
            if len(self.target.cards) > 0:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to " + str(self.target.cards[0])
            else:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to empty"
        elif self.card is not None:
            if len(self.target) > 0:
                return "id: " + str(self.id) + ", flip: " + str(self.card[0]) + "to " + str(self.target[0])
            else:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to other side of trash"
        else:
            return "id: " + str(self.id) + ", recycle deck"

    def __repr__(self):
        if isinstance(self.target, solitaire.Pile) and self.card is not None:
            if len(self.target.cards) > 0:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to " + str(self.target.cards[0])
            else:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to empty"
        elif self.card is not None:
            if len(self.target) > 0:
                return "id: " + str(self.id) + ", flip: " + str(self.card[0]) + "to " + str(self.target[0])
            else:
                return "id: " + str(self.id) + ", move: " + str(self.card[0]) + "to other side of trash"
        else:
            return "id: " + str(self.id) + ", recycle deck"