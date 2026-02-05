# game.py
import arcade
import random
from settings import *
from sprites import Bird, Pipe, Ground, Cloud
from particles import ParticleSystem, ExplosionSystem
from physics import PhysicsEngine, Camera, ParallaxBackground
from views import GameOverView, LevelCompleteView


class GameView(arcade.View):
    def __init__(self, level=1, initial_score=0):
        super().__init__()
        self.level = level
        self.score = initial_score
        self.pipes = arcade.SpriteList()
        self.bird = Bird()
        self.ground = Ground()
        self.physics_engine = PhysicsEngine(self.bird, self.pipes, self.ground)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = ParallaxBackground()
        self.particle_system = ParticleSystem()
        self.explosion_system = ExplosionSystem()
        self.clouds = [Cloud() for _ in range(5)]

        # Настройки уровня
        level_settings = LEVELS.get(self.level, LEVELS[1])
        self.pipe_gap = level_settings["gap"]
        self.pipe_speed = level_settings["speed"]
        self.pipe_spacing = level_settings["pipe_spacing"]

        # Игровые переменные
        self.game_over = False
        self.game_started = False
        self.pipes_passed = 0
        self.pipe_timer = 0
        self.distance_traveled = 0
        self.last_pipe_x = SCREEN_WIDTH

        # Звуки
        self.jump_sound = arcade.load_sound(":resources:sounds/jump5.wav")
        self.crash_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.score_sound = arcade.load_sound(":resources:sounds/coin5.wav")

        # Инициализация
        self.init_background()
        self.create_starting_pipes()

    def init_background(self):
        # Создаем параллакс-слои
        self.background.add_layer((135, 206, 235), 0.1, SCREEN_HEIGHT // 4)  # Небо
        self.background.add_layer((176, 224, 230), 0.2, SCREEN_HEIGHT // 3)  # Облачный слой
        self.background.add_layer((70, 130, 180), 0.3, SCREEN_HEIGHT // 2)  # Горы

    def create_starting_pipes(self):
        # Создаем начальные трубы
        for i in range(3):
            x = SCREEN_WIDTH + i * self.pipe_spacing
            self.create_pipe_pair(x)

    def create_pipe_pair(self, x):
        # Создаем пару труб (верхнюю и нижнюю)
        gap_center = random.randint(self.pipe_gap + 100, SCREEN_HEIGHT - GROUND_HEIGHT - self.pipe_gap - 100)

        # Верхняя труба
        top_height = gap_center - self.pipe_gap // 2
        top_pipe = Pipe(x, top_height // 2, top_height, True)
        self.pipes.append(top_pipe)

        # Нижняя труба
        bottom_height = SCREEN_HEIGHT - GROUND_HEIGHT - (gap_center + self.pipe_gap // 2)
        bottom_pipe = Pipe(x, SCREEN_HEIGHT - GROUND_HEIGHT - bottom_height // 2, bottom_height, False)
        self.pipes.append(bottom_pipe)

        self.last_pipe_x = x

    def on_draw(self):
        arcade.start_render()

        # Применяем камеру
        self.camera.apply_to_viewport()

        # Рисуем фон
        self.background.draw()

        # Облака
        for cloud in self.clouds:
            cloud.draw()

        # Трубы
        self.pipes.draw()

        # Птица
        self.bird.draw()

        # Земля
        self.ground.draw()

        # Частицы
        self.particle_system.draw()
        self.explosion_system.draw()

        # Интерфейс
        self.draw_ui()

    def draw_ui(self):
        # Счет
        arcade.draw_text(
            f"Score: {self.score}",
            20, SCREEN_HEIGHT - 40,
            TEXT_COLOR, 24
        )

        # Уровень
        arcade.draw_text(
            f"Level: {self.level}",
            20, SCREEN_HEIGHT - 70,
            TEXT_COLOR, 20
        )

        # Пройденное расстояние
        arcade.draw_text(
            f"Distance: {int(self.distance_traveled)}",
            20, SCREEN_HEIGHT - 100,
            TEXT_COLOR, 20
        )

        # Прогресс уровня
        level_progress = min(self.pipes_passed / 10, 1.0)
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30,
            SCREEN_WIDTH * 0.8 * level_progress, 20,
            (50, 205, 50, 150)
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30,
            SCREEN_WIDTH * 0.8, 20,
            TEXT_COLOR, 2
        )

        if not self.game_started and not self.game_over:
            arcade.draw_text(
                "CLICK TO START!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                TEXT_COLOR, 36,
                anchor_x="center"
            )

        if self.game_over:
            arcade.draw_text(
                "GAME OVER!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.RED, 48,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        if not self.game_started or self.game_over:
            return

        # Обновление физики
        collision = self.physics_engine.update()

        if collision:
            self.handle_collision(collision)

        # Обновление труб
        for pipe in self.pipes:
            pipe.center_x -= self.pipe_speed

            # Проверка прохождения трубы
            if (not pipe.passed and pipe.is_top and
                    pipe.center_x + pipe.width / 2 < self.bird.center_x - BIRD_SIZE / 2):
                pipe.passed = True
                self.score += 1
                self.pipes_passed += 1
                arcade.play_sound(self.score_sound)

                # Эффект при получении очка
                self.particle_system.emit(
                    pipe.center_x,
                    SCREEN_HEIGHT // 2,
                    5,
                    (255, 255, 0)
                )

        # Удаление вышедших за экран труб
        for pipe in self.pipes[:]:
            if pipe.center_x < -pipe.width:
                self.pipes.remove(pipe)

        # Создание новых труб
        self.pipe_timer += 1
        if self.pipe_timer > self.pipe_spacing / self.pipe_speed:
            self.create_pipe_pair(self.last_pipe_x + self.pipe_spacing)
            self.pipe_timer = 0

        # Обновление земли
        self.ground.update()
        self.distance_traveled += self.pipe_speed * delta_time

        # Обновление камеры
        self.camera.update(self.bird.center_x, self.bird.center_y)

        # Обновление фона
        self.background.update(self.pipe_speed * 0.5)

        # Обновление облаков
        for cloud in self.clouds:
            cloud.update()

        # Обновление частиц
        self.particle_system.update()
        self.explosion_system.update()

        # Проверка перехода на следующий уровень
        if self.pipes_passed >= 10:
            self.level_complete()

    def handle_collision(self, collision_type):
        if not self.game_over:
            self.game_over = True
            arcade.play_sound(self.crash_sound)

            # Создаем взрыв
            self.explosion_system.create_explosion(
                self.bird.center_x,
                self.bird.center_y
            )

            # Тряска камеры
            self.camera.shake(10, 20)

    def level_complete(self):
        level_complete_view = LevelCompleteView(self.level, self.score)
        self.window.show_view(level_complete_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.game_started:
            self.game_started = True
            return

        if not self.game_over:
            self.physics_engine.jump()
            arcade.play_sound(self.jump_sound)

            # Эффект при взмахе крыльями
            self.particle_system.emit(
                self.bird.center_x,
                self.bird.center_y - 15,
                3,
                (255, 255, 200)
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and not self.game_over:
            self.physics_engine.jump()
            arcade.play_sound(self.jump_sound)

        elif key == arcade.key.ESCAPE:
            from views import StartView
            start_view = StartView()
            self.window.show_view(start_view)