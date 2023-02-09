import numpy as np
import pygame
from string import ascii_lowercase as al

class Board():
    def __init__(self, screen: pygame.Surface):
        self.entities = [
            Rook("w_R", 1, 1),
            # Rook("w_R", 8, 1),
            # Knight("w_N", 2, 1),
            # Knight("w_N", 7, 1),
            # Bishop("w_B", 3, 1),
            # Bishop("w_B", 6, 1),
            # Queen("w_Q", 4, 1),
            # King("w_K", 5, 1),
            # Pawn("w_P", 1, 2),
            # Pawn("w_P", 2, 2),
            # Pawn("w_P", 3, 2),
            # Pawn("w_P", 4, 2),
            # Pawn("w_P", 5, 2),
            # Pawn("w_P", 6, 2),
            # Pawn("w_P", 7, 2),
            # Pawn("w_P", 8, 2),
            # Rook("b_R", 1, 8),
            # Rook("b_R", 8, 8),
            # Knight("b_N", 2, 8),
            # Knight("b_N", 7, 8),
            # Bishop("b_B", 3, 8),
            # Bishop("b_B", 6, 8),
            # Queen("b_Q", 4, 8),
            # King("b_K", 5, 8),
            # Pawn("b_P", 1, 7),
            # Pawn("b_P", 2, 7),
            # Pawn("b_P", 3, 7),
            # Pawn("b_P", 4, 7),
            # Pawn("b_P", 5, 7),
            # Pawn("b_P", 6, 7),
            # Pawn("b_P", 7, 7),
            # Pawn("b_P", 8, 7),
        ]
        self.move_dots = []
        self.image = pygame.image.load("images\\board.png").convert()
        self.screen = screen
        
    def display(self):
        screen.blit(self.image, (0, 0))

class Pieces():
    
    def __init__(self, piece: str, rank: int, file: int, game_piece: bool = True):
        self.image = pygame.image.load(f"images\{piece}.png")
        self.name = f"{piece}_{al[rank - 1]}{file}"
        self.rect = self.image.get_rect()
        self.rank = rank
        self.file = file
        self.game_piece = game_piece
        
    def get_position(self):
        return (self.rank - 1) * 60 - 1, 480 - (self.file * 60)
    
    def display(self, screen: pygame.Surface):
        x, y = self.get_position()
        self.rect.left = x
        self.rect.top = y
        screen.blit(self.image, (x, y))
    
    def rank_legal(self): #up-down rook/queen/king
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        x.remove(self.rank)
        return x
    
    def file_legal(self): #left-right rook/queen/king
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        x.remove(self.file)
        return x
    
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
                        if piece.legal[0]:
                            r_leg = [(piece.file, rank) for rank in piece.rank_legal()]
                        if piece.legal[1]:
                            h_leg = [(file, piece.rank) for file in piece.file_legal()]
                        legal_squares = r_leg + h_leg
                        for square in legal_squares:
                            board.move_dots.append(Move(square))
                        print(board.move_dots)
                    else:
                        print("need to move here")


    board.display()
    for piece in board.entities:
        piece.display(screen)
        # --- update the screen with what we've drawn
    pygame.display.flip()
    # --- limit the screen fps
    clock.tick(30)