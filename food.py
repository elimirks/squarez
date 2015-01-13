#!/usr/bin/env python3
import pygame, random

from entity import Entity
from badguy import *

class Food(Entity):
	def randomFood(board):
		"""Factory method for creates a new random food type
		If you create new types of food, add them to this list.
		"""
		return random.choice([
			GrowFood(board),
			ShrinkFood(board),
			FastFood(board),
			SlowFood(board),
		])

	def __init__(self, board):
		self.size = 10
		self.x, self.y = board.randomXYTuple(self.size)

	def hitPlayer(self, board):
		board.addScore(1)

		if board.getScore() % 10 == 0:
			badguy = RandomBadguy(board)
		else:
			badguy = SimpleBadguy(board)

		board.addBadguy(badguy)
		board.shuffleFood(self)


class GrowFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(0, 255, 0), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		# No size limit :D
		growBy = 2
		board.player.size += growBy
		board.player.x -= growBy/2
		board.player.y -= growBy/2


class ShrinkFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(0, 0, 255), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		# Limit the minimum size of the player
		if board.player.getSize() > 5:
			shrinkBy = 2
			board.player.size -= shrinkBy
			board.player.x += shrinkBy/2
			board.player.y += shrinkBy/2


class FastFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(255, 0, 255), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.speed += 10


class SlowFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(255, 0, 0), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.speed = max(board.player.speed - 10, 10)

