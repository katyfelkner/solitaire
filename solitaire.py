from card_elements import Card, Deck, Pile
from action import Action
from copy import deepcopy

class Game:

    values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    suits = { #keys are unicode symbols for suits
        u'\u2660': "black",
        u'\u2665': "red",
        u'\u2663': "black",
        u'\u2666': "red",
    }

    numPlayPiles = 7

    def __init__(self):
        self.deck = Deck(self.values, self.suits)
        self.playPiles = []
        for i in range(self.numPlayPiles):
            thisPile = Pile()
            [thisPile.addCard(self.deck.takeFirstCard(flip=False)) for j in range(i + 1)]
            thisPile.flipFirstCard()
            self.playPiles.append(thisPile)
        self.blockPiles = {suit: Pile() for suit in self.suits}
        self.trashPileUp = []
        self.trashPileDown = [self.deck.takeFirstCard(flip=False) for i in range(0, len(self.deck.cards))]

    def getGameElements(self):
        returnObject = {
            "playPiles": [pile for pile in self.playPiles],
            "blockPiles": {suit: pile for suit, pile in self.blockPiles.items()},
            "trash pile up": ", ".join([str(card) for card in self.trashPileUp]),
            "trash pile down": ", ".join([str(card) for card in self.trashPileDown])
        }
        return returnObject

    def printGame(self):
        returnString = {
            "playPiles": [str(pile) for pile in self.playPiles],
            "blockPiles": {suit: str(pile) for suit, pile in self.blockPiles.items()},
            "trash pile up": ", ".join([str(card) for card in self.trashPileUp]),
            "trash pile down": ", ".join([str(card) for card in self.trashPileDown])
        }
        return returnString

    def checkCardOrder(self,higherCard,lowerCard):
        notKing = True
        if lowerCard.value == 'K':
            notKing = False
        suitsDifferent = self.suits[higherCard.suit] != self.suits[lowerCard.suit]
        valueConsecutive = self.values[self.values.index(higherCard.value)-1] == lowerCard.value
        return suitsDifferent and valueConsecutive and notKing

    def checkIfCompleted(self):
        deckEmpty = len(self.deck.cards)==0
        pilesEmpty = all(len(pile.cards)==0 for pile in self.playPiles)
        blocksFull = all(len(pile.cards)==13 for suit,pile in self.blockPiles.items())
        return deckEmpty and pilesEmpty and blocksFull

    def addToBlock(self, card):
        if card is None:
            return False
        elif len(self.blockPiles[card.suit].cards)>0:
            highest_value = self.blockPiles[card.suit].cards[0].value
            if self.values[self.values.index(highest_value)+1] == card.value:
                self.blockPiles[card.suit].cards.insert(0,card)
                return True
            else:
                return False
        else:
            if card.value=="A":
                self.blockPiles[card.suit].cards.insert(0,card)
                return True
            else:
                return False

    def canAddToBlock(self, card):
        """Check whether we can add the card to the block, without actually doing it. If it can be moved, return target pile."""
        if card is None:
            return False
        elif len(self.blockPiles[card.suit].cards) > 0:
            highest_value = self.blockPiles[card.suit].cards[0].value
            if self.values[self.values.index(highest_value) + 1] == card.value:
                return self.blockPiles[card.suit]
            else:
                return False
        else:
            if card.value == "A":
                return self.blockPiles[card.suit]
            else:
                return False

    def canMoveBlockToPile(self, card):
        moves = []
        if card is None:
            return False
        for pile in self.playPiles:
            if len(pile.cards)>0:
                if self.checkCardOrder(pile.cards[0], card):
                    moves.append(pile)
        if len(moves) > 0:
            return moves
        else:
            return False

    def takeTurn(self, verbose=False):

        #1: check if there are any play pile cards you can play to block piles
        for pile in self.playPiles:
            if len(pile.cards) > 0 and self.addToBlock(pile.cards[0]):
                card_added = pile.cards.pop(0)
                if len(pile.cards) > 0 and not pile.cards[0].flipped:
                    pile.cards[0].flip()
                if verbose:
                    print("Adding play pile card to block: {0}".format(str(card_added)))
                return True

        #2: check if cards in deck can be added
        if len(self.trashPileUp) > 0 and self.addToBlock(self.trashPileUp[-1]):
            card_added = self.trashPileUp[-1]
            self.trashPileUp.pop(-1)
            if verbose:
                print("Adding card from deck to block: {0}".format(str(card_added)))
            return True

        #3: move kings to open piles
        for pile in self.playPiles:
            if len(pile.cards)==0: #pile has no cards
                for pile2 in self.playPiles:
                    if len(pile2.cards)>1 and pile2.cards[0].value == "K":
                        card_added = pile2.cards.pop(0)
                        if len(pile2.cards) > 0 and not pile2.cards[0].flipped:
                            pile2.cards[0].flip()
                        pile.addCard(card_added)
                        if verbose:
                            print("Moving {0} from Pile to Empty Pile".format(str(card_added)))
                        return True

                if len(self.trashPileUp) > 0 and self.trashPileUp[-1].value == "K":
                    card_added = self.trashPileUp[-1]
                    pile.addCard(card_added)
                    self.trashPileUp.pop(-1)
                    if verbose:
                        print("Moving {0} from Deck to Empty Pile".format(str(card_added)))
                    return True

        #4: add drawn card to playPiles
        for pile in self.playPiles:
            if len(pile.cards)>0 and len(self.trashPileUp) > 0:
                if self.checkCardOrder(pile.cards[0],self.trashPileUp[-1]):
                    card_added = self.trashPileUp[-1]
                    pile.addCard(card_added)
                    self.trashPileUp.pop(-1)
                    if verbose:
                        print("Moving {0} from Deck to Pile".format(str(card_added)))
                    return True

        #5: move around cards in playPiles
        for pile1 in self.playPiles:
            pile1_flipped_cards = pile1.getFlippedCards()
            if len(pile1_flipped_cards)>0:
                for pile2 in self.playPiles:
                    pile2_flipped_cards = pile2.getFlippedCards()
                    if pile2 is not pile1 and len(pile2_flipped_cards)>0:
                        for transfer_cards_size in range(1,len(pile1_flipped_cards)+1):
                            cards_to_transfer = pile1_flipped_cards[:transfer_cards_size]
                            if self.checkCardOrder(pile2.cards[0],cards_to_transfer[-1]):
                                pile1_downcard_count = len(pile1.cards) - len(pile1_flipped_cards)
                                pile2_downcard_count = len(pile2.cards) - len(pile2_flipped_cards)
                                if pile2_downcard_count < pile1_downcard_count:
                                    [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                    pile1.cards = pile1.cards[transfer_cards_size:]
                                    if len(pile1.cards) > 0 and not pile1.cards[0].flipped:
                                        pile1.cards[0].flip()
                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
                                elif pile1_downcard_count==0 and len(cards_to_transfer) == len(pile1.cards):
                                    [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                    pile1.cards = []
                                    if len(pile1.cards) > 0 and not pile1.cards[0].flipped:
                                        pile1.cards[0].flip()

                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
        return False

    def simulate(self,  recycles, verbose=False):

        actions = self.getPossibleMoves()
        turnResult = self.takeTurn(verbose=verbose)
        if recycles == 10:
            print("You recycled too much")
            return

        if turnResult:
            self.simulate(recycles,verbose=verbose)

        else:
            # End: draw from deck
            if len(self.trashPileDown) > 0:

                currentCard = self.trashPileDown.pop(0)
                currentCard.flip()
                self.trashPileUp.append(currentCard)
                print("Drawing new card: {0}".format(str(currentCard)))
                return self.simulate(recycles,verbose=verbose)
            else:
                if len(self.trashPileUp) > 1:
                    # recycle trash
                    self.trashPileDown = self.trashPileUp
                    self.trashPileUp = []
                    for i in self.trashPileDown:
                        i.flip()
                    #self.trashPileDown.extend([self.trashPileUp.pop(0).flip() for i in range(0, len(self.trashPileUp))])
                    print("Recycling deck")
                    recycles += 1
                    return self.simulate(recycles,verbose=verbose)
                elif verbose:
                    print("No more moves left!")
                return


    # Get all possible moves that can be made and add to a list of actions
    def getPossibleMoves(self):
        actions = []

        try:
            # 1. Find all possible moves between play piles
            for pile1 in self.playPiles:
                pile1_flipped_cards = pile1.getFlippedCards()

                # if a pile is empty and another pile has a king
                if len(pile1.cards) == 0:  # pile has no cards
                    for pile2 in self.playPiles:
                        if len(pile2.cards) > 1 and pile2.cards[0].value == "K":
                            # if there are unflipped cards left, give flip bonus +5 reward
                            if len(pile2.getFlippedCards()) < len(pile2.cards):
                                if not (pile2.getFlippedCards()[0].value == pile1.cards[0].value):
                                    actions.append(
                                        Action(pile2.getFlippedCards(), pile2, pile1, 1, flipBonus=True))  # seems ok?
                            elif len(pile2.getFlippedCards()) == len(pile2.cards):
                                if not (pile2.getFlippedCards()[0].value == pile1.cards[0].value):
                                    actions.append(Action(pile2.getFlippedCards(), pile2, pile1, 1))

                # iterate through every other pile
                if len(pile1_flipped_cards) > 0:
                    for pile2 in self.playPiles:
                        pile2_flipped_cards = pile2.getFlippedCards()
                          

                        #if they're different piles and pile2 has any faceup cards
                        if pile2 is not pile1 and len(pile2_flipped_cards) > 0:
                            #iterate through every possible upward facing stack in pile1
                            for transfer_cards_size in range(1, len(pile1_flipped_cards) + 1):
                                cards_to_transfer = pile1_flipped_cards[:transfer_cards_size]
                              #if end of pile2 can be appended by top of a pile1 pile add it to actions
                                if self.checkCardOrder(pile2.cards[0], cards_to_transfer[-1]):
                                    #if the move opens a card to be flipped, give flip bonus +5 reward
                                    if (len(cards_to_transfer) == len(pile1_flipped_cards)) and not len(pile1_flipped_cards)==len(pile1.cards):
                                        actions.append(Action(reversed(cards_to_transfer),pile1,pile2,1,flipBonus=True))
                                    else:
                                        actions.append(Action(reversed(cards_to_transfer), pile1, pile2, 1))

            #2. Find all moves from play piles to blocks
            for pile in self.playPiles:
                if len(pile.cards) > 0:
                    add = self.canAddToBlock(pile.cards[0])
                    if add:
                        #if the move opens a card to be flipped, give flip bonus +5 reward
                        if len(pile.getFlippedCards()) == 1 and len(pile.cards) > 1:
                            actions.append(Action(pile.cards[0], pile, add,2,flipBonus=True))
                        else:
                            actions.append(Action(pile.cards[0], pile, add, 2))

            # 3. Find all moves from blocks to play piles (negative reward)
            for suit in self.suits:
                if len(self.blockPiles[suit].cards) > 0:
                    add = self.canMoveBlockToPile(self.blockPiles[suit].cards[0])
                    if add:
                        for dest in add:
                            actions.append(Action(self.blockPiles.get(suit).cards[0], self.blockPiles[suit], dest, 3))

            # 4. Check if can draw card from waste pile
            if len(self.trashPileDown) > 0:
                actions.append(Action([self.trashPileDown[0]], self.trashPileDown, self.trashPileUp, 4))

            # 5. Check if can recycle waste pile
            if len(self.trashPileDown) < 1:
                # recycle trash
                # for now, we represent this action as (None, self.trashPileUp, self.trashPileDown)
                actions.append(Action(None, self.trashPileUp, self.trashPileDown, 5))

            # 6. Find all moves from trash to play piles
            for pile in self.playPiles:
                if len(self.trashPileUp) > 0:
                    if len(pile.cards) == 0 and self.trashPileUp[-1].value == 'K':
                        actions.append(Action([self.trashPileUp[-1]], self.trashPileUp, pile, 6))

                    if len(pile.cards) > 0:
                        add = self.checkCardOrder(pile.cards[0], self.trashPileUp[-1])
                        if add:
                            actions.append(Action([self.trashPileUp[-1]], self.trashPileUp, pile, 6))

            # 7. Find all moves from trash to blocks
            if len(self.trashPileUp) > 0:
                add = self.canAddToBlock(self.trashPileUp[-1])
                if add:
                    actions.append(Action([self.trashPileUp[-1]], self.trashPileUp, add, 7))

            # check all actions are legal - in particular, we want to stop trying to move a card onto itself
            for a in actions:
                if a.id != 4 and a.id != 5:
                    if len(a.target.cards) > 0 and a.card[0].value == a.target.cards[0].value:
                        actions.remove(a)
        except:
            pass

        return actions

#################################################################################

    #1. Move a card between two piles - no reward
    def moveBetweenPiles(self,movingCards,origin,dest):

        for card in movingCards:
            dest.addCard(card)
            origin.cards.pop(0)

        #print("Moved between piles")

        if len(origin.cards) > 0 and not origin.cards[0].flipped:
            origin.cards[0].flip()
            return 5
        else:
            return 0

    #2. Move a card from pile to block - reward 10
    def movePileToBlock(self,movingCards,origin,dest):

        self.addToBlock(movingCards)
        origin.cards.pop(0)
        #print("Adding play pile card to block: {0}".format(str(movingCards)))

        #+5 reward if moving card causes a flip
        if len(origin.cards) > 0 and not origin.cards[0].flipped:
            origin.cards[0].flip()
            return 15
        else:
            return 10

    #3. Move a card from block back to pile - reward -15
    def moveBlockToPile(self,movingCards,origin,dest):
        origin.cards.pop(0)
        dest.addCard(movingCards)
        #print("Moving card from block to pile: {0}".format(str(movingCards)))
        return -15

    #4. Draw a card from the deck - no reward
    def drawDeck(self,movingCards,origin,dest):
        self.trashPileDown.pop(0)
        movingCards.flip()
        self.trashPileUp.append(movingCards)
        #print("drew {0} from deck".format(str(movingCards)))
        return 0


    #5. Recycle deck - reward -100
    def recycleDeck(self):
        self.trashPileDown = self.trashPileUp
        self.trashPileUp = []
        for i in self.trashPileDown:
            i.flip()
        #print("Recycling deck")
        return -100

    #6. Move a card from waste to pile - reward 5
    def wasteToPile(self,movingCards,origin,dest):
        dest.addCard(movingCards)
        self.trashPileUp.pop(-1)
        #print("Moving {0} from Deck to Pile".format(str(movingCards)))
        return 5

    #7. Move a card from waste to block - reward 10
    def wasteToBlock(self,movingCards,origin,dest):
        self.addToBlock(movingCards)
        self.trashPileUp.pop(-1)
        #print("Adding card from deck to block: {0}".format(str(movingCards)))
        return 10

    def make_move(self,action):

        movingCards = action.card
        origin = action.pile
        dest = action.target

        if action.id == 1:
            return self.moveBetweenPiles(movingCards,origin,dest)

        elif action.id == 2:
            return self.movePileToBlock(movingCards,origin,dest)

        elif action.id == 3:
            return self.moveBlockToPile(movingCards,origin,dest)

        elif action.id == 4:
            return self.drawDeck(movingCards[0],origin,dest)

        elif action.id == 5:
            return self.recycleDeck()

        elif action.id == 6:
            return self.wasteToPile(movingCards[0],origin,dest)

        elif action.id == 7:
            return self.wasteToBlock(movingCards[0],origin,dest)


    def get_predicted_reward(self, action):
        if action.id == 1:
            return 2.5

        elif action.id == 2:
            return 12.5

        elif action.id == 3:
            return -15

        elif action.id == 4:
            return -10

        elif action.id == 5:
            return -100

        elif action.id == 6:
            return 5

        elif action.id == 7:
            return 10

    def test_move(self, action):
        # test a move and get back the reward and what the game state WOULD BE if that move were taken

        test_game = deepcopy(self)

        reward = test_game.make_move(action)

        return reward, test_game

