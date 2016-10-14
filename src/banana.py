import pygame
import random


class Banana:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.rect = img.get_rect()
        self.set_center_pos(x, y)
        self.speed = speed
        self.rotate_direction = random.choice([1, -1])

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def ensure_travel_right(self):
        self.speed[0] = 1

    def ensure_travel_left(self):
        self.speed[0] = -1

    def set_center_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move_at_speed(self):
        self.rect = self.rect.move(self.speed)
        return self.rect

    def rotate_tick(self):
        self.img = pygame.transform.rotate(self.img, self.rotate_direction * 90)  # not 90n causes bad distortion
        self.rect = self.img.get_rect(center=self.rect.center)

    def __str__(self):
        return "{} - {}".format(self.rect, self.speed)
