import pygame as pg
import math
import random

count = score = 0

pg.init()
window_size = width, height = (640,480)
screen = pg.display.set_mode(window_size)
screen.fill('white')
pg.display.set_caption('簡單的接球遊戲')

my_icon = pg.image.load('images/NCCU_logo.jpg')
bg_image = pg.image.load('images/NCCU_field.jpg')
pg.display.set_icon(my_icon)

pg.mixer.init()
pg.mixer.music.load('sounds/bg_music.mp3')
pg.mixer.music.play(-1,0.0)
bong = pg.mixer.Sound('sounds/drop.ogg')
kill_it = pg.mixer.Sound('sounds/kill_it.ogg')
multi_kill = pg.mixer.Sound('sounds/multi_kill.ogg')
winner = pg.mixer.Sound('sounds/winner.ogg')

class BallSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/smallball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [random.randint(50, width-50),
        random.randint(50, height-50)]
        self.xStep, self.yStep = (random.randint(-10,10),
        random.randint(-10,10))
    def move(self):
        if pg.sprite.spritecollideany(self, horiz_walls):
            self.yStep = -self.yStep
            self.xStep = random.randint(-10,10)
        if pg.sprite.spritecollideany(self, vert_walls):
            self.xStep = -self.xStep
            self.yStep = random.randint(-10,10)
        self.rect.x += self.xStep
        self.rect.y += self.yStep
    bong.play()

class BlockSprite(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w, h))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        clock = pg.time.Clock()

ball = BallSprite()
WALL_SIZE = 10
top_line = BlockSprite(0, 0, width, WALL_SIZE)
bottom_line = BlockSprite(0, height-WALL_SIZE,width, WALL_SIZE)
left_line = BlockSprite(0, 0, WALL_SIZE, height)
right_line = BlockSprite(width-WALL_SIZE, 0,WALL_SIZE, height)

class MySprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(1,13):
            filename = 'images/run%04d.png' % i
            self.images.append(pg.image.load(filename))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [width//2, height//2]
    def update(self):
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]
    def move(self, direction):
        if direction == 'u' and not pg.sprite.collide_rect(self, top_line):
            self.rect.y -= 10
        if direction == 'd' and not pg.sprite.collide_rect(self, bottom_line):
            self.rect.y += 10
        if direction == 'l' and not pg.sprite.collide_rect(self, left_line):
            self.rect.x -= 10
        if direction == 'r' and not pg.sprite.collide_rect(self, right_line):
            self.rect.x += 10 

horiz_walls = pg.sprite.Group(top_line, bottom_line)
vert_walls = pg.sprite.Group(left_line, right_line)
ball_group = pg.sprite.Group(ball)
sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, ball_group)

my_sprite = MySprite()
sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, my_sprite, ball)

clock = pg.time.Clock()
pg.time.set_timer(pg.USEREVENT, 3000)
pg.time.set_timer(pg.USEREVENT+1, 1000)

font = pg.font.SysFont('ヒラキノ明朝pron',30)
def show_text(x, y, text):
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))

done = pause = False
while not done:
    time_passed = clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            done = True
        if event.type == pg.USEREVENT:
            new_ball = BallSprite()
            ball_group.add(new_ball)
            sprites.add(new_ball)
        if event.type == pg.MOUSEBUTTONDOWN:
            collides = pg.sprite.spritecollide(my_sprite, ball_group, True)
            for collided_ball in collides:
                score += 1
                new_ball = BallSprite()
                ball_group.add(new_ball)
                sprites.add(new_ball)
        if event.type == pg.USEREVENT+1:
            count += 1

    pg.display.update()
    screen.blit(bg_image, [0,0])
    show_text(10,440, f"Score:{score}")
    show_text(520,440, f"Time:{count}")

    while pause:
        for event in pg.event.get():
            if event.type==pg.QUIT or \
            (event.type==pg.KEYUP and event.key==pg.K_ESCAPE):
                done=True
                pause=False
        if event.type==pg.KEYUP and event.key==pg.K_SPACE:
            pause=False
            count = score = 0
            for b in ball_group:
                b.kill()
    pos = pg.mouse.get_pos()
    if pos[0] - my_sprite.rect.centerx > 50:
        my_sprite.move('r')
    if pos[0] - my_sprite.rect.centerx < -50:
        my_sprite.move('l')
    if pos[1] - my_sprite.rect.centery > 50:
        my_sprite.move('d')
    if pos[1] - my_sprite.rect.centery < 50:
        my_sprite.move('u')
    ball_group.update()
    my_sprite.update()
    sprites.draw(screen)
    if score >= 10:
        pause=True
        show_text(150,100,'by 112405112 傳一丁 陳宥諼')
        winner.play()
pg.quit()
