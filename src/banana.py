import pygame


class Banana:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.rect = img.get_rect()
        self.set_center_pos(x, y)
        self.speed = speed

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def reverse_x_speed(self):
        self.speed[0] *= -1

    def reverse_y_speed(self):
        self.speed[1] *= -1

    def set_center_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move_at_speed(self):
        self.rect = self.rect.move(self.speed)
        return self.rect

    def __str__(self):
        return "{} - {}".format(self.rect, self.speed)