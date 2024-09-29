from constants import *

import enum
import time

import pygame
from pygame import Rect

from car import Car

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)


class CarMutator:
    def mutate(self, car: Car, index: int) -> bool:
        raise NotImplementedError


class RoadObject(CarMutator):
    y: int

    def __init__(self, y):
        self.y = y

    def draw(self, road, window: pygame.Surface, font: pygame.font.Font) -> None:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError


class TrafficLightStatus(enum.Enum):
    green = "green"
    yellow = "yellow"
    red = "red"


class TrafficLight(RoadObject):
    status: TrafficLightStatus
    time_transition: int  # Time until transitioning to next status
    _last_updated: float

    def __init__(self, y, start_time = 30):
        super().__init__(y)
        self.status = TrafficLightStatus.green
        self.time_transition = start_time
        self._last_updated = time.time()

    def transition(self) -> None:
        if self.status == TrafficLightStatus.green:
            self.status = TrafficLightStatus.red
            self.time_transition = 2
        elif self.status == TrafficLightStatus.red:
            self.status = TrafficLightStatus.green
            self.time_transition = 15


    def update(self) -> None:
        time_elapsed = time.time() - self._last_updated
        self._last_updated = time.time()

        self.time_transition -= time_elapsed
        if self.time_transition <= 0:
            self.transition()

    def mutate(self, car: Car, index: int) -> bool:
        if self.status != TrafficLightStatus.green and car.speed > 0:
            if index == 0:
                car.decelerate()
                return True
        return False

    def draw(self, road, window: pygame.Surface, font: pygame.font.Font):
        rect = Rect(road.spawn_coords[0] - 100, self.y, 200, 100)
        pygame.draw.rect(window, {
            TrafficLightStatus.green: TRAFFIC_LIGHT_GREEN,
            TrafficLightStatus.yellow: TRAFFIC_LIGHT_YELLOW,
            TrafficLightStatus.red: TRAFFIC_LIGHT_RED
        }[self.status], rect)

        text_surface = font.render(str(int(self.time_transition)), True, (255, 255, 255))
        window.blit(text_surface, (road.spawn_coords[0] - (font.size(str(int(self.time_transition)))[0]) / 2, self.y + 5))
