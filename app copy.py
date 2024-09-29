import pickle

from constants import *
from interactions import TrafficLight
from road import NaiveRoad, SmartRoad

import pandas as pd
import pygame
import time
import random

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("速度计算模拟程式")
font = pygame.font.Font(None, 36)

roads = [
    NaiveRoad(100, [
        TrafficLight(300, 11),

    ], []),
    SmartRoad(500, [
        TrafficLight(300, 11),
    ], [])
]

stored_data = {"finished": [], "average_speed": [], "average_distance": []}
if __name__ == "__main__":
    clock = pygame.time.Clock()
    pressed = False
    cooldown = 0
    last_exported = time.time()

    while True:
        clock.tick(FPS)
        for road in roads:
            road.populate_with_cars(TARGET_NUM_CARS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # Save the exported data
                dataframe = pd.DataFrame(stored_data)
                with open(str(time.time()) + ".pkl", "wb") as file:
                    pickle.dump(dataframe, file)

                quit()

            if event.type == pygame.KEYDOWN and not pressed and time.time() - cooldown >= 0:
                cooldown = time.time()
                if event.key == pygame.K_LEFT:  # 按下指着左边的箭头，在左边生成车子
                    roads[0].spawn_car()

                if event.key == pygame.K_RIGHT:  # 按下指着右边的箭头，在右边生成车子
                    roads[1].spawn_car()

                if event.key == pygame.K_UP:  # 按下指着上边的箭头，在左边的第一辆车会开始减速
                    if len(roads[0].cars) > 0:
                        roads[0].cars[0].manual_decelerate = True

                if event.key == pygame.K_DOWN:
                    if len(roads[1].cars) > 0:
                        roads[1].cars[0].manual_decelerate = True


            # 避免一次性检测到太多次按键（按了一下，就只触发事件一次）
            elif event.type == pygame.KEYUP:
                pressed = False

        # Export if needed
        if time.time() - last_exported >= 5:
            last_exported = time.time()
            a, b, c = roads[0].export()
            stored_data["finished"].append(a)
            stored_data["average_speed"].append(b)
            stored_data["average_distance"].append(c)

        window.fill(BACKGROUND_COLOR)
        for road in roads:
            road.update()
            road.draw(window, font)
        pygame.display.update()
