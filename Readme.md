# Dynamic Connect-4


### Project 1 - AI course (ECSE 526) - McGill - Fall 2016
Check project instuctions [here](http://www.cim.mcgill.ca/~jer/courses/ai/as1).

### The game 


"dynamic connect-3" is played on a 5x4 grid or 7x6 as follows:
Starting from the initial position, players take turns moving one piece of their colour by one square,
either horizontally or vertically. White plays first. Pieces can only move to unoccupied squares.
The winner is the first player to line up three of its pieces either horizontally, vertically, or diagonally.


### Intrusctions


The game is coded using python 2.7. Thus to execute it on any linux machine, you only need to type: 
- python humans_vs_ai.py to play (as human)
- python vsServer.py to make the program play using the "official" game server on 132.206.74.211 port 12345 

First step is to choose the board size then to enter the game Id and our side (white or black).
Then you have to make your move knowing the following:
Each square in the grid can be labeled by its <x,y> position, with 1,1 corresponding to the top-left square.
Moves are entered by specifying the position of the piece to move in the form <x,y> followed by one of the compass directions, N, S, E, W.
For example, to move the black piece at the bottom left of the board one square to the right, the command would be 14E.
