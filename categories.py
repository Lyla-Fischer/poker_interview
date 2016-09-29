from enum import Enum #note that the installed package needs to be enum32, not the default enum
import heapq
from collections import defaultdict, namedtuple

from ordered_enum import OrderedEnum

Card = namedtuple('Card', ['rank', 'suit'])
Rank = OrderedEnum("Rank", "2 3 4 5 6 7 8 9 10 J Q K A")
Suit = Enum("Suit", "S H D C")
def makeCard(cardString):
    """ card strings come in the form "JH", "4C", "4S", "JC", "9H" """
    return Card(Rank[cardString[:-1]], Suit[cardString[-1]])
Card.__str__ = lambda card: card.rank + card.suit

RankCount = namedtuple("RankCount", ['rank', 'count', 'cards'])
def count_ranks(cards):
    """
    Return a list of RankCount objects according to the number of cards of each rank in the input
    cards - an array of Card objects
    """
    rank_counts = defaultdict(list)
    for card in cards:
        rank_counts[card.rank].append(card)

    return [RankCount(rank, len(cards), cards) for rank, cards in rank_counts.items()]



class Hand:
    Categories = OrderedEnum("Categories", "high_card pair two_pair three_of_a_kind straight flush full_house four_of_a_kind straight_flush")
    hand_size = 5

    def __init__(self, cards):
        """
        Initialize a Hand object
        cards - an array of cards in the form ["JH", "4C", "4S", "JC", "9H"]
        """

        self.cards = [makeCard(card) for card in cards]

        self.category = Hand.Categories.high_card

        #non-multiple-based hands
        if self.is_flush(self.cards):
            if self.is_straight(self.cards):
                self.category = Hand.Categories.straight_flush
            else:
                self.category = Hand.Categories.flush # four_of_a_kind and full_house are impossible if it is a flush
        elif self.is_straight(self.cards):
            self.category = Hand.Categories.straight # multiples are impossible in a straight, and we ruled out flushes

        #everything else is a multiple-based hand
        rank_counts = count_ranks(self.cards)
        sorted_multiples = sorted(rank_counts, key=lambda count_tuple:(count_tuple.count,count_tuple.rank))

        highest_multiple = sorted_multiples.pop()
        self.tie_breaks = []
        if highest_multiple.count == 4:
            self.category = Hand.Categories.four_of_a_kind
            self.tie_breaks = [highest_multiple]

        elif highest_multiple.count == 3:
            minor_multiple = sorted_multiples.pop()
            if minor_multiple.count == 2:
                self.category = Hand.Categories.full_house
                self.tie_breaks = [highest_multiple, minor_multiple]
            else:
                self.category = Hand.Categories.three_of_a_kind
                self.tie_breaks = [highest_multiple]
                sorted_multiples.append(minor_multiple) # because we didn't use it

        elif highest_multiple.count == 2:
            minor_multiple = sorted_multiples.pop()
            if minor_multiple.count == 2:
                self.category = Hand.Categories.two_pair
                self.tie_breaks = [highest_multiple, minor_multiple]
            else:
                self.category = Hand.Categories.pair
                self.tie_breaks = [highest_multiple]
                sorted_multiples.append(minor_multiple) # because we didn't use it

        else:
            sorted_multiples.append(highest_multiple) # we never actually used it, so we put it back


        sorted_rank = sorted(sorted_multiples) # everything that wasn't popped based off of multiples will be sorted by rank, now
        while self._num_card_rep(self.tie_breaks) < self.hand_size:
            self.tie_breaks.append(sorted_rank.pop())

    def __cmp__(self, other):
        return cmp((self.category, self.tie_breaks), (other.category, other.tie_breaks))

    @staticmethod
    def _num_card_rep(counts):
        """
        Return the total number of cards that are included for consideration of tie breaks

        Keyword Arguments:
        counts - an array of RankCount objects
        """
        return sum(rank_count.count for rank_count in counts)

    @staticmethod
    def is_flush(cards):
        """ 
        Return boolean of whether the cards array is all the same suit.

        Keyword Arguments:
        cards - an array of Card objects
        """
        suit = cards[0][-1]
        for card in cards:
            if not card[-1] == suit:
                return False
        return True 

    @staticmethod
    def is_straight(cards):
        """ 
        Return boolean of whether the Cards array is made of consecutive ranks.

        Keyword Arguments:
        cards - an array of Card or RankCount objects
        """
        sorted_cards = sorted([card.rank.value for card in cards])
        for i in range(len(sorted_cards)-1):
            if not (sorted_cards[i] + 1 == sorted_cards[i+1]):
                return False
        return True


