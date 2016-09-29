# def test_categories:
	

# ["5S", "5H", "5D", "4S", "4H", "4D", "3D", "3S"] 

import unittest

from categories import Hand, makeCard, Rank, count_ranks, RankCount, max_straight

class TestHand(unittest.TestCase):

    # def test_heap_multiples(self):
    # 	heaped_multiples = Hand.heap_multiples({"J":4, "2":3})
    # 	print heaped_multiples
    # 	self.assertEqual(heaped_multiples, [(4, "J"), (3,"2")], "failure in heap_multiples")

    def test_max_straight(self):
    	cards = map(makeCard, ["10S", "6S", "9S", "8S", "7S"])
    	straight = max_straight(cards)
    	self.assertEqual(straight, sorted(map(makeCard, ["10S", "6S", "9S", "8S", "7S"]), reverse=True))

    	cards = map(makeCard, ["10S", "6S", "9S", "8S", "8C", "7S"])
    	straight = max_straight(cards)
    	self.assertEqual(straight, sorted(map(makeCard, ["10S", "6S", "9S", "8S", "7S"]), reverse=True))

    	cards = map(makeCard, ["10S", "6S", "9S", "8S", "5C", "7S"])
    	straight = max_straight(cards)
    	self.assertEqual(straight, sorted(map(makeCard, ["10S", "6S", "9S", "8S", "7S"]), reverse=True))

    def test_categories(self):

    	my_hand = Hand(["KH", "QH", "JH", "AH", "10H"])
    	self.assertEqual(my_hand.category, Hand.Categories.straight_flush)

    	my_hand = Hand(["10S", "6S", "9S", "8S", "7S"])
    	self.assertEqual(my_hand.category, Hand.Categories.straight_flush)

    	my_hand = Hand(["JH", "JC", "9H", "JS", "JD"])
    	self.assertEqual(my_hand.category, Hand.Categories.four_of_a_kind)

    	my_hand = Hand(["JH", "JC", "JS", "9D", "9H"])
    	self.assertEqual(my_hand.category, Hand.Categories.full_house)

    	my_hand = Hand(["10S", "9S", "8S", "5S", "6S"])
    	self.assertEqual(my_hand.category, Hand.Categories.flush)

    	my_hand = Hand(["10H", "6S", "9D", "8S", "7S"])
    	self.assertEqual(my_hand.category, Hand.Categories.straight)

    	my_hand = Hand(["JH", "JC", "9H", "JS", "8D"])
    	self.assertEqual(my_hand.category, Hand.Categories.three_of_a_kind)

    	my_hand = Hand(["JH", "JC", "QS", "9D", "9H"])
    	self.assertEqual(my_hand.category, Hand.Categories.two_pair)

    	my_hand = Hand(["JH", "JC", "QS", "5D", "9H"])
    	self.assertEqual(my_hand.category, Hand.Categories.pair)

    	my_hand = Hand(["JH", "3C", "4S", "5C", "9H"])
    	self.assertEqual(my_hand.category, Hand.Categories.high_card)

    def test_category_options(self):

    	my_hand = Hand(["10H", "6S", "9D", "8S", "7S", "7D", "7H"])
    	self.assertEqual(my_hand.category, Hand.Categories.straight)

    	my_hand = Hand(["10H", "6S", "9D", "8S", "7S", "7D", "7H", "7C"])
    	self.assertEqual(my_hand.category, Hand.Categories.four_of_a_kind)

    	my_hand = Hand(["10H", "6S", "9D", "8S", "7S", "7D", "7H", "8C"])
    	self.assertEqual(my_hand.category, Hand.Categories.full_house)

    	my_hand = Hand(["10S", "9S", "8S", "5S", "6S", "10H", "6D", "9D", "8C", "7C"])
    	self.assertEqual(my_hand.category, Hand.Categories.flush)

    	my_hand = Hand(["KH", "QH", "JH", "AH", "10H", "10S", "6S", "9S", "8S", "7S"])
    	self.assertEqual(my_hand.category, Hand.Categories.straight_flush)
    	# It gets the royal flush

    	my_hand = Hand(["5S", "5H", "5D", "4S", "4H", "4D", "3D", "3S"])
    	self.assertEqual(my_hand.category, Hand.Categories.full_house)
    	# It gets the fours

    	my_hand = Hand(["5S", "5H", "5D", "5C", "4S", "4H", "3C", "3D", "3S"])
    	self.assertEqual(my_hand.category, Hand.Categories.four_of_a_kind)
    	# get the 4 kicker



    def test_cmp(self):
    	pair_to_high_card = Hand(["JH", "JC", "QS", "5D", "9H"]) < Hand(["JH", "3C", "4S", "5C", "9H"])
    	self.assertEqual(pair_to_high_card, False)

    	straight_to_flush = Hand(["10H", "6S", "9D", "8S", "7S"]) < Hand(["10S", "9S", "8S", "5S", "6S"])
    	self.assertEqual(straight_to_flush, True)


    def test_deck_validation(self):
    	"""
    	Test with some hands that are impossible to form with a 52-card deck
    	Five-of-a-kind
    	Something that is both a flush and has a pair (flush wins)
    	Something that is both a flush and four-of-a-kind (four-of-a-kind wins)
    	"""
    	pass

if __name__ == '__main__':
    unittest.main()