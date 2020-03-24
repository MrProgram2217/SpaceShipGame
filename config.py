import pygame

display_width = 600
display_height = 900

pygame.font.init()
pygame.init()
myfont = pygame.font.Font('font\Teko-Bold.ttf', 45)       # init font

player_speed = 3            # speed of the player
speed_of_update_game = 80   # update speed
stars_speed = 1             # speed of stars
shell_speed = 8             # shell's speed
explode_time = 40           # frames of show explode
player_lifes = 3            # player's lifes in the begin
max_lifes = 5               # max lifes that player can have
max_super_shots = 5         # max super shots that player can have
max_game_speed = 6          # max speed of the game
bonus_speed = 3             # bonus's speed
super_shot_speed = 4        # super shot's speed

enemy_quan = 30             # quantity of enemys
stars_quan = 200            # quantity of stars

frames_bet_shots = 30       # frames between new shells


player_img = [pygame.image.load('player\player_1.png'),
             pygame.image.load('player\player_2.png') ]             # player images anim
player_options = [ 80, 100 ]      # player options


shell_img = [pygame.image.load('shell\shell_1.png'),
             pygame.image.load('shell\shell_2.png') ]               # shell images anim
shell_options = [ 5, 11 ]         # shell options


enemy_img = [pygame.image.load('enemy\enemy_1_1.png'),
             pygame.image.load('enemy\enemy_1_2.png'),
             pygame.image.load('enemy\enemy_1_dam.png') ]           # enemy images anim
enemy_options = [ 96, 102 ]       # enemy options


explode_img = [ pygame.image.load('effects\explode_1.png'),
                pygame.image.load('effects\explode_2.png') ]        # explode images anim
explode_options = [ 96, 96 ]      # explode options


super_shot_img = [ pygame.image.load('effects\super_shot_1.png'),
                   pygame.image.load('effects\super_shot_2.png')]   # super shot images anim
super_shot_options = [ 80, 80 ]   # super shot options

empty_img = pygame.image.load('effects\empty.png')                  # empty texture


heart = [ pygame.image.load('effects\heart.png'),
          pygame.image.load('effects\heart_large.png') ]            # heart texture
heart_options = [ [48, 48], [64, 64] ]      # hearts options

sounds = [ pygame.mixer.Sound('sounds\collect.wav'),
           pygame.mixer.Sound('sounds\collect_super_shot.wav'),
           pygame.mixer.Sound('sounds\explosion.wav'),
           pygame.mixer.Sound('sounds\hit_player.wav'),
           pygame.mixer.Sound('sounds\shot.wav')]                   # import sounds