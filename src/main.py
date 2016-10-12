def main():
    import sys, time, random
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    from banana import Banana

    print("Excellent - pygame is installed and imported!")
    pygame.init()

    size = width, height = 960, 540
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Banana dodge v2')
    spawn_rate, frames_until_spawn = 200, 1

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    font = pygame.font.Font(None, 36)
    text = font.render("Banana dodge v2", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    bananas = []

    def spawn_banana():
        img = pygame.image.load("../img/banana.bmp")
        speed = [random.choice([0, 0, 0, -1, 1]), 2]
        bananas.append(Banana(img, int(random.random() * width), 0, speed))

    def print_all_bananas():
        for b in bananas:
            print(b)

    while True:
        frames_until_spawn -= 1
        if frames_until_spawn <= 0:
            spawn_banana()
            frames_until_spawn = spawn_rate
            #print("Banana spawn!")
            #print_all_bananas()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #elif event.type == pygame.MOUSEBUTTONDOWN:
             #   clicked_x, clicked_y = event.pos
              #  if banana_rect.collidepoint(clicked_x, clicked_y):
               #     print("Banana down!")

        rem = []
        for b in bananas:
            b.move_at_speed()
            if b.get_rect().left < 0 or b.get_rect().right > width:
                b.reverse_x_speed()
            if b.get_rect().top < 0:
                # do nothing for now - maybe ensure positive y speed?
                pass
            elif b.get_rect().top > height:
                rem.append(b)  # despawn
        bananas = [b for b in bananas if b not in rem]

        text = font.render("{} frames until banana".format(frames_until_spawn), 1, (10, 10, 10))
        background.fill((250, 250, 250))
        background.blit(text, textpos)
        screen.blit(background, (0, 0))
        for b in bananas:
            screen.blit(b.get_img(), b.get_rect())
        pygame.display.flip()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
    print("See you again soon!")
