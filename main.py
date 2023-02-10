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
        self.move_dots = []
        self.entities = self.pieces + self.move_dots
        self.image = pygame.image.load("images\\board.png").convert()
        self.screen = screen
        
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
        return (self.rank - 1) * 60 - 2, 480 - (self.file * 60)
    
    def display(self, screen: pygame.Surface):
        x, y = self.get_position()
        self.rect.left = x
        self.rect.top = y
        screen.blit(self.image, (x, y))
    
    def straight_legal(self, square, limit): #up-down, left-right
        squares = [1, 2, 3, 4, 5, 6, 7, 8]
        if self.colour == "b":
            squares.reverse() # [8, 7, 6, 5, 4, 3, 2, 1]
            square -= 1
        location = squares.pop(square - 1)
        if limit != 0:
            legal_squares = squares[max(0, location-limit+1):min(location+limit-1, 7)]
        else:
            legal_squares = squares
        # legal_squares.remove(direction)
        print(square, squares, location, legal_squares)
        return legal_squares
    
    #HORIZONTAL IS RANK
    # VERTICAL IS FILE
    
    def diagonal_legal(self, limit): #bishop/queen/king
        z, y = (1, 2)
        
        return z, y
    
class Pawn(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.start = True
        self.legal = (1, 0, 0, 2)
        
class Rook(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.start = True
        self.legal = (1, 1, 0, 0)
    
        
class Knight(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = (0, 0, 0, 0)

class Bishop(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = (0, 0, 1, 0)

class Queen(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.legal = (1, 1, 1, 0)

class King(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.start = True
        self.legal = (1, 1, 1, 1)

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
                    if piece.game_piece:
                        board.move_dots, board.entities = [], board.pieces
                        r_leg, f_leg, d_leg, n_leg, p_leg = [], [], [], [], []
                        if piece.legal[0]:
                            f_leg = [(piece.rank, file) for file in piece.straight_legal(piece.file, piece.legal[3])]
                        if piece.legal[1]:
                            r_leg = [(rank, piece.file) for rank in piece.straight_legal(piece.rank, piece.legal[3])]
                        if piece.legal[2]:
                            d_leg = [()]

                        legal_squares = f_leg + r_leg
                        board.move_dots.extend(Move(square) for square in legal_squares)
                        board.entities = board.entities + board.move_dots
                    else:
                        print(f"need to move to {piece.rank, piece.file}")


    board.display()
    for piece in board.entities:
        piece.display(screen)
        # --- update the screen with what we've drawn
    for dot in board.move_dots:
        dot.display(screen)
    pygame.display.flip()
    # --- limit the screen fps
    clock.tick(30)