import arcade
import random
from pyglet.graphics import Batch

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Flappy bird"

backsound = arcade.load_sound("sounds/backsound.mp3")
hlop = arcade.load_sound("sounds/hlop.mp3")
lose = arcade.load_sound("sounds/lose.mp3")
scorez = arcade.load_sound("sounds/score.mp3")

bird_picture = "images/Bird.png"

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = Bird(bird_picture, 0.09)
        self.score = 0

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player)
        self.player.moving = True
        self.player.started = True
        self.player.jump_up()

        self.pipe_list = arcade.SpriteList()
        self.new_pipe = Pipe()
        self.new_pipe_pair = PipePair(self.new_pipe)
        self.pipe_list.append(self.new_pipe)
        self.pipe_list.append(self.new_pipe_pair)

        self.background = arcade.load_texture("images/Background.png")
        arcade.play_sound(backsound, volume=0.1, loop=True)



    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pipe_list.draw()
        self.batch.draw()
        self.all_sprites.draw()




    def on_update(self, delta_time):
        self.current_pipe = self.new_pipe
        if self.player.started:
            self.player.move(delta_time)
        if self.player.dead:
            self.window.show_view(GameOverView())
        if self.new_pipe.center_x < SCREEN_WIDTH - 300:
            self.new_pipe = Pipe()
            self.new_pipe_pair = PipePair(self.new_pipe)
            self.pipe_list.append(self.new_pipe)
            self.pipe_list.append(self.new_pipe_pair)
        if self.player.center_x - self.player.radius > self.current_pipe.center_x + 0.5 * self.current_pipe.width + 3:
            self.score += 1
            arcade.play_sound(scorez, volume=0.2)
        if self.player.moving:
            for pipe in self.pipe_list:
                pipe.update(delta_time)
                if pipe.center_x < -30:
                    self.pipe_list.remove(pipe)
            self.hit_list = arcade.check_for_collision_with_list(self.player, self.pipe_list)
            if len(self.hit_list) > 0:
                self.player.moving = False
                arcade.play_sound(lose, volume=1)
                self.player.change_y = 5
        self.batch = Batch()
        self.fonts = arcade.Text(
            f"{self.score}",
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/4*3,
            arcade.color.WHITE,
            bold = True,
            font_size= 50,
            align="center",
            font_name="Comic Sans MS",
            batch=self.batch
        )


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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.player.started:
            self.player.started = True
            self.player.moving = True
            self.player.jump_up()
        elif button == arcade.MOUSE_BUTTON_LEFT and self.player.started and self.player.moving:
            self.player.jump_up()


class Pipe(arcade.Sprite):
    def __init__(self):
        super().__init__("data/Pipe.png", 0.336)
        self.center_x = SCREEN_WIDTH + 80
        self.center_y = random.randint(100, 550) - 642
        self.change_x = -250
        self.gap = 50
        self.pair_centre_y = self.center_y + self.gap + 642 * 2

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time


class PipePair(arcade.Sprite):
    def __init__(self, pair):
        super().__init__("data/Pipe.png", 0.336)
        self.center_x = SCREEN_WIDTH + 80
        self.center_y = pair.pair_centre_y
        self.change_x = -250
        self.angle = 180

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time



class Bird(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)
        self.center_x = 0.5 * SCREEN_WIDTH
        self.center_y = 0.6 * SCREEN_HEIGHT
        self.radius = 7
        self.change_y = 0
        self.moving = False
        self.started = False
        self.dead = False

    def move(self, d_time):
        if self.center_y < self.radius + 2 or self.center_y > SCREEN_HEIGHT+80:
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
            arcade.play_sound(hlop, volume=0.3)
            self.change_y = 10




class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Сохраняем, чтобы вернуться
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, font_name="Comic Sans MS", anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20,font_name="Comic Sans MS", anchor_x="center", batch=self.batch)

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
        self.title= arcade.Sprite("images/Title2.png", scale=0.2)
        self.birrd = arcade.Sprite("images/Bird.png", scale=0.09)
        self.title.center_x = SCREEN_WIDTH / 2
        self.title.center_y = SCREEN_HEIGHT - 170
        self.birrd.center_x = SCREEN_WIDTH * 0.5
        self.birrd.center_y = SCREEN_HEIGHT * 0.6
        self.titles = arcade.SpriteList()
        self.titles.append(self.title)
        self.titles.append(self.birrd)
        self.batch = Batch()
        self.space_text = arcade.Text("Нажми SPACE(LM), чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=10,font_name="Comic Sans MS", anchor_x="center", batch=self.batch)
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
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            game_view = GameView()  # Создаём игровой вид
            self.window.show_view(game_view)  # Переключаем

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.RED_ORANGE  # Фон для меню

        self.batch = Batch()
        self.main_text = arcade.Text("GAME OVER", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40,font_name="Comic Sans MS", anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми ESCAPE, чтобы выйти!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=15,font_name="Comic Sans MS", anchor_x="center", batch=self.batch)
        self.background = arcade.load_texture("images/Background2.png")

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
