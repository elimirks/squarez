#!/usr/bin/env python3
import pygame, math, sys, random
from pygame.locals import *

from entity import Entity

class Badguy(Entity):
	"""Parent bad guy class. When the player hits this entity, it will die!"""
	def __init__(self, size, color):
		Entity.__init__(self, 0, 0, size)
		self.color = color
		self.timeAlive = 0
		self.SPAWN_TIME = 0.5
	
	def move(self, board, elapsedTime):
		self.timeAlive += elapsedTime
		if self.timeAlive > self.SPAWN_TIME:
			self._step(board, elapsedTime)
	
	def draw(self, display):
		if self.timeAlive < self.SPAWN_TIME:
			size = (self.timeAlive / self.SPAWN_TIME) * self.size
			deltaSize = self.size - size
			rect = (self.x + deltaSize/2, self.y + deltaSize/2, size, size)
		else:
			rect = self.getRect()

		pygame.draw.rect(display, self.color, rect)
	
	def hitPlayer(self, board):
		board.player.die()

	def _step(self, board, elapsedTime):
		"""Should be used in sub classes instead of the 'move' method"""
		pass


class SimpleBadguy(Badguy):
	def __init__(self, board):
		Badguy.__init__(self, 10, pygame.Color(255, 255, 255))
		self.xVelocity = self._randomVelocity()
		self.yVelocity = self._randomVelocity()

	def _randomVelocity(self):
		return random.choice([-1, 1]) * random.randint(10, 50)
	
	def _bounceOffWalls(self, board, elapsedTime):
		newX = self.x + self.xVelocity * elapsedTime
		if newX > board.getWidth() - self.size or newX < 0:
			self.xVelocity = -self.xVelocity
		
		newY = self.y + self.yVelocity * elapsedTime
		if newY > board.getHeight() - self.size or newY < 0:
			self.yVelocity = -self.yVelocity
	
	def _step(self, board, elapsedTime):
		self._bounceOffWalls(board, elapsedTime)
		self.x += elapsedTime * self.xVelocity
		self.y += elapsedTime * self.yVelocity


class RandomBadguy(SimpleBadguy):
	"""A badguy that will randomly change direction"""
	def __init__(self, board):
		SimpleBadguy.__init__(self, board)
		self.color = pygame.Color(255, 127, 127)

	def _randomizeVelocity(self):
		if random.randint(0, 100) == 0:
			self.xVelocity = self._randomVelocity()
		if random.randint(0, 200) == 0:
			self.yVelocity = self._randomVelocity()
	
	def _step(self, board, elapsedTime):
		self._randomizeVelocity()
		SimpleBadguy._step(self, board, elapsedTime)

