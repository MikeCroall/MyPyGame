import pygame


class Label:
    def __init__(self, text):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(text, 1, (10, 10, 10))
        self.rect = self.text.get_rect()

    def get_rendered_text(self):
        return self.text

    def get_rect(self):
        return self.rect

    def set_text(self, text):
        self.text = self.font.render(text, 1, (10, 10, 10))
        self.rect = self.text.get_rect()
