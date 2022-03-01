import pygame
import board
import sprites
from sprites import TILE_SIZE as t_size

BOARD_SIZE_X = 25
BOARD_SIZE_Y = 25
NUMBER_OF_BOMBS = 120
GUI_HEIGHT = 50

class Game:
    def __init__(self, window):
        self.window = window
        self.board = board.Board(self.window, BOARD_SIZE_X, BOARD_SIZE_Y, NUMBER_OF_BOMBS, 0, GUI_HEIGHT)
        self.playing = True
        self.first_move = True

        # gui
        self.is_button_clicked = False
        self.sprite_button = sprites.button_face_smiling
        self.sprite_button_clicked = sprites.button_face_smiling_clicked

    def draw(self):
        self.window.blit(sprites.gui_bar, (0,0))
        if not self.is_button_clicked:
            self.window.blit(self.sprite_button, (281, 5))
        else:
            self.window.blit(self.sprite_button_clicked, (281, 5))
        self.board.draw_board()

        # update screen
        pygame.display.update()

    def play(self): # function called on the main loop
        self.draw()

    def down_click_on_screen(self, x, y, button):
        if y < 50:
            if x > 281 and x < 318:
                if button == 1:
                    self.click_button()
        else:
            if self.playing:
                if button == 1: # left mouse click
                    if not self.board.uncover_field(x//t_size, (y-GUI_HEIGHT)//t_size): # lose
                        if self.first_move:
                            print("zrobiono")
                            self.board.reset()
                            while not self.board.uncover_field(x//t_size, (y-GUI_HEIGHT)//t_size):
                                self.board.reset()
                        else:
                            self.playing = False
                            self.sprite_button = sprites.button_face_lose
                            self.sprite_button_clicked = sprites.button_face_lose_clicked
                    elif self.board.is_win(): #check if win
                        self.playing = False
                        self.sprite_button = sprites.button_face_win
                        self.sprite_button_clicked = sprites.button_face_win_clicked

                elif button == 3:
                    self.board.put_flag(x//t_size, (y-GUI_HEIGHT)//t_size)

        self.first_move = False

    def up_click_on_screen(self, x, y, button):
        if y < 50:
            if x > 281 and x < 318:
                if button == 1:
                    self.release_button()

    def reset(self):
        self.playing = True
        self.board.reset()
        self.first_move = True
        self.sprite_button = sprites.button_face_smiling
        self.sprite_button_clicked = sprites.button_face_smiling_clicked

    def click_button(self):
        self.is_button_clicked = True

    def release_button(self):
        self.is_button_clicked = False
        self.reset()
