import board_game
import random

def is_threatened_non_diagonal(board, i,j,  player_sym):
    """checking if there is a threat from non - diagonal directions to cell in
        the (i,j) place"""
    offset_list=[2,-2]      #negative for left side and down side
    l_index=["i","j"]
    for offset in offset_list:
        for index in l_index:
            if is_seq_exist(board, i,j,offset, player_sym, index):
                return True
    return False



def in_range(board, val):
    """return if a given value is inside the board.matrix dimensions range.
       pre: board.cols==board.rows """
    if val<0:
        return False
    if val>(board.cols-1):
        return False
    return True


def is_seq_exist (board, i,j, offset, player_sym, index):
    """checking if there is a sequence of the player_sym from positive direction"
        i.e : from above  and to the right to the cell, and from negative
        direction, i.e: from below and left """ 
    if offset>0:         #positive offset
        rng=range(1, offset+1)
    else:                #negative offset
        rng=range(-2,0)
    if index=="j":       #vertical checking     
        for k in rng:
            #checking k is possible value in the board.matrix
            if not in_range(board,j+k) :
               return False
        for k in rng:
            #the column is fixed, the rows are changing: vertical checking 
            if (board.get_cell(i,j+k)) != player_sym:            
                return False
        #there is a sequence
        return True
    elif index=="i":      #horizontal checking
        for k in rng:
            if not in_range(board,i+k) :
                return False
        for k in rng:
            #the row is fixed and the columns are changing: horizontal checking   
             if (board.get_cell(i+k,j)) != player_sym:           
                return False
        #there is a sequence
        return True

def is_threatened_both_sides(board, i,j ,player_sym):
    """for middle cells another checking is requiered: is the cell has
       two neighbors- from the sides or from above and below"""
    if in_range(board , j-1) and in_range(board, j+1):  #for vertical checking
        if (board.get_cell(i,j+1)==player_sym) and (board.get_cell(i,j-1)==player_sym):
            return True
    if in_range(board, i-1) and in_range(board, i+1):   #for horizontal checking
        if (board.get_cell(i-1,j)==player_sym) and (board.get_cell(i+1,j)==player_sym):
            return True
    #there are less than 2 neighbors
    return False

def is_threatened_diagonal(board,i,j, player_sym):
    """checking if there is a threat from diagonal direction"""
    if(i==0) and(j==0):
        return board.get_cell(1,1)==board.get_cell(2,2)==player_sym
    elif (i==2)and(j==0):
        return board.get_cell(1,1)==board.get_cell(0,2)==player_sym
    elif (i==0) and (j==2):
        return board.get_cell(1,1)==board.get_cell(2,0)==player_sym
    elif (i==2) and (j==2):
        return board.get_cell(1,1)==board.get_cell(0,0)==player_sym

def is_threatened(board, i,j,player_sym):
    """return if threat exist from any direction to the cell in the (i,j) place"""
    if board.get_cell(i,j)!=" ":                            #if cell is occupied it can't be threatened
        return False
    nd=is_threatened_non_diagonal(board, i,j,player_sym)
    d= is_threatened_diagonal(board, i,j,player_sym)
    bs=is_threatened_both_sides(board, i,j,player_sym)
    if nd or d or bs:
        return True
    return False

def is_threat_exist(board, player_sym):
    """checking if there is a cell which is threaten in the board. return
        a list of those cells"""
    threatened=[]
    for i in range(3):
        for j in range (3):
            if is_threatened(board, i,j, player_sym):
                threatened.append ((i,j))
    return threatened

def create_threat(board, player_sym,other_sym):
    """return a list of cells which if will be seted to player_sym,
       a threat to the other player will be created. there is a priority to cells
        which are also corners. """
    corners=[(0,0), (2,0),(0,2),(2,2)]
    opt_cells=[]
    for i in range(3):
        for j in range (3):
            if board.get_cell(i,j)==" ":
                board.set_cell(i,j,player_sym)
                if is_threat_exist(board,player_sym):
                    opt_cells.append((i,j))
                board.clear_cell(i,j)       
    #if setting a cell from opt_cells will lead that the other
    #player will be able to create a double threat, this cell
    #will be removed from the options
    for k in range (len(opt_cells),0,-1):    #iterate over all the optional cells in opt_cells revrsely
        
            
        c1=opt_cells[k-1]
        board.set_cell(c1[0], c1[1], player_sym)   #set the cell to the player_sym
        other_t=is_threat_exist(board, player_sym) #create the list of the other player threatened cells
        if len(other_t)==1:                        #if len(other_t)>1 winnig is guaranteed anyway
            board.set_cell(other_t[0][0], other_t[0][1], other_sym) #set the threatened cell to other_sym
            new_threats=is_threat_exist(board, other_sym)           # check the threats to player
            board.clear_cell(other_t[0][0], other_t[0][1])
            board.clear_cell(c1[0],c1[1])
            if len(new_threats)>1:         
                
                opt_cells.remove(c1)
        board.clear_cell(c1[0],c1[1])


    ret_cells=[elem for elem in opt_cells if elem in corners]
    if ret_cells==[]:           #there are no corners
        db("00no_cor")
        return opt_cells
    else:
        db("cor")
        return ret_cells


def computer_move(board, turn, player_sym, other_player_sym):
    """excute the computer strategy: select the center if possible. if the player
        already has two - cells sequence -> set the third and win.
        if the other player can create a winning sequence (threat is exist)-> block it.
        else: try to create 2 cell sequence (create threat) if possible.
        else: choose the first empety cell in the board.matrix. """
    if turn==0:                                      #computer starting, the board.matrix is empty
        board.set_cell(1,1,player_sym)               #set the center
    elif turn==1:
        if board.get_cell(1,1)==" ":
            board.set_cell(1,1,player_sym)
        else:
            board.set_cell(0,0,player_sym)
    else:
        target=is_threat_exist(board, player_sym)    #is the computer has 2 cells sequence?
        if target:
               i=target[0][0]
               j=target[0][1]
               if board.get_cell(i,j)==" ":
                     board.set_cell(i,j,player_sym)  #set the third and win
                     db("win?")
            
        else:
            cells=is_threat_exist(board, other_player_sym)   #is threat exist from the other player (user)?
            if cells:
                i=cells[0][0]
                j=cells[0][1]
                board.set_cell(i,j,player_sym)               #block it
                db("is t")
            else:        
                cells=create_threat(board, player_sym,other_player_sym)    #try to create a threat
                if cells:
                    i=cells[0][0]
                    j=cells[0][1]
                    board.set_cell(i,j,player_sym)
                    db("create t")
                
                else:
                    num_of_moves=0
                    for i in range(3):
                        for j in range(3):
                            if num_of_moves==0:
                                if board.get_cell(i,j)==" ":
                                    board.set_cell(i,j,player_sym)    #choose empty cell
                                    db("draw"+str(num_of_moves))
                                    num_of_moves+=1
                                    
    board.print_board()

def is_win(board, player_sym):
    """check if there a winning sequence in the board"""
    seq=0
    for i in range (3):
        for j in range (3):
            if board.get_cell(i,j)==player_sym:
                seq+=1
        if seq==3:
            return True
        seq=0
    seq=0
    for i in range (3):
        for j in range (3):
            if board.get_cell(j,i)==player_sym:
                seq+=1
        if seq==3:
            return True
        seq=0
        #for diagonal sequences
    if board.get_cell(0,0)==board.get_cell(1,1)==board.get_cell(2,2)==player_sym:
        return True
    if board.get_cell(2,0)==board.get_cell(1,1)==board.get_cell(0,2)==player_sym:
        return True
    return False

def db(msg=""):
    print("db: ", end="")
    if msg=="":
       print("here")
    else:
       print(msg)


def player_move(board, player_sym):
    """exacute the user turn"""
    i=parse_input("enter first coordinate ")
    j=parse_input("enter second coordinate ")
    while board.get_cell(i,j)!=" ":
        print("cell is occupied")
        i=parse_input("enter first coordinate ")
        j=parse_input("enter second coordinate ")

    board.set_cell(i,j,player_sym)
    board.print_board() 
   
    

def parse_input(inst):
    """get the input from user and checking if legal"""

    i=input(inst)
    while not legal(i):
        i=input(inst)
    return int(i)-1

def legal(x ):
    """return trueif input is a number in range(1,4)"""
    
    if x=="":             #ignore new lines
        print(end="")
        return False
    else:
        if (len (x)>1) or (ord(x)>51 or ord(x)<49):
            print("ilegal number")
            return False
     
    return True






def play(b, player_sym,other_sym,turn):
    """exacuting the tic tac toe game: first the turn is played by calling to the current exacute
       function according to the player_sym. after that, checking the board status:
       is there is a winning sequence on the board?
       is there still empety cells on board (turn< 9)?"""
    if player_sym=="x":
        print(" THE COMPUTER MOVE IS: ")
        computer_move(b,turn,player_sym, other_sym)
    else:
        player_move(b,player_sym)
    turn+=1
    if is_win(b,player_sym):
            print(player_sym+ " won!")      #annaunce the winner
            return None                     #terminate the game
    elif turn ==9:                          #there is no winner, board is full
         print ("draw")                     #annunce "draw"
         return None                        #terminate the game
    else:                                   #game still can be played
         play(b,other_sym, player_sym,turn)
    
def instructions(to_show):
    """printing the game's instructions, with example how the board is represents the game"""
    if to_show:
        print("INSTRUCTIONS: ")
        print("press ENTER to progress")
        c=board_game.Board(3,3,True)
        print("this is the game board: ")
        c.print_board()
        t=input()
        print("you have to fill the cells and create a winner sequence")
        print("at every turn choose tow numbers, every one is  between 1-3 ")
        t=input()
        print ("for example: if the player symbol is *0* and 2,3 was chosen, the board will show like that:")
        print("enter first coordinate 2\nenter second coordinate 3")
        t=input()
        c.set_cell(1,2,"0")
        c.print_board()
        print("the player who will begin will be chosen  randomly")
        t=input()
        print("The game is startng")
    else:
        print(end="")
    
            
def main():
    """intialize the game. computre allways has the "x" symbol, and user has the "0" symbol"""
    print ("This is a TIC TAC TOE game\nUser symbol is *0*\nComputer symbol is *x*\n ")
    instructions(1)
    x=0# random.randint(0,1)       #the first player is randomly chosen
    b=board_game.Board(3,3,True)   #initializing the game's board


    if x==0:                       #computer is starting
        print ("computer is starting")
        play(b, "x","0", 0)
    else:
        print("user is starting")
        play(b, "0","x", 0) 
        
   
#############
#  TESTER   #
#############    




def test1():
    computer_move(b,0, "x", "0")
    b.set_cell(2,1, "0")
    b.print_board()
    computer_move(b,2,"x","0")
    b.set_cell(2,2, "0")
    b.print_board()
    computer_move(b,4,"x","0")
    b.set_cell(0,2, "0")
    b.print_board()
    computer_move(b,6,"x","0")

#test1()
main()
