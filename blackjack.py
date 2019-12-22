import random
import time
import json

suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

cards = []
for value in values:
	for suit in suits:
		cards.append(value + ' of ' + suit)

player_cards = []
computer_cards = []
players = ['COMPUTER', None]

class blackjack:

	def __init__(self, suits, values, cards, player_cards, computer_cards, players, turn = None, player_win_status = None, computer_win_status = None, player_key = None, computer_key = None):
		self.suits = suits
		self.values = values
		self.cards = cards
		self.player_cards = player_cards
		self.computer_cards = computer_cards
		self.players = players
		self.turn = turn
		save_file = open("money.json")		
		self.money_left = json.loads(save_file.read())
		self.player_win_status = None
		self.computer_win_status = None
		self.player_key = player_key
		self.computer_key = computer_key

	def start(self): 
		print("Hi mortal, welcome to a fun game of blackjack! You are going to lose all your money though, I'd bet!")
		global name		
		name = raw_input("What is your name?: ")
		self.players[1] = name
		print("Okay " + name + ", how much money are you willing to bet? You have " + str(self.money_left) + " dollars!")

		condition = True
		while condition:
			try:
				global money_bet
				money_bet = int(raw_input("Money bet: "))
				if money_bet > self.money_left:
					print("Please, you are not that rich.")
				elif money_bet < 1:
					print("You have to bet something, stop acting like you aren't a gambling addict.")
				else:	
					condition = False
			except ValueError:
				print("Seriously, do you not know what numbers are?")
	
		for i in range(2):
			card = random.choice(self.cards)
			self.player_cards.append(card)
			self.cards.remove(card)
			card = random.choice(self.cards)
			self.computer_cards.append(card)
			self.cards.remove(card)
		self.turn = name
		self.get_move()
		sum_of_computer_cards = self.get_move() #could be none or sum of cards
		self.get_winner(sum_of_computer_cards)

	def get_move(self):
		if self.turn == name:
			condition = True
			while condition:
				print self.player_cards
				sum_of_cards = self.count_cards(self.player_cards)
				print "Sum: " + str(sum_of_cards)
				self.player_win_status = self.check_win(self.player_cards)
				print "Would you like to draw another card? (y/n):"
				draw_another_card = raw_input("")
				if draw_another_card == 'y' or draw_another_card == 'Y':
					card = random.choice(self.cards)
					self.player_cards.append(card)
					self.cards.remove(card)
					condition = True
				elif draw_another_card == 'n' or draw_another_card == 'N':
					condition = False
				else:
					print("Only put y or n. It is that easy.")
					condition = True
			self.turn = 'COMPUTER'

		elif self.turn == 'COMPUTER':
			sum_of_cards = 0
			condition = True
			while condition:
				self.computer_win_status = self.check_win(self.computer_cards)
				sum_of_cards = self.count_cards(self.computer_cards)
				if self.computer_win_status == True:
					condition = False
		#None
				else:
					if sum_of_cards >= 17:
						condition = False 
					else: 
						card = random.choice(self.cards)
						self.computer_cards.append(card)
						self.cards.remove(card)
						condition = True
			print "Waiting for Computer..."			
			time.sleep(2)
			return sum_of_cards
	
	def check_win(self, cards):
		winning_combinations = {
			"Blackjack" : [["Ace", "King"], ["Ace", "Queen"], ["Ace", "Jack"], ["10", "Ace"]],
			"Triple 7": ['7','7','7'],
			"Double Ace": ["Ace", "Ace"]
		}
		lst_without_suit = []
		for card in cards:
			card_components = card.split()
			lst_without_suit.append(card_components[0])

		for key in winning_combinations:
			if sorted(lst_without_suit) in winning_combinations[key] or sorted(lst_without_suit) == winning_combinations[key]:
				if self.turn == name:
					self.player_key = key
				else:
					self.computer_key = key
				return True

		sum_of_cards = self.count_cards(cards)
		if sum_of_cards <= 21:
			if len(cards) == 5:
				if self.turn == name:
					self.player_key = "Five Cards"
				else:
					self.computer_key = "Five Cards"
				return True
			else: 
				return False 
		else:
			return False
			
	def get_winner(self, sum_of_computer_cards):
		money_received = {
			"Blackjack": money_bet * 2,
			"Triple 7": money_bet * 7,
			"Double Ace": money_bet * 3,
			"Five Cards": money_bet * 2
		}
		for money_key in money_received:
			if money_key == self.player_key:
				player_earnings = money_received[money_key]
				print(name + ": " + self.player_key)
			if money_key == self.computer_key:
				computer_earnings = money_received[money_key]
				print("Computer: " + self.computer_key)
	
		if self.player_win_status == True:
			print("Congratulations " + name + "! You won!")
			self.money_left += player_earnings
		if self.computer_win_status == True:
			print("Computer won!")
			self.money_left -= computer_earnings
		if self.player_win_status == False and self.computer_win_status == False:
			player_sum_of_cards = self.count_cards(self.player_cards)
			if player_sum_of_cards > 21 and sum_of_computer_cards > 21:
				print("You both suck!")
			elif player_sum_of_cards == sum_of_computer_cards:
				print("Tie. Boring!")
			elif player_sum_of_cards <= 21 and sum_of_computer_cards > 21:
				print(name + " won!")
				self.money_left += money_bet
			elif player_sum_of_cards > 21 and sum_of_computer_cards <= 21:
				print("Computer won!")
				self.money_left -= money_bet
			else:
				if player_sum_of_cards > sum_of_computer_cards:
					self.money_left += money_bet
					print(name + " won!")
				else:
					self.money_left -= money_bet
					print("Computer won!")
				
		save_file = file("money.json", "w")
		save_file.write(json.dumps(self.money_left))
		print "Computer's cards: " + ", ".join(self.computer_cards)
		print "Computer's sum: " + str(sum_of_computer_cards)

	def count_cards(self, cards):
		sum_of_cards = 0
		count_of_ace = 0
		for card in cards:
			try:
				card_components = card.split()
				value = int(card_components[0])
				sum_of_cards += value
			except ValueError:
				if card_components[0] == 'Ace':
					sum_of_cards += 11
					count_of_ace += 1
				elif card_components[0] == 'King' or 'Queen' or 'Jack':
					sum_of_cards += 10
		if sum_of_cards > 21:
			if count_of_ace > 0:
				for i in range(count_of_ace):
					sum_of_cards -= 10
					if sum_of_cards <= 21:
						break
		return sum_of_cards

	def play_again(self):
		while status:
				whether_rematch = raw_input("Do you want a rematch? (y/n)? ")
				if whether_rematch == 'y' or 'Y':
					status = False
					play = True
				elif whether_rematch == 'n' or 'N':
					status = False
					play = False
				else:
					print("Only y or n.")
					status = True

blackjack = blackjack(suits, values, cards, player_cards, computer_cards, players)
