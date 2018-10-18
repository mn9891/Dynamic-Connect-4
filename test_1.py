#! Amen
#! /usr/bin/env python3
from itertools import groupby, chain

NONE = '.'
WHITE = '0'
BLACK = '1'

def diagonalsPos (matrix, cols, rows):
	"""Get positive diagonals, going from bottom-left to top-right."""
	for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
		yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg (matrix, cols, rows):
	"""Get negative diagonals, going from top-left to bottom-right."""
	for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
		yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class Game:
	def __init__ (self, cols = 5, rows = 4, requiredToWin = 3):
		"""Create a new game."""
		self.cols = cols
		self.rows = rows
		self.win = requiredToWin
		""""Initial configuration"""
		self.board = [[NONE] * rows for _ in range(cols)]
		for  jj in range(4):
			if jj  % 2 == 0:
				self.board[0][jj] = WHITE
				self.board[4][jj] = BLACK
			else:
				self.board[4][jj] = WHITE
				self.board[0][jj] = BLACK		


	def insert (self, column, color):
		"""Insert the color in the given column."""
		c = self.board[column]
		if c[0] != NONE:
			raise Exception('Column is full')

		i = -1
		while c[i] != NONE:
			i -= 1
		c[i] = color

		self.checkForWin()
	
	def move (self, command):
		"""Move  in the given direction."""
		self.command=command
		#~ self.color=color
		column=int(command[0])-1
		row=int(command[1])-1
		direction=command[2]
		c = self.board[column][row]
		if direction == 'S':
			row2=row+1
			column2=column
		elif direction == 'N':
			row2=row-1
			column2=column
		elif direction == 'E':
			row2=row
			column2=column+1
		else:
			row2=row
			column2=column-1
		#~ c2 = self.board[column2][row2]
		#~ if c2== NONE and self.color == c and column2 in range(5) and row2 in range(4):
		self.board[column2][row2]=c
		self.board[column][row]=NONE
		#~ else: print('errrrr')
			
			
		#~ if c!= NONE: #chane none by 'the right color' and also verify if destination is valid
			#~ raise Exception('ERRRROR')
			
		self.checkForWin()

	##################################
	##################################
	
	def __minimax(self, player):
		if self.checkForWin():
			if player:
				return (-1,None)
			else:
				return (+1,None)
		#elif self.tied():          #here, need to def tied function and specify tie conditions
			#return (0,None)
		elif player:
			best = (-2,None)
			for poss_move in self.checkPossibleMove(player):  
				value = self.move(poss_move).__minimax(getEnemy(player))[0]
				if value>best[0]:
					best = (value,poss_move)
			return best
		else:
			best = (+2,None)
			for poss_move in self.checkPossibleMove(player):  
				value = self.move(poss_move).__minimax(getEnemy(player))[0]
				if value<best[0]:
					best = (value,poss_move)
			return best

	def best(self):
		return self.__minimax(True)[1]

	def tied(self):
		for (x,y) in self.fields:
			if self.fields[x,y]==self.empty:
				return False
		return True
	
	##################################
	##################################	
	
	def checkPossibleMove(self,player):
		""" Check the possible moves for the piece in the position (y,x) """
		positions=self.getSquares(player)							#list of squares currently occupied by player
		cmd_list=[]											#list of possible move or command
		list2=[]												#list of  available squares to move to
		for pos in positions:
			y=pos[0]
			x=pos[1]
			if y+1 in range(5):
				if self.board[y+1][x]==NONE: 			#possible move to the south
					cmd_list.extend([[''.join([str(y+1),str(x+1),'E'])]])	
					list2.extend([[y+1,x]])
			if y-1 in range(5):
				if self.board[y-1][x]==NONE: 			#possible move to the north
					cmd_list.extend([[''.join([str(y+1),str(x+1),'W'])]])	
					list2.extend([[y-1,x]])
			if x+1 in range(4):
				if self.board[y][x+1]==NONE: 			#possible move to the est
					cmd_list.extend([[''.join([str(y+1),str(x+1),'S'])]])	
					list2.extend([[y,x+1]])
			if x-1 in range(4):
				if self.board[y][x-1]==NONE:			#possible move to the west
					cmd_list.extend([[''.join([str(y+1),str(x+1),'N'])]])	
					list2.extend([[y,x-1]])
		return cmd_list
		

	def getSquares(self, player):
		"""" Get the list of squares occupied by player """
		list=[]						#list of squares currently occupied by player
		for i in range(5):
			for j in range(4):
				c=self.board[i][j]
				if c==player:
					list.extend([[i,j]])
		return list
	
	def checkForWin (self):
		"""Check the current board for a winner."""
		w = self.getWinner()
		if w:
			self.printBoard()
			raise Exception(w + ' won!')
	
	def numberOfRuns(self):
		"""Get the number of runs (2 aligned same color pieces) for each player on the current board."""
		lines = (
			self.board, # columns
			zip(*self.board), # rows
			diagonalsPos(self.board, self.cols, self.rows), # positive diagonals
			diagonalsNeg(self.board, self.cols, self.rows) # negative diagonals
		)
		z=[0,0]
		for line in chain(*lines):
			for color, group in groupby(line):
				if len(list(group)) == 2:
					if color == WHITE:
						z[0]+=1
					elif color == BLACK:
						z[1]+=1
		return z

	def getWinner (self):
		"""Get the winner on the current board."""
		lines = (
			self.board, # columns
			zip(*self.board), # rows
			diagonalsPos(self.board, self.cols, self.rows), # positive diagonals
			diagonalsNeg(self.board, self.cols, self.rows) # negative diagonals
		)
		
		for line in chain(*lines):
			for color, group in groupby(line):
				if color != NONE and len(list(group)) >= self.win:
					return color
	
	def getEnemy(player):
		if player == WHITE:
			return BLACK
		return WHITE
		
	def printBoard (self):
		"""Print the board."""
		#print(' '.join(map(str, range(self.cols))))
		for y in range(self.rows):
			print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
		print()


if __name__ == '__main__':
	g = Game()
	gameID, var2 = input("Enter gameID and player\'s color: ").split()
	turn = WHITE
	while True:
		g.printBoard()
		print(g.getSquares(turn))
		print(g.checkPossibleMove(turn))
		print('NoR for W and B respectfully: {}'.format(g.numberOfRuns()))
		command = input('{}\'s turn: '.format('White' if turn == WHITE else 'Black'))
		g.move(command)
		turn = BLACK if turn == WHITE else WHITE
