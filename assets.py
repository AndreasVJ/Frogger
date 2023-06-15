import pygame

goal1 = pygame.image.load("assets/goal1.png")
goal2 = pygame.image.load("assets/goal2.png")

frog = pygame.image.load("assets/frog.png")

heart = pygame.image.load("assets/heart.png")
empty_heart = pygame.image.load("assets/empty_heart.png")

red_car_left = pygame.image.load("assets/red_car.png")
yellow_car_left = pygame.image.load("assets/yellow_car.png")
white_car_left = pygame.image.load("assets/white_car.png")
red_car_right = pygame.transform.flip(red_car_left.copy(), True, False)
yellow_car_right = pygame.transform.flip(yellow_car_left.copy(), True, False)
white_car_right = pygame.transform.flip(white_car_left.copy(), True, False)

left_cars = [red_car_left, yellow_car_left, white_car_left]
right_cars = [red_car_right, yellow_car_right, white_car_right]

red_truck_left = pygame.image.load("assets/red_truck.png")
purple_truck_left = pygame.image.load("assets/purple_truck.png")
red_truck_right = pygame.transform.flip(red_truck_left.copy(), True, False)
purple_truck_right = pygame.transform.flip(purple_truck_left.copy(), True, False)

left_trucks = [red_truck_left, purple_truck_left]
right_trucks = [red_truck_right, purple_truck_right]

small_log = pygame.image.load("assets/small_log.png")
medium_log = pygame.image.load("assets/medium_log.png")
large_log = pygame.image.load("assets/large_log.png")

font40 = pygame.font.Font("freesansbold.ttf", 40)
font60 = pygame.font.Font("freesansbold.ttf", 60)
