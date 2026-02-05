# physics.py
import arcade
import math
from settings import *


class PhysicsEngine:
    def __init__(self, bird, pipes, ground):
        self.bird = bird
        self.pipes = pipes
        self.ground = ground
        self.gravity = GRAVITY

    def update(self):
        # Применяем гравитацию
        self.bird.change_y += self.gravity

        # Обновляем позицию птицы
        self.bird.center_y += self.bird.change_y
        self.bird.update()

        # Проверка столкновений с землей
        if self.bird.center_y - BIRD_SIZE / 2 <= GROUND_HEIGHT:
            self.bird.center_y = GROUND_HEIGHT + BIRD_SIZE / 2
            self.bird.change_y = 0
            return "ground"

        # Проверка столкновений с потолком
        if self.bird.center_y + BIRD_SIZE / 2 >= SCREEN_HEIGHT:
            self.bird.center_y = SCREEN_HEIGHT - BIRD_SIZE / 2
            self.bird.change_y = 0

        # Проверка столкновений с трубами
        for pipe in self.pipes:
            if (abs(self.bird.center_x - pipe.center_x) < (BIRD_SIZE / 2 + pipe.width / 2) and
                    abs(self.bird.center_y - pipe.center_y) < (BIRD_SIZE / 2 + pipe.height / 2)):
                return "pipe"

        return None

    def jump(self):
        self.bird.change_y = JUMP_STRENGTH

    def get_distance_to_next_pipe(self):
        # Находим ближайшую непройденную трубу
        for pipe in self.pipes:
            if pipe.center_x + pipe.width / 2 > self.bird.center_x and not pipe.passed:
                return pipe.center_x - self.bird.center_x
        return None


class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0
        self.shake_intensity = 0
        self.shake_duration = 0

    def apply(self, x, y):
        return (x - self.offset_x, y - self.offset_y)

    def update(self, target_x, target_y):
        # Плавное слежение
        self.offset_x += (target_x - self.offset_x - self.screen_width * 0.3) * 0.1
        self.offset_y += (target_y - self.offset_y - self.screen_height * 0.5) * 0.1

        # Эффект тряски камеры
        if self.shake_duration > 0:
            self.shake_duration -= 1
            self.offset_x += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.offset_y += random.uniform(-self.shake_intensity, self.shake_intensity)

    def shake(self, intensity=5, duration=10):
        self.shake_intensity = intensity
        self.shake_duration = duration


class ParallaxBackground:
    def __init__(self):
        self.layers = []
        self.clouds = []

    def add_layer(self, color, speed_multiplier, height):
        self.layers.append({
            'color': color,
            'speed': speed_multiplier,
            'height': height,
            'scroll': 0
        })

    def update(self, speed):
        for layer in self.layers:
            layer['scroll'] += speed * layer['speed']

    def draw(self):
        # Рисуем слои фона
        for i, layer in enumerate(self.layers):
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2,
                layer['height'],
                SCREEN_WIDTH,
                layer['height'] * 2,
                layer['color']
            )

            # Рисуем повторяющиеся элементы для параллакса
            for x in range(-100, SCREEN_WIDTH + 100, 100):
                offset_x = (x + layer['scroll']) % (SCREEN_WIDTH + 200) - 100
                if i == 0:  # Дальние горы
                    arcade.draw_triangle_filled(
                        offset_x, layer['height'] + 50,
                                  offset_x - 50, layer['height'],
                                  offset_x + 50, layer['height'],
                        (layer['color'][0] - 20, layer['color'][1] - 20, layer['color'][2] - 20)
                    )