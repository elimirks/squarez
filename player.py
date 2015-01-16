#!/usr/bin/env python3
import pygame
from pygame.locals import *

from entity import Entity

class Player(Entity):
	"""Responsible for the main character square."""
	def __init__(self, board):
		size = 15
		x = board.getWidth()/2 - size/2
		y = board.getHeight()/2 - size/2
		Entity.__init__(self, x, y, size)
		self.speed = 100
		self.dead = False

	def draw(self, display):
		pygame.draw.rect(display, pygame.Color(255, 255, 0), self.getRect())
	
	def move(self, board, elapsedTime):
		if self.isDead():
			return

		self._respondToKeyEvents(elapsedTime)
		self._ensureWithinScreenBounds(board)

	def _respondToKeyEvents(self, elapsedTime):
		if pygame.key.get_pressed()[pygame.K_UP]:
			self.y -= self.speed * elapsedTime
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			self.y += self.speed * elapsedTime
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			self.x -= self.speed * elapsedTime
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.x += self.speed * elapsedTime
	
	def _ensureWithinScreenBounds(self, board):
		self.x = min(max(0, self.x), board.getWidth() - self.size)
		self.y = min(max(0, self.y), board.getHeight() - self.size)
	
	def grow(self, amount):
		self.size += amount
		self.x -= amount/2
		self.y -= amount/2
	
	def shrink(self, amount):
		minimumSize = 5
		if self.size > minimumSize:
			self.size = max(minimumSize, self.size - amount)
			self.x += amount/2
			self.y += amount/2

	def increaseSpeed(self, amount):
		self.speed += amount
	
	def decreaseSpeed(self, amount):
		minimumSpeed = 30
		self.speed = max(self.speed - 10, minimumSpeed)

	def die(self):
		self.dead = True

	def isDead(self):
		return self.dead

