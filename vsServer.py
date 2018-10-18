#Amen
from itertools import groupby, chain
from copy import deepcopy
from random import shuffle
import sys
import logging
#~ sys.setrecursionlimit(5000)
import socket
import time
NONE = '.'
white = '0'
black = '1'
NbrCols=5
NbrRows=4
def diagonalsPos (matrix, cols, rows):
	"""Get positive diagonals, going from bottom-left to top-right."""
	for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
		yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg (matrix, cols, rows):
	"""Get negative diagonals, going from top-left to bottom-right."""
	for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
		yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class Game:
	def __init__ (self, cols, rows, requiredToWin = 3):
		"""Create a new game."""
		self.cols = cols
		self.rows = rows
		self.win = requiredToWin
		""""Initial configuration"""
		self.board = [[NONE] * rows for _ in range(cols)]
		if NbrCols==5:
			for  jj in range(NbrRows):
				if jj  % 2 == 0:
					self.board[0][jj] = white
					self.board[4][jj] = black
				else:
					self.board[4][jj] = white
					self.board[0][jj] = black
		elif NbrCols==7:
			self.board[1][1]=white
			self.board[1][2]=black
			self.board[1][3]=white
			self.board[1][4]=black
			self.board[5][4]=white
			self.board[5][3]=black
			self.board[5][2]=white
			self.board[5][1]=black
	
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
		
		self.board[column2][row2]=c
		self.board[column][row]=NONE
		

	
	##################################
	
	def minimax(self, player,depth):
		if self.checkForWin()==white:
			return (10000,None)
		elif self.checkForWin()==black:
			return (-10000,None)
			return (-10000,None)
		elif depth == 0:
			return (self.heuristic(),None)
		#elif self.tied():          #here, need to def tied function and specify tie conditions
			#return (0,None)
		elif player==white:
			best = (-1000,None)
			#~ print( 'AM1= {}'.format(self.checkPossibleMove(player)))
			g_aux=deepcopy(self)
			for poss_move in self.checkPossibleMove(player):
				#~ print(poss_move)
				self.move(poss_move[0])
				#~ self.printBoard()
				value = self.minimax(self.getEnemy(player),depth-1)[0]
				if value>best[0]:
					best = (value,poss_move[0])
				self=deepcopy(g_aux)
			return best
		else:
			best = (+1000,None)
			#~ print( 'AM2= {}'.format(self.checkPossibleMove(player)))
			g_aux=deepcopy(self)
			for poss_move in self.checkPossibleMove(player):
				#~ print(poss_move)
				self.move(poss_move[0])
				#~ self.printBoard()
				value = self.minimax(self.getEnemy(player),depth-1)[0]
				if value<best[0]:
					best = (value,poss_move[0])
				self=deepcopy(g_aux)
			return best
		
	def __minimaxAlphaBeta(self, player,depth,alpha,beta):
		if depth == 0:
			return (self.heuristic(),None)
		elif self.getWinner()==white:
			
			return (10000,None)
		elif self.getWinner()==black:
			#~ print(depth)
			return (-10000,None)
		elif player==white:
			
			best = (alpha,None)
			#~ print( 'AM1= {}'.format(self.checkPossibleMove(player)))
			g_aux=deepcopy(self)
			for poss_move in self.checkPossibleMove(player):
				#~ print('max')
				#~ print(poss_move)
				self.move(poss_move[0])
				#~ self.printBoard()
				value = self.__minimaxAlphaBeta(self.getEnemy(player),depth-1,alpha,beta)[0]
				if value == -10000:
					print('zzzzzzzzzzz')
				if value>alpha:
					alpha=value
					if alpha >= beta:
						return beta, poss_move[0]
					best = (alpha,poss_move[0])
				self=deepcopy(g_aux)
				#~ print(alpha,beta)
				#~ print( 'Alpha,beta= {},{}'.format(alpha,beta))
			#~ print(best[1])
				if depth==7:
					print('move, value= {}, {}'.format(poss_move,value))
			return best
		else:
			best = (beta,None)
			#~ print( 'AM2= {}'.format(self.checkPossibleMove(player)))
			g_aux=deepcopy(self)
			for poss_move in self.checkPossibleMove(player):
				#~ print('min')
				#~ print(poss_move)
				self.move(poss_move[0])
				#~ self.printBoard()
				value = self.__minimaxAlphaBeta(self.getEnemy(player),depth-1,alpha,beta)[0]
				if value<beta:
					beta=value
					if beta <= alpha:
						return alpha, poss_move[0]
					best = (beta,poss_move[0])
				self=deepcopy(g_aux)
				#~ print(alpha,beta)
			#~ print( 'Alpha,beta= {},{}'.format(alpha,beta))
				if depth==7:
					print('move, value= {}, {}'.format(poss_move,value))
			return best

	def best(self,player,depth):
		return self.minimax(player,depth)[1]
	
	def bestAlphaBeta(self,player,depth,alpha,beta):
		return self.__minimaxAlphaBeta(player,depth,alpha,beta)[1]
	
	def tied(self):
		for (x,y) in self.fields:
			if self.fields[x,y]==self.empty:
				return False
		return True
	
	##################################
	
	def checkPossibleMove(self,player):
		""" Check the possible moves for the piece in the position (y,x) """
		positions=self.getSquares(player)							#list of squares currently occupied by player
		cmd_list=[]											#list of possible move or command
		list2=[]												#list of  available squares to move to
		for pos in positions:
			y=pos[0]
			x=pos[1]
			if y+1 in range(NbrCols):
				if self.board[y+1][x]==NONE: 			#possible move to the est
					cmd_list.extend([[''.join([str(y+1),str(x+1),'E'])]])	
					list2.extend([[y+1,x]])
			if y-1 in range(NbrCols):
				if self.board[y-1][x]==NONE: 			#possible move to the west
					cmd_list.extend([[''.join([str(y+1),str(x+1),'W'])]])	
					list2.extend([[y-1,x]])
			if x+1 in range(NbrRows):
				if self.board[y][x+1]==NONE: 			#possible move to the south
					cmd_list.extend([[''.join([str(y+1),str(x+1),'S'])]])	
					list2.extend([[y,x+1]])
			if x-1 in range(NbrRows):
				if self.board[y][x-1]==NONE:			#possible move to the north
					cmd_list.extend([[''.join([str(y+1),str(x+1),'N'])]])	
					list2.extend([[y,x-1]])
		return cmd_list
		

	def getSquares(self, player):
		"""" Get the list of squares occupied by player """
		list=[]						#list of squares currently occupied by player
		for i in range(NbrCols):
			for j in range(NbrRows):
				c=self.board[i][j]
				if c==player:
					list.extend([[i,j]])
		return list
	
	def checkForWin (self):
		"""Check the current board for a winner."""
		w = self.getWinner()
		return w

	
	def heuristic(self):
		r=self.numberOfRuns()[0]-self.numberOfRuns()[1]
		return r
	
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
					if color == white:
						z[0]+=1
					elif color == black:
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
	
	def getEnemy(self, player):
		if player == white:
			return black
		return white
		
	def printBoard (self):
		"""Print the board."""
		#print(' '.join(map(str, range(self.cols))))
		for y in range(self.rows):
			print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
		print()


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+", format="%(asctime)-15s %(message)s")
	#board size
	board_size = raw_input("Please enter 1 for 5*4 board or 2 for 7*6 board:")
	if board_size=='1':
		NbrCols=5
		NbrRows=4
	else:
		NbrCols=7
		NbrRows=6
	#create the game
	g = Game(NbrCols,NbrRows)
	logging.info("Game created")
	
	#connection to the server
	TCP_IP = '132.206.74.211'
	TCP_PORT = 12345 
	BUFFER_SIZE = 1024
	gameID, player_color = raw_input("Enter gameID and player\'s color: ").split()
	MESSAGE=' '.join((gameID,player_color,'\n'))
	#~ logging.info(str(gameID), str(player_color))
	if player_color == 'white':
		us=white
		opponent=black
	elif player_color=='black':
		us=black
		opponent=white
	turn = white
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)
	data=s.recv(BUFFER_SIZE) #waiting, side echoed
	alpha=-17
	beta=17
	w=None
	print('This is the current board:')
	g.printBoard()
	while w==None:
		if turn == us:
			t = time.time()
			g_aux=deepcopy(g)
			print( 'Possible moves= {}'.format(g.checkPossibleMove(turn)))
			move=g_aux.bestAlphaBeta(turn,6,alpha,beta)
			#~ move=g_aux.best(turn,2)
			###print(move)
			g.move(move)
			MESSAGE=' '.join((move,'\n'))
			s.send(MESSAGE)
			data=s.recv(BUFFER_SIZE) #echoed move
			print('This is the current board after our move:')
			g.printBoard()
			print('elapsed time= {}'.format(time.time() - t))
		else:
			command = s.recv(BUFFER_SIZE)
			g.move(command)
			print('This is the current board after opponent\'s move:')
			g.printBoard()
			
			
		turn = black if turn == white else white
		w= g.checkForWin()
	g.printBoard()
	turn = black if turn == white else white
	print('{} won! '.format(turn))