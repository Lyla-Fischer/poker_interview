from enum import Enum #note that the installed package needs to be enum32, not the default enum
import heapq
from collections import defaultdict, namedtuple

from ordered_enum import OrderedEnum

Card = namedtuple('Card', ['rank', 'suit'])
Rank = OrderedEnum("Rank", "2 3 4 5 6 7 8 9 10 J Q K A")
Rank.__str__ = lambda rank: rank.name
Suit = Enum("Suit", "S H D C")
def makeCard(cardString):
    """ card strings come in the form "JH", "4C", "4S", "JC", "9H" """
    return Card(Rank[cardString[:-1]], Suit[cardString[-1]])
Card.__str__ = lambda card: card.rank.name + card.suit.name

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


SuitCount = namedtuple("SuitCount", ['suit', 'count', 'cards'])
def count_suits(cards):
    """
    Return a list of SuitCount objects according to the number of cards of each suit in the input
    cards - an array of Card objects
    """
    suit_counts = defaultdict(list)
    for card in cards:
        suit_counts[card.suit].append(card)

    return [RankCount(suit, len(cards), cards) for suit, cards in suit_counts.items()]


def get_kickers(binned_multiples, num_kickers):
    """
    Return the highest num_kickers Cards represented in binned_multiples, an array of RankCount objects
    """
    sorted_rank = sorted(binned_multiples) # everything that wasn't popped based off of multiples will be sorted by rank, now
    kickers = []
    while len(kickers) < num_kickers:
        num_needed = num_kickers - len(kickers)
        cards = sorted_rank.pop().cards
        num_available = len(cards)
        kickers += cards[ 0:min(num_needed, num_available)]
    return kickers


def max_straight(cards):
    """ 
    Return a list of cards which consitute a the maximum straight, if a straight is present in the input
    Otherwise, return None

    Keyword Arguments:
    cards - an array of Card objects
    """
    binned_cards = count_ranks(cards)
    sorted_cards = sorted([(card_class.value, cards) for card_class, num_cards, cards in binned_cards])
    
    i = 1
    my_straight = []
    my_straight.append(sorted_cards[-1][1][0])
    while (i < len(sorted_cards)) and (len(my_straight) < Hand.hand_size):
        this_rank = sorted_cards[-1-i]
        if not (this_rank[0] + 1 == my_straight[-1].rank.value):
            my_straight = []
        my_straight.append(this_rank[1][0])
        i+=1

    if len(my_straight) == Hand.hand_size:
        return my_straight
    else:
        return None


class Hand:
    Categories = OrderedEnum("Categories", "high_card pair two_pair three_of_a_kind straight flush full_house four_of_a_kind straight_flush")
    hand_size = 5

    def __init__(self, cards):
        """
        Initialize a Hand object
        cards - an array of cards in the form ["JH", "4C", "4S", "JC", "9H"]
        """

        self.cards = [makeCard(card) for card in cards]


        sorted_multiples = sorted(count_ranks(self.cards), key=lambda count_tuple:(count_tuple.count, count_tuple.rank))
        major_multiple = sorted_multiples.pop()
        #In the case of a full house, it doesn't matter if there is three of a lower rank, we still use the higher rank
        minor_multiple_candidates = sorted([rank_count for rank_count in sorted_multiples if rank_count.count >= 2])
        minor_multiple = minor_multiple_candidates[-1] if len(minor_multiple_candidates) > 0 else None
        self.tie_breaks = []

        suit_counts = count_suits(self.cards)
        straight_flushes = [max_straight(cards) for suit, count, cards in suit_counts if count >= Hand.hand_size]
        flushes = [sorted(cards, reverse=True) for suit, count, cards in suit_counts if count >= Hand.hand_size]
        straight = max_straight(self.cards)
        if len(filter(None, straight_flushes)) > 0:
            self.category = self.Categories.straight_flush
            self.final_hand = max(straight_flushes)
            self.tie_breaks = max(self.final_hand)

        elif major_multiple.count == 4:
            self.category = Hand.Categories.four_of_a_kind
            kickers = get_kickers(sorted_multiples, 1)
            self.final_hand = major_multiple.cards + kickers
            self.tie_breaks = [major_multiple] + kickers

        elif (major_multiple.count == 3) and minor_multiple:
            self.category = Hand.Categories.full_house
            self.final_hand = major_multiple.cards + minor_multiple.cards
            self.tie_breaks = [major_multiple, minor_multiple]

        elif flushes:
            self.category = self.Categories.flush
            self.final_hand = max(flushes)
            self.tie_breaks = self.final_hand # This has already been sorted 

        elif straight:
            self.category = self.Categories.straight
            self.final_hand = straight
            self.tie_breaks = max(self.final_hand)

        elif major_multiple.count == 3:
            self.category = Hand.Categories.three_of_a_kind
            kickers = get_kickers(sorted_multiples, 2)
            self.final_hand = major_multiple.cards + kickers
            self.tie_breaks = [major_multiple] + kickers

        elif (major_multiple.count == 2):
            minor_multiple = sorted_multiples.pop()
            if minor_multiple.count == 2:
                self.category = Hand.Categories.two_pair
                kickers = get_kickers(sorted_multiples, 1)
                self.final_hand = major_multiple.cards + minor_multiple.cards + kickers
                self.tie_breaks = [major_multiple, minor_multiple] + kickers

            else:
                self.category = Hand.Categories.pair
                sorted_multiples.append(minor_multiple) # because we didn't use it
                kickers = get_kickers(sorted_multiples, 3)
                self.final_hand = major_multiple.cards + kickers
                self.tie_breaks = [major_multiple] + kickers
        else:
            self.category = Hand.Categories.high_card
            sorted_multiples.append(major_multiple) # we never actually used it, so we put it back
            kickers = get_kickers(sorted_multiples, 5)
            self.final_hand = kickers
            self.tie_breaks = kickers


    def __cmp__(self, other):
        return cmp((self.category, self.tie_breaks), (other.category, other.tie_breaks))

    def __str__(self):
        return str([str(card) for card in self.final_hand]) + ": " + self.category.name + ", " + str([str(repr.rank) for repr in self.tie_breaks])







