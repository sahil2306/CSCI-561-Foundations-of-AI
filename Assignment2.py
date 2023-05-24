import numpy as np
import time as t
import copy

# 0 = empty, 1 = white, 2 = black

class Game:
    def __init__(self, board,player,opponent,capturedw,capturedb):
        self.board = board
        self.player = player
        self.opponent = opponent
        self.capturedw = capturedw
        self.capturedb = capturedb

    def checkCapture(self,board,player,opponent,i,j):

        isCaptured=0

        # Check rows
        if j <= 15:
            if board[i][j+1]==opponent and board[i][j+2]==opponent and board[i][j+3]==player:
                board[i][j+1] = 0
                board[i][j+2] = 0
                isCaptured+=2

        if j >= 3:
            if board[i][j-1]==opponent and board[i][j-2]==opponent and board[i][j-3]==player:
                board[i][j-1] = 0
                board[i][j-2] = 0
                isCaptured+=2

        # Check columns
        if i <= 15:
            if board[i+1][j]==opponent and board[i+2][j]==opponent and board[i+3][j]==player:
                board[i+1][j] = 0
                board[i+2][j] = 0
                isCaptured+=2

        if i >= 3:
            if board[i-1][j]==opponent and board[i-2][j]==opponent and board[i-3][j]==player:
                board[i-1][j] = 0
                board[i-2][j] = 0
                isCaptured+=2

        # Check diagonals (positive slope)
        if i <= 15 and j <= 15:
            if board[i+1][j+1]==opponent and board[i+2][j+2]==opponent and board[i+3][j+3]==player:
                board[i+1][j+1] = 0
                board[i+2][j+2] = 0
                isCaptured+=2

        if i >= 3 and j >= 3:
            if board[i-1][j-1]==opponent and board[i-2][j-2]==opponent and board[i-3][j-3]==player:
                board[i-1][j-1] = 0
                board[i-2][j-2] = 0
                isCaptured+=2

        # Check diagonals (negative slope)
        if i <= 15 and j >= 3:
            if board[i+1][j-1]==opponent and board[i+2][j-2]==opponent and board[i+3][j-3]==player:
                board[i+1][j-1] = 0
                board[i+2][j-2] = 0
                isCaptured+=2

        if i >= 3 and j <= 15:
            if board[i-1][j+1]==opponent and board[i-2][j+2]==opponent and board[i-3][j+3]==player:
                board[i-1][j+1] = 0
                board[i-2][j+2] = 0
                isCaptured+=2
    
        
        return isCaptured

    # Check all possible captures
    # Optimization 1: only check the smaller matrix
    def checkAllCaptures(self,board,player,opponent,min_i,max_i,min_j,max_j):
        score=0
        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                if board[i][j]==player:
                    score+=self.checkCapture(board,player,opponent,i,j)
        return score

    # Check a win
    # Send captured
    def checkWinner(self,board,capturedw,capturedb):
        if capturedb>=10 or capturedw>=10 :
            return True
        
        for i in range(0,19):
            for j in range(0,19):
                if j<15:
                    if np.all(board[i, j:j+5] == 1) or np.all(board[i, j:j+5] == 2):
                        return True
                if i<15:    
                    if np.all(board[i:i+5, j] == 1) or np.all(board[i:i+5, j] == 2):
                        return True
                if i<15 and j<15:
                    if((np.all(np.diag(board[i:i+5, j:j+5]))==1) or (np.all(np.diag(board[i:i+5, j:j+5]))==2)):
                        return True
                    if((np.all(np.diag(np.fliplr(board[i:i+5, j:j+5])))==1) or (np.all(np.diag(np.fliplr(board[i:i+5, j:j+5])))==2)):
                        return True
        return False

    # Evaluation function and helper functions
    # Optimization 2: all in 1 loop
    # Optimization 3: add for 2,3 in a row
    def getScores(self,board,player,opponent,min_i,max_i,min_j,max_j):
        score = 0
        p5=0
        o5=0
        p4=0
        o4=0
        p3=0
        o3=0

        # Horizontal
        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                num_p = np.count_nonzero(board[i, j:j+5] == player)
                num_o = np.count_nonzero(board[i, j:j+5] == opponent)
                num_b = np.count_nonzero(board[i, j:j+5] == 0)

                if num_p== 5:
                    p5 +=1
                if num_o == 5:
                    o5 +=1
                if num_p == 4 and num_b == 1:
                    p4 +=1
                if num_o == 4 and num_b == 1:
                    o4 +=1
                if num_p == 3 and num_b == 2:
                    p3 +=1
                if num_o == 3 and num_b == 2:
                    o3 +=1
                
        # Vertical
        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                num_p = np.count_nonzero(board[i:i+5, j] == player)
                num_o = np.count_nonzero(board[i:i+5, j] == opponent)
                num_b = np.count_nonzero(board[i:i+5, j] == 0)

                if num_p== 5:
                    p5 +=1
                if num_o == 5:
                    o5 +=1
                if num_p == 4 and num_b == 1:
                    p4 +=1
                if num_o == 4 and num_b == 1:
                    o4 +=1
                if num_p == 3 and num_b == 2:
                    p3 +=1
                if num_o == 3 and num_b == 2:
                    o3 +=1
        
        # Diagonal
        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                if i<15 and j<15:
                    num_p = np.count_nonzero(np.diag(board[i:i+5, j:j+5]) == player)
                    num_o = np.count_nonzero(np.diag(board[i:i+5, j:j+5]) == opponent)
                    num_b = np.count_nonzero(np.diag(board[i:i+5, j:j+5]) == 0)
                
                    if num_p== 5:
                        p5 +=1
                    if num_o == 5:
                        o5 +=1
                    if num_p == 4 and num_b == 1:
                        p4 +=1
                    if num_o == 4 and num_b == 1:
                        o4 +=1
                    if num_p == 3 and num_b == 2:
                        p3 +=1
                    if num_o == 3 and num_b == 2:
                        o3 +=1

                    
                    num_p = np.count_nonzero(np.diag(np.fliplr(board[i:i+5, j:j+5])) == player)
                    num_o = np.count_nonzero(np.diag(np.fliplr(board[i:i+5, j:j+5])) == opponent)
                    num_b = np.count_nonzero(np.diag(np.fliplr(board[i:i+5, j:j+5])) == 0)
                
                    if num_p== 5:
                        p5 +=1
                    if num_o == 5:
                        o5 +=1
                    if num_p == 4 and num_b == 1:
                        p4 +=1
                    if num_o == 4 and num_b == 1:
                        o4 +=1
                    if num_p == 3 and num_b == 2:
                        p3 +=1
                    if num_o == 3 and num_b == 2:
                        o3 +=1
        
        
        return p5*10000000000 - o5*10000000000 + p4*10000000 - o4*1000000 + p3*100000 - o3*100000

    def evaluate(self,board,player,opponent,min_i,max_i,min_j,max_j,captured_by_player,captured_by_opponent):
        score = 0
        score += self.getScores(board,player,opponent,min_i,max_i,min_j,max_j)
        
        score += captured_by_player*10000 - captured_by_opponent*10000

        possible_captures_by_player = self.checkAllCaptures(board,player,opponent,min_i,max_i,min_j,max_j)
        possible_captures_by_opponent = self.checkAllCaptures(board,opponent,player,min_i,max_i,min_j,max_j)

        if(captured_by_player+possible_captures_by_player==10):
            score += 10000000000
        elif(captured_by_opponent+possible_captures_by_opponent==10):
            score -= 10000000000
        else:
            score += possible_captures_by_player*10000 - possible_captures_by_opponent*10000

        return score

# Minimax
def minimax(state, board, depth, maximizingPlayer,alpha,beta,player,opoonent,player_captured,opp_captured,min_i,max_i,min_j,max_j):
    if depth==0 or state.checkWinner(board,player_captured,opp_captured):
        return state.evaluate(board,player,opponent,min_i,max_i,min_j,max_j,player_captured,opp_captured),None
                
    if maximizingPlayer:
        position = None
        bestValue = float("-inf")

        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                if board[i][j] == 0:
                    # Make Move
                    board2 = copy.deepcopy(board)
                    board2[i][j] = player
                    

                    # Check for Capture 
                    captured_by_player = state.checkCapture(board2,i,j,player,opponent)
                    player_captured += captured_by_player
                    
                    captured_white = 0
                    captured_black = 0

                    if(player == 1):
                        captured_white = captured_by_player
                    else:
                        captured_black = captured_by_player
                    
                    new_state = Game(board2,opponent,player,capturedw+captured_white,capturedb+captured_black)

                    # Minimax
                    value,_ = minimax(new_state,board2,depth-1,False,alpha,beta,player,opponent,player_captured,opp_captured,max(0,min(min_i,i-2)),min(18,max(max_i,i+2)),max(0,min(min_j,j-2)),min(18,max(max_j,j+2)))


                    # Update Best Value
                    if value>bestValue:
                        bestValue = value
                        position = (i,j)

                    # CHECK bestValue or value
                    alpha = max(alpha, bestValue)
                    if beta<=alpha:
                        break

        return bestValue,position

    else:
        position = None
        bestValue = float("inf")
        
        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                if board[i][j] == 0:
                    
                    board2 = copy.deepcopy(board)
                    board2[i][j] = opponent
                    
                    # Check for Capture 
                    captured_by_opponent = state.checkCapture(board2,i,j,opponent,player)
                    opp_captured += captured_by_opponent
                    captured_white = 0
                    captured_black = 0

                    if(opponent == 1):
                        captured_white = captured_by_opponent
                    else:
                        captured_black = captured_by_opponent
                    
                    new_state = Game(board2,player,opponent,capturedw+captured_white,capturedb+captured_black)

                    # Minimax
                    value,_ = minimax(new_state,board2,depth-1,True,alpha,beta,player,opponent,player_captured,opp_captured,max(0,min(min_i,i-2)),min(18,max(max_i,i+2)),max(0,min(min_j,j-2)),min(18,max(max_j,j+2)))


                    # Update Best Value
                    if value < bestValue:   
                        bestValue = value
                        position = (i,j)

                    beta = min(beta, bestValue)
                    if value <= alpha:
                        break

        return bestValue,position
    

if __name__ == '__main__':

    # read the file-----------
    st = t.process_time()

    with open('input.txt', 'r') as f:
        extracted_data = f.readlines()

    data = [x.strip() for x in extracted_data]

    player = data[0][0]
    if player == 'W':
        player = 1
    else:
        player = 2

    time = data[1]
    wcaptured,bcaptured = data[2].split(',')
    
    lines = [line.strip() for line in data[3:]]

    countw=0
    countb=0

    min_i=18
    max_i=0
    min_j=18
    max_j=0

    board = np.zeros((19, 19), dtype=int)
    for i in range(19):
        for j in range(len(lines[i])):
            if lines[i][j] == 'w':
                countw+=1
                board[i][j] = 1
                min_j=min(min_j,j)
                max_j=max(max_j,j)
                min_i=min(min_i,i)
                max_i=max(max_i,i)
            elif lines[i][j] == 'b':
                countb+=1
                board[i][j] = 2
                min_j=min(min_j,j)
                max_j=max(max_j,j)
                min_i=min(min_i,i)
                max_i=max(max_i,i)
                
    time = float(time)
    capturedw = int(wcaptured)
    capturedb = int(bcaptured)

    # Set player and opponent-----------
    
    opponent = 2
    if(player == 2):
        opponent = 1 
        opp_captured = capturedw
        player_captured = capturedb
    else:
        opponent = 2
        opp_captured = capturedb
        player_captured = capturedw

    position = (9,9)

    # Start Game Conditions-----------    
    if(countw==0 and countb==0):
        position = (9,9)
    elif(countw==1 and countb==0):
        if(board[9][8]==1):
            position = (9,8)
    elif(countw==1 and countb==1):
        if(board[9][9]==1):
            position = (10,9)
    else:
        # Minimax-----------
        gm = Game(board,player,opponent,player_captured,opp_captured)
        depth=1

        bestval,position = minimax(gm,board,depth,True,float("-inf"),float("inf"),player,opponent,player_captured,opp_captured,max(0,min_i-2),min(18,max_i+2),max(0,min_j-2),min(18,max_j+2))

        et = t.process_time()
        elapsed_time = et - st

    #     print("\nbestval: ",bestval,"\nposition: ",position,"\ntime: ",elapsed_time)

    # print(position)

    if(position==None):
        for i in range(0,19):
            for j in range(0,19):
                if board[i][j] == 1:
                    min_j=min(min_j,j)
                    max_j=max(max_j,j)
                    min_i=min(min_i,i)
                    max_i=max(max_i,i)
                elif board[i][j] == 2:
                    min_j=min(min_j,j)
                    max_j=max(max_j,j)
                    min_i=min(min_i,i)
                    max_i=max(max_i,i)

        min_i = max(0,min_i)
        max_i = min(18,max_i)
        min_j = max(0,min_j)
        max_j = min(18,max_j)


        for i in range(min_i,max_i+1):
            for j in range(min_j,max_j+1):
                if(board[i][j]==0):
                    position = (i,j)
                    break

    # print(position)
    row = 19-position[0]
    col = position[1]
    
    if(position[1]>=8):
        col = chr(position[1]+66)
    else:
        col = chr(position[1]+65)

    sol = str(row)+col
    print(sol, file=open("output.txt", "w"),end='')    