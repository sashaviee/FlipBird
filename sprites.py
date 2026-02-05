# sprites.py
import arcade
import random
import math
from settings import *


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = SCREEN_WIDTH // 4
        self.center_y = SCREEN_HEIGHT // 2
        self.width = BIRD_SIZE
        self.height = BIRD_SIZE
        self.color = (255, 255, 0)  # Желтый
        self.change_y = 0
        self.angle = 0
        self.alive = True
        self.wing_angle = 0
        self.wing_direction = 1

    def update(self):
        # Анимация крыльев
        self.wing_angle += self.wing_direction * 5
        if abs(self.wing_angle) > 20:
            self.wing_direction *= -1

        # Поворот птицы в зависимости от скорости
        self.angle = max(-30, min(30, self.change_y * 3))

    def draw(self):
        # Тело птицы
        arcade.draw_rectangle_filled(
            self.center_x, self.center_y,
            self.width, self.height,
            self.color
        )

        # Крылья
        wing_x = self.center_x - 10
        wing_y = self.center_y
        wing_width = 25
        wing_height = 15

        arcade.draw_rectangle_filled(
            wing_x, wing_y,
            wing_width, wing_height,
            (200, 200, 0),
            self.wing_angle
        )

        # Глаз
        arcade.draw_circle_filled(
            self.center_x + 10,
            self.center_y + 5,
            5, (0, 0, 0)
        )

        # Клюв
        arcade.draw_triangle_filled(
            self.center_x + 15, self.center_y,
            self.center_x + 25, self.center_y + 5,
            self.center_x + 25, self.center_y - 5,
            (255, 165, 0)
        )


class Pipe(arcade.Sprite):
    def __init__(self, x, y, height, is_top=True):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = PIPE_WIDTH
        self.height = height
        self.is_top = is_top
        self.color = (50, 205, 50)  # Зеленый
        self.passed = False

    def draw(self):
        # Основная труба
        arcade.draw_rectangle_filled(
            self.center_x, self.center_y,
            self.width, self.height,
            self.color
        )

        # Шляпка трубы
        cap_y = self.center_y
        if self.is_top:
            cap_y -= self.height / 2 + 20
        else:
            cap_y += self.height / 2 + 20

        arcade.draw_rectangle_filled(
            self.center_x, cap_y,
            self.width + 40, 40,
            (34, 139, 34)  # Темно-зеленый
        )

        # Детали трубы
        detail_color = (60, 179, 113)
        for i in range(3):
            offset = i * 30 - 30
            arcade.draw_rectangle_filled(
                self.center_x, self.center_y + offset,
                               self.width - 20, 10,
                detail_color
            )


class Ground(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.Texture.create_empty("ground", (SCREEN_WIDTH, GROUND_HEIGHT))
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = GROUND_HEIGHT // 2
        self.width = SCREEN_WIDTH
        self.height = GROUND_HEIGHT
        self.scroll_x = 0

    def draw(self):
        # Рисуем землю с текстурой травы
        for x in range(0, SCREEN_WIDTH + 50, 50):
            arcade.draw_rectangle_filled(
                x - self.scroll_x % 50,
                GROUND_HEIGHT // 2,
                50, GROUND_HEIGHT,
                GROUND_COLOR
            )

            # Трава
            arcade.draw_rectangle_filled(
                x - self.scroll_x % 50,
                GROUND_HEIGHT,
                50, 10,
                (34, 139, 34)
            )

            # Детали
            arcade.draw_circle_filled(
                x - self.scroll_x % 50 + 10,
                20, 5, (139, 69, 19)
            )

    def update(self):
        self.scroll_x += PIPE_SPEED


class Cloud:
    def __init__(self):
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
        self.y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 50)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(30, 60)

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = SCREEN_WIDTH + 100
            self.y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 50)

    def draw(self):
        # Рисуем пушистое облако
        arcade.draw_circle_filled(self.x, self.y, self.size, (255, 255, 255, 200))
        arcade.draw_circle_filled(self.x - self.size // 2, self.y, self.size // 1.5, (255, 255, 255, 200))
        arcade.draw_circle_filled(self.x + self.size // 2, self.y, self.size // 1.5, (255, 255, 255, 200))
        arcade.draw_circle_filled(self.x, self.y + self.size // 2, self.size // 1.5, (255, 255, 255, 200))