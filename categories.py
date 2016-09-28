from enum import Enum #note that the installed package needs to be enum32, not the default enum
import heapq
from collections import defaultdict, namedtuple
from ordered_enum import OrderedEnum

Card = namedtuple('Card', ['rank', 'suit'])
RankCount = namedtuple("RankCount", ['rank', 'count'])
Rank = OrderedEnum("Rank", "2 3 4 5 6 7 8 9 10 J Q K A")
Suit = Enum("Suit", "S H D C")

class Hand:
    Categories = OrderedEnum("Categories", "high_card pair two_pair three_of_a_kind straight flush full_house four_of_a_kind straight_flush")
    hand_size = 5

    def __init__(self, cards):

        cards = self.normalize_cards(cards)

        self.category = Hand.Categories.high_card

        #non-multiple-based hands
        if self.is_flush(cards):
            if self.is_straight(cards):
                self.category = Hand.Categories.straight_flush
            else:
                self.category = Hand.Categories.flush # four_of_a_kind and full_house are impossible if it is a flush
        elif self.is_straight(cards):
            self.category = Hand.Categories.straight # multiples are impossible in a straight, and we ruled out flushes

        #everything else is a multiple-based hand
        rank_count = self.rank_count(cards)
        sorted_multiples = sorted(rank_count.items(), key=lambda count_tuple:(count_tuple[1],count_tuple[0]))

        highest_multiple = sorted_multiples.pop()
        self.tie_breaks = []
        if highest_multiple[1] == 4:
            self.category = Hand.Categories.four_of_a_kind
            self.tie_breaks = [highest_multiple]

        elif highest_multiple[1] == 3:
            minor_multiple = sorted_multiples.pop()
            if minor_multiple[1] == 2:
                self.category = Hand.Categories.full_house
                self.tie_breaks = [highest_multiple, minor_multiple]
            else:
                self.category = Hand.Categories.three_of_a_kind
                self.tie_breaks = [highest_multiple]
                sorted_multiples.append(minor_multiple) # because we didn't use it

        elif highest_multiple[1] == 2:
            minor_multiple = sorted_multiples.pop()
            if minor_multiple[1] == 2:
                self.category = Hand.Categories.two_pair
                self.tie_breaks = [highest_multiple, minor_multiple]
            else:
                self.category = Hand.Categories.pair
                self.tie_breaks = [highest_multiple]
                sorted_multiples.append(minor_multiple) # because we didn't use it

        else:
            sorted_multiples.append(highest_multiple) # we never actually used it, so we put it back


        sorted_rank = sorted(sorted_multiples) # everything that wasn't popped based off of multiples will be sorted by rank, now
        while self.num_tie_breaks(self.tie_breaks) < self.hand_size:
            self.tie_breaks.append(sorted_rank.pop())

    def __cmp__(self, other):
        return cmp((self.category, self.tie_breaks), (other.category, other.tie_breaks))

    @staticmethod
    def rank_count(cards):
        """
        Return a dictionary with key:index of Rank:num_cards

        Keyword Arguments:
        cards - an array of Card objects
        """
        rank_count = defaultdict(int)
        for card in cards:
            rank_count[card[0:-1]] += 1 
        return rank_count

    @staticmethod
    def num_tie_breaks(tie_breaks):
        """
        Return the total number of cards that are included for consideration of tie breaks

        Keyword Arguments:
        tie_breaks - an array of tuples of the form (card, count)
        """
        return sum(tie_break[1] for tie_break in tie_breaks)

    @staticmethod
    def is_flush(cards):
        """ 
        Return boolean of whether the cards array is a flush.

        Keyword Arguments:
        cards - an array of cards in the form ["JH", "4C", "4S", "JC", "9H"]
        """
        suit = cards[0][-1]
        for card in cards:
            if not card[-1] == suit:
                return False
        return True 

    @staticmethod
    def is_straight(cards):
        """ 
        Return boolean of whether the cards array is a straight.

        Keyword Arguments:
        cards - an array of Card objects
        """
        sorted_cards = sorted([card.rank.value for card in cards])
        for i in range(len(sorted_cards)-1):
            if not (sorted_cards[i] + 1 == sorted_cards[i+1]):
                return False
        return True

    @staticmethod
    def normalize_cards(cards):
        """ 
        Return an array of Card objects

        Keyword Arguments:
        cards - an array of cards in the form ["JH", "4C", "4S", "JC", "9H"]
        """
        return [Card(Rank[card[:-1]], Suit[card[-1]]) for card in cards]


