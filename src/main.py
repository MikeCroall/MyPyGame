def main():
    import sys, time, random
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    from banana import Banana
    from label import Label

    print("Excellent - pygame is installed and imported!")
    pygame.init()

    size = width, height = 960, 540
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Banana dodge v2')
    spawn_rate, frames_until_spawn = 200, 1
    bananas_dodged, lives = 0, 3

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    labels = [
        Label("0 frames until banana"),
        Label("0 bananas dodged"),
        Label("3 lives")
    ]
    bananas = []

    def spawn_banana():
        img = pygame.image.load("../img/banana.bmp")
        speed = [random.choice([0, 0, 0, -1, 1]), 2]
        bananas.append(Banana(img, int(random.random() * width), 0, speed))

    while True:
        frames_until_spawn -= 1
        if frames_until_spawn <= 0:
            spawn_banana()
            frames_until_spawn = spawn_rate

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
            if b.get_rect().left < 0:  # separated to ensure speed doesn't alternate +ve -ve and thus not really change
                b.ensure_travel_right()
            elif b.get_rect().right > width:
                b.ensure_travel_left()
            if b.get_rect().top > height:
                rem.append(b)  # despawn because reached bottom
                bananas_dodged += 1

            # todo test for collision with player

        bananas = [b for b in bananas if b not in rem]

        # update labels ready for drawing
        labels[0].set_text("{} frames until banana".format(frames_until_spawn))
        labels[1].set_text("{} bananas dodged".format(bananas_dodged))
        labels[2].set_text("{} lives".format(lives))

        # draw on background
        background.fill((250, 250, 250))
        top = 8
        for l in labels:
            l.get_rect().top = top
            l.get_rect().left = 4
            background.blit(l.get_rendered_text(), l.get_rect())
            top += l.get_rect().height + 8

        # draw background on screen then draw on screen in front
        screen.blit(background, (0, 0))
        for b in bananas:
            screen.blit(b.get_img(), b.get_rect())

        pygame.display.flip()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
    print("See you again soon!")
