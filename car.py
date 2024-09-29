from constants import *

import numpy as np
import time
import math
import pygame


class Car:
    speed: int
    color: int
    max_speed: int
    prev_updated_time: float
    decelerating: bool
    accelerating: bool
    position: tuple[int, int]

    manual_decelerate: bool = False

    def __init__(self, position: tuple[int, int], speed: int, max_speed: int):
        self.speed = speed
        self.color = np.random.randint(0, 255, 3)  # 车子颜色
        self.prev_updated_time = time.time()  # 上一次更新地理位置等讯息的时间
        self.max_speed = max_speed
        self.decelerating = False  # 不在动吗？
        self.accelerating = False  # 在加速吗？
        self.position = position

    # 根据速度以及上一次self.prev_updated_time，用s=vt公式计算距离，把车子原本的y坐标减去距离就会得到新位置（车子往上走的）
    def move(self) -> None:
        x, y = self.position
        time_diff = time.time() - self.prev_updated_time

        distance_m = self.speed * time_diff
        distance_pixel = distance_m * PIXEL_PER_METRE

        y -= distance_pixel
        self.position = (x, y)  # 重设位置
        self.prev_updated_time = time.time()

    # 与前面那一辆车的距离，根据软件里面的pixel与现实的比例计算
    def distance_to(self, other) -> float:
        front_car_pos = other.position
        this_car_pos = self.position
        return math.dist(front_car_pos, this_car_pos) / PIXEL_PER_METRE

    # 让车子减速
    def decelerate(self) -> None:
        self.decelerating = True
        self.accelerating = False
        time_diff = time.time() - self.prev_updated_time
        speed_decreased = DECELERATION * time_diff
        self.speed = max(0, self.speed - speed_decreased)

    # 让车子加速
    def accelerate(self) -> None:
        self.decelerating = False
        self.accelerating = True
        time_diff = time.time() - self.prev_updated_time
        speed_increased = ACCELERATION * time_diff
        self.speed = min(self.max_speed, self.speed + speed_increased)

    # 把车子显示在屏幕里
    def draw(self, window: pygame.Surface) -> None:
        x, y = self.position
        x = int(x)
        y = int(y)
        pygame.draw.circle(window, self.color, (x, y), CIRCLE_RADIUS)

    # 现实车子的速度
    def draw_speed(self, window: pygame.Surface, font: pygame.font.Font) -> None:
        text = f"Speed: {int(self.speed)} m/s"
        color = self.color

        text_surface = font.render(text, True, color)
        text_rectangle = text_surface.get_rect()

        circle_x, circle_y = self.position
        rect_center_x, rect_center_y = (circle_x - SPEED_WIDTH / 2 - 75, circle_y)
        text_rectangle.center = (rect_center_x, rect_center_y)

        border_left = rect_center_x - text_rectangle.width / 2 - BORDER_MARGIN
        border_top = rect_center_y - text_rectangle.height / 2 - BORDER_MARGIN
        border_width = text_rectangle.width + BORDER_MARGIN * 2
        border_height = text_rectangle.height + BORDER_MARGIN * 2

        border = pygame.Rect(border_left, border_top, border_width, border_height)
        pygame.draw.rect(window, color, border)
        pygame.draw.rect(window, SPEED_BG_COLOR, text_rectangle)
        window.blit(text_surface, text_rectangle)
