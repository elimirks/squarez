#!/usr/bin/env python3
import pygame

class Entity:
	"""Used to set standards to how game entities are designed"""
	def __init__(self, x : int, y : int, size : int):
		self.x = x
		self.y = y
		self.size = size

	def move(self, board, elapsedTime : float):
		"""Used to move the entity based on the elapsedTime (in seconds)"""
		pass

	def getRect(self):
		return pygame.Rect(self.x, self.y, self.size, self.size)

	def getSize(self):
		return self.size

	def draw(self, display):
		"""Draw the entity - Typically as a square"""
		pass
	
	def hitPlayer(self, board):
		"""This method will be invoked on the object if hit by the player"""
		pass

