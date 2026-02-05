# views.py
import arcade
import random
from settings import *
from database import GameDatabase


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = GameDatabase()
        self.high_scores = self.db.get_high_scores(5)
        self.title_y = SCREEN_HEIGHT
        self.clouds = []
        for _ in range(10):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50),
                'speed': random.uniform(0.2, 0.8),
                'size': random.randint(40, 80)
            })

    def on_show(self):
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Фон
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,
            BACKGROUND_COLOR
        )

        # Облака
        for cloud in self.clouds:
            arcade.draw_circle_filled(cloud['x'], cloud['y'], cloud['size'], (255, 255, 255, 180))
            arcade.draw_circle_filled(cloud['x'] - cloud['size'] // 2, cloud['y'], cloud['size'] // 1.5,
                                      (255, 255, 255, 180))
            arcade.draw_circle_filled(cloud['x'] + cloud['size'] // 2, cloud['y'], cloud['size'] // 1.5,
                                      (255, 255, 255, 180))

        # Анимированный заголовок
        arcade.draw_text(
            "FLAPPY BIRD",
            SCREEN_WIDTH // 2,
            self.title_y,
            arcade.color.YELLOW,
            60,
            anchor_x="center",
            font_name="arial"
        )

        # Птица на стартовом экране
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            BIRD_SIZE, BIRD_SIZE,
            (255, 255, 0)
        )

        # Кнопка старта
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            200, 60,
            (50, 205, 50)
        )
        arcade.draw_text(
            "START GAME",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            TEXT_COLOR,
            24,
            anchor_x="center",
            anchor_y="center"
        )

        # Лучшие результаты
        arcade.draw_text(
            "HIGH SCORES:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 1.8,
            TEXT_COLOR,
            28,
            anchor_x="center"
        )

        for i, score in enumerate(self.high_scores):
            arcade.draw_text(
                f"{i + 1}. {score[0]}: {score[1]} (Level {score[2]})",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - i * 40,
                TEXT_COLOR,
                18,
                anchor_x="center"
            )

        # Управление
        arcade.draw_text(
            "Click to jump! Avoid pipes!",
            SCREEN_WIDTH // 2,
            100,
            TEXT_COLOR,
            20,
            anchor_x="center"
        )

    def on_update(self, delta_time):
        # Анимация заголовка
        if self.title_y > SCREEN_HEIGHT - 100:
            self.title_y -= 5

        # Движение облаков
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -100:
                cloud['x'] = SCREEN_WIDTH + 100
                cloud['y'] = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)

    def on_mouse_press(self, x, y, button, modifiers):
        # Проверка нажатия на кнопку старта
        if (SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and
                SCREEN_HEIGHT // 3 - 30 < y < SCREEN_HEIGHT // 3 + 30):
            game_view = GameView()
            self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self, score=0, level=1, player_name="Player"):
        super().__init__()
        self.score = score
        self.level = level
        self.player_name = player_name
        self.db = GameDatabase()
        self.db.save_score(player_name, score, level)
        self.high_scores = self.db.get_high_scores(5)
        self.statistics = self.db.get_statistics()

    def on_show(self):
        arcade.set_background_color((50, 50, 50, 230))

    def on_draw(self):
        arcade.start_render()

        # Полупрозрачный фон
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,
            (0, 0, 0, 200)
        )

        # Заголовок
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.RED,
            60,
            anchor_x="center"
        )

        # Результаты
        arcade.draw_text(
            f"Score: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 200,
            TEXT_COLOR,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Level: {self.level}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 250,
            TEXT_COLOR,
            30,
            anchor_x="center"
        )

        # Кнопки
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2,
            200, 50,
            (50, 205, 50)
        )
        arcade.draw_text(
            "PLAY AGAIN",
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2,
            TEXT_COLOR,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2 + 150,
            SCREEN_HEIGHT // 2,
            200, 50,
            (220, 20, 60)
        )
        arcade.draw_text(
            "MAIN MENU",
            SCREEN_WIDTH // 2 + 150,
            SCREEN_HEIGHT // 2,
            TEXT_COLOR,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        # Статистика
        if self.statistics:
            arcade.draw_text(
                f"Games Played: {self.statistics['games_played']}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 3,
                TEXT_COLOR,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Best Score: {self.statistics['best_score']}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 3 - 40,
                TEXT_COLOR,
                20,
                anchor_x="center"
            )

    def on_mouse_press(self, x, y, button, modifiers):
        # Кнопка "Играть снова"
        if (SCREEN_WIDTH // 2 - 250 < x < SCREEN_WIDTH // 2 - 50 and
                SCREEN_HEIGHT // 2 - 25 < y < SCREEN_HEIGHT // 2 + 25):
            game_view = GameView()
            self.window.show_view(game_view)

        # Кнопка "Главное меню"
        elif (SCREEN_WIDTH // 2 + 50 < x < SCREEN_WIDTH // 2 + 250 and
              SCREEN_HEIGHT // 2 - 25 < y < SCREEN_HEIGHT // 2 + 25):
            start_view = StartView()
            self.window.show_view(start_view)


class LevelCompleteView(arcade.View):
    def __init__(self, current_level, score):
        super().__init__()
        self.current_level = current_level
        self.score = score
        self.next_level = current_level + 1

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            f"LEVEL {self.current_level} COMPLETE!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            arcade.color.GOLD,
            50,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Next Level: {self.next_level}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            TEXT_COLOR,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Current Score: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            TEXT_COLOR,
            30,
            anchor_x="center"
        )

        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            200, 50,
            (50, 205, 50)
        )
        arcade.draw_text(
            "CONTINUE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            TEXT_COLOR,
            24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and
                SCREEN_HEIGHT // 3 - 25 < y < SCREEN_HEIGHT // 3 + 25):
            game_view = GameView(level=self.next_level, initial_score=self.score)
            self.window.show_view(game_view)