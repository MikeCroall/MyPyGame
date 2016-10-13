import pygame, math


class Player:
    def __init__(self, img, speed, screen_bounds):
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed
        self.position_middle_bottom(screen_bounds)

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def go_left(self):
        self.rect = self.rect.move([-1 * math.fabs(self.speed[0]), 0])

    def go_right(self):
        self.rect = self.rect.move([math.fabs(self.speed[0]), 0])

    def position_middle_bottom(self, screen_bounds):
        width, height = screen_bounds
        self.rect.bottom = height - 5
        self.rect.centerx = int(width / 2)
