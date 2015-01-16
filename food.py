#!/usr/bin/env python3
import pygame, random

from entity import Entity
from badguy import *

class Food(Entity):
	"""The class to handle getting points ( coins, food, etc :] )"""
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
	
	def _initNewBadguy(self, board):
		score = board.getScore()

		if score == 1:
			return SmartBadguy(board)
		elif score % 10 == 0:
			return RandomBadguy(board)
		else:
			return SimpleBadguy(board)

	def hitPlayer(self, board):
		board.addScore(1)
		badguy = self._initNewBadguy(board)
		board.addBadguy(badguy)
		board.shuffleFood(self)


class GrowFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(0, 255, 0), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.grow(2)


class ShrinkFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(0, 0, 255), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.shrink(2)


class FastFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(255, 0, 255), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.increaseSpeed(10)


class SlowFood(Food):
	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(255, 0, 0), self.getRect())

	def hitPlayer(self, board):
		Food.hitPlayer(self, board)
		board.player.decreaseSpeed(10)

