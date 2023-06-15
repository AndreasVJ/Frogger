import pygame
import random
import sys

from game_objects import MovingGameObject
from assets import *
from constants import *


class Spawner:
    def __init__(self, x: float, y: float, min_vel: float, max_vel: float) -> None:
        self.x = x
        self.y = y
        self.min_vel = min_vel
        self.max_vel = max_vel

        self.prev_spawn_time = -sys.maxsize
        self.objects: list[MovingGameObject] = []
    

    def spawn(self) -> None:
        " Implemented in subclasses"


    def handle_spawning(self, time: int) -> None:
        if time - self.prev_spawn_time > SPAWN_TIME_LIMIT:
            if random.random() * (time - self.prev_spawn_time) / FPS > 30:
                self.spawn()
                self.prev_spawn_time = pygame.time.get_ticks()

    
    def update_objects(self, dt: int) -> None:
        for object in self.objects:
            object.update(dt)
        
        if (len(self.objects)):
            obj0 = self.objects[0]
            
            if (self.x < 0):
                if obj0.x >= X_TILES:
                    self.objects.pop(0)
            elif obj0.x + obj0.width < 0:
                self.objects.pop(0)


    def draw_objects(self, screen: pygame.Surface) -> None:
        for object in self.objects:
            object.draw(screen)


class RoadSpawner(Spawner):
    def __init__(self, x: float, y: float, min_vel: float, max_vel: float) -> None:
        super().__init__(x, y, min_vel, max_vel)
    

    def spawn(self) -> None:
        vel = random.uniform(self.min_vel, self.max_vel)

        if random.random() < TRUCK_PROBABILITY:
            truck_index = random.randrange(0, len(left_trucks))
            self.objects.append(MovingGameObject(self.x, self.y, vel, 2, 1, left_trucks[truck_index] if vel < 0 else right_trucks[truck_index]))
        else:
            car_index = random.randrange(0, len(left_cars))
            self.objects.append(MovingGameObject(self.x, self.y, vel, 1, 1, left_cars[car_index] if vel < 0 else right_cars[car_index]))


class WaterSpawner(Spawner):
    def __init__(self, x: float, y: float, min_vel: float, max_vel: float) -> None:
        super().__init__(x, y, min_vel, max_vel)

    def spawn(self) -> None:
        value = random.random()
        speed = random.uniform(self.min_vel, self.max_vel)
        
        if value < LARGE_LOG_PROBABILITY:
            self.objects.append(MovingGameObject(self.x, self.y, speed, 4, 1, large_log))
        elif value < LARGE_LOG_PROBABILITY + MEDIUM_LOG_PROBABILITY:
            self.objects.append(MovingGameObject(self.x, self.y, speed, 3, 1, medium_log))
        else:
            self.objects.append(MovingGameObject(self.x, self.y, speed, 2, 1, small_log))