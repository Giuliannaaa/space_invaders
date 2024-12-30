import random
import pygame, sys
from game import Game

# Initialize the game
pygame.init()

# Set up the screen
WINDOW_WIDTH = 675
WINDOW_HEIGHT = 650
OFFSET = 10

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = pygame.font.Font("Font/PixelifySans-VariableFont_wght.ttf", 24)
level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

screen = pygame.display.set_mode((WINDOW_WIDTH + OFFSET, WINDOW_HEIGHT + 0.25* OFFSET))

pygame.display.set_caption("Space Invaders")


def victory_message(screen, font, screen_width, screen_height):
    if len(game.aliens_group) == 0 and len(game.mystery_ship_group) == 0:
        victory_surf = font.render('You won', False, 'white')
        victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(victory_surf, victory_rect)
        pygame.display.update() 
        pygame.time.delay(2000)

clock = pygame.time.Clock()
# --- ---
# spaceship = Spaceship(WINDOW_WIDTH, WINDOW_HEIGHT)
# spaceship_group = pygame.sprite.GroupSingle()
# spaceship_group.add(spaceship)

# obstacle = Obstacle(100, 100)
# ---
# laser = Laser((100, 100), 6, WINDOW_HEIGHT)
# laser2 = Laser((100, 200), -6, WINDOW_HEIGHT)
# lasers_group = pygame.sprite.Group()
# lasers_group.add(laser, laser2)

game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

# The main game loop
running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
            
        if event.type == MYSTERYSHIP:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()
    
    # Updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        # game.alien_shoot_laser()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()
        victory_message(screen, font, WINDOW_WIDTH, WINDOW_HEIGHT)
        
    # --- ---
    # spaceship_group.update()
    # ---
    # lasers_group.update()
    
    # Drawing
    screen.fill(GREY)
    
    # UI
    pygame.draw.rect(screen, YELLOW, (2, 2, 675, 650), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (5, WINDOW_HEIGHT - 50), (WINDOW_WIDTH - 5, WINDOW_HEIGHT - 50), 2)
    
    if game.run:
        screen.blit(level_surface, (490, 610, 45, 45))
    else:
        screen.blit(game_over_surface, (490, 610, 45, 45))

    x = 50
    surface = pygame.Surface((25, 25))
    surface.fill(YELLOW)
    
    for life in range(game.lives):
        screen.blit(surface, (x, 615))
        x += 50
    
    # Score
    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(str(formatted_score), False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (495, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (495, 40, 50, 50))
    # --- ---
    # spaceship_group.draw(screen)
    # spaceship_group.sprite.lasers_group.draw(screen)
    # obstacle.blocks_group.draw(screen)
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
        
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)
    
    # ---
    # lasers_group.draw(screen)
    
    pygame.display.update()
    clock.tick(60)
    