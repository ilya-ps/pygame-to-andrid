import pygame

image_path = '/data/data/com.app.myapp/files/app/'
clock = pygame.time.Clock()
clock1 = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1920, 1080))        # flags=pygame.NOFRAME (без рамок)
pygame.display.set_caption('Pygame Ilya Game')      # название
icon = pygame.image.load('images/icon.png')         # загрузка иконки
pygame.display.set_icon(icon)                       # установка иконки


bg = pygame.image.load('images/bg.png').convert()
# walk_left = [
#     pygame.image.load('images/player_left/player_left1.png'),
#     pygame.image.load('images/player_left/player_left2.png'),
#     pygame.image.load('images/player_left/player_left3.png'),
#     pygame.image.load('images/player_left/player_left4.png'),
#     pygame.image.load('images/player_left/player_left5.png'),
#     pygame.image.load('images/player_left/player_left6.png'),
#     pygame.image.load('images/player_left/player_left7.png')
# ]
walk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right5.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right6.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right7.png')
]

zombie = pygame.image.load('images/zombie.png').convert_alpha()
zombie_list_in_game = []


player_anim_count = 0
bg_x = 0

player_speed = 45
player_x = 300
player_y = 750

is_jump = False
jump_count = 11


bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
# bg_sound.play()

zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 2500)

label = pygame.font.Font('fonts/RobotoSlab-Light.ttf', 100)
lose_label = label.render('GAME OVER!', False, ('Red'))
restart_label = label.render('Try again', False, ('Green'))
restart_label_rect = restart_label.get_rect(topleft=(700, 550))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []


gameplay = True


running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1920, 0))
    screen.blit(walk_right[player_anim_count], (player_x, player_y))


    if gameplay:
        player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))

        if zombie_list_in_game:
            for (i, el) in enumerate(zombie_list_in_game):
                screen.blit(zombie, el)
                el.x -= 15

                if el.x < -10:
                    zombie_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1800:
            player_x += player_speed

        if not is_jump:                                       #цикл прыжка
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -11:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 11

        if player_anim_count == 6:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1920:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 80

                if el.x > 2000:
                    bullets.pop(i)

                if zombie_list_in_game:
                    for (index, zombie_el) in enumerate(zombie_list_in_game):
                        if el.colliderect(zombie_el):
                            zombie_list_in_game.pop(index)
                            bullets.pop(i)



    else:
        screen.fill('Black')
        screen.blit(lose_label, (600, 350))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 300
            zombie_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == zombie_timer:
            zombie_list_in_game.append(zombie.get_rect(topleft=(1920, 750)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_r and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1
    clock.tick(20)