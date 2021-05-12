import pygame, sys, random

pygame.init()

screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()

def draw_floor():
    screen.blit(floor,(floor_position_x,500))
    screen.blit(floor, (floor_position_x + 400,500))

def draw_bg():
    screen.blit(bg_surface, (bg_x,0))
    screen.blit(bg_surface, (bg_x + 400,0))

# def create_pipe():
#     new_pipe = pipe_surface.get_rect(midtop = (510, 350))
#     return new_pipe

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (520, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (520, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
        
def check_colissions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        collision_sound.play()
        die_sound.play()
        return False
    return True
    
    
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird  


def bird_animation():
    new_bird = bird_frames[bird_index] 
    new_bird_rect = new_bird.get_rect(center = (200, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 100))
        screen.blit(score_surface, score_rect)
    

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (250, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score:{str(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (250, 250))
        screen.blit(high_score_surface, high_score_rect) 

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

game_font = pygame.font.Font('score', 40)

def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 0.5
                score_sound.play()
                #can_score = False



# bird
# 1st step for the bird
# bird = pygame.image.load('bird1.png').convert_alpha()
# bird_rect = bird.get_rect(center = (170,300))
# 2nd step for the bird
bird_up = pygame.transform.scale2x(pygame.image.load('bluebird-upflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('bluebird-midflap.png').convert_alpha())
bird_down = pygame.transform.scale2x(pygame.image.load('bluebird-downflap.png').convert_alpha())
bird_frames = [bird_down, bird_mid, bird_down]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (200, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)



# pipe
pipe_surface = pygame.image.load('pipe-green down.png')
pipe_surface = pygame.transform.scale2x((pipe_surface))
pipe_list = []
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200 )

bg_surface = pygame.image.load('background.png').convert()
bg_x = 0
pipe_height = [240, 300, 350]
floor = pygame.image.load('floor.png').convert()
floor_position_x = 0
gravity = 0.25  
bird_movement = 0
game_active = True

score = 0
high_score = 0
can_score = True

game_over_surface = pygame.image.load('gameover.png')
game_over_rect = game_over_surface.get_rect(center = (250, 350))

flap_sound = pygame.mixer.Sound('sfx_wing.wav')
die_sound = pygame.mixer.Sound('sfx_die.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
collision_sound = pygame.mixer.Sound('sfx_hit.wav')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

            

        

    floor_position_x -= 3
    bg_x -= 1

    draw_bg()

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_colissions(pipe_list)

        
        
    
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()     
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
    draw_floor()
    if bg_x <= -400:
        bg_x = 0
    
    if floor_position_x <= -400:
        floor_position_x = 0
    
    pygame.display.update()
    clock.tick(70)
