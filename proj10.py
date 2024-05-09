##############################################################################
#   CSE 231 project 10
#     
#   By: Jack McNamara
#
#   algorithm:
#   the program initilizes a game of aces up.
#   user can input a number of options to control what moves they wish to make.
#       depending on the option diffrent functions will be exicuted to cary out
#       the desired tasks if the comands are valid.
#       the user can continue this until they win the game or chose to quit
#   program ends and the user is notified of their victory or notified that 
#   they have selected to quit
################################################################################   


import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''


def init_game():
    """makes the stock, tableau, and foundation to be usedfor the rest of 
    the game"""
    # makes stock and shuffles
    stock = cards.Deck()
    stock.shuffle()
    # Makes a tuple of lists and lists the tuple
    tableau = [],[],[],[]
    tableau = list(tableau)
    # goes through each column in tableau and deals a card 
    for i,l in enumerate(tableau):
        tableau[i].append(stock.deal())
    # makes an empty list for foundation
    foundation = list()
    return (stock,tableau,foundation)
    
def deal_to_tableau( tableau, stock):
    # if the len of the stock is 4 or more then it deals a card to each column
    if stock.__len__() >= 4:
        for i,l in enumerate(tableau):
            tableau[i].append(stock.deal())
    # otherwise it deals to as many coulmns as it can
    else:
        for num in range(stock.__len__()-1):
            tableau[num].append(stock.deal)

           
def validate_move_to_foundation( tableau, from_col ):
    """evaluates the validity of a move from a column in the tableau to the 
    foundation"""
    try:
        # tries to index the card from the given coulmn
        card_to_move = tableau[from_col][-1]
        card_suit = card_to_move.suit()
        # if the card is an ace it cannot be moved
        if card_to_move.rank() == 1:
            print("\nError, cannot move {}.".format(card_to_move))
            # sets the return bool to false
            ret_bool = False
        else:
           # goes through each column
            for col in tableau:
                # if the column is not empty
                if len(col) != 0:
                    # takes the botom card of the column
                    card = col[-1]
                    # if the suit of the card matches the suit of the card being
                    # moved
                    if card.suit() == card_suit:
                        card_rank = card.rank()
                        # if the card is a ace the value is made 14
                        if card_rank == 1:
                            card_rank = 14
                        # if there is ever a a card higher than then the card 
                        # being moved , true is returned
                        if card_rank > card_to_move.rank():
                            return True
            # otherwise it is an invalid move
            ret_bool = False
            print("\nError, cannot move {}.".format(card_to_move))
    except:
        # if there is no card in the desired column to move the card from, the 
        # except suite will be entered and the move is invalid
        print("\nError, no card in column: {}".format(from_col+1))
        ret_bool = False
    return ret_bool


    
def move_to_foundation( tableau, foundation, from_col ):
    """moves a card from a desired column to teh foundation if the move is 
    valid"""
    # checks to see if the prospective move is valid
    valid_move = validate_move_to_foundation(tableau, from_col)
    # if the move is valid...
    if valid_move == True:
        # getes the bottom card from the column and moves it to the foundation
        to_foundation = tableau[from_col].pop(-1)
        foundation.append(to_foundation)


def validate_move_within_tableau( tableau, from_col, to_col ):
    """checks the validity of a move within the tablau from one column to 
    another"""
    # checking if the to_col is empty
    to_col_bool = bool(tableau[to_col])
    # if it empty then it cehcks if the from_col does have a card
    if to_col_bool == False:
        if bool(tableau[from_col]) == True:
            # the move is valid
            ret_bool = True
        else:
            # if there is no card in from_col the move is invalid 
            print("\nError, no card in column: {}".format(from_col+1))
            ret_bool = False
    else:
       # if there is a card in to_col the move is invalid
        ret_bool = False
        print("\nError, target column is not empty: {}".format(to_col+1))
    return ret_bool


def move_within_tableau( tableau, from_col, to_col ):
    """if a move within the tableau is valid it will be exicuted by this 
    function"""
    # checks to see if move is valid by calling validate_move_within_tableau
    valid_move = validate_move_within_tableau(tableau, from_col , to_col)
    # if it is valid...
    if valid_move == True:
        # the card is poped from the column
        to_new_col = tableau[from_col].pop(-1)
        # and added to the new column
        tableau[to_col].append(to_new_col) 

        
def check_for_win( tableau, stock ):
    """checks the tableau and stock to seee if the game is won"""
    # sets all ace bool to false
    tab_all_aces = False
    # initalizes counter to zero
    ace_count = 0
    # sets no other card bool to false
    no_other_cards = True
    # goes through each column
    for col in tableau:
        # goes through each card in the column
        for card in col:
            # if the rank of the card is  an ace the count is increased by 1
            if card.rank() == 1:
                ace_count += 1
            # otherwise the no other card booleon is made false and the loop 
            # breaks
            else:
                no_other_cards = False
                break
    # if the ace count is 4 and there are no other cards in the tableau
    if ace_count == 4 and no_other_cards ==True:
        # the tab all aces is True
        tab_all_aces = True
    # if the stock is empty and the tableau is all aces then the return bool is 
    # made true
    if stock.is_empty() == True and tab_all_aces == True:
        ret_bool = True
    # otherwise the return bool is false
    else:
        ret_bool = False
    return ret_bool

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    """makes a list of the users inputs and retruns the list"""
    return_list = []
    user_input = input("\nInput an option (DFTRHQ): ")
    try:   
        
        if user_input.lower() =='d':
            # D is the option added to the return list
            return_list.append('D')
        elif user_input[0].lower() =='f':
            # splits to make a list with f and the column to move from
            return_list = user_input.split()
            # subtracts the column by 1 to get the proper index
            return_list[1] = int(return_list[1])-1
            # checks to see if the index is out of the index range range
            if return_list[1] not in range(0,4):
                # if it is an error is given and the return list is empty
                print("\nError in option: {}" .format(user_input))
                return_list = []
            else:
               # the upercase of the entry is given in the return list
                return_list[0] = return_list[0].upper()
        elif user_input[0].lower() == 't':
            # splits to make a list of the option and the columns
            return_list = user_input.split()
            # subtracts 1 from the columns to get their indexies
            return_list[1] = int(return_list[1])-1
            return_list[2] = int(return_list[2])-1
            # if either of the columns re not in the range an error is give and 
            # the return list will be empty
            if return_list[1] not in range(0,4) or return_list[2] not in range(0,4):
                print("\nError in option: {}" .format(user_input))
                return_list = []    
           # makes the option upper case
            else:
                return_list[0] = return_list[0].upper()
        # appends the upercase of the input for 'r','h',and'q'
        elif user_input.lower() == 'r':
            return_list.append('R')
        elif user_input.lower() == 'h':
            return_list.append('H')
        elif user_input.lower() == 'q':
            return_list.append('Q')
        # if the input does not mathc any of the above an error is returned
        # along with an empty list
        else:
            print("\nError in option: {}" .format(user_input))
            return_list = []
    except:
        # if there is ane error in the try suite the input is invalid and the 
        # user is notified 
        print("\nError in option: {}" .format(user_input))
        return_list = []
    return return_list

def main():
    print(RULES)
    print(MENU)
    # makes the data structures to beign with
    stock,tableau,foundation = init_game()
    # prints original hand
    display(stock, tableau, foundation)
    # gets the users option
    get_op_list = get_option()
    # while the option is invalid
    while bool(get_op_list) == False:
        # get a new option
        get_op_list = get_option()
   # until the user enters q the loop continues
    while get_op_list[0].lower() != 'q':
        # if the user enters d then  the program deals
        if get_op_list[0].lower()=='d':
            deal_to_tableau(tableau, stock)
        elif get_op_list[0].lower()=='f':
            # makes the move column
            move_c = get_op_list[1]
            # calls move_to_foundation to move the card if possible
            move_to_foundation(tableau, foundation, move_c)
        elif get_op_list[0].lower()=='t':
            # makes the value of the columns
            from_col = get_op_list[1]
            to_col = get_op_list[2]
            # moves the card if the move is possible
            move_within_tableau(tableau, from_col, to_col)
       # if the user coices r the game is re-initalized and prints a the rules
       # and menu
        elif get_op_list[0].lower() == 'r':
            print("\n=========== Restarting: new game ============")
            print(RULES)
            print(MENU)
            # re-initilizes game
            stock,tableau,foundation = init_game()
        # prints menu if user enters h
        elif get_op_list[0].lower() == 'h':
            print(MENU)
        # checks for win after each input
        win_check = check_for_win(tableau, stock)
        # if the player has won the loop breaks
        if win_check == True:
            break
        # if the game is not over the hand is displayed
        display(stock, tableau, foundation)
       # a new input is accepted
        get_op_list = get_option()
        while bool(get_op_list) == False:
            get_op_list = get_option()
    # if the player won they are notified
    if win_check == True:
        print("\nYou won!")
    # otherwise they are notified that they quit the game
    else:
        print("\nYou have chosen to quit.")
        
        

if __name__ == '__main__':
     main()

