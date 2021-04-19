# Chess (0–2 players)

> A fully functional chess programme made from scratch with pygame which includes an AI and basic GUI. 

| ![2 player demo](https://static.wixstatic.com/media/d051dc_d4ecf43e416d48c3a1c1695fd0078b8c~mv2.gif) | ![AI demo](https://static.wixstatic.com/media/d051dc_22a6655b6d7c45c78711001a27e60c70~mv2.gif) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| User vs User (Scholar's Mate)                                | User vs AI                                                   |

## General info

To play as white, turn `player_one` to `True` in `ChessMain.py`. To play as black, turn `player_two` to `True`. If both variables are set to `True` then the user can control both white and black. To set the AI to control white or black, turn one (user vs AI or AI vs user) or both (AI vs AI) of these variables to `False` as desired. <u>The user will play as white (`player_one`) and the AI as black (`player_two`) by default.</u> The AI difficulty can be adjusted by the `set_depth` variable (set to 4 by default) in `ChessAI.py`. If the engine is slow, you can improve the performance by reducing the AI difficulty. Finally, <u>to play please run `ChessMain.py`.</u>

`ChessMain.py` is responsible for user input and displaying the current state of the game. If the programme screen is too large, adjust the `board_width` and `board_height` variables. You may also want to adjust the move log display. Recommendations are included in the file. 

`ChessEngine.py` contains the guts of the chess game state. It is composed of three classes: `GameState`, `CastleRights`, and `Move`. `GameState` stores information about the current state of the game and handles how moves are made and undone, determines valid moves given the current state, and keeps a move log. `CastleRights` stores the current state of castling rights, and `Move` stores information about particular moves, including start and end positions, which pieces were moved and captured, and special moves such as en passant, pawn promotion, and castling. The latter also defines how strings are handled for the displayed move log.

`ChessAI.py` deals with information related to the AI. The current algorithm being utilised is a NegaMax algorithm with alpha beta pruning, which is a type of MiniMax algorithm. Alpha beta pruning eliminates the need to check all moves within a game state if better options have already been found. More information can be found in the file. The AI makes moves based on a scoring system which factors in points per piece and positioning on the board.

Although fully functional, this code has a lot of room for improvement. Namely, AI scoring does not consider 'smart moves' that a human would recognise, such as optimal positioning for defending ally pieces and capturing enemy pieces. The chess notation for the move log also does not specify checks, checkmates, or when multiple same-type pieces can capture the same square. Undoing a move only works for 2 player games. Finally, the interface could be improved via, for example, the inclusion of a player select screen, AI difficulty selection, flipping the board when playing black, and piece dragging. 

The following files are included in this repo:

* `Chess`: Project folder
  * `ChessMain.py`: Code determining user input and display
  * `ChessEngine.py`: Code determining chess moves and move log notation 
  * `ChessAI.py`: Code determining AI
  * `Chessimages`: Folder of chess piece images
  * `__init__.py`: Python initialiser 

In-game hotkeys:

- Press 'r' to restart the game
- Press 'z' to undo a move (only in 2 player games)

## Technologies

Python 3.7.9 and Pygame 2.0.1

## Inspiration

This project utilised the amazing Pygame tutorials offered by Eddie Sharick, from which substantial customisations and improvements were made. 

## Contact

Created by [@katrinaalaimo](https://www.katrinaalaimo.com/) — feel free to contact me!