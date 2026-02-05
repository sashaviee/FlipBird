# main.py
import arcade
from settings import *
from views import StartView


def main():
    # Создаем окно
    window = arcade.Window(
        SCREEN_WIDTH, SCREEN_HEIGHT,
        SCREEN_TITLE,
        resizable=False
    )

    # Начинаем со стартового экрана
    start_view = StartView()
    window.show_view(start_view)

    # Запускаем игру
    arcade.run()


if __name__ == "__main__":
    main()