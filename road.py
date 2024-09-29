import time

from car import Car
from constants import *
import pygame
import numpy as np

from interactions import RoadObject, CarMutator


class Road:
    cars: list[Car]
    rect: pygame.Rect
    spawn_coords: tuple[int, int]
    objects: list[RoadObject]
    mutations: list[CarMutator]
    last_updated: float

    export_finished = 0
    export_speeds = []
    export_distances = []

    def __init__(self, x: int, objects: list[RoadObject], mutations: list[CarMutator]):
        self.cars = []
        self.objects = objects
        self.mutations = mutations
        self.rect = pygame.Rect(x, 0, 200, HEIGHT)
        self.spawn_coords = (x + 100, HEIGHT - 50)
        self.last_updated = time.time()
        self.last_population = time.time()

    def add_car(self, car: Car) -> None:
        self.cars.append(car)

    def spawn_car(self) -> Car:
        s = np.random.randint(CAR_LOWER_SPEED, CAR_UPPER_SPEED + 1)
        car = Car(self.spawn_coords, s, s)
        
        self.cars.append(car)
        return car
    
    def populate_with_cars(self, num_cars: int) -> None:
        if time.time() - self.last_population >= AUTO_ADD_CAR_COOLDOWN and len(self.cars) < num_cars:
            self.spawn_car()
            self.last_population = time.time()

    def draw(self, window: pygame.Surface, font: pygame.font.Font) -> None:
        pygame.draw.rect(window, ROAD_COLOR, self.rect)
        for object in self.objects:
            object.draw(self, window, font)
        for car in self.cars:
            car.draw(window)
            car.draw_speed(window, font)
    
    def export(self):
        a = self.export_finished
        b = 0 if len(self.export_speeds) == 0 else sum(self.export_speeds) / len(self.export_speeds)
        c = 0 if len(self.export_distances) == 0 else sum(self.export_distances) / len(self.export_distances)
        self.export_finished = 0
        self.export_speeds = []
        self.export_distances = []
        return a, b, c

    def update(self):
        raise NotImplemented()


class NaiveRoad(Road):
    def __init__(self, x: int, objects: list[RoadObject], mutations: list[CarMutator]):
        super().__init__(x, objects, mutations)

    def update(self) -> None:
        to_export = False
        if time.time() - self.last_updated >= 5:
            to_export = True
            self.last_updated = time.time()

        for obj in self.objects:
            obj.update()

        to_remove = []
        for i in range(len(self.cars)):
            car = self.cars[i]

            chain_mutated = False
            # Calculate chain effect for this car if it's behind other cars
            if i != 0:
                front = self.cars[i - 1]
                distance = car.distance_to(front)
                if to_export:
                    self.export_distances.append(distance)
                if distance <= DEC_LOWER_BOUND_DIST and car.speed > 0:
                    car.decelerate()
                    chain_mutated = True
                elif car.speed == car.max_speed or car.speed == 0:
                    # Stop accelerating/decelerating if cannot go further
                    car.accelerating = False
                    car.decelerating = False

            # When a car gets close to an object, allow the object to mutate it
            obj_mutated = False
            if not chain_mutated:  # Chain effect mutation takes precedence over object mutations
                for obj in self.objects:
                    obj_mutated = obj.mutate(car, i)
                    if obj_mutated:
                        break
                if car.manual_decelerate:
                    # A special case, where we manually decelerate cars if requested
                    if car.speed > 0:
                        car.decelerate()
                        obj_mutated = True
                    else:
                        car.manual_decelerate = False

            # Finally, if neither chain nor object mutated this car, allow it to accelerate to its maximum speed
            if not chain_mutated and not obj_mutated and car.speed < car.max_speed:
                car.accelerate()

            car.move()
            if to_export and car.speed >= 5:
                self.export_speeds.append(car.speed)
            if car.position[1] <= 15:
                to_remove.append(car)  # Remove cars that have exceeded the map boundaries
                self.export_finished += 1

        for car in to_remove:
            self.cars.remove(car)


class SmartRoad(Road):
    def __init__(self, x: int, objects: list[RoadObject], mutations: list[CarMutator]):
        super().__init__(x, objects, mutations)

    def update(self) -> None:
        to_export = False
        if time.time() - self.last_updated >= 5:
            to_export = True
            self.last_updated = time.time()

        for obj in self.objects:
            obj.update()

        to_remove = []
        for i in range(len(self.cars)):
            car = self.cars[i]

            chain_mutated = False
            # Calculate chain effect for this car if it's behind other cars
            if i != 0:
                front = self.cars[i - 1]
                distance = car.distance_to(front)
                safe_distance = car.speed * 1.5 + (car.speed ** 2) / (2 * DECELERATION)+5
                if to_export:
                    self.export_distances.append(distance)
                if distance <= safe_distance and car.speed > (distance - safe_distance) / 1.5:
                    car.decelerate()
                    chain_mutated = True
                elif car.speed == car.max_speed or car.speed == 0:
                    # Stop accelerating/decelerating if cannot go further
                    car.accelerating = False
                    car.decelerating = False

            # When a car gets close to an object, allow the object to mutate it
            obj_mutated = False
            if not chain_mutated:  # Chain effect mutation takes precedence over object mutations
                for obj in self.objects:
                    obj_mutated = obj.mutate(car, i)
                    if obj_mutated:
                        break
                if car.manual_decelerate:
                    # A special case, where we manually decelerate cars if requested
                    if car.speed > 0:
                        car.decelerate()
                        obj_mutated = True
                    else:
                        car.manual_decelerate = False

            # Finally, if neither chain nor object mutated this car, allow it to accelerate to its maximum speed
            if not chain_mutated and not obj_mutated and car.speed < car.max_speed:
                car.accelerate()

            car.move()
            if to_export and car.speed >= 5:
                self.export_speeds.append(car.speed)
            if car.position[1] <= 15:
                to_remove.append(car)  # Remove cars that have exceeded the map boundaries
                self.export_finished += 1

        for car in to_remove:
            self.cars.remove(car)
