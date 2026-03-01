import arcade
from pyglet.graphics import Batch
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Flappy bird"

bird_picture = "images/Bird.png"

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Здесь спрайты, физика, как в уроке 7
        #arcade.set_background_color(arcade.color.WHITE)
        self.player = Bird(bird_picture, 0.09)
        #self.player_sprite = arcade.Sprite("images/Bird.png", scale=0.09)
        #self.player_sprite.center_x = SCREEN_WIDTH // 2
        #self.player_sprite.center_y = SCREEN_HEIGHT // 2

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player)
        self.player.moving = True
        self.player.started = True
        self.player.jump_up()

        self.background = arcade.load_texture("images/Background.png")

    def on_draw(self):
        self.clear()
        # Рисуем спрайты, сцену...
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.all_sprites.draw()



    def on_update(self, delta_time):
        # Обновляем физику
        if self.player.started:
            self.player.move(delta_time)
        if self.player.dead:
            self.window.show_view(GameOverView())


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)  # Передаём текущий вид, чтобы вернуться
            self.window.show_view(pause_view)
        if key == arcade.key.SPACE and not self.player.started:
            self.player.started = True
            self.player.moving = True
            self.player.jump_up()

        elif key == arcade.key.SPACE and self.player.started and self.player.moving:
            self.player.jump_up()
        # Другие клавиши для движения...




class Bird(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)
        self.center_x = 0.5 * SCREEN_WIDTH
        self.center_y = 0.6 * SCREEN_HEIGHT
        self.radius = 10
        self.change_y = 0
        self.moving = False
        self.started = False
        self.dead = False

    def move(self, d_time):
        if self.center_y < self.radius + 2:
            self.moving = False
            self.dead = True
        self.change_y -= 40 * d_time
        self.center_y += self.change_y
        if self.change_y > 0:
            self.angle = 3 * self.change_y
        elif self.change_y < 0 and self.change_y > -15:
            self.angle = 3 * self.change_y
        else:
            self.angle = -45

    def jump_up(self):
        if self.moving and not self.dead:
            self.change_y = 13



class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Сохраняем, чтобы вернуться
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(self.game_view)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню
        self.title= arcade.Sprite("images/Title.png", scale=3)
        self.birrd = arcade.Sprite("images/Bird.png", scale=0.09)
        self.title.center_x = SCREEN_WIDTH / 2
        self.title.center_y = SCREEN_HEIGHT - 100
        self.birrd.center_x = SCREEN_WIDTH * 0.5
        self.birrd.center_y = SCREEN_HEIGHT * 0.6
        self.titles = arcade.SpriteList()
        self.titles.append(self.title)
        self.titles.append(self.birrd)
        self.batch = Batch()
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=10, anchor_x="center", batch=self.batch)
        self.background = arcade.load_texture("images/Background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.titles.draw()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView()  # Создаём игровой вид
            self.window.show_view(game_view)  # Переключаем

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.RED_ORANGE  # Фон для меню

        self.batch = Batch()
        self.main_text = arcade.Text("GAME OVER", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.RED, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми ESCAPE, чтобы выйти!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.RED, font_size=15, anchor_x="center", batch=self.batch)
        self.background = arcade.load_texture("images/Background.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()



window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
menu_view = MenuView()
window.show_view(menu_view)
arcade.run()
