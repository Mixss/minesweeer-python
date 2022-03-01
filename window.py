import pygame
import game

GUI_HEIGHT = 50

class Window:
    window = None
    run = True

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.setup()
        self.game = game.Game(self.window)

    def setup(self):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Minesweeper")

    def show(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    self.game.down_click_on_screen(x,y, event.button)
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    self.game.up_click_on_screen(x,y, event.button)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.reset()

            self.game.play()