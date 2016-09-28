# def test_categories:
	

# ["5S", "5H", "5D", "4S", "4H", "4D", "3D", "3S"] 

import unittest

from categories import Hand

class TestHand(unittest.TestCase):

    # def test_heap_multiples(self):
    # 	heaped_multiples = Hand.heap_multiples({"J":4, "2":3})
    # 	print heaped_multiples
    # 	self.assertEqual(heaped_multiples, [(4, "J"), (3,"2")], "failure in heap_multiples")

    def test_rank_count(self):
    	hand = ["JH", "4C", "4S", "JC", "9H"] 
    	rank_count = Hand.rank_count(hand)
    	self.assertEqual(rank_count, {'4':2, 'J':2, '9':1})

    def test_num_tie_breaks(self):
    	tie_breaks = [('4',3)] 
    	num_tie_breaks = Hand.num_tie_breaks(tie_breaks)
    	self.assertEqual(num_tie_breaks, 3)

    	tie_breaks = [('4',3), ('J',1)] 
    	num_tie_breaks = Hand.num_tie_breaks(tie_breaks)
    	self.assertEqual(num_tie_breaks, 4)

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

    def test_cmp(self):
    	pair_to_high_card = Hand(["JH", "JC", "QS", "5D", "9H"]) < Hand(["JH", "3C", "4S", "5C", "9H"])
    	self.assertEqual(pair_to_high_card, False)

    	straight_to_flush = Hand(["10H", "6S", "9D", "8S", "7S"]) < Hand(["10S", "9S", "8S", "5S", "6S"])
    	self.assertEqual(straight_to_flush, True)


    def test_deck_validation(self):
    	"""
    	Test with some hands that are impossible to form with a 52-card deck
    	Five-of-a-kind
    	Something that is both a flush and has a pair
    	Something that is both a flush and four-of-a-kind
    	"""
    	pass

if __name__ == '__main__':
    unittest.main()