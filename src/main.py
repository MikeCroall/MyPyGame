def main():
    import sys, time, random
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    print("Excellent - pygame is installed and imported!")
    pygame.init()

    size = width, height = 960, 540
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Banana dodge v2')
    spawn_rate, frames_until_spawn = 500, 0

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    font = pygame.font.Font(None, 36)
    text = font.render("Banana dodge v2", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    banana = pygame.image.load("../img/banana.bmp")
    banana_rect = banana.get_rect()
    banana_speed = [random.choice([0.1, -0.1, 0.5, -0.5]), 2]

    while True:
        frames_until_spawn -= 1
        if frames_until_spawn <= 0:
            # todo spawn_banana() and add to list (use banana class)
            frames_until_spawn = spawn_rate
            print("Banana spawn!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_x, clicked_y = event.pos
                if banana_rect.collidepoint(clicked_x, clicked_y):
                    print("Banana down!")

        banana_rect = banana_rect.move(banana_speed)
        if banana_rect.left < 0 or banana_rect.right > width:
            banana_speed[0] *= -1
        if banana_rect.top < 0:
            banana_speed[1] *= -1
        elif banana_rect.top > height:
            # todo despawn banana (remove from list)
            pass

        text = font.render("{} frames until banana".format(frames_until_spawn), 1, (10, 10, 10))
        background.fill((250, 250, 250))
        background.blit(text, textpos)
        screen.blit(background, (0, 0))
        screen.blit(banana, banana_rect)
        pygame.display.flip()

        time.sleep(0.005)

if __name__ == "__main__":
    main()
    print("See you again soon!")
