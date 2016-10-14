import pygame


class Projectile:
    def __init__(self, img, speed, player_rect):
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed
        self.set_position(player_rect)

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def move_at_speed(self):
        self.rect = self.rect.move(self.speed)
        return self.rect

    def set_position(self, player_rect):
        self.rect.top = player_rect.top
        self.rect.centerx = player_rect.centerx
