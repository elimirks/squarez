#!/usr/bin/env python3
import pygame, random

from player import Player
from food import Food

class Board:
	"""Used to organize and handle the gist of the game"""
	def __init__(self, width, height):
		self.score = 0
		self.width = width
		self.height = height
		self._initEntities()
	
	def _initEntities(self):
		self.player = Player(self)
		self.entities = [
			self.player,
			Food.randomFood(self),
			Food.randomFood(self),
		]
	
	def _drawHud(self, display):
		font = pygame.font.Font(None, 24)
		text = font.render("Score: %d" % self.score, 1, (255, 255, 255))
		textpos = text.get_rect()
		display.blit(text, textpos)

		if self.isGameOver():
			self._drawGameOverHud(display)

	def _drawGameOverHud(self, display):
		font = pygame.font.Font(None, 64)
		text = font.render("GAME OVER", 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = display.get_rect().centerx
		textpos.centery = display.get_rect().centery
		display.blit(text, textpos)

		font = pygame.font.Font(None, 24)
		text = font.render("(Press Space to Play Again)", 1, (255, 255, 255))
		textpos = text.get_rect()
		textpos.centerx = display.get_rect().centerx
		textpos.centery = display.get_rect().centery + 32
		display.blit(text, textpos)
	
	def _generateXYTupleFarAwayFromPlayer(self, size):
		quadrant_width = self.width / 2
		quadrant_height = self.height / 2

		if self.player.getRect().x < quadrant_width:
			x = random.randint(quadrant_width + 50, self.width - size)
		else:
			x = random.randint(0, quadrant_width - size - 50)
		
		if self.player.getRect().y < quadrant_height:
			y = random.randint(quadrant_height + 50, self.height - size)
		else:
			y = random.randint(0, quadrant_height - size - 50)

		return (x, y)

	def move(self, elapsedTime):
		for entity in self.entities:
			if entity != self.player:
				if self.player.getRect().colliderect(entity.getRect()):
					entity.hitPlayer(self)

		for entity in self.entities:
			entity.move(self, elapsedTime)

	def draw(self, display):
		self._drawHud(display)
		for entity in self.entities:
			entity.draw(display)

	def isGameOver(self):
		return self.player.isDead()

	def addScore(self, amount):
		self.score += amount

	def getScore(self):
		return self.score
	
	def getHeight(self):
		return self.height
	
	def getWidth(self):
		return self.width
	
	def addBadguy(self, badguy):
		self.entities.append(badguy)

		x, y = self._generateXYTupleFarAwayFromPlayer(badguy.getSize())
		badguy.x, badguy.y = (x, y)

	def shuffleFood(self, food):
		self.entities.insert(0, Food.randomFood(self))
		self.entities.remove(food)
	
	def randomXYTuple(self, size):
		x = random.randint(0, self.width - size)
		y = random.randint(0, self.height - size)
		return (x, y)

