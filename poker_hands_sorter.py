import sys
from collections import OrderedDict


class PokerHand:
    def __init__(self, player_id, cards):
        self.cards = cards
        self.player_id = player_id
        # map cards
        self.map = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
        self.rank_label_map = {'1': 'High Card', '2': 'Pair', '3': 'Two Pairs', '4': 'Three of a kind',
                               '5': 'Straight', '6': 'Flush', '7': 'Full House', '8': 'Four of a kind',
                               '9': 'Straight Flush', '10': 'Royal Flush'}
        self.num_cards = self.__map_cards(self, cards)
        self.num_cards = self.__sort_cards(self.num_cards)
        self.rank, self.key_cards = self.__calculate_rank(self)
        self.rank_label = self.__get_rank_label(self, self.rank)

    @staticmethod
    def __get_rank_label(self, rank):
        return self.rank_label_map[rank]

    @staticmethod
    def __sort_cards(cards):
        return sorted(cards, key=lambda x: int(x[:-1]))

    @staticmethod
    def __map_cards(self, cards):
        return [self.map[i[0]] + i[1] if i[0] in list(self.map.keys()) else i for i in cards]

    @staticmethod
    def __check_straight(self):
        vals = [int(i[:-1]) for i in self.num_cards]
        prev_val = vals[0]
        for val in vals[1:]:
            if val != prev_val + 1:
                return False
            prev_val += 1
        return True

    @staticmethod
    def __check_same_val(cards):
        return len(set([i[:-1] for i in cards])) == 1

    @staticmethod
    def __check_same_suit(cards):
        return len(set([i[-1] for i in cards])) == 1

    @staticmethod
    def __check_n_same_val_cards(self, cards, n):
        """ """
        possible_pairs = [cards[i - n:i] for i in range(len(cards) + 1) if i >= n]
        same_val_cards = []
        for pair in possible_pairs:
            if self.__check_same_val(pair):
                same_val_cards += pair

        # check if appended pairs doesn't have duplicates
        same_val_cards = list(OrderedDict.fromkeys(same_val_cards)) \
            if len(list(OrderedDict.fromkeys(same_val_cards))) % n == 0 else []
        return same_val_cards

    @staticmethod
    def __check_full_house(self):
        three_of_a_kind = self.__check_n_same_val_cards(self, self.num_cards, 3)
        if len(three_of_a_kind) > 0:
            cards = self.num_cards.copy()
            [cards.remove(i) for i in three_of_a_kind]
            if self.__check_n_same_val_cards(self, cards, 2):
                return cards
        return []

    @staticmethod
    def __check_straight_flush(self):
        if self.__check_same_suit(self.num_cards) and self.__check_straight(self):
            return self.num_cards
        return []

    @staticmethod
    def __check_royal_flush(self):
        royals = list(range(10, 15))
        if not self.__check_same_suit(self.num_cards):
            return []
        for i in self.num_cards:
            if int(i[:-1]) not in royals:
                return []
        return self.num_cards

    @staticmethod
    def __calculate_rank(self):
        # check royal flush
        key_cards = self.__check_royal_flush(self)
        if key_cards:
            return '10', key_cards

        # check straight flush
        key_cards = self.__check_straight_flush(self)
        if key_cards:
            return '9', key_cards

        # check four of a kind
        key_cards = self.__check_n_same_val_cards(self, self.num_cards, 4)
        if key_cards:
            return '8', key_cards

        # check full house
        key_cards = self.__check_full_house(self)
        if key_cards:
            return '7', key_cards

        # check flush
        key_cards = self.__check_same_suit(self.num_cards)
        if key_cards:
            return '6', self.num_cards

        # check straight
        key_cards = self.__check_straight(self)
        if key_cards:
            return '5', self.num_cards

        # check three of a kind
        key_cards = self.__check_n_same_val_cards(self, self.num_cards, 3)
        if key_cards:
            return '4', key_cards

        # check two different pairs
        key_cards = self.__check_n_same_val_cards(self, self.num_cards, 2)
        if len(key_cards) > 2:
            return '3', key_cards

        # check pair
        key_cards = self.__check_n_same_val_cards(self, self.num_cards, 2)
        if key_cards:
            return '2', key_cards

        # return highest value card
        return '1', [self.num_cards[-1]]


class Sorter:
    def __init__(self, hand1, hand2):
        self.hand1 = hand1
        self.hand2 = hand2
        self.winner_hand = None

    @staticmethod
    def __get_max_val_cards_id(cards1, cards2):
        # assumes sorted in order and has same length
        if len(cards1) != len(cards2):
            return None
        cards1 = sorted(cards1, key=lambda x: int(x[:-1]), reverse=True)
        cards2 = sorted(cards2, key=lambda x: int(x[:-1]), reverse=True)
        for i in range(len(cards1)):
            if int(cards1[i][:-1]) == int(cards2[i][:-1]):
                continue
            elif int(cards1[i][:-1]) > int(cards2[i][:-1]):
                return 0
            else:
                return 1
        return None

    def get_winner_hand(self):
        player_hands = [self.hand1, self.hand2]
        if self.hand1.rank == self.hand2.rank:
            winner_hand_ind = self.__get_max_val_cards_id(self.hand1.key_cards, self.hand2.key_cards)
            if winner_hand_ind is not None:
                self.winner_hand = player_hands[winner_hand_ind]
            else:
                # get remaining cards player 1
                player_1_remaining_cards = player_1_hand.num_cards
                [player_1_remaining_cards.remove(i) for i in player_1_hand.key_cards]
                # get remaining cards player 2
                player_2_remaining_cards = player_2_hand.num_cards
                [player_2_remaining_cards.remove(i) for i in player_2_hand.key_cards]
                winner_hand_ind = self.__get_max_val_cards_id(player_1_remaining_cards, player_2_remaining_cards)
                if winner_hand is not None:
                    self.winner_hand = player_hands[winner_hand_ind]
        else:
            ranks = [player_1_hand.rank, player_2_hand.rank]
            self.winner_hand = player_hands[ranks.index(max(ranks))]
        return self.winner_hand


if __name__ == '__main__':
    poker_hands = sys.stdin.read().splitlines()
    player_1_wins = 0
    player_2_wins = 0
    for hand in poker_hands:
        # hand = '4H 4C 6S 7S KD 2C 3S 9S 9D TD'
        player_1_cards = hand.split(' ')[:5]
        player_2_cards = hand.split(' ')[5:]
        player_1_hand = PokerHand(1, player_1_cards)
        player_2_hand = PokerHand(2, player_2_cards)
        # print('-------------------------')
        # print(f'player 1 cards: {player_1_hand.cards} | Player 1 rank: {player_1_hand.rank_label}')
        # print(f'player 2 cards: {player_2_hand.cards} | Player 2 rank: {player_2_hand.rank_label}')
        sorter = Sorter(player_1_hand, player_2_hand)
        winner_hand = sorter.get_winner_hand()
        if winner_hand:
            if winner_hand.player_id == 1:
                player_1_wins += 1
            else:
                player_2_wins += 1
        # print(f"WINNER: {'Player ' + str(winner_hand.player_id) if winner_hand else 'Tie'}")

    print('---------------RESULTS---------------')
    print('Player 1', player_1_wins)
    print('Player 2', player_2_wins)
