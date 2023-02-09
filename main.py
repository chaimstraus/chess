import numpy as np
import pygame
from string import ascii_lowercase as al

class Board():
    def __init__(self, screen: pygame.Surface):
        self.pieces = {
            "wr1": Rook("w_R", 1, 1),
            "wr2": Rook("w_R", 8, 1),
            "wn1": Knight("w_N", 2, 1),
            "wn2": Knight("w_N", 7, 1),
            "wb1": Bishop("w_B", 3, 1),
            "wb2": Bishop("w_B", 6, 1),
            "wQ": Queen("w_Q", 4, 1),
            "wK": King("w_K", 5, 1),
            "wp1": Pawn("w_P", 1, 2),
            "wp2": Pawn("w_P", 2, 2),
            "wp3": Pawn("w_P", 3, 2),
            "wp4": Pawn("w_P", 4, 2),
            "wp5": Pawn("w_P", 5, 2),
            "wp6": Pawn("w_P", 6, 2),
            "wp7": Pawn("w_P", 7, 2),
            "wp8": Pawn("w_P", 8, 2),
            "br1": Rook("b_R", 1, 8),
            "br2": Rook("b_R", 8, 8),
            "bn1": Knight("b_N", 2, 8),
            "bn2": Knight("b_N", 7, 8),
            "bb1": Bishop("b_B", 3, 8),
            "bb2": Bishop("b_B", 6, 8),
            "bQ": Queen("b_Q", 4, 8),
            "bK": King("b_K", 5, 8),
            "bp1": Pawn("b_P", 1, 7),
            "bp2": Pawn("b_P", 2, 7),
            "bp3": Pawn("b_P", 3, 7),
            "bp4": Pawn("b_P", 4, 7),
            "bp5": Pawn("b_P", 5, 7),
            "bp6": Pawn("b_P", 6, 7),
            "bp7": Pawn("b_P", 7, 7),
            "bp8": Pawn("b_P", 8, 7),
        }
        self.image = pygame.image.load("images\\board.png").convert()
        self.screen = screen
        
    def display(self):
        screen.blit(self.image, (0, 0))

class Pieces():
    
    def __init__(self, piece: str, rank: int, file: int):
        self.image = pygame.image.load(f"images\{piece}.png")
        self.name = f"{piece}_{al[rank - 1]}{file}"
        self.rect = self.image.get_rect()
        self.rank = rank
        self.file = file
    
    def get_position(self):
        return (self.rank - 1) * 60 - 1, 480 - (self.file * 60)
    
    def display(self, screen: pygame.Surface):
        x, y = self.get_position()
        self.rect.left = x
        self.rect.top = y
        screen.blit(self.image, (x, y))
    
    def rank_legal(self): #up-down rook/queen/king
        return [1, 2, 3, 4, 5, 6, 7, 8].remove(self.rank)
    
    def file_legal(self): #left-right rook/queen/king
        return [1, 2, 3, 4, 5, 6, 7, 8].remove(self.file)
    
    def diagonal_legal(self): #bishop/queen/king
        pass
    
class Pawn(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
        self.start = True
        self.legal = (1, 0, 0, 2)
        
class Rook(Pieces):
    def __init__(self, piece, rank, file):
        super().__init__(piece, rank, file)
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
        self.legal = (1, 1, 1, 1)

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
            for piece in board.pieces.values():
                if piece.rect.collidepoint(x, y):
                    print(piece.name)
                    # do movement stuff here
                    for type in piece.legal:
                        print(type)

    board.display()
    for piece in board.pieces.values():
        piece.display(screen)
        # --- update the screen with what we've drawn
    pygame.display.flip()
    # --- limit the screen fps
    clock.tick(30)