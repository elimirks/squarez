#!/usr/bin/env python3
import pygame, math, sys, random
from pygame.locals import *

from board import Board

if __name__ == '__main__':
	screen_width = 640
	screen_height = 480

	pygame.init()
	display = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Amazing Game')
	fpsClock = pygame.time.Clock()

	board = Board(screen_width, screen_height)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if board.isGameOver() and event.type == KEYUP and event.key == K_SPACE:
				board = Board(screen_width, screen_height)

		board.move(fpsClock.get_time() / 1000)
		display.fill((0, 0, 0))
		board.draw(display)

		pygame.display.update()
		fpsClock.tick(60)

