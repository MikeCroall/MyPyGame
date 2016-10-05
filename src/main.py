def main():
    import sys
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    print("Excellent - pygame is installed and imported!")

    pygame.init()
    size = width, height = 960, 540
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)

    banana = pygame.image.load("../img/banana.bmp")
    banana_rect = banana.get_rect()
    banana_speed = [1, 1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_x, clicked_y = event.pos
                if banana_rect.collidepoint(clicked_x, clicked_y):
                    print("You have defeated the magical banana!")

        banana_rect = banana_rect.move(banana_speed)
        if banana_rect.left < 0 or banana_rect.right > width:
            banana_speed[0] *= -1
        if banana_rect.top < 0 or banana_rect.bottom > height:
            banana_speed[1] *= -1

        screen.fill(black)
        screen.blit(banana, banana_rect)
        pygame.display.flip()

        #todo sleep a bit

main()
print("See you again soon!")