from random import randint
import sprites
from sprites import TILE_SIZE as t_size


class Board:

    def __init__(self, window, width, height, number_of_bombs, board_x, board_y):
        self.window = window
        self.width = width
        self.height = height
        self.number_of_bombs = number_of_bombs
        self.bombs = None
        self.covered = None
        self.checked_if_uncovered = None
        self.flags = None
        self.board_x = board_x
        self.board_y = board_y

        self.reset()


    def reset(self):
        self.bombs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.covered = [[True for x in range(self.width)] for y in range(self.height)]
        self.checked_if_uncovered = [[False for x in range(self.width)] for y in range(self.height)]
        self.flags = [[False for x in range(self.width)] for y in range(self.height)]
        self.create_board()

    def game_over(self):
        for y in range(self.width):
            for x in range(self.height):
                if not self.flags[x][y]:
                    if self.bombs[x][y] == -1:
                        self.covered[x][y] = False
                elif self.bombs[x][y] != -1: # bad flag placement
                    self.flags[x][y] = False
                    self.covered[x][y] = False
                    self.bombs[x][y] = -3

    #function returns True if game was not lost
    def uncover_field(self, x, y):
        if not self.covered[x][y] or self.flags[x][y]:
            return True
        #check if it is a bomb
        if self.bombs[x][y] == -1:
            self.game_over()
            self.bombs[x][y] = -2
            return False

        self.covered[x][y] = False
        self.checked_if_uncovered[x][y] = True

        if self.bombs[x][y] > 0:
            return True
        elif self.bombs[x][y] == 0:  # case when you have to uncover larger patch
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    # make sure we don't go out of range
                    if x + i < 0 or y + j < 0 or x + i >= self.width or y + j >= self.height:
                        continue
                    # do the same procedure if adjacent tile is an empty one
                    if self.bombs[x + i][y + j] == 0 and not self.checked_if_uncovered[x + i][y + j]:
                        self.uncover_field(x + i, y + j)

                    self.covered[x + i][y + j] = False
        return True

    def put_flag(self, x ,y):
        self.flags[x][y] = not self.flags[x][y]

    def create_board(self):
        # first put only bombs
        for i in range(self.number_of_bombs):
            while True:
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)
                if self.bombs[x][y] == 0:
                    break

            self.bombs[x][y] = -1

        for y in range(self.width):
            for x in range(self.height):
                if self.bombs[x][y] != -1:
                    self.bombs[x][y] = self.get_number_of_adjacent_bombs(x, y)

    def get_number_of_adjacent_bombs(self, x, y):
        summ = 0
        if x > 0 and y > 0 and self.bombs[x - 1][y - 1] == -1:
            summ += 1
        if y > 0 and self.bombs[x][y - 1] == -1:
            summ += 1
        if x < self.width - 1 and y > 0 and self.bombs[x + 1][y - 1] == -1:
            summ += 1
        if x > 0 and self.bombs[x - 1][y] == -1:
            summ += 1
        if x < self.width - 1 and self.bombs[x + 1][y] == -1:
            summ += 1
        if x > 0 and y < self.width - 1 and self.bombs[x - 1][y + 1] == -1:
            summ += 1
        if y < self.width - 1 and self.bombs[x][y + 1] == -1:
            summ += 1
        if x < self.width - 1 and y < self.width - 1 and self.bombs[x + 1][y + 1] == -1:
            summ += 1
        return summ

    def uncover_all(self):
        for y in range(self.width):
            for x in range(self.height):
                if not self.flags[x][y]:
                    self.covered[x][y] = False

    def is_win(self):
        covered_count = 0
        for y in range(self.width):
            for x in range(self.height):
                if self.covered[x][y]:
                    covered_count += 1
        if covered_count == self.number_of_bombs:
            for y in range(self.width):
                for x in range(self.height):
                    if self.covered[x][y]:
                        self.flags[x][y] = True
            return True
        else:
            return False

    def draw_board(self):
        for y in range(self.width):
            for x in range(self.height):
                if self.covered[x][y]:
                    if not self.flags[x][y]:
                        self.window.blit(sprites.tile_top, (t_size * x + self.board_x, t_size * y + self.board_y))
                    else:
                        self.window.blit(sprites.tile_flag, (t_size * x + self.board_x, t_size * y + self.board_y))
                else:
                    bombs = self.bombs[x][y]
                    if bombs == 0:
                        self.window.blit(sprites.tile_empty, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 1:
                        self.window.blit(sprites.tile_1, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 2:
                        self.window.blit(sprites.tile_2, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 3:
                        self.window.blit(sprites.tile_3, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 4:
                        self.window.blit(sprites.tile_4, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 5:
                        self.window.blit(sprites.tile_5, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 6:
                        self.window.blit(sprites.tile_6, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 7:
                        self.window.blit(sprites.tile_7, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == 8:
                        self.window.blit(sprites.tile_8, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == -1:
                        self.window.blit(sprites.tile_bomb, (t_size * x + self.board_x, t_size * y + self.board_y))
                    elif bombs == -3:
                        self.window.blit(sprites.tile_flag_wrong, (t_size * x + self.board_x, t_size * y + self.board_y))
                    else:
                        self.window.blit(sprites.tile_bomb_gameover, (t_size * x + self.board_x, t_size * y + self.board_y))
