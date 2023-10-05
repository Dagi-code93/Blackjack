import random
import time
import os

class Cards:
    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
    ranks = ['narf', 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    def __init__(self, rank, suit):
        self.suit = self.suits[suit]
        self.rank = self.ranks[rank]

    def get_value(self, rank):
        self.value = rank
        the_index = self.ranks.index(self.value)
        if the_index > 1 and the_index < 10:
            return the_index
        elif the_index >= 10:
            return 10
        elif the_index == 1:
            return 11
        else:
            print('Error unknown rank')

    def get_rank(self):
        return self.rank
    
    def __str__(self):
        return self.rank + ' Of ' + self.suit

class Deck(Cards):
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                self.cards.append(Cards(rank, suit))

    def shuffle(self):
        rng = random.Random()
        rng.shuffle(self.cards)
        
    def multiply(self, num_decks):
        for i in range(num_decks - 1):
            for suit in range(4):
                for rank in range(1,14):
                    self.cards.append(Cards(rank, suit))

    def isempty(self):
        return self.cards == []
    
    def number_of_cards_left(self):
        return len(self.cards)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    def pop(self):
        return self.cards.pop()

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.isempty():
                break
            card = self.pop()
            hand = hands[i % num_hands]
            hand.add(card)
     
    def __str__(self): 
        s = ''
        for i in range(len(self.cards)):
            s = s + '-' * i + str(self.cards[i]) + '\n'   
        return s


class Player(Deck):
    def __init__(self, name='Player'):
        self.cards = []
        self.name = name
    
    def add(self, card):
        self.cards.append(card)
 
    def __str__(self):
        s = 'Hand ' + self.name
        if self.isempty():
            s += ' is empty\n'
        else:
            s += ' contains\n'     
        return s + Deck.__str__(self)
    
class Dealer(Deck):
    def __init__(self):
        self.cards = []
        self.name = 'Dealer' 
        self.temp = ''
        
    def add(self, card):
        self.cards.append(card)

    def hide_second_deal(self):
        self.temp = self.cards[1]
        self.cards[1] = 'UNKNOWN'

    def reveal_second_deal(self):
        self.cards.append('')
        
    def __str__(self):
        s = 'Hand ' + self.name
        if self.isempty():
            s += ' is empty\n'
        else:
            if len(self.cards) == 2:
                s += ' contains\n'
                self.hide_second_deal()     
            elif len(self.cards) > 2:
                s += ' contains\n'
                self.cards[1] = self.temp
            else:
                s += ' contains\n'
        return s + Deck.__str__(self)
    
class cardGame(Cards):
    def __init__(self, num_decks, player_name):
        self.playing_deck = Deck()
        self.playing_deck.multiply(int(num_decks))
        self.playing_deck.shuffle()
        self.player = Player(player_name)
        self.dealer = Dealer()
        self.player_name = player_name
        self.dealer_name = self.dealer.name
        self.player_sum = 0
        self.dealer_sum = 0
        self.deal_player_round = 1
        self.deal_dealer_round = 1
        self.rank = 0

    def play_round(self):

        self.playing_deck.deal([self.dealer], 1)
        print(self.dealer)
        print('-------------------------------------------------------------')
        print('{} sum : {}'.format(self.dealer_name, self.keep_dealer_score()))
        print('-------------------------------------------------------------')

        time.sleep(1)
        
        self.playing_deck.deal([self.player], 1)
        print(self.player)
        print('-------------------------------------------------------------')
        print('{} sum : {}'.format(self.player_name, self.keep_player_score()))
        print('-------------------------------------------------------------')
        
        time.sleep(1)
        
        self.playing_deck.deal([self.dealer], 1)
        print(self.dealer)
        print('-------------------------------------------------------------')
        print('{} sum : UNKNOWN'.format(self.dealer_name))
        print('-------------------------------------------------------------')

        time.sleep(1)
        
        self.playing_deck.deal([self.player], 1)
        
    
    def keep_player_score(self):
        self.player_cards_left = self.player.number_of_cards_left()
        self.player_sum = 0
        if self.player_cards_left > 2:
            for i in self.player.cards:
                self.player_sum += self.playing_deck.get_value(i.get_rank())
            return self.player_sum
        else:
            for i in self.player.cards:
                self.player_sum += self.playing_deck.get_value(i.get_rank())
            return self.player_sum

    def keep_dealer_score(self):
        self.dealer_cards_left = self.dealer.number_of_cards_left()
        self.dealer_sum = 0
        if self.dealer_cards_left > 2:
            for i in self.dealer.cards:
                self.dealer_sum += self.playing_deck.get_value(i.get_rank())
            return self.dealer_sum
        else:
            try:
                self.dealer.cards.remove('UNKNOWN')
                self.dealer.add(self.dealer.temp)
                for i in self.dealer.cards:
                    self.dealer_sum += self.playing_deck.get_value(i.get_rank())
                return self.dealer_sum
            except:
                for i in self.dealer.cards:
                    self.dealer_sum += self.playing_deck.get_value(i.get_rank())
                return self.dealer_sum

    def first_deal_checkup(self):
        self.keep_dealer_score()
        self.keep_player_score()
        self.h_or_s = ''
        if self.player_sum == 21:
            print(self.player)
            self.dealer.reveal_second_deal()
            if self.dealer_sum < 21:
                print(self.dealer)
                self.playing_deck.deal([self.dealer], 1)
                print(self.dealer)
                self.first_deal_checkup()
                
            if self.dealer_sum == 21:
                print('-------The dealer also got a black jack so it is a draw --------')
            print('-------The dealer got {} so you win --------'.format(self.dealer_sum))
        elif self.player_sum < 21:
            print(self.player)
            print('-------------------------------------------------------------')
            print('{} sum : {}'.format(self.player_name, self.keep_player_score()))
            print('-------------------------------------------------------------')
            print('!-------------- So do you want to hit or stay(h/s)? ----------------------!')
            self.h_or_s = input('Hit or Stay >> ')
            if self.h_or_s.lower() == 'h':
                self.playing_deck.deal([self.player], 1)
                self.first_deal_checkup()
            elif self.h_or_s.lower() == 's':
                self.dealer.reveal_second_deal()
                print(self.dealer)
                if self.player_sum >= self.dealer_sum:
                    print('!-------------------The dealer has {} and you have {}.----------------------!'.format(self.dealer_sum,self.player_sum))
                    time.sleep(1)
                    print('!-------------------The dealer is going to HIT.----------------------!'.format(self.dealer_sum,self.player_sum))
                    self.playing_deck.deal([self.dealer], 1)
                    print(self.dealer)
                    self.keep_player_score()
                    
                else:
                    for i in self.player.cards:
                        self.rank = self.playing_deck.get_value(i.get_rank())
                        if self.rank == 11:
                            self.player_sum -= 10
                            self.first_deal_checkup()
                    print('!-------------------The dealer has {} and you have {}.----------------------!'.format(self.dealer_sum,self.player_sum))
                    print('------------------------------------------------------------------------------')
                    print('---------------So you LOSE and the dealer WINS.-------------')
                    print('------------------------------------------------------------------------------')
                        
        elif self.player_sum > 21:
            for i in self.player.cards:
                self.rank = self.playing_deck.get_value(i.get_rank())
                print('the rank : ' + str(self.rank))
                if self.rank == 11:
                    self.player_sum -= 10
            self.keep_player_score()
            if self.player_sum < 21:
                self.first_deal_checkup()
            print(self.player)
            print('-------------------------------------------------------------')
            print('{} sum : {}'.format(self.player_name, self.player_sum))
            print('-------------------------------------------------------------')
            print('!-------------------You Busted!!!----------------------!')
            self.dealer.reveal_second_deal()
            print(self.dealer)
            print('!-------------------The dealer has {} and you have so you lose.----------------------!'.format(self.dealer_sum,self.player_sum))

    def stay_dealer_move(self):
        del(self.dealer.cards[2])
        self.keep_player_score()
        self.keep_dealer_score()

        if self.player_sum >= self.dealer_sum and self.dealer_sum < 22 and self.player_sum < 22:
            print('!-------------------The dealer has {} and you have {}.----------------------!'.format(self.dealer_sum,self.player_sum))
            time.sleep(1)
            print('!-------------------The dealer is going to HIT.----------------------!'.format(self.dealer_sum,self.player_sum))
            self.playing_deck.deal([self.dealer], 1)
            print(self.dealer)
            self.stay_dealer_move()

        elif  (self.dealer_sum >= 22 and self.player_sum < 22):
            for i in self.dealer.cards:
                self.rank = self.playing_deck.get_value(i.get_rank())
                print('the rank : ' + str(self.rank))
                if self.rank == 11:
                    self.dealer_sum -= 10
            self.stay_dealer_move()
            print('!-------------------The dealer has {} and you have {}.----------------------!'.format(self.dealer_sum,self.player_sum))
            print('------------------------------------------------------------------------------')
            print('---------------So you WIN and the dealer LOSES.-------------')
            print('------------------------------------------------------------------------------') 
            
        elif self.player_sum < self.dealer_sum and self.dealer_sum < 22 and self.player_sum < 22:
            for i in self.player.cards:
                print('the rank : ' + str(self.rank))
                if self.rank == 11:
                    self.player_sum -= 10
            self.keep_dealer_score()
            self.stay_dealer_move()
            print('!-------------------The dealer has {} and you have {}.----------------------!'.format(self.dealer_sum,self.player_sum))
            print('------------------------------------------------------------------------------')
            print('---------------So you LOSE and the dealer WINS.-------------')
            print('------------------------------------------------------------------------------')

    def restart(self):
        print('----------------RESTARTING---------------------------')
        time.sleep(3)
        self.dealer.cards = []
        self.player.cards = []
        self.play_round()
        self.first_deal_checkup()
        self.restart()
    
name = input('Name : ')
decks = input('Num of Decks : ')
game = cardGame(decks, name)
game.play_round()
game.first_deal_checkup()
game.restart()

