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
    from projectile import Projectile

    print("Excellent - pygame is installed and imported!")
    pygame.init()

    paused = False
    screen_scale = 1
    screen_size = screen_width, screen_height = screen_scale * 960, screen_scale * 540
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Banana dodge v2')
    banana_spawn_rate, frames_until_banana_spawn = 100, 1
    bananas_dodged, bananas_shot, lives = 0, 0, 3
    player_bob_rate = 3
    shooting_cool_down, frames_until_can_shoot = 75, 30
    projectile_speed = [0, -4 * int(screen_height / 480)]
    background_colour = (250, 250, 250)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(background_colour)

    player_1 = Player(pygame.image.load("../img/nyan-balloon.png"), [int(screen_width / 480), 0], screen_size)

    labels = [
        Label("0 frames until banana"),
        Label("0 frames until shooting is available"),
        Label("0 bananas dodged"),
        Label("0 bananas shot"),
        Label("3 lives")
    ]  # note: NOT a dictionary, to maintain ordering
    pause_label = pygame.font.Font(None, 50).render("Paused", 1, (10, 10, 10))
    pause_label_rect = pause_label.get_rect()
    pause_label_rect.centerx = background.get_rect().centerx
    pause_label_rect.centery = background.get_rect().centery

    bananas = []
    projectiles = []

    def spawn_banana():
        speed = [random.choice([0, 0, 0, 0, 0, -1, -1, 1, 1, -2, 2]), 2]
        if random.random() < 0.05:
            img = pygame.image.load("../img/life-banana.bmp")
            bananas.append(Banana(True, img, int(random.random() * screen_width), 0, speed))
        else:
            img = pygame.image.load("../img/banana.bmp")
            bananas.append(Banana(False, img, int(random.random() * screen_width), 0, speed))

    def shoot_projectile_from_player(player):
        img = pygame.image.load("../img/projectile.png")
        projectiles.append(Projectile(img, projectile_speed, player.get_rect()))

    def background_fade():
        background_recover_rate = 2
        r, g, b = background_colour
        if background_colour != (250, 250, 250):
            if r < 250:
                r += background_recover_rate
            elif r > 250:
                r -= background_recover_rate
            if g < 250:
                g += background_recover_rate
            elif g > 250:
                g -= background_recover_rate
            if b < 250:
                b += background_recover_rate
            elif b > 250:
                b -= background_recover_rate
        return r, g, b

    def update_labels():
        # update labels ready for drawing
        labels[0].set_text("{} frames until banana (every {} frames)".format(frames_until_banana_spawn, banana_spawn_rate))
        labels[1].set_text("{} frames until shooting is available".format(frames_until_can_shoot))
        labels[2].set_text("{} bananas dodged".format(bananas_dodged))
        labels[3].set_text("{} bananas shot".format(bananas_shot))
        labels[4].set_text("{} lives".format(lives))

    def process_events(p_paused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    p_paused = not p_paused
                    if p_paused:
                        screen.blit(pause_label, pause_label_rect)
                        pygame.display.flip()
        return p_paused

    def show_death_messages(p_background, p_bananas_dodged, p_bananas_shot, p_screen):
        print("Game over!\n{} bananas dodged successfully".format(p_bananas_dodged))
        game_over_label = pygame.font.Font(None, 40).render("Game over!", 1, (10, 10, 10))
        bananas_dodged_label = pygame.font.Font(None, 36).render(
            "You dodged {} bananas, and shot {}!".format(p_bananas_dodged, p_bananas_shot), 1, (10, 10, 10))
        escape_exit_label = pygame.font.Font(None, 25).render("Press Esc to exit", 1, (10, 10, 10))
        gol_rect = game_over_label.get_rect()
        bdl_rect = bananas_dodged_label.get_rect()
        eel_rect = escape_exit_label.get_rect()
        gol_rect.centerx = p_background.get_rect().centerx
        bdl_rect.centerx = p_background.get_rect().centerx
        eel_rect.centerx = p_background.get_rect().centerx
        gol_rect.bottom = p_background.get_rect().centery - gol_rect.height - 10
        bdl_rect.centery = p_background.get_rect().centery
        eel_rect.top = p_background.get_rect().centery + gol_rect.height + 10
        p_screen.blit(game_over_label, gol_rect)
        p_screen.blit(bananas_dodged_label, bdl_rect)
        p_screen.blit(escape_exit_label, eel_rect)
        pygame.display.flip()

    while lives > 0:
        paused = process_events(paused)

        if not paused:
            frames_until_banana_spawn -= 1
            if frames_until_can_shoot > 0:
                frames_until_can_shoot -= 1
            if frames_until_banana_spawn <= 0:
                spawn_banana()
                frames_until_banana_spawn = banana_spawn_rate

            # player movement
            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if player_1.get_rect().left > 0:
                    player_1.go_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if player_1.get_rect().right < screen_width:
                    player_1.go_right()
            if keys[pygame.K_SPACE]:
                if frames_until_can_shoot <= 0:
                    frames_until_can_shoot = shooting_cool_down
                    shoot_projectile_from_player(player_1)

            for p in projectiles:
                p.move_at_speed()

            rem_b = []
            for b in bananas:
                b.move_at_speed()
                if b.get_rect().left < 0:  # separated to ensure correct direction is stuck to
                    b.ensure_travel_right()
                elif b.get_rect().right > screen_width:
                    b.ensure_travel_left()

                if b.get_rect().colliderect(player_1.get_rect()):
                    rem_b.append(b)
                    if b.get_gives_life():
                        if lives < 10:
                            lives += 1
                            background_colour = (0, 254, 254)
                    else:
                        lives -= 1
                        background_colour = (250, 0, 0)
                else:
                    ind = b.get_rect().collidelist([x.get_rect() for x in projectiles])
                    if ind != -1:
                        if b.get_gives_life():
                            if lives < 10:
                                lives += 1
                                background_colour = (0, 254, 254)
                        else:
                            bananas_shot += 1  # life-bananas don't count towards this
                        rem_b.append(b)
                        del projectiles[ind]
                    elif b.get_rect().top > screen_height:  # if not collided with player, check for locational despawn
                        rem_b.append(b)
                        bananas_dodged += 1
                        if banana_spawn_rate > 15:
                            banana_spawn_rate -= 2

            bananas = [b for b in bananas if b not in rem_b]

            update_labels()

            # draw on background
            background_colour = background_fade()
            background.fill(background_colour)
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
                b.rotate_tick()
                screen.blit(b.get_img(), b.get_rect())
            for p in projectiles:
                screen.blit(p.get_img(), p.get_rect())

            # animate bobbing
            player_1.balloon_bob(player_bob_rate)
            screen.blit(player_1.get_img(), player_1.get_rect())

            pygame.display.flip()
            time.sleep(0.01)
        else:
            time.sleep(0.2)  # paused

    show_death_messages(background, bananas_dodged, bananas_shot, screen)

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
