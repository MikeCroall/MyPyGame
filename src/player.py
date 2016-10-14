import pygame, math


class Player:
    def __init__(self, img, speed, screen_bounds):
        w, h = screen_bounds
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed
        self.usual_bottom = -1
        self.position_middle_bottom(screen_bounds)
        self.balloon_bob_height = 0
        self.balloon_bob_mode = "down"
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

    def balloon_bob(self):
        if self.balloon_bob_mode == "down":
            if self.balloon_bob_height < 10:
                self.balloon_bob_height += 1
            else:
                self.balloon_bob_mode = "up"
        else:
            if self.balloon_bob_height > -10:
                self.balloon_bob_height -= 1
            else:
                self.balloon_bob_mode = "down"
        self.rect.bottom = self.usual_bottom + self.balloon_bob_height
