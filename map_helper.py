import time

import pygame as pg


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir):
	hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
	if hits:
		if dir == 'x':
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
			sprite.vel.x = 0
			sprite.hit_rect.centerx = sprite.pos.x
		if dir == 'y':
			if hits[0].rect.centery > sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
			if hits[0].rect.centery < sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
			sprite.vel.y = 0
			sprite.hit_rect.centery = sprite.pos.y


def get_obstacle_cordinations():
	"""get the obstacle cordinates from a file"""
	with open('obsticle_cordinates.txt') as f:
		lines = f.readlines()
	obstacle_cordinations_array = eval(lines[0])
	return obstacle_cordinations_array


if __name__ == "__main__":
	t = time.time()
	print(get_obstacle_cordinations())
	print(time.time() -t)