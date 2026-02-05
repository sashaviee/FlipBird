# settings.py
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Flappy Bird"

# Цвета
BACKGROUND_COLOR = (100, 149, 237)  # Небесно-голубой
GROUND_COLOR = (101, 67, 33)
TEXT_COLOR = (255, 255, 255)

# Параметры игры
GRAVITY = 0.8
JUMP_STRENGTH = -12
PIPE_SPEED = 5
PIPE_GAP = 200
PIPE_WIDTH = 80
PIPE_SPACING = 300
BIRD_SIZE = 30
GROUND_HEIGHT = 100

# Уровни сложности
LEVELS = {
    1: {"gap": 220, "speed": 5, "pipe_spacing": 320},
    2: {"gap": 200, "speed": 6, "pipe_spacing": 300},
    3: {"gap": 180, "speed": 7, "pipe_spacing": 280},
    4: {"gap": 160, "speed": 8, "pipe_spacing": 260},
    5: {"gap": 140, "speed": 9, "pipe_spacing": 240}
}

# Анимация
BIRD_ANIMATION_SPEED = 0.2
PARTICLE_LIFETIME = 1.0