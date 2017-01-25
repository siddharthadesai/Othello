# othello.py
# Siddhartha Desai

#
# Othello Errors
#
class OthelloDimensionError(Exception):
    '''Raised if the user tries to create the board with dimensions that are
    not even integers between 4 and 16'''
    pass

class OthelloOutOfBoundsError(Exception):
    '''Raised if the user tries to place a disk out of bounds''' 
    pass

class OthelloNotEmptyError(Exception):
    '''Raised if the user tries to place a disk in a nonempty spot'''
    pass

class OthelloNoValidMoves(Exception):
    '''Raised if there are no more valid moves for the current player'''
    pass


#
# Othello class
# 
class othello:
    def __init__(self, rows, cols, turn, top_left):
        '''othello class constructor'''
        # Check if dimensions are valid
        self._check_valid_dimensions(rows, cols)
        
        # Initialize variables
        self._num_rows = rows
        self._num_cols = cols
        self._player_turn = turn
        self._white_score = 2
        self._black_score = 2
        self._board = []

        # Create a new starting board
        self._create_board(top_left)

    ### Setting up board functions    
    def _create_board(self, top_left: str) -> None:
        '''Create an empty board and then fill it with the middle 4 pieces'''
        for col in range(self._num_cols):
            self._board.append([])
            for row in range(self._num_rows):
                self._board[-1].append([])
    
        self._fill_starting_pieces(top_left)

    def _fill_starting_pieces(self, top_left: str) -> None:
        '''Fill in the initial middle 4 pieces depending on the user's top
        left color choice'''
        _half_rows = int(self._num_rows/2)
        _half_cols = int(self._num_cols/2)     

        if top_left == 'W':
            self._board[_half_cols - 1][_half_rows - 1] = 'W'
            self._board[_half_cols - 1][_half_rows] = 'B'
            self._board[_half_cols][_half_rows - 1] = 'B'
            self._board[_half_cols][_half_rows] = 'W'
        else:
            self._board[_half_cols - 1][_half_rows - 1] = 'B'
            self._board[_half_cols - 1][_half_rows] = 'W'
            self._board[_half_cols][_half_rows - 1] = 'W'
            self._board[_half_cols][_half_rows] = 'B'

    def _check_valid_dimensions(self, num_rows, num_cols) -> None:
        '''Check if the board dimensions that were specified are valid'''
        if num_rows % 2 != 0 and num_cols % 2 != 0:
            raise OthelloNotEvenError('Number of rows and columns needs to be an even integer.')
        if num_rows < 4 or num_rows > 16 or \
           num_cols < 4 or num_cols > 16:
            raise OthelloDimensionError('Number of rows and columns must be between 4 and 16')


    ### Setter methods
    def set_board(self, location: list, turn: str) -> None:
        '''Given a location, place the proper turn in it'''
        x = location[0]; y = location[1]
        self._board[x][y] = turn

    def change_player(self) -> None:
        '''Changes the current player to the opposite player'''
        if self._player_turn == 'W':
            self._player_turn = 'B'
        else:
            self._player_turn = 'W'

    def update_score(self) -> None:
        '''Update the the scores'''
        white_score = 0
        black_score = 0
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                if self._board[col][row] == 'W':
                    white_score += 1
                if self._board[col][row] == 'B':
                    black_score += 1
        self._white_score = white_score
        self._black_score = black_score
        

    ### Getter Methods
    def current_turn(self) -> str:
        '''Return the current player'''
        return self._player_turn

    def opposite_turn(self) -> str:
        '''Return the opposite player'''
        if self._player_turn == 'W':
            return 'B'
        else:
            return 'W'

    def get_board(self) -> list:
        '''Return the board'''
        return self._board

    def get_num_rows(self) -> int:
        '''Return the number of board rows'''
        return self._num_rows

    def get_num_cols(self) -> int:
        '''Return the number of board columns'''
        return self._num_cols

    def get_white_score(self) -> int:
        '''Return the white player's score'''
        return self._white_score

    def get_black_score(self) -> int:
        '''Return the black player's score'''
        return self._black_score
    
    
    ### Helper methods to print out variables of the board
    def print_board(self) -> None:
        '''Print the board'''
        print('    ', end='')
        for column in range(1, self._num_cols + 1):
            if column < 10:
                print(column, ' ', end='')
            else:
                print(column, end=' ')
        print()

        for row in range(self._num_rows):
            print('{:2} '.format(row+1), end='')
            for col in range(self._num_cols):
                if len(self._board[col][row]) == 0:
                    print('[ ]', end='')
                else:
                    print('[{}]'.format(self._board[col][row]), end='')
            if col == self._num_cols - 1:
                print()

    def print_score(self) -> None:
        '''Print out the scores'''
        print('Black: {}  White: {}'.format(self._black_score,
                                            self._white_score))
        
    def print_turn(self) -> None:
        '''Print out the current turn'''
        print('Turn: {}'.format(self._player_turn))


#
# Othello Functions
#
def make_a_move(game: othello, location: list) -> None:
    '''Checks if the location is not out of bounds and not already filled. It
    then checks if the board changed, if it didn't, then make sure that the
    same player repeats his move. At the end, update the score'''
    _require_valid_row_col_number(game, location[0], location[1])
    _is_empty(game, location)

    changed = _flip(game, location)
    if not changed:
        # print("Not a valid move. Still player {}'s turn.".format(game.current_turn()))
        game.change_player()
        
    game.update_score()
    

### Checking functions
def _require_valid_row_col_number(game: othello, row_num: int, col_num: int):
    '''Checks if the location is inside the board's dimensions'''
    _require_valid_row_number(game, row_num)
    _require_valid_col_number(game, col_num)

def _require_valid_row_number(game: othello, row_num: int):
    '''Checks if the row number is inside the board's dimensions and is a valid
    number (integer)'''
    if type(row_num) != int:
        raise ValueError('Row number is invalid')
    if not _valid_row_number(game, row_num):
        raise OthelloOutOfBoundsError('Row number must be between 1 and {}.'.format(game.get_num_rows()))

def _require_valid_col_number(game: othello, col_num: int):
    '''Checks if the column number is inside the board's dimensions and is a
    valid number (integer)'''
    if type(col_num) != int:
        raise ValueError('Column number is invalid')
    if not _valid_col_number(game, col_num):
        raise OthelloOutOfBoundsError('Column number must be between 1 and {}.'.format(game.get_num_cols()))

def _valid_row_number(game: othello, row_num: int) -> bool:
    '''Checks if the row number is inside the board's dimensions'''
    return 0 <= row_num < game.get_num_rows()
    
def _valid_col_number(game: othello, col_num: int) -> bool:
    '''Checks if the column number is inside the board's dimensions'''
    return 0 <= col_num < game.get_num_cols()

def _is_empty(game: othello, location: list) -> None:
    '''Raises an exception if the location is not empty'''
    if len(game.get_board()[location[1]][location[0]]) != 0:
        raise OthelloNotEmptyError()


### Winning functions
def is_board_full(game: othello) -> bool:
    '''Checks if the board is full'''
    for row in range(game.get_num_rows()):
        for col in range(game.get_num_cols()):
            if len(game.get_board()[col][row]) == 0:
                return False
    return True


def winning_player(game: othello, full: bool, mode: str) -> str:
    '''If the board is full, check who won depending on the mode'''
    if full:
        # Higher score wins
        if mode == 'high':
            if game.get_white_score() > game.get_black_score():
                return 'W'
            elif game.get_white_score() < game.get_black_score():
                return 'B'
            else:
                return 'WB'
        # Lower score wins
        elif mode == 'low':
            if game.get_white_score() > game.get_black_score():
                return 'B'
            elif game.get_white_score() < game.get_black_score():
                return 'W'
            else:
                return 'WB'
        else:
            return
    return

def _any_available_moves(game: othello) -> bool:
    '''Checks if there are any available moves'''
    game_board = game.get_board()
    for row in range(game.get_num_rows()):
        for col in range(game.get_num_cols()):
            if len(game_board[col][row]) == 0:
                check1 = _flip_horizontal_vertical(game, [row, col], False)
                check2 = _flip_diagonal(game, [row, col], False)
                
                if check1 or check2:
                    return True
    return False
    

### Functions to flip pieces on the board when a move is made
def _flip(game, location) -> bool:
    '''Checks if there are any pieces to flip'''
    check1 = _flip_horizontal_vertical(game, location, True)
    check2 = _flip_diagonal(game, location, True)

    return check1 or check2:

def _flip_horizontal_vertical(game: othello, location: list, value: bool) -> bool:
    '''Scans the horizontal and vertical directions for pieces to flip'''
    game_board = game.get_board()
    x = location[0]; y = location[1]
    hori_left_list = []; hori_right_list = []
    verti_up_list = []; verti_down_list = []
    flip_list = []

    # Horizontal Left
    left_y = y-1
    if left_y >= 0:
        while game_board[left_y][x] == game.opposite_turn():
            # print('Horizontal Left')
            hori_left_list.append([left_y, x])
            left_y -= 1
            if left_y < 0:
                hori_left_list = []
                break
        
    # Horizontal Right
    right_y = y+1
    if right_y < game.get_num_cols():
        while game_board[right_y][x] == game.opposite_turn():
            # print('Horizontal Right')
            hori_right_list.append([right_y, x])
            right_y += 1
            if right_y >= game.get_num_cols():
                hori_right_list = []
                break

    # Vertical Up
    up_x = x-1
    if up_x >= 0:
        while game_board[y][up_x] == game.opposite_turn():
            # print('Vertical Up')
            verti_up_list.append([y, up_x])
            up_x -= 1
            if up_x < 0:
                verti_up_list = []
                break

    # Vertical Down
    down_x = x+1
    if down_x < game.get_num_rows():
        while game_board[y][down_x] == game.opposite_turn():
            # print('Vertical Down')
            verti_down_list.append([y, down_x])
            down_x += 1
            if down_x >= game.get_num_rows():
                verti_down_list = []
                break

    # Only add the list if the next piece in the direction is the same
    if len(hori_left_list) != 0 and left_y >= 0:
        if game_board[left_y][x] == game.current_turn():
            flip_list.extend(hori_left_list)
    if len(hori_right_list) != 0 and right_y < game.get_num_cols():
        if game_board[right_y][x] == game.current_turn():
            flip_list.extend(hori_right_list)
    if len(verti_up_list) != 0 and up_x >= 0:
        if game_board[y][up_x] == game.current_turn():
            flip_list.extend(verti_up_list)
    if len(verti_down_list) != 0 and down_x < game.get_num_rows():
        if game_board[y][down_x] == game.current_turn():
            flip_list.extend(verti_down_list)

    # If value is True, set the board and flip the pieces
    if len(flip_list) != 0 and value:    
        game.set_board([y, x], game.current_turn())
        _flip_pieces(game, flip_list, game.current_turn())
        return True
    # If the value is False, just check if there are pieces to be flipped
    if not value:
        if len(flip_list) == 0:
            return False
        else:
            return True
    return False

def _flip_diagonal(game: othello, location: list, value = bool) -> bool:
    '''Scans the diagonal directions for pieces to flip'''
    game_board = game.get_board()
    x = location[0]; y = location[1]
    north_west_list = []; south_east_list = []
    north_east_list = []; south_west_list = []
    flip_list =  []

    # North West
    nw_x = x-1; nw_y = y-1
    if nw_x >= 0 and nw_y >= 0:
        while game_board[nw_y][nw_x] == game.opposite_turn():
            # print('North West')
            north_west_list.append([nw_y, nw_x])
            nw_x -= 1; nw_y -= 1
            if nw_x < 0 or nw_y < 0:
                north_west_list = []
                break

    # South East
    se_x = x+1; se_y = y+1
    if se_x < game.get_num_rows() and se_y < game.get_num_cols():
        while game_board[se_y][se_x] == game.opposite_turn():
            # print('South East')
            south_east_list.append([se_y, se_x])
            se_x += 1; se_y += 1
            if se_x >= game.get_num_rows() or se_y >= game.get_num_cols():
                south_east_list = []
                break

    # North East
    ne_x = x+1; ne_y = y-1
    if ne_x < game.get_num_rows() and ne_y >= 0:
        while game_board[ne_y][ne_x] == game.opposite_turn():
            # print('North East')
            north_east_list.append([ne_y, ne_x])
            ne_x += 1; ne_y -= 1
            if ne_x >= game.get_num_rows() or ne_y < 0:
                north_east_list = []
                break

    # South West
    sw_x = x-1; sw_y = y+1
    if sw_x >= 0 and sw_y < game.get_num_cols():
        while game_board[sw_y][sw_x] == game.opposite_turn():
            # print('South West')
            south_west_list.append([sw_y, sw_x])
            sw_x -= 1; sw_y += 1
            if sw_x < 0 or sw_y >= game.get_num_cols():
                south_west_list = []
                break
            
    # Only add the list if the next piece in the direction is the same            
    if len(north_west_list) != 0 and nw_x >= 0 and nw_y >= 0:
        if game_board[nw_y][nw_x] == game.current_turn():
            flip_list.extend(north_west_list)
    if len(south_east_list) != 0 and se_x < game.get_num_rows() and se_y < game.get_num_cols():
        if game_board[se_y][se_x] == game.current_turn():
            flip_list.extend(south_east_list)
    if len(north_east_list) != 0 and ne_x < game.get_num_rows() and ne_y >= 0:
        if game_board[ne_y][ne_x] == game.current_turn():
            flip_list.extend(north_east_list)
    if len(south_west_list) != 0 and sw_x >= 0 and sw_y < game.get_num_cols():
        if game_board[sw_y][sw_x] == game.current_turn():
            flip_list.extend(south_west_list)

    #print(flip_list)

    # If value is True, set the board and flip the pieces
    if len(flip_list) != 0 and value:
        game.set_board([y, x], game.current_turn())
        _flip_pieces(game, flip_list, game.current_turn())
        return True
    # If the value is False, just check if there are pieces to be flipped
    if not value:
        if len(flip_list) == 0:
            return False
        else:
            return True
    return False
 
def _flip_pieces(game: othello, locations: list, turn: str) -> list:
    '''Flip all the pieces that are specified in the location list'''
    for disk in locations:
        game.set_board(disk, turn)

                                      
