import pygame
import pygame.mixer
import pygame.font
from pygame.locals import *
import math
import itertools
import sys
import thread
import random
from time import sleep

pygame.init()

fullscreen = False

speed = 0.15
interval = 400.0

bord_graphic = pygame.image.load('bord.png')
pipe_graphic = pygame.image.load('pipes.png')
pipe_graphic.set_colorkey((255,0,255))

screen = pygame.display.set_mode((1280,720), fullscreen)
clock = pygame.time.Clock()

class Bord(object):
	
	def __init__(self):
		self.y = 200
		self.vy = -1.0
	
	def flap(self):
		self.vy = -4.0
	
	def pump(self, dt):
		self.vy += 0.01 * dt
		self.y += self.vy

class Obstacles(object):

	def __init__(self):
		self.x = 0
		self.pipes = [360]
		self.since_pipe = 0
	
	def pump(self, dt):
		self.x += speed * dt
		self.since_pipe += speed * dt
		
		if self.since_pipe >= interval:
			
			self.pipes.append(random.randint(100,600))
			self.since_pipe -= interval
		
class Engine(object):
	def __init__(self):
		self.dt = 0
		self.t1 = pygame.time.get_ticks()
		self.t2 = 0
		
	def MainLoop(self):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit()
				else:
					bord.flap()
		
		self.t2 = pygame.time.get_ticks()
		self.dt = self.t2 - self.t1
		self.t1 = self.t2
		
		bord.pump(self.dt)
		obstacles.pump(self.dt)
		
		self.DrawGraphics()
		
		clock.tick(120)
		
		pygame.display.update()

	def DrawGraphics(self):
		
		screen.fill((0,0,0))
		
		bord_rendered = pygame.transform.rotozoom(bord_graphic, -bord.vy*20, 1)
		screen.blit(bord_rendered, (interval - (bord_rendered.get_width() / 2) , bord.y - (bord_rendered.get_height() / 2)))
		
		if len(obstacles.pipes) <= 4:
			for p in range( 0, len(obstacles.pipes) - 1 ):
				screen.blit(pipe_graphic, (1280 + interval - obstacles.x + interval*p, obstacles.pipes[p] - 720) )
		else:
			for p in range( len(obstacles.pipes) - 5 , len(obstacles.pipes) - 1 ):
				screen.blit(pipe_graphic, (1280 + interval - obstacles.x + interval*p , obstacles.pipes[p] - 720) )
			

dt = 0
t1 = pygame.time.get_ticks()
t2 = 0

obstacles = Obstacles()
bord = Bord()
engine = Engine()

while 1:
	engine.MainLoop()