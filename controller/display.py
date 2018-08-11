import pygame
from pygame.locals import *
import os
import math
#import numpy as np
#import cv2

msgHeader = "[DISPLAY]: "

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 1200

CALIBRATION_IMG_PATH = os.path.join(os.path.dirname(__file__), '..',
									'resources', 'media', 'calibration', 'checkerboard.png')

DEFAULT_MAP_PATH = os.path.join(os.path.dirname(__file__), '..',
								'resources', 'maps', 'autocars_default', 'map_default.png')

BLANK_MAP_PATH = os.path.join(os.path.dirname(__file__), '..',
								'resources', 'media', 'backgrounds', 'map_blank.png')

class Display():
	def __init__(self, map_image_path=None):
		self.DEBUG = False
		self.background_image_path = DEFAULT_MAP_PATH
		if map_image_path:
			self.background_image_path = map_image_path
		pygame.init()
		self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
		self.font = pygame.font.SysFont('Arial', 30)
		self.background_image = self.loadBackground()
		self.calibration_img = self.loadCalibrationImage()
		self.isDisplaying = True
		self.show_waypoints = False
		print(msgHeader + "Initialisation complete.")

	# Load and scale background image.
	def loadBackground(self):
		try:
			background_image = pygame.image.load(self.background_image_path)
			scale_factor = DISPLAY_WIDTH / background_image.get_rect().size[0]
			background_image = pygame.transform.rotozoom(background_image, 0, scale_factor)
			return background_image
		except:
			print(msgHeader + "Could not load map image from path " + self.background_image_path + ". (Fatal)")
			exit()

	# Load and scale calibration image.
	def loadCalibrationImage(self):
		raw_img = pygame.image.load(CALIBRATION_IMG_PATH)
		scale_factor = DISPLAY_WIDTH / raw_img.get_rect().size[0]
		return pygame.transform.rotozoom(raw_img, 0, scale_factor)

	# Create image from raw world data.
	def createImage(self, worldData):
		self.screen.blit(self.background_image, (0, 0))
		if self.DEBUG:
			yOffset = 0
			for vehicle in worldData['vehicles']:
				try:
					pos = vehicle.position
					pos[0] = int(pos[0] * (1600 / 640))
					pos[1] = int(pos[1] * (1200 / 480))
					angle = vehicle.orientation - 90
					pygame.draw.circle(self.screen, (0, 0, 0), pos, 50, 1)
					angleLine = (pos[0] + 200 * math.cos(math.radians(angle)), pos[1] + 200 * math.sin(math.radians(angle)))
					pygame.draw.line(self.screen, (0, 0, 0), pos, angleLine, 5)
					text = self.font.render("Agent " + str(vehicle.owner.ID) + ": " + str(pos) + ", " + str(angle), True,
											(0, 0, 0))
					self.screen.blit(text, (50, yOffset))
					yOffset += 30
					marker = self.font.render(str(vehicle.owner.ID), True, (0, 0, 0))
					self.screen.blit(marker, pos)
				except Exception as e:
					pass
		if (self.show_waypoints or self.DEBUG) and 'waypoints' in worldData:
			for way in worldData['waypoints']:
				x = int(way[0] * 1600 / 640)
				y = int(way[1] * 1200 / 480)
				pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 5, 1)

	def connectingToTrackerScreen(self):
		self.screen.fill((255, 255, 255))
		text = self.font.render("Connecting to the tracker...", True, (0, 0, 0))
		self.screen.blit(text, (DISPLAY_WIDTH - 500, DISPLAY_HEIGHT - 200))
		pygame.display.flip()

	def calibrationScreen(self, corners=None):
		self.screen.blit(self.calibration_img, (0, 0))
		if corners is not None:
			tl = corners[0][0]
			tr = corners[0][1]
			bl = corners[0][2]
			br = corners[0][3]
			pygame.draw.line(self.screen, (255, 0, 0), tl, tr, 5)
			pygame.draw.line(self.screen, (255, 0, 0), tl, bl, 5)
			pygame.draw.line(self.screen, (255, 0, 0), bl, br, 5)
			pygame.draw.line(self.screen, (255, 0, 0), br, tr, 5)

			tl = corners[1][0]
			tr = corners[1][1]
			bl = corners[1][2]
			br = corners[1][3]
			pygame.draw.line(self.screen, (0, 255, 0), tl, tr, 5)
			pygame.draw.line(self.screen, (0, 255, 0), tl, bl, 5)
			pygame.draw.line(self.screen, (0, 255, 0), bl, br, 5)
			pygame.draw.line(self.screen, (0, 255, 0), br, tr, 5)
			text = self.font.render("Calibrated successfully.", True, (0, 0, 0))
		else:
			text = self.font.render("Calibrating camera perspective...", True, (0, 0, 0))
		self.screen.blit(text, (DISPLAY_WIDTH - 500, DISPLAY_HEIGHT - 200))
		pygame.display.flip()

	def blankScreen(self):
		self.screen.fill((255, 255, 255))
		pygame.display.flip()

	# def generateBackgroundFromWaypoints(self, waypoints):
	# 	if len(waypoints) == 0:
	# 		return
	# 	C, R = self.background_image.get_rect().size
	# 	temp = np.full([R, C], 255, np.uint8)
	# 	temp = cv2.cvtColor(temp, cv2.GRAY2BGR)
	# 	for way in waypoints:
	# 		cv2.circle(temp, [way[0], way[1]], 3, (0, 0, 0), -1)
	# 	try:
	# 		self.background_image = pygame.image.frombuffer(temp.tostring(), temp.shape[1::-1], "RGB")
	# 		self.scale_factor = DISPLAY_WIDTH / self.background_image.get_rect().size[0]
	# 		self.background_image = pygame.transform.rotozoom(self.background_image, 0, self.scale_factor)
	# 	except:
	# 		print("Oh no, background image failed to generate!")

	def connectingToCarsScreen(self):
		self.screen.fill((255, 255, 255))
		text = self.font.render("Connecting to cars...", True, (0, 0, 0))
		self.screen.blit(text, (DISPLAY_WIDTH - 500, DISPLAY_HEIGHT - 200))
		pygame.display.flip()

	def identifyingCarsScreen(self, agents):
		self.screen.fill((255, 255, 255))
		cellWidth = 100
		cellHeight = 200
		xOffset = int(DISPLAY_WIDTH / 4)
		top = DISPLAY_HEIGHT - 300
		for agent in agents:
			pygame.draw.rect(self.screen, (0, 0, 0),
							 Rect(xOffset, top, cellWidth, cellHeight), 4)
			id = self.font.render(str(agent.ID), True, (0, 0, 0))
			self.screen.blit(id, (int(cellWidth / 2) + xOffset, top - 50))
			xOffset += cellWidth + 50

		text = self.font.render("Place each car in its cell.", True, (0, 0, 0))
		self.screen.blit(text, (DISPLAY_WIDTH - 500, DISPLAY_HEIGHT - 200))
		pygame.display.flip()

	def handle_input(self):
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				self.isDisplaying = False
				pygame.quit()

	# Update the world display.
	def update(self, worldData):
		self.handle_input()
		self.createImage(worldData)
		pygame.display.flip()
