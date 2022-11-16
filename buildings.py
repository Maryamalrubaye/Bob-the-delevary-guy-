import pygame as pg

vec = pg.math.Vector2


class House(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h,name):
        self.groups = game.houses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Restaurant(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h,name):
        self.groups = game.restaurants
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
