import math
import pygame


class Player:
    MAX_BOB_HEIGHT = 10

    def __init__(self, img, speed, screen_bounds):
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed
        self.usual_bottom = -1
        self.position_middle_bottom(screen_bounds)
        self.balloon_bob_sin_angle = 0
        self.travelling = "right"

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def go_left(self):
        if self.travelling == "right":
            self.img = pygame.transform.flip(self.img, True, False)
        self.travelling = "left"
        self.rect = self.rect.move([-1 * math.fabs(self.speed[0]), 0])

    def go_right(self):
        if self.travelling == "left":
            self.img = pygame.transform.flip(self.img, True, False)
        self.travelling = "right"
        self.rect = self.rect.move([math.fabs(self.speed[0]), 0])

    def position_middle_bottom(self, screen_bounds):
        width, height = screen_bounds
        self.rect.bottom = height - 12
        self.usual_bottom = self.rect.bottom
        self.rect.centerx = int(width / 2)

    def balloon_bob(self, bob_rate_as_angle):
        self.balloon_bob_sin_angle = (self.balloon_bob_sin_angle + bob_rate_as_angle) % 360
        self.rect.bottom = self.usual_bottom + (
            math.sin(math.radians(self.balloon_bob_sin_angle)) * Player.MAX_BOB_HEIGHT)
