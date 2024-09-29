WIDTH = 800
HEIGHT = 1080
BACKGROUND_COLOR = (255, 255, 255)
ROAD_COLOR = (0, 0, 0)
FPS = 60
SPEED_BG_COLOR = (255, 255, 255)
SPEED_WIDTH = 50
SPEED_HEIGHT = 30
BORDER_MARGIN = 5
TRAFFIC_LIGHT_RED = (204, 50, 50)
TRAFFIC_LIGHT_YELLOW = (231, 180, 22)
TRAFFIC_LIGHT_GREEN = (45, 201, 55)

TARGET_NUM_CARS = 7

AUTO_ADD_CAR_COOLDOWN = 4

# 车子的减速度 (v^2=u^2+2as)，加上了一些微调数值方便展示
def calculate_deceleration(car_lower_speed, car_upper_speed, dec_lower_bound_dist):
    mean_speed = (car_lower_speed + car_upper_speed) / 2
    a = (0 - mean_speed**2) / (2 * dec_lower_bound_dist - 3 - 10)
    a = round(a, 1)
    a = abs(a) * 2
    return a


CIRCLE_RADIUS = 15
CAR_LOWER_SPEED = 20  # 20 m/s
CAR_UPPER_SPEED = 30  # 30 m/s
DEC_LOWER_BOUND_DIST = 40
DECELERATION = calculate_deceleration(CAR_LOWER_SPEED, CAR_UPPER_SPEED, DEC_LOWER_BOUND_DIST)+1  # m/s-2
ACCELERATION = 2.5  # 5 ms-2
START_ACC_DIST = 5  # 5m
TIME_UNTIL_REACCELERATION = 3
PIXEL_PER_METRE = HEIGHT / 600
CAR_ADD_GAP = 2  # 2s
