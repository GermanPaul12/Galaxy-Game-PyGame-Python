import pygame
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Test Game')

LIGHT_BLUE = (162, 210, 255)
BLACK = (0, 0, 0)
RED = (217, 4, 41)
YELLOW = (254, 228, 64)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    "Gun+Silencer.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    "Grenade+1.mp3")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


SPACE = pygame.transform.scale(pygame.image.load(
    "space.png"), (WIDTH, HEIGHT))


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    "spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    "spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)



def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    yellow_health_text = HEALTH_FONT.render(f"HEALTH: {yellow_health}", 1, LIGHT_BLUE)
    red_health_text = HEALTH_FONT.render(f"HEALTH: {red_health}", 1, LIGHT_BLUE)
    
    WIN.blit(yellow_health_text, (10 , 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10 , 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY    
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x + BORDER.width + 5:  # RIGHT
        yellow.x += VELOCITY     
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY    
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VELOCITY   
        
        
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:  # LEFT
        red.x -= VELOCITY    
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY < WIDTH - red.width + 10:  # RIGHT
        red.x += VELOCITY     
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY    
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:  # DOWN
        red.y += VELOCITY          


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)    
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)  
            
        elif bullet.x < 0:
            red_bullets.remove(bullet)           


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, LIGHT_BLUE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global yellow_health
    global red_health
    
    yellow = pygame.Rect(50, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(800, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    yellow_bullets = []
    red_bullets = []
    
    yellow_health = 10
    red_health = 10
    
    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:    
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"
            
        if red_health <= 0:     
            winner_text = "Yellow Wins!"       
             
        if winner_text != "":
            draw_winner(winner_text)  # Someone Won    
            break
                
        keys_pressed = pygame.key.get_pressed()
        
        
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)       
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)      
             
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
    
    main()               
    
if __name__ == '__main__':
    main()     