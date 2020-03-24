import pygame
import sys
from random import randint,choice
from config import *

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode( (display_width, display_height) )
pygame.display.set_caption( 'Space Battle' )

game_over = False

enemy_array = []
shell_array = []
explode_array = []
stars_array = []
super_shots_array = []
bonus_array = []                     # in game bonuses

avail_super_shots = 0                # available super shots
array_long_y = 0                     # to spawn enemys in the top
game_speed = 3                       # speed of the game
killed = 0                           # quantity of killed enemys

time_to_spawn_shell = frames_bet_shots
score_back = 1                       # help game score
score = 1                            # in game score

class Player:
    def __init__(self, x, y, width, height, live, image_1, image_2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.live = live
        self.image_1 = image_1
        self.image_2 = image_2

        self.image = self.image_1

    def draw(self):
        display.blit( self.image, ( self.x, self.y ) )

    def move_player(self, botton):
        if (botton == 'left') and (self.x >= 0):
            self.x -= player_speed
        elif (botton == 'right') and (self.x <= display_width - self.width):
            self.x += player_speed

        if (botton == 'up') and (self.y >= 0):
            self.y -= player_speed
        elif (botton == 'down') and (self.y <= display_height - self.height):
            self.y += player_speed

    def change_texture(self):
        if self.image == self.image_1:
            self.image = self.image_2
        else:
            self.image = self.image_1

class Shell(Player):
    def move_shell(self):
        self.y -= shell_speed

    def move_super_shot(self):
        self.y -= super_shot_speed

class Enemy(Player):
    def move_enemy(self):
        self.y += game_speed

    def damage_texture(self, tex):
        self.image = tex

class Bonus(Enemy):
    pass

class Star:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y =y
        self.width = width
        self.height = height
        self.color = color

    def draw_star(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height))

    def move_star(self):
        self.y += stars_speed


player = Player( display_width/2,                           # make player
                 display_height - player_options[1] - 50,
                 player_options[0],
                 player_options[1],
                 player_lifes,
                 player_img[0], player_img[1] )

super_shot = None

def run_game():
    global game_speed, score, time_to_spawn_shell, score_back, player_speed, frames_bet_shots

    game = True
    make_stars_array(stars_array)
    make_enemy_array(enemy_array)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:      # STOP
            game = False

        if keys[pygame.K_SPACE]:
            spawn_shell()              # make shots
        if keys[pygame.K_s]:
            make_super_shot(super_shots_array)           # make super shot

        display.fill((15,15,15))        # draw background

        check_destroy(enemy_array, shell_array)     # check collisions
        check_player_collisions(enemy_array)

        draw_stars_array(stars_array)         # draw everythong
        draw_shell_arr(shell_array)
        player.draw()
        draw_enemy_arr(enemy_array)
        draw_explode(explode_array)
        draw_bonus_array(bonus_array)
        draw_hearts()
        draw_super_shot(enemy_array)
        draw_avail_super_shots()              # end here

        if not game_over:
            if keys[pygame.K_LEFT]:           # control player
                player.move_player('left')
            elif keys[pygame.K_RIGHT]:
                player.move_player('right')
            if keys[pygame.K_UP]:
                player.move_player('up')
            elif keys[pygame.K_DOWN]:
                player.move_player('down')

            if score_back % 3000 == 0:          # soawn heart
                add_bonus_heart()
            elif score_back % 1500 == 0:
                add_bonus_super_shot()
            add_bonus_to_player(bonus_array)

            score_back += 1
            score = score_back // 10                  # score
            if score_back % 4000 == 0 and game_speed < max_game_speed:    # to make game faster
                game_speed += 1
                player_speed += 1
                frames_bet_shots -= 2

            if time_to_spawn_shell > 0:
                time_to_spawn_shell -= 1        # to make time between shots

            if score_back % 10 == 0:             # make anim
                player.change_texture()

        textsurface = myfont.render('SCORE: ' + str(killed), False, (255, 255, 255) )   # draw stats
        display.blit(textsurface,(0,-10))

        if game_over:
            myfont_game_over = pygame.font.Font('font\Teko-Bold.ttf', 120)
            textsurface = myfont_game_over.render('GAME OVER', False, (255, 255, 255))      # Draw Game Over
            display.blit(textsurface,(0,display_height/2 - 120))

        pygame.display.update()
        clock.tick( speed_of_update_game )

def spawn_shell():
    global shell_array, time_to_spawn_shell

    if time_to_spawn_shell == 0:
        sounds[4].play()
        shell = Shell(player.x + player.width/2 - shell_options[0],
                    player.y - shell_options[1],
                    shell_options[0],
                    shell_options[1],
                    1,
                    shell_img[0],
                    shell_img[1])

        shell_array.append( shell )
        time_to_spawn_shell = frames_bet_shots 

def rand_lifes(chance):
    rand_live = randint(0, 10)
    if rand_live >= chance:
        return 2
    else:
        return 1

def draw_bonus_array(array):
    for bonus in array:
        bonus.draw()
        bonus.move_enemy()

        if bonus.y > display_height:
            array.pop(0)

def make_enemy(array):
    if len(array) == 0:
        y_coord = -200
    else:
        y_coord = array[-1].y - randint(250,350) + game_speed*(game_speed*5)

    enemy = Enemy( randint(0,display_width-enemy_options[0]),
                   y_coord,
                   enemy_options[0],
                   enemy_options[1],
                   rand_lifes(7),
                   enemy_img[0],
                   enemy_img[1] )

    array.append( enemy )
    array_long_y = y_coord

def add_explode(array, coord):
    sounds[2].play()
    array.append( [coord.x, coord.y, explode_time] )

def make_enemy_array(array):
    for i in range (enemy_quan):
        make_enemy(array)

def change_enemy_coord(enemy, array, i):
    global killed

    array.pop(i)
    make_enemy(array)
    add_explode(explode_array, enemy)
    killed += 1

def draw_enemy_arr(array):
    global game_over
    i = 0

    for enemy in array:
        enemy.draw()
        enemy.move_enemy()

        if (enemy.y + enemy.height) > display_height + enemy.height:
            kill_player()
            change_enemy_coord(enemy, enemy_array, i)

        if score_back % 12 == 0:
            enemy.change_texture()
        i+=1

def check_destroy(enemys, shells):
    global explode_array

    for shell in shells:
        i = 0
        for enemy in enemys:
            if (enemy.y <= shell.y <= enemy.y + enemy.height) and (enemy.x <= shell.x <= enemy.x + enemy.width):
                if enemy.live == 1:
                    change_enemy_coord(enemy, enemy_array, i)
                else:
                    enemy.live -= 1
                    enemy.damage_texture(enemy_img[2])

                try:
                    shells.pop(0)
                except:
                    pass
            i+=1

def add_bonus_to_player(array):
    global player_lifes, avail_super_shots

    for bonus in array:
        if collision(player, bonus):
            sounds[0].play()
            if bonus.live == 1:
                if player.live < max_lifes:
                    player.live += 1
            else:
                if avail_super_shots < max_super_shots:
                    avail_super_shots += 1
            array.clear()

def draw_avail_super_shots():
    for i in range (avail_super_shots):
        display.blit( super_shot_img[0], ( display_width - super_shot_options[0] - i*super_shot_options[1], heart_options[0][1] ) )

def add_bonus_super_shot():
    global bonus_array

    bonus = Bonus( randint(0, display_width-super_shot_options[0]),
                   -100,
                   super_shot_options[0],
                   super_shot_options[1],
                   2,
                   super_shot_img[1],
                   super_shot_img[1] )

    bonus_array.append(bonus)

def make_super_shot(array):
    global super_shot, avail_super_shots

    if avail_super_shots > 0 and super_shot == None:
        super_shot = Shell(player.x,
                           player.y - super_shot_options[1],
                           super_shot_options[0],
                           super_shot_options[1],
                           1,
                           super_shot_img[0],
                           super_shot_img[1])
        avail_super_shots -= 1

def draw_super_shot(array):
    global super_shot
    i = 0

    if not super_shot == None:
        super_shot.draw()
        super_shot.move_super_shot()

        if super_shot.y + super_shot.height< 0:
            super_shot = None

        elif score_back % 15 == 0:
            super_shot.change_texture()

        for enemy in array:
            if super_shot != None:
                if collision(super_shot, enemy):
                    super_shot = None

                    for sec_enemy in array:
                        if sec_enemy.y > -350:
                            i += 1
                    for k in range(i):
                        change_enemy_coord(array[0], array, 0)

def draw_explode(array): 
    # explode[0]: x; explode[1]: y; explode[2]: anim_time;

    for explode in array:
        if explode[2] > explode_time/2:
            display.blit( explode_img[0], ( explode[0], explode[1] ) )
            explode[2] -= 1
        elif explode[2] > 0:
            display.blit( explode_img[1], ( explode[0], explode[1] ) )
            explode[2] -= 1
        if explode[2] == 0:
            array.pop(0)

def make_stars_array(array):
    for i in range (stars_quan):
        x = randint(0, display_width-5)
        y = randint(0, display_height)
        star = Star(x, y, 1, 1, (200,200,200))

        array.append(star)

def add_bonus_heart():
    global bonus_array

    bonus = Bonus( randint(0,display_width-heart_options[1][0]),
                   -100,
                   heart_options[1][0],
                   heart_options[1][1],
                   1,
                   heart[1],
                   heart[1] )

    bonus_array.append(bonus)

def draw_stars_array(array):
    for star in array:
        star.draw_star()
        star.move_star()

        if star.y > display_height:
            star.y = -1

def draw_hearts():
    for i in range (player.live):
        display.blit( heart[0], ( display_width - heart_options[0][0] - i*heart_options[0][1], 0 ) )

def draw_shell_arr(array):
    global shell_array

    for shell in array:
        shell.draw()
        shell.move_shell()

        if (shell.y + shell.height) < 0:
            shell_array.pop(0)

def check_player_collisions(array):
    i = 0
    for enemy in array:
        if collision(player, enemy):
            kill_player()
            change_enemy_coord(enemy, enemy_array, i)
        i+=1

def collision(active, obj):
    if (obj.y <= active.y <= obj.y + obj.height) and ((obj.x <= active.x <= obj.x + obj.width) or (obj.x <= active.x + active.width <= obj.x + obj.width)):
        return True
    return False

def kill_player():
    global game_over
    if (player.live == 1) and (not game_over):
        game_over = True
        player.image = empty_img
        add_explode(explode_array, player)
        player.x = display_width
    player.live -= 1

print('\nLSHIFT - stop game\nLEFT - move left\nRIGHT - move right\nSPACE - shot\nS - super shot')         # how 2 play
run_game()