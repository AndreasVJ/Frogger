import pygame

from assets import *
from constants import *


class GameObject:
    def __init__(self, x: float, y: float, width: float, height: float, img: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
    

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.img, (self.x*TILE_SIZE, self.y*TILE_SIZE))
    

    def collision(self, object: 'GameObject') -> bool:
        return self.x < object.x + object.width and self.x + self.width > object.x and self.y < object.y + object.height and self.y + self.height > object.y


class MovingGameObject(GameObject):
    def __init__(self, x: float, y: float, vel: float, width, height, img) -> None:
        super().__init__(x, y, width, height, img)
        self.vel = vel
    

    def update(self, dt: int) -> None:
        self.x += self.vel * dt / 1000


class Player(GameObject):
    def __init__(self, x: float, y: float, health: int, img: pygame.Surface) -> None:
        super().__init__(x, y, 1, 1, img)
        self.max_health = health
        self.health = health

        self.__score = 0
        self.standing_on_log = False
        
        self.score_text = font40.render(f'Score: {self.__score}', True, (0, 0, 0))


    @property
    def score(self) -> int:
        return self.__score
    
    @score.setter
    def score(self, value) -> None:
        self.__score = value
        self.score_text = font40.render(f'Score: {self.__score}', True, (0, 0, 0))


    def draw_stats(self, screen: pygame.Surface) -> None:
        # Draw health
        for i in range(self.max_health):
            if i < self.health:
                screen.blit(heart, (5 + i*45, 5))
            else:
                screen.blit(empty_heart, (5 + i*45, 5))
    
        # Draw score
        screen.blit(self.score_text, (300, 5))




    def reset_position(self) -> None:
        self.x = PLAYER_SPAWN_X
        self.y = PLAYER_SPAWN_Y
