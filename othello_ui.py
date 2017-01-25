# othello_ui.py
# Siddhartha Desai

import othello

def user_interface():
    '''Interface that is presented to the user'''
    print('Welcome to Othello.\n')
    # Ask user for dimensions
    board_dimensions = _ask_for_dimensions()
    print()
    # Ask user for color choice
    color_choice = _ask_white_or_black()
    print()
    # Ask user for color in the top left
    top_left = _ask_top_left()
    print()
    # Ask user for game mode (highest wins / lowest wins)
    game_mode = _ask_game_mode()

    # Create othello game
    game = othello.othello(board_dimensions[0], board_dimensions[1], color_choice, top_left)
    # game = othello.othello(8, 8, 'B', 'B')
    
    _display_stats(game)
    no_valid_moves = 0

    # Main loop that asks the players for moves
    while True:
        try:
            # If the board is full, determine the winner
            winner = othello.winning_player(game, othello.is_board_full(game), game_mode)
            if ('W' or 'B' or 'WB') == winner:
                break

            # If there is no available moves, then raise exception
            if not othello._any_available_moves(game):
                _display_board(game)
                raise othello.OthelloNoValidMoves()

            _ask_for_move(game)
            game.change_player()
            _display_stats(game)
            no_valid_moves = 0

        except othello.OthelloOutOfBoundsError:
            _display_stats(game)
            print('Move specified was out of the board.')

        except othello.OthelloNotEmptyError:
            _display_stats(game)
            print('Cannot place piece over an existing piece.')

        except othello.OthelloNoValidMoves:
            game.change_player()
            no_valid_moves += 1
            
            # If both players are unable to move, break out of loop
            if no_valid_moves == 2:
                winner = othello.winning_player(game, True, game_mode)
                break
            
            print('Player {} has no available moves.'.format(game.opposite_turn()))
            print("Player {}'s turn again.".format(game.current_turn()))

    print('Game Over')
   
    if winner == 'W' or winner == 'B':
        print('Player {} wins!'.format(winner))
    elif winner == 'WB':
        print('No winner.')
            

def _ask_for_dimensions() -> list:
    '''Ask user for the board dimensions'''
    while True:
        try:
            num_rows = _ask_for_rows()
            num_cols = _ask_for_cols()
            return [num_rows, num_cols]
        except ValueError:
            print('Did not give a valid column number\n')


def _ask_for_rows() -> int:
    '''Ask user for number of board rows. Needs to be an even integer between
    between 4 and 16.'''
    while True:
        rows = input('Please specify the number of rows:\nMust be an even integer between 4 - 16: ').strip()
        if len(rows) == 0:
            print("No input given.\n")
        else:
            int_rows = int(rows)
            error_message = ''
            if int_rows % 2 != 0:
                error_message += 'Input was not an even number\n'
            if int_rows < 4:
                error_message += 'Input was less than 4 rows\n'
            elif int_rows > 16:
                error_message += 'Input was greater than 16 rows\n'
            print(error_message)
        if not (len(rows) == 0) and not (int(rows) % 2 != 0) and not (int(rows) < 4) and not (int(rows) > 16):
            return int(rows)


def _ask_for_cols() -> int:
    '''Ask user for number of board columns. Needs to be an even integer between
    between 4 and 16.'''
    while True:
        cols = input('Please specify the number of columns:\nMust be an even integer between 4 - 16: ').strip()
        if len(cols) == 0:
            print("No input given.\n")
        else:
            error_message = ''
            int_cols = int(cols)
            if int_cols % 2 != 0:
                error_message += 'Input was not an even number\n'
            if int_cols < 4:
                error_message += 'Input was less than 4 rows\n'
            elif int_cols > 16:
                error_message += 'Input was greater than 16 rows\n'
            print(error_message)
        if not (len(cols) == 0) and not (int(cols) % 2 != 0) and not (int(cols) < 4) and not (int(cols) > 16):
            return int(cols)


def _ask_white_or_black() -> str:
    '''Ask user if they want to play as black or white'''
    while True:
        color = input('Would you like to start first (black) or second (white): ')
        if len(color) == 0:
            print("No starting color given\n")
        else:
            color = color.strip().lower()
            if color == 'black':
                return 'B'
            elif color == 'white':
                return 'W'
            else:
                print('Not a valid color.\n')

def _ask_top_left() -> str:
    '''Ask user which color disc should be placed in the top left'''
    while True:
        color = input('Which color do you want the top left piece? (black) or (white): ')
        if len(color) == 0:
            print("No starting color given\n")
        else:
            color = color.strip().lower()
            if color == 'black':
                return 'B'
            elif color == 'white':
                return 'W'
            else:
                print('Not a valid color.\n')


def _ask_game_mode() -> str:
    '''Ask the user if they want a higher score to win or a lower score to win'''
    while True:
        game_mode = input("Should the (high)er score win or (low)er score win? ")
        if len(game_mode) == 0:
            print("No game mode given\n")
        else:
            game_mode = game_mode.strip().lower()
            if game_mode == 'high':
                return 'high'
            elif game_mode == 'low':
                return 'low'
            else:
                print("Invalid game mode\n")


def _ask_for_move(game: othello) -> None:
    '''Ask the user for a move'''
    while True:
        move = input("Please type in a move, example: 1, 2: ")
        if len(move) == 0:
            print("No move given\n")
        if len(move.strip().split(',')) != 2:
            print('Did not specify a row and column.\n')
        else:
            move = move.strip()
            try:
                move = move.split(',')
                row = int(move[0].strip()) - 1
                col = int(move[1].strip()) - 1
                othello.make_a_move(game, [row, col])
                return
            
            except ValueError:
                print()
                print('Did not type in a valid number.\n')


def _display_stats(game: othello):
    '''Display the scores, board, and current turn''' 
    print()
    print('-----------------------------------------------')
    _display_score(game)
    _display_board(game)
    _display_turn(game)
    print('-----------------------------------------------')
    print()

def _display_board(game: othello):
    '''Display the board'''
    game.print_board()
    print()
    
def _display_score(game: othello):
    '''Display the score'''
    game.print_score()
    print()

def _display_turn(game: othello):
    '''Display the current turn'''
    game.print_turn()


if __name__ == '__main__':
    user_interface()
