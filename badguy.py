#!/usr/bin/env python3
import pygame, random, math
from pygame.locals import *

from entity import Entity

class Badguy(Entity):
	"""Parent bad guy class. When the player hits this entity, it will die!"""
	def __init__(self, color):
		Entity.__init__(self, 0, 0, size=10)
		self.color = color
		self.timeAlive = 0
		self.SPAWN_TIME = 0.5
	
	def move(self, board, elapsedTime):
		self.timeAlive += elapsedTime
		if self.timeAlive > self.SPAWN_TIME:
			self._step(board, elapsedTime)
	
	def draw(self, display):
		"""Handles the spawn animation of the badguy, as well as stepping it.
		
		To control the movement of the badguy, use the _step method.
		"""
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
	"""Simple badguy that keeps a constant velocity"""
	def __init__(self, board):
		Badguy.__init__(self, pygame.Color(255, 255, 255))
		self.xVelocity = self._randomVelocity()
		self.yVelocity = self._randomVelocity()

	def _randomVelocity(self):
		"""Random velocity as an integer - Between 10-50 pixels per second"""
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
		self._lastDirectionChange = 0

	def _randomizeVelocity(self, elapsedTime):
		self._lastDirectionChange += elapsedTime

		# Only change directions at most once per second.
		if self._lastDirectionChange > 1:
			self._lastDirectionChange = 0
			chanceEachSecond = 3
			if random.randint(0, chanceEachSecond) == 0:
				self.xVelocity = self._randomVelocity()
			if random.randint(0, chanceEachSecond) == 0:
				self.yVelocity = self._randomVelocity()
	
	def _step(self, board, elapsedTime):
		self._randomizeVelocity(elapsedTime)
		SimpleBadguy._step(self, board, elapsedTime)


class SmartBadguy(Badguy):
	"""A badguy that will chase the player"""
	def __init__(self, board):
		Badguy.__init__(self, pygame.Color(127, 255, 127))
		self.speed = 30
	
	def _step(self, board, elapsedTime):
		player = board.player

		deltaX = abs(player.x - self.x)
		deltaY = abs(player.y - self.y)
		angle = math.atan(deltaY / deltaX)

		# Determine the quadrant and adjust the angle relative to self
		if player.y < self.y:
			if player.x < self.x: # Second quadrant
				angle = math.pi - angle
			#else: First quadrant, so do nothing.
		else:
			if player.x < self.x: # Third quadrant
				angle = math.pi + angle
			else: # Fourth quadrant
				angle = -angle

		# The Y axis (unlike on a normal cartesian plane) is negative as it goes up.
		self.y -= elapsedTime * self.speed * math.sin(angle)
		self.x += elapsedTime * self.speed * math.cos(angle)

