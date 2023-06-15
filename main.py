import pygame
pygame.init()

from game_objects import Player
from world import World
from assets import *
from constants import *


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

world = World("maps/default.csv")
player = Player(PLAYER_SPAWN_X, PLAYER_SPAWN_Y, 3, frog)

game_over = False

while True:
    time = pygame.time.get_ticks()
    dt = clock.tick(FPS)

    world.update(time, dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    exit()

                case pygame.K_r:
                    player.health = player.max_health
                    player.score = 0
                    player.reset_position()
                    game_over = False
            
            if not game_over:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        if (player.y >= 1):
                            player.y -= 1
                            grid_value = world.grid[round(player.y)][round(player.x)]
                            if grid_value == "1" or grid_value == "2":
                                player.reset_position()
                                player.score += 1
                    
                    case pygame.K_a | pygame.K_LEFT:
                        if (player.x >= 1):
                            player.x -= 1
                    
                    case pygame.K_s | pygame.K_DOWN:
                        if (player.y < Y_TILES - 1):
                            player.y += 1
                    
                    case pygame.K_d | pygame.K_RIGHT:
                        if (player.x < X_TILES - 1):
                            player.x += 1

    if not game_over:
        world.handle_collisions(player, dt)

        world.draw(screen)
        player.draw(screen)
        player.draw_stats(screen)


        if player.health <= 0:

            with open("highscore.txt", "r") as file:
                highscore = int(file.read())
            
            if player.score > highscore:
                with open("highscore.txt", "w") as file:
                    file.write(str(player.score))
                
                highscore = player.score

            game_over = True
            game_over_text = font60.render("Game Over", True, (0, 0, 0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (WIDTH // 2, HEIGHT // 2 - 110)
            screen.blit(game_over_text, game_over_text_rect)

            highscore_text = font40.render(f"Highscore: {highscore}", True, (0, 0, 0))
            highscore_text_rect = highscore_text.get_rect()
            highscore_text_rect.center = (WIDTH // 2, HEIGHT // 2 - 65)
            screen.blit(highscore_text, highscore_text_rect)

            try_again_text = font40.render("press 'r'", True, (0, 0, 0))
            try_again_text_rect = try_again_text.get_rect()
            try_again_text_rect.center = (WIDTH // 2, HEIGHT // 2 - 25)
            screen.blit(try_again_text, try_again_text_rect)
            
        pygame.display.update()
