def main():
    import sys, time, random
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    from player import Player
    from banana import Banana
    from label import Label

    print("Excellent - pygame is installed and imported!")
    pygame.init()

    paused = False
    size = width, height = 960, 540
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Banana dodge v2')
    spawn_rate, frames_until_spawn = 100, 1
    bananas_dodged, lives = 0, 3
    bob_rate, frames_until_bob = 7, 7

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    player_1 = Player(pygame.image.load("../img/nyan-balloon.png"), [2, 0], size)

    labels = [
        Label("0 frames until banana"),
        Label("0 bananas dodged"),
        Label("3 lives")
    ]  # note: NOT a dictionary, to maintain ordering
    pause_label = pygame.font.Font(None, 50).render("Paused", 1, (10, 10, 10))
    pause_label_rect = pause_label.get_rect()
    pause_label_rect.centerx = background.get_rect().centerx
    pause_label_rect.centery = background.get_rect().centery

    bananas = []

    def spawn_banana():
        img = pygame.image.load("../img/banana.bmp")
        speed = [random.choice([0, 0, 0, -1, 1]), 2]
        bananas.append(Banana(img, int(random.random() * width), 0, speed))

    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        screen.blit(pause_label, pause_label_rect)
                        pygame.display.flip()

        if not paused:
            frames_until_spawn -= 1
            if frames_until_spawn <= 0:
                spawn_banana()
                frames_until_spawn = spawn_rate

            # player movement
            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if player_1.get_rect().left > 0:
                    player_1.go_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if player_1.get_rect().right < width:
                    player_1.go_right()

            rem = []
            for b in bananas:
                b.move_at_speed()
                if b.get_rect().left < 0:  # separated to ensure speed doesn't alternate +ve -ve and thus not really change
                    b.ensure_travel_right()
                elif b.get_rect().right > width:
                    b.ensure_travel_left()

                if b.get_rect().colliderect(player_1.get_rect()):
                    rem.append(b)
                    lives -= 1
                elif b.get_rect().top > height:  # if did not collide with player, check if ready for locational despawn
                    rem.append(b)
                    bananas_dodged += 1
                    if spawn_rate > 20:
                        spawn_rate -= 2

            bananas = [b for b in bananas if b not in rem]

            # update labels ready for drawing
            labels[0].set_text("{} frames until banana (every {} frames)".format(frames_until_spawn, spawn_rate))
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
                # animate spinning
                if frames_until_bob <= 1:
                    b.rotate_tick()
                screen.blit(b.get_img(), b.get_rect())

            # animate bobbing
            frames_until_bob -= 1
            if frames_until_bob <= 0:
                player_1.balloon_bob()
                frames_until_bob = bob_rate
            screen.blit(player_1.get_img(), player_1.get_rect())

            pygame.display.flip()
            time.sleep(0.01)
        else:
            time.sleep(0.2)  # paused

    print("Game over!\n{} bananas dodged successfully".format(bananas_dodged))

    game_over_label = pygame.font.Font(None, 40).render("Game over!", 1, (10, 10, 10))
    bananas_dodged_label = pygame.font.Font(None, 36).render("You dodged {} bananas!".format(bananas_dodged), 1,
                                                             (10, 10, 10))
    escape_exit_label = pygame.font.Font(None, 25).render("Press Esc to exit", 1, (10, 10, 10))
    gol_rect = game_over_label.get_rect()
    bdl_rect = bananas_dodged_label.get_rect()
    eel_rect = escape_exit_label.get_rect()
    gol_rect.centerx = background.get_rect().centerx
    bdl_rect.centerx = background.get_rect().centerx
    eel_rect.centerx = background.get_rect().centerx
    gol_rect.bottom = background.get_rect().centery - gol_rect.height - 10
    bdl_rect.centery = background.get_rect().centery
    eel_rect.top = background.get_rect().centery + gol_rect.height + 10

    screen.blit(game_over_label, gol_rect)
    screen.blit(bananas_dodged_label, bdl_rect)
    screen.blit(escape_exit_label, eel_rect)

    pygame.display.flip()

    escaped = False
    while not escaped:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                escaped = (event.key == pygame.K_ESCAPE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Please exit using the X button, or Esc on the death screen next time!")
    print("See you again soon!")
