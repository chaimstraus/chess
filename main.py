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
        self.white_piece_locations = []
        self.black_piece_locations = []
        for piece in self.pieces:
            if piece.colour == "w":
                self.white_piece_locations.append(piece.get_board_position())
            else:
                self.black_piece_locations.append(piece.get_board_position())
        
        self.move_dots = []
        self.capture_dots = []
        self.dots = []
        self.active_piece = None
        self.image = pygame.image.load("images\\board.png").convert()
        self.screen = screen
    
    def update_piece_locations(self):
        self.piece_locations = [piece.get_board_position() for piece in self.pieces]
        self.white_piece_locations = []
        self.black_piece_locations = []
        for piece in self.pieces:
            if piece.colour == "w":
                self.white_piece_locations.append(piece.get_board_position())
            else:
                self.black_piece_locations.append(piece.get_board_position())
    
    def display(self):
        screen.blit(self.image, (0, 0))

class Pieces():
    def __init__(self, piece: str, rank: int, file: int, game_piece: bool = True, reset: bool = False):
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
    
    def check_interception(self, square):
        if square in board.piece_locations:
            if self.colour == "w" and square in board.black_piece_locations:
                return True, True
            elif self.colour == "b" and square in board.white_piece_locations:
                return True, True
            return True, False
        return False, False
    
    def legal_moves(self):  # sourcery skip: low-code-quality        
        limit = self.legal[1]
        legal_squares_file = []
        legal_squares_rank = []
        legal_squares_diagonal = []
        legal_squares_knight = []
        legal_captures = []

        # vertical movement (in the rank)
        if self.legal[0][0]:
            lsfb = [list(map(int, x)) for x in "12345678".split(str(self.file))]
            lsfb[0].reverse()

            for move_list in lsfb:
                if limit:
                    move_list = move_list[:limit]
                for move in move_list:
                    if (
                        self.name[2] == "P"
                        and ((self.colour == "w" and move < self.file)
                        or (self.colour == "b" and move > self.file))
                    ):
                        continue
                    if (self.rank, move) in board.piece_locations:
                        if self.name[2] != "P":
                            if self.colour == "b" and (self.rank, move) in board.white_piece_locations:
                                legal_captures.append((self.rank, move))
                            elif self.colour == "w" and (self.rank, move) in board.black_piece_locations:
                                legal_captures.append((self.rank, move))
                        break
                    else:
                        legal_squares_file.append((self.rank, move))

        # horizontal movement (in the file)
        if self.legal[0][1]:
            lsrb = [list(map(int, x)) for x in "12345678".split(str(self.rank))]
            lsrb[0].reverse()

            for move_list in lsrb:
                if limit:
                    move_list = move_list[:limit]
                for move in move_list:
                    if (move, self.file) in board.piece_locations:
                        if self.colour == "b" and (move, self.file) in board.white_piece_locations:
                            legal_captures.append((move, self.file))
                        elif self.colour == "w" and (move, self.file) in board.black_piece_locations:
                            legal_captures.append((move, self.file))
                        break
                    legal_squares_rank.append((move, self.file))

        # diagonal movement
        if self.legal[0][2]:
            up_right = False
            up_left = False
            down_right = False
            down_left = False
            for i in range(1, 9):
                if i < limit + 1 or limit == 0:
                    if self.rank - i > 0:
                        
                        if self.file - i > 0:
                            square = (self.rank - i, self.file - i)
                            if not down_left:
                                intercept, capture = self.check_interception(square)
                                if intercept:
                                    down_left = True
                                    if capture:
                                        legal_captures.append(square)
                                else:
                                    legal_squares_diagonal.append(square)
                        
                        if self.file + i <= 8:
                            square = (self.rank - i, self.file + i)
                            if not up_left:
                                intercept, capture = self.check_interception(square)
                                if intercept:
                                    up_left = True
                                    if capture:
                                        legal_captures.append(square)
                                else:
                                    legal_squares_diagonal.append(square)
                    
                    if self.rank + i <= 8:
                        
                        if self.file + i <= 8:
                            square = (self.rank + i, self.file + i)
                            intercept, capture = self.check_interception(square)
                            if not up_right:
                                if intercept:
                                    up_right = True
                                    if capture:
                                        legal_captures.append(square)
                                else:
                                    legal_squares_diagonal.append(square)
                        
                        if self.file - i > 0:
                            square = (self.rank + i, self.file - i)
                            intercept, capture = self.check_interception(square)
                            if not down_right:
                                if intercept:
                                    down_right = True
                                    if capture:
                                        legal_captures.append(square)
                                else:
                                    legal_squares_diagonal.append(square)

        #knight movement (L)
        if self.legal[0][3]:
            all_squares_knight = (
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
            occupied_squares = []
            legal_squares_knight = [(rank, file) for rank, file in all_squares_knight if rank in range(1, 9) and file in range(1, 9)]
            for i in legal_squares_knight:
                if i in board.piece_locations:
                    occupied_squares.append(i)
                    if self.colour == "w" and i in board.black_piece_locations:
                        legal_captures.append(i)
                    elif self.colour == "b" and i in board.white_piece_locations:
                        legal_captures.append(i)
            legal_squares_knight = [x for x in legal_squares_knight if x not in occupied_squares]                        

        all_moves = legal_squares_rank + legal_squares_file + legal_squares_diagonal + legal_squares_knight
        
        # pawn capturing
        if self.name[2] == "P":
            for i in [-1, 1]:
                pos = (self.rank + i, self.file + (1 if self.colour == "w" else -1))
                if pos in (board.black_piece_locations if self.colour == "w" else board.white_piece_locations):
                    legal_captures.append(pos)
        
        return all_moves, legal_captures
    
class Pawn(Pieces):
    # shadow pawns behind two square moves that only other pawns can see
    # for en passant
    # it makes me upset that this can actually work
    # leave an outline on rank, (3/6)
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
    def __init__(self, pos, capture = False):
        super().__init__("capture_dot" if capture else "dot", pos[0], pos[1], False)
        self.capture = capture

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('chess')
    screen_size = [480, 480]
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    board = Board(screen)
    white_turn = True
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                piece_contact = False
                for square in board.dots:
                    if square.rect.collidepoint(x, y):
                        if square.capture:
                            for piece in board.pieces:
                                if piece.get_board_position() == (square.rank, square.file):
                                    board.pieces.remove(piece)

                        board.active_piece.name = f"{board.active_piece.name[:3]}_{al[square.rank-1]}{square.file}"
                        board.active_piece.rank = square.rank
                        board.active_piece.file = square.file

                        if hasattr(board.active_piece, "start"):
                            board.active_piece.start = False
                            board.active_piece.legal[1] = 1
                        if hasattr(board.active_piece, "castle"):
                            board.active_piece.castle = False

                        board.move_dots = []
                        board.capture_dots = []
                        board.dots = []
                        board.active_piece = None
                        piece_contact = True
                        white_turn = not(white_turn)
                
                user_pieces = [piece for piece in board.pieces if piece.colour == ("w" if white_turn else "b")]
                for piece in user_pieces:
                    if piece.rect.collidepoint(x, y):
                        board.move_dots = []
                        board.capture_dots = []
                        board.dots = []
                        if piece == board.active_piece:
                            board.active_piece = None
                        else:
                            board.active_piece = piece
                            legal_squares = piece.legal_moves()
                            board.move_dots = [Move(square) for square in legal_squares[0]]
                            board.capture_dots = [Move(square, True) for square in legal_squares[1]]
                            board.dots = board.move_dots + board.capture_dots
                        piece_contact = True

                if not piece_contact:
                    board.active_piece = None
                    board.move_dots = []
                    board.capture_dots = []
                    board.dots = []
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board.__init__(screen)

        board.update_piece_locations()
        board.display()
        for piece in board.pieces:
            piece.display(screen)
        for dot in board.move_dots:
            dot.display(screen)
        for dot in board.capture_dots:
            dot.display(screen)

        pygame.display.flip()
        clock.tick(30)