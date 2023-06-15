import pygame
import csv
from pathlib import Path

from game_objects import Player
from spawner import RoadSpawner, WaterSpawner
from assets import *
from constants import *


class World:
    def __init__(self, path: str) -> None:

        self.background = pygame.Surface((TILE_SIZE*X_TILES, TILE_SIZE*Y_TILES))
        self.water_spawners: list[WaterSpawner] = []
        self.road_spawners: list[RoadSpawner] = []
        self.grid: list[list[str]] = []

        with open(Path(__file__).parent / path, "r") as file:
            data = csv.reader(file, delimiter=';')
            
            self.min_vehicle_speed, self.max_vehicle_speed, self.min_log_speed, self.max_log_speed = [eval(i) for i in next(data)]

            for y, line in enumerate(data):
                self.grid.append([])
                for x, tile in enumerate(line):
                    pos_rect = (TILE_SIZE*x, TILE_SIZE*y, TILE_SIZE, TILE_SIZE)

                    match tile:
                        case "g":
                            pygame.draw.rect(self.background, (0, 255, 0), pos_rect)
                        
                        case "1":
                            self.background.blit(goal1, pos_rect)
                        
                        case "2":
                            self.background.blit(goal2, pos_rect)
                        
                        case "w" | "wsl" | "wsr":
                            pygame.draw.rect(self.background, (0, 0, 255), pos_rect)

                            if tile == "wsl":
                                self.water_spawners.append(WaterSpawner(x, y, -self.max_log_speed, -self.min_log_speed))
                            elif tile == "wsr":
                                self.water_spawners.append(WaterSpawner(x - 4, y, self.min_log_speed, self.max_log_speed))
                        
                        case "r" | "rsl" | "rsr":
                            pygame.draw.rect(self.background, (100, 100, 100), pos_rect)
                            
                            if tile == "rsl":
                                self.road_spawners.append(RoadSpawner(x + 1, y, -self.max_vehicle_speed, -self.min_vehicle_speed))
                            elif tile == "rsr":
                                self.road_spawners.append(RoadSpawner(x - 2, y, self.min_vehicle_speed, self.max_vehicle_speed))

                    self.grid[y].append(tile[0])


    def update(self, time: int, dt: int) -> None:
        for spawner in self.water_spawners:
            spawner.update_objects(dt)
            spawner.handle_spawning(time)

        for spawner in self.road_spawners:
            spawner.update_objects(dt)
            spawner.handle_spawning(time)

    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
    
        for spawner in self.water_spawners:
            spawner.draw_objects(screen)

        for spawner in self.road_spawners:
            spawner.draw_objects(screen)
    

    def handle_collisions(self, player: Player, dt: int) -> None:

        # Only check collisions with cars when standing on a road
        if self.grid[round(player.y)][round(player.x)] == 'r':
            for spawner in self.road_spawners:
                for object in spawner.objects:
                    if player.collision(object):
                        player.reset_position()
                        player.health -= 1

        # Only check collisions with logs when standing on water
        if self.grid[round(player.y)][round(player.x)] == 'w':
            player.standing_on_log = False
            
            for spawner in self.water_spawners:
                for object in spawner.objects:
                    if player.collision(object):
                        player.x += object.vel * dt / 1000
                        
                        if player.x + player.width > X_TILES:
                            player.x = X_TILES - 1
                        elif player.x < 0:
                            player.x = 0

                        player.standing_on_log = True
                        break

                if player.standing_on_log:
                    break

            if not player.standing_on_log:
                player.reset_position()
                player.health -= 1
        else:
            player.x = round(player.x)
