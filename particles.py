# particles.py
import arcade
import random
import math
from settings import *


class Particle:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.size = random.uniform(2, 5)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.2  # Гравитация
        self.life -= self.decay
        self.size *= 0.98

    def draw(self):
        if self.life > 0:
            alpha = int(255 * self.life)
            arcade.draw_circle_filled(
                self.x, self.y,
                self.size,
                (*self.color[:3], alpha)
            )


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=10, color=(255, 255, 255)):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()


class FeatherParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 200))
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(2, 5)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.size = random.uniform(3, 8)

    def update(self):
        super().update()
        self.angle += self.rotation_speed
        self.vx *= 0.98  # Сопротивление воздуха
        self.vy *= 0.98

    def draw(self):
        if self.life > 0:
            alpha = int(255 * self.life)
            arcade.draw_rectangle_filled(
                self.x, self.y,
                self.size, self.size / 3,
                (*self.color[:3], alpha),
                self.angle
            )


class ExplosionSystem:
    def __init__(self):
        self.particles = []

    def create_explosion(self, x, y):
        # Разные типы частиц для взрыва
        colors = [
            (255, 0, 0),  # Красный
            (255, 165, 0),  # Оранжевый
            (255, 255, 0),  # Желтый
            (255, 140, 0)  # Темно-оранжевый
        ]

        for _ in range(30):
            color = random.choice(colors)
            particle = Particle(x, y, color)
            particle.vx = random.uniform(-10, 10)
            particle.vy = random.uniform(-10, 10)
            particle.size = random.uniform(4, 8)
            particle.decay = random.uniform(0.03, 0.06)
            self.particles.append(particle)

        # Добавляем перья
        for _ in range(10):
            self.particles.append(FeatherParticle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()