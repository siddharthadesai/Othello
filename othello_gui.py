# othello_gui.py
# Siddhartha Desai

import othello
import disk
import tkinter
from tkinter.messagebox import showinfo

class OthelloGameOver(Exception):
    '''Raised if the game is over'''
    pass

class OthelloGUI:
    '''Othello GUI class'''
    ### Othello GUI Constructor
    def __init__(self):
        # Initialize variables
        self._state = []
        self._rows = None
        self._cols = None
        self._color = None
        self._top_left = None
        self._mode = None
        self._button_pressed = False

        # Create main window
        self._main_window = tkinter.Tk()
        #self._main_window.wm_minsize(width=230, height=400)

        # Initialize textvariable StringVars
        self._row_choice = tkinter.StringVar()
        self._col_choice = tkinter.StringVar()
        self._color_choice = tkinter.StringVar()
        self._top_left_choice = tkinter.StringVar()
        self._mode_choice = tkinter.StringVar()

        # Create user choices
        dimensions = ('4', '6', '8', '10', '12', '14', '16')
        colors = ('Black', 'White')
        modes = ('High', 'Low')

        # Create option widgets
        self._othello_text = tkinter.Label(self._main_window, text = 'OTHELLO', font = ('Helvetica', 30))
        self._row_text = tkinter.Label(self._main_window, text = 'Number of rows:')
        self._col_text = tkinter.Label(self._main_window, text = 'Number of columns:')
        self._color_text = tkinter.Label(self._main_window, text = 'Black or white:')
        self._top_left_text = tkinter.Label(self._main_window, text = 'Top left color:')
        self._mode_text = tkinter.Label(self._main_window, text = 'High or Low Mode:')

        self._row_menu = tkinter.OptionMenu(self._main_window, self._row_choice, *dimensions, command = self._set_row)
        self._col_menu = tkinter.OptionMenu(self._main_window, self._col_choice, *dimensions, command = self._set_col)
        self._color_menu = tkinter.OptionMenu(self._main_window, self._color_choice, *colors, command = self._set_color)
        self._top_left_menu = tkinter.OptionMenu(self._main_window, self._top_left_choice, *colors, command = self._set_top_left)
        self._mode_menu = tkinter.OptionMenu(self._main_window, self._mode_choice, *modes, command = self._set_mode)

        self._play_button = tkinter.Button(self._main_window, text = 'Play Game', command = self._set_button)

        # Set up grid layout
        self._othello_text.grid(row = 0, columnspan = 2, padx = 10, pady = 10)
        self._row_text.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.W)
        self._col_text.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = tkinter.W)
        self._color_text.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = tkinter.W)
        self._top_left_text.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = tkinter.W)
        self._mode_text.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        self._row_menu.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tkinter.E)
        self._col_menu.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = tkinter.E) 
        self._color_menu.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = tkinter.E)
        self._top_left_menu.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = tkinter.E)
        self._mode_menu.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = tkinter.E)
        self._play_button.grid(row = 6, columnspan = 2, padx = 10, pady = 10)

        # Set up grid configurations
        self._main_window.rowconfigure(0, weight = 1)
        self._main_window.columnconfigure(0, weight = 1)


    ### Event setting methods
    def _set_row(self, event: tkinter.Event) -> None:
        '''Set # of rows to user row choice'''
        self._rows = int(self._row_choice.get())
        self._create_game()
        # print(self._rows)
        
    def _set_col(self, event: tkinter.Event) -> None:
        '''Set # of columns to user column choice'''
        self._cols = int(self._col_choice.get())
        self._create_game()
        # print(self._cols)
        
    def _set_color(self, event: tkinter.Event) -> None:
        '''Set color to user color choice'''
        self._color = self._color_choice.get()
        if self._color == 'Black':
            self._color = 'B'
        else:
            self._color = 'W'
        self._create_game()
        # print(self._color)
        
    def _set_top_left(self, event: tkinter.Event) -> None:
        '''Set top left color to user top left color choice'''
        self._top_left = self._top_left_choice.get()
        if self._top_left == 'Black':
            self._top_left = 'B'
        else:
            self._top_left = 'W'
        self._create_game()
        # print(self._top_left)
        
    def _set_mode(self, event: tkinter.Event) -> None:
        '''Set mode to user mode choice'''
        self._mode = self._mode_choice.get().lower()
        self._create_game()
        # print(self._mode)
        
    def _set_button(self) -> None:
        '''Set button pressed equal to true to allow for continuation'''
        self._button_pressed = True
        self._create_game()

        
    ### Game Updating Methods
    def start(self) -> None:
        '''Run the tkinter mainloop'''
        self._main_window.mainloop()

    def _create_game(self):
        '''Delete the previous widgets, and call the game widget making functions
        if button has been pressed. If not, then reset back to False'''
        if ((self._rows and self._cols and self._color and self._top_left and self._mode) != None) and self._button_pressed:
            self._game = othello.othello(self._rows, self._cols, self._color, self._top_left)

            # Delete option window widgets
            self._othello_text.grid_remove()
            self._row_text.grid_remove()
            self._col_text.grid_remove()
            self._color_text.grid_remove()
            self._top_left_text.grid_remove()
            self._mode_text.grid_remove()
            self._row_menu.grid_remove()
            self._col_menu.grid_remove()
            self._color_menu.grid_remove()
            self._top_left_menu.grid_remove()
            self._mode_menu.grid_remove()
            self._play_button.grid_remove()

            # Create the canvas and update the disk state'''
            self._create_canvas()
            self._create_state()
        else:
            self._button_pressed = False

    def _create_canvas(self):
        '''Create the tkinter canvas on the main window'''
        if self._rows > self._cols:
            span = 650 / self._rows
        else:
            span = 650 / self._cols
            
        self._canvas = tkinter.Canvas(
            master = self._main_window,
            width = self._cols * span, height = self._rows * span,
            background = '#FFDAB9')

        self._canvas.grid(
            row = 0, column = 0, columnspan = 3, padx = 0, pady = 0,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        
        self._canvas.bind('<Configure>', self._canvas_resized)
        self._canvas.bind('<Button-1>', self._mouse_click)            
        
        #force = tkinter.Event()
        #self._canvas_resized(force)'''

    def _create_state(self):
        '''Go through the board and create a Disk object for each piece'''
        self._state = []
        board = self._game.get_board()

        # Calculate pixel lengths
        delta_x = self._canvas.winfo_width() / self._cols
        delta_y = self._canvas.winfo_height() / self._rows
        half_delta_x = delta_x - (delta_x / 2)
        half_delta_y = delta_y - (delta_y / 2)

        # Create a Disk object for each piece in the board and append to list
        for row in range(self._rows):
            for col in range(self._cols):
                if board[col][row] != []:
                    px = (delta_x * col) + half_delta_x
                    py = (delta_y * row) + half_delta_y
                    rx = half_delta_x * 0.75
                    ry = half_delta_y * 0.75
                    self._state.append(self._produce_disk(px, py, rx, ry, board[col][row]))

        self._redraw_disks()

        # Create labels for keeping track of score and turn
        self._white_score_label = tkinter.StringVar()
        self._black_score_label = tkinter.StringVar()
        self._player_turn_label = tkinter.StringVar()
        self._white_score_label = tkinter.Label(self._main_window, text = 'White: {}'.format(self._game.get_white_score()), font = ('Helvetica', 16))
        self._black_score_label = tkinter.Label(self._main_window, text = 'Black: {}'.format(self._game.get_black_score()), font = ('Helvetica', 16))
        self._player_turn_label = tkinter.Label(self._main_window, text = 'Turn: {}'.format(self._game.current_turn()), font = ('Helvetica', 16))
        self._player_turn_label.grid(row = 1, columnspan = 3, padx = 10, pady = 10, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._white_score_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = tkinter.W)
        self._black_score_label.grid(row = 2, column = 2, padx = 10, pady = 5, sticky = tkinter.E)
        
    def _produce_disk(self, px: float, py: float, rx: float, ry: float, color: str) -> disk.Disk:
        '''Given inputs, return a Disk object'''
        canvas_x = self._canvas.winfo_width()
        canvas_y = self._canvas.winfo_height()
    
        return disk.Disk((px/canvas_x, py/canvas_y), (rx/canvas_x, ry/canvas_y), color)
        

    ### Event Handlers
    def _canvas_resized(self, event: tkinter.Event) -> None:
        '''When the canvas is resized, delete all widgets and redraw them'''
        self._canvas.delete(tkinter.ALL)
        
        self._draw_grid()
        self._redraw_disks()

    def _mouse_click(self, event: tkinter.Event) -> None:
        '''When the mouse is clicked, convert pixels into row and column. Then
        run the game flow method'''
        canvas_x = self._canvas.winfo_width()
        canvas_y = self._canvas.winfo_height()
        
        # print(event.x, event.y)
        row = int(event.y // (canvas_y / self._rows))
        col = int(event.x // (canvas_x / self._cols))
        # print(row)
        # print(col)
            
        is_winner = self._game_flow(row, col)
        # othello_ui._display_board(self._game)
        if is_winner:
            self._create_state()
            self._redraw_disks()
            self._display_winner()
            return

        self._create_state()
        self._redraw_disks()


    ### Drawing Methods
    
    
    def _draw_grid(self) -> None:
        '''Draw grid lines'''
        delta_x = self._canvas.winfo_width() / self._cols
        delta_y = self._canvas.winfo_height() / self._rows
        for i in range(self._cols):
            self._canvas.create_line(delta_x*i, 0, delta_x*i, self._canvas.winfo_height(), fill = 'black')
        for j in range(self._rows):
            self._canvas.create_line(0, delta_y*j, self._canvas.winfo_width(), delta_y*j, fill = 'black')            

    def _redraw_disks(self) -> None:
        '''Draw disks from the list of Disk objects'''
        canvas_px = self._canvas.winfo_width()
        canvas_py = self._canvas.winfo_height()
        
        for disk in self._state:
            center_x = canvas_px * disk.center()[0] 
            center_y = canvas_py * disk.center()[1]
            radius_x = canvas_px * disk.radius()[0]
            radius_y = canvas_py * disk.radius()[1]
            
            self._canvas.create_oval(
                center_x - radius_x,
                center_y - radius_y,
                center_x + radius_x,
                center_y + radius_y,
                fill = disk.color(), outline = disk.opposite_color())

    def _display_winner(self) -> None:
        '''Display a pop up window when someone wins'''
        winner_str = 'Player {} wins!\n\nWhite score: {}\nBlack score: {}'.format(self._winner, self._game.get_white_score(), self._game.get_black_score())
        showinfo(message = winner_str)


    ### Main Gameplay Methods
    def _game_flow(self, row: int, col: int) -> bool:
        '''Incorporating the game play logic into GUI'''
        try:
            # If the board is full, determine the winner
            self._winner = othello.winning_player(self._game, othello.is_board_full(self._game), self._mode)
            if ('W' or 'B' or 'WB') == self._winner:
                return True

            # If there is no available moves, then raise exception
            if not othello._any_available_moves(self._game):
                raise othello.OthelloNoValidMoves()
            
            othello.make_a_move(self._game, [row, col])
            self._redraw_disks()
            self._game.change_player()
            self._create_state()

            self._winner = othello.winning_player(self._game, othello.is_board_full(self._game), self._mode)
            if ('W' or 'B' or 'WB') == self._winner:
                return True

            if not othello._any_available_moves(self._game):
                raise othello.OthelloNoValidMoves()
        
        except othello.OthelloNotEmptyError:
            pass

        except othello.OthelloNoValidMoves:
            self._game.change_player()
            self._create_state()
            try:
                if not othello._any_available_moves(self._game):
                    # If there is no available moves again, then raise exception
                    # print('Player {} has no available moves.'.format(self._game.current_turn()))
                    raise OthelloGameOver()
                # print('Player {} has no available moves.'.format(self._game.opposite_turn()))
                # print("Player {}'s turn again.".format(self._game.current_turn()))
                
            except OthelloGameOver:
                # Game is over
                # print('Player {} has no available moves.'.format(self._game.opposite_turn()))
                self._winner = othello.winning_player(self._game, True, self._mode)
                return True

        self._winner = othello.winning_player(self._game, othello.is_board_full(self._game), self._mode)
        if ('W' or 'B' or 'WB') == self._winner:
                return True
            
        return False


if __name__ == '__main__':
    game = OthelloGUI().start()














    
