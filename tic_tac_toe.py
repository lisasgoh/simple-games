import random

values = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['O', 'X']
players = ['COMPUTER', ''] 
turn = []
current_symbol = ['']

class tic_tac_toe(object):

	def __init__(self, values, symbols, players, turn, digits, current_symbol):	
		self.values = values
		self.symbols = symbols
		self.players = players
		self.turn = turn
		self.digits = digits
		self.current_symbol = current_symbol
	
	def start(self):
		print("Welcome to a game of Tic-Tac-Toe!")
		condition = True
		self.players.pop()
		global name 
		name = raw_input("What is your name?: ")
		while condition == True:				
			global player_symbol
			player_symbol  = raw_input("Hi " + name + ", which symbol do you want? Please only pick from 'O' or 'X': ")
			if player_symbol == 'o' or 'x':
				player_symbol = player_symbol.upper()
			if player_symbol == self.symbols[0]:#this makes it such that the symbol index = to the symbol player index
				self.players.insert(0, name)
				condition = False
			elif player_symbol == self.symbols[1]:
				self.players.append(name)
				condition = False
			else:
				print("Invalid symbol. Please type again.")
				condition = True
		who_goes_first = self.players[random.randint(0,1)] 
		self.turn.append(who_goes_first)
		print(who_goes_first + " goes first!")
		condition = True
		while condition:
			self.main()
			condition = self.check_condition()

	def main(self):
		self.draw_board()
		self.get_move()
	
	def draw_board(self):
		board = [[self.values[0] +'|', self.values[1] + '|', self.values[2]], ['_', ' _', ' _'], [self.values[3] +'|', self.values[4] + '|', self.values[5]], ['_', ' _', ' _'], [self.values[6] +'|', self.values[7] + '|', self.values[8]]]		
		for lst in board:
			board_row = ''.join(lst)		
			print(board_row)
	
	def determine_winner(self):
		self.draw_board()
		if self.current_symbol[0] == self.symbols[0]: #at first it was current_symbol[0]
			print(self.players[0] + " won!") 
		else:	
			print(self.players[1] + " won!")

	def horizontal_win(self):
		i = 0		
		while i < 7:		
			if self.values[i] == self.values[i+1] == self.values[i+2] and self.values[i] != ' ':
				return False
			else:
				i += 3
		return True

	def vertical_win(self):
		for i in range(3):
			if self.values[i] == self.values[i+3] == self.values[i+6] and self.values[i] != ' ':
				return False
		return True

	def diagonal_win(self):
		if self.values[0] == self.values[4] == self.values[8] and self.values[0] != ' ' or self.values[2] == self.values[4] == self.values[6] and self.values[2] != ' ':
			return False
		else:
			return True

	def tie(self):
		count = 0
		for i in range(9):
			if self.values[i] == 'O' or self.values[i] == 'X':
				count += 1				
		if count == 9:
			return False
		else:
			return True

	def get_move(self):
		if self.turn[0] == 'COMPUTER':
			self.computer_move()
		else:						
			self.current_symbol[0] = player_symbol	
			condition = True
			while condition:			
				which_tile = raw_input("Which tile to replace?: ")
				if which_tile in digits:		
					if self.values[int(which_tile)-1] != ' ':
						print("Tile is taken. Please choose another one.") 
						status = True
						while status:
							which_tile = raw_input("Type a new number: ")
							if which_tile not in digits:
								print("Not in range. Please input number from 1 to 9 only.")
								status = True
							elif self.values[int(which_tile)-1] != ' ':
								print("Tile is taken. Please choose another one.")
								status = True
							else:
								status = False
					for i in range(2):
						if self.players[i] == name:				
							self.values[int(which_tile)-1] = self.symbols[i]
					condition = False
				else:
					print("Not in range. Please input number from 1 to 9 only.")
					condition = True
			self.turn[0] = 'COMPUTER'

	def computer_move(self):
		print("Computer's turn!")	
		for i in range(2):
			if self.players[i] == 'COMPUTER':			
				computer_symbol = i
				self.current_symbol[0] = symbols[i] 
		if self.values[4] == ' ':
			self.values[4] = self.symbols[computer_symbol]
		else:
			x = 0
			mode = 'trial'
			for i in range(9): #check if win
				if self.values[i] == ' ':
					self.values[i] = self.symbols[computer_symbol] #change to computer symbol
					condition = self.check_condition(mode)	
					if condition == False: #if wins'
						x = 1
						break
					else:
						self.values[i] = ' '
			if x != 1:		
				for i in range(9): #check for block
					if self.values[i] == ' ':	
						self.values[i] = player_symbol #change to player's symbol
						condition = self.check_condition(mode)
						if !condition: #if player wins
							self.values[i] = self.symbols[computer_symbol] #change to computer symbol	
							x = 1
							break
						else:
							self.values[i] = ' '				
			
			if x != 1:
				corners = [0,2,6,8]
				empty_corner = []
				for corner in corners:
					if self.values[corner] == ' ':
						empty_corner.append(corner)
				if len(empty_corner) > 0:
					self.values[random.choice(empty_corner)] = self.symbols[computer_symbol]	
				else:				
					which_tile = random.randint(0,8)					
					while self.values[which_tile] != ' ':
						which_tile = random.randint(0,8)
					self.values[which_tile] = self.symbols[computer_symbol]
		self.turn[0] = name
	
	def check_condition(self, mode=None):		
		condition_1 = self.horizontal_win()
		condition_2 = self.vertical_win()
		condition_3 = self.diagonal_win()
		condition_4 = self.tie()
		if condition_1 and condition_2 and condition_3 and condition_4:
			return True #no win
		elif mode == None and !condition_4:
			self.draw_board()
			print("Game over! It is a tie.")
			return False
		else:
			if mode == None:
				self.determine_winner()
				return False #win
			else:
				return False

tic_tac_toe = tic_tac_toe(values, symbols, players, turn, digits, current_symbol)

