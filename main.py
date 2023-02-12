import numpy as np
import pygame
from string import ascii_lowercase as al

class Board():
    def __init__(self, screen: pygame.Surface):
        self.pieces = [
            Rook("w_R", 1, 1),
            Rook("w_R", 8, 1),
            Knight("w_N", 2, 1),
            Knight("w_N", 7, 1),
            Bishop("w_B", 3, 1),
            Bishop("w_B", 6, 1),
            Queen("w_Q", 4, 1),
            King("w_K", 5, 1),
            Pawn("w_P", 1, 2),
            Pawn("w_P", 2, 2),
            Pawn("w_P", 3, 2),
            Pawn("w_P", 4, 2),
            Pawn("w_P", 5, 2),
            Pawn("w_P", 6, 2),
            Pawn("w_P", 7, 2),
            Pawn("w_P", 8, 2),
            Rook("b_R", 1, 8),
            Rook("b_R", 8, 8),
            Knight("b_N", 2, 8),
            Knight("b_N", 7, 8),
            Bishop("b_B", 3, 8),
            Bishop("b_B", 6, 8),
            Queen("b_Q", 4, 8),
            King("b_K", 5, 8),
            Pawn("b_P", 1, 7),
            Pawn("b_P", 2, 7),
            Pawn("b_P", 3, 7),
            Pawn("b_P", 4, 7),
            Pawn("b_P", 5, 7),
            Pawn("b_P", 6, 7),
            Pawn("b_P", 7, 7),
            Pawn("b_P", 8, 7),
        ]
        self.piece_locations = [piece.get_board_position() for piece in self.pieces]
        self.move_dots = []
        self.entities = self.pieces + self.move_dots
        self.active_piece = None
        self.image = pygame.image.load("images\\board.png").convert()
        self.screen = screen
    
    def update_piece_locations(self):
        self.piece_locations = [piece.get_board_position() for piece in self.pieces]
    
    def display(self):
        screen.blit(self.image, (0, 0))

class Pieces():
    def __init__(self, piece: str, rank: int, file: int, game_piece: bool = True):
        self.image = pygame.image.load(f"images\{piece}.png")
        self.colour = piece[0]
        self.name = f"{piece}_{al[rank - 1]}{file}"
        self.rect = self.image.get_rect()
        self.rank = rank
        self.file = file
        self.game_piece = game_piece
        
    def get_position(self):
        return (self.rank - 1) * 60 - 1, 480 - (self.file * 60)
    
    def get_board_position(self):
        return (self.rank, self.file)
    
    def display(self, screen: pygame.Surface):
        x, y = self.get_position()
        self.rect.left = x
        self.rect.top = y
        screen.blit(self.image, (x, y))
    
    def legal_moves(self):  # sourcery skip: low-code-quality        
        limit = self.legal[1]
        legal_squares_file = []
        legal_squares_rank = []
        legal_squares_diagonal = []
        legal_squares_knight = []

        if self.legal[0][0]:
            lsfb = [list(map(int, x)) for x in "12345678".split(str(self.file))]
            lsfb[0].reverse()

            for move_list in lsfb:
                if limit:
                    move_list = move_list[:limit]
                for move in move_list:
                    if (self.rank, move) in board.piece_locations:
                        break
                    if (
                        self.name[2] == "P"
                        and (self.colour == "w" and move < self.file)
                        or (self.colour == "b" and move > self.file)
                    ):
                        continue
                    legal_squares_file.append((self.rank, move))

        if self.legal[0][1]:
            lsrb = [list(map(int, x)) for x in "12345678".split(str(self.rank))]
            lsrb[0].reverse()

            for move_list in lsrb:
                if limit:
                    move_list = move_list[:limit]
                for move in move_list:
                    if (move, self.file) in board.piece_locations:
                        break
                    legal_squares_rank.append((move, self.file))

        if self.legal[0][2]:
            for i in range(1, 9):
                if i < limit + 1 or limit == 0:
                    if self.rank - i > 0:
                        if self.file - i > 0:
                            legal_squares_diagonal.append((self.rank - i, self.file - i))
                        if self.file + i <= 8:
                            legal_squares_diagonal.append((self.rank - i, self.file + i))
                    if self.rank + i <= 8:
                        if self.file + i <= 8:
                            legal_squares_diagonal.append((self.rank + i, self.file + i))
                        if self.file - i > 0:
                            legal_squares_diagonal.append((self.rank + i, self.file - i))

        #knight movement
        if self.legal[0][3]:
            legal_squares_knight.extend(
                (
                    (self.rank + 2, self.file + 1),
                    (self.rank + 2, self.file - 1),
                    (self.rank - 2, self.file - 1),
                    (self.rank - 2, self.file + 1),
                    (self.rank + 1, self.file + 2),
                    (self.rank + 1, self.file - 2),
                    (self.rank - 1, self.file - 2),
                    (self.rank - 1, self.file + 2),
                )
            )
            legal_squares_knight = [(rank, file) for rank, file in legal_squares_knight if rank in range(1, 9) and file in range(1, 9) and (rank, file) not in board.piece_locations]

        all_moves = legal_squares_rank + legal_squares_file + legal_squares_diagonal + legal_squares_knight
        all_moves.sort()
        # print(all_moves)
        # legal_moves = [square for square in all_moves if square not in board.piece_locations]
        # print(legal_moves)
        # legal_captures = [square for square in all_moves if square in board.piece_locations]
        # print(legal_captures)
        
        return all_moves
    
class Pawn(Pieces):
    # shadow pawns behind two square moves that only other pawns can see
    # for en passant
    # it makes me upset that this can actually work
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.start = True
        self.legal = [(1, 0, 0, 0), 2]
        
class Rook(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.castle = True
        self.legal = ((1, 1, 0, 0), 0)
    
class Knight(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = ((0, 0, 0, 1), 0)

class Bishop(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = ((0, 0, 1, 0), 0)

class Queen(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = ((1, 1, 1, 0), 0)

class King(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.castle = True
        self.legal = ((1, 1, 1, 0), 1)

class Move(Pieces):
    def __init__(self, pos):
        super().__init__("dot", pos[0], pos[1], False)
        

pygame.init()
pygame.display.set_caption('chess')
screen_size = [480, 480]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
board = Board(screen)
done = False
while not done:
# --- main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for piece in board.entities:
                if piece.rect.collidepoint(x, y):
                    if isinstance(piece, Move):
                        print(f"{board.active_piece.name[0]}{board.active_piece.name[2]}: {board.active_piece.name[4:]}-{al[piece.rank-1]}{piece.file}")
                        board.active_piece.name = f"{board.active_piece.name[:3]}_{al[piece.rank-1]}{piece.file}"
                        board.active_piece.rank = piece.rank
                        board.active_piece.file = piece.file

                        if hasattr(board.active_piece, "start"):
                            board.active_piece.start = False
                            board.active_piece.legal[1] = 1
                        if hasattr(board.active_piece, "castle"):
                            board.active_piece.castle = False

                        board.move_dots = []
                        board.entities = board.pieces
                        board.active_piece = None
                        board.update_piece_locations()

                    elif piece == board.active_piece:
                        board.active_piece = None
                        board.move_dots = []
                        board.entities = board.pieces

                    else:
                        # print("piece")
                        board.move_dots = []
                        board.entities = board.pieces
                        board.active_piece = piece
                        legal_squares = piece.legal_moves()
                        board.move_dots.extend(Move(square) for square in legal_squares)
                        board.entities = board.entities + board.move_dots

    board.display()
    for piece in board.pieces:
        piece.display(screen)
    for dot in board.move_dots:
        dot.display(screen)
    pygame.display.flip()
    # --- limit the screen fps
    clock.tick(30)