import os

from controller.agent import Agent
from controller.vision import Vision
from controller.world import World
from controller.display import Display, BLANK_MAP_PATH
from controller.zenwheels.cars import *
from controller.zenwheels.comms import CarCommunicator
import time

msgHeader = "[MAIN]: "


def main(map_image_path, map_info_path, car_parameters, map_parameters):
	print("")
	print("========================================")
	print("         TABLETOP CAR SIMULATOR         ")
	print("========================================")
	print("")

	print(msgHeader + "Begin initialisation.")

	# Initialise display.
	display = Display(map_image_path=map_image_path)

	# Initialise vision server.
	display.connectingToTrackerScreen()
	vision = Vision()

	# Initialise agents and their vehicles.
	agents = []
	vehicles = []
	for car in car_parameters:
		enabled = car[2]
		if not enabled:
			continue
		agentID = MAC_TO_ID[car[1]]
		agent = Agent(agentID, agentType=car[4], vehicleType=car[5], strategyFile=car[3])
		agents.append(agent)
		vehicles.append(agent.vehicle)

	if not agents:
		print(msgHeader + "No cars enabled. Exiting...")
		exit()

	# Load Waypoints
	f = open(map_info_path, 'rb')
	waypoints = eval(f.read())

	# Attempt to capture waypoints if flag waypoint is set
	if len(waypoints) == 1 and frozenset(waypoints[0]) == frozenset([-457, -457, -457]):
		display.blankScreen()
		print(msgHeader + "Capture Waypoints map type detected!")
		time.sleep(1)  # Wait for refresh
		waypoints = []
		for point in vision.get_capture_map_data():
			# There's 3 values in the normal waypoint data, only the first two are used
			point.append(0)
			waypoints.append(point)
		display.background_image_path = BLANK_MAP_PATH
		display.background_image = display.loadBackground()
		# display.generateBackgroundFromWaypoints(waypoints)
		display.show_waypoints = True
		display.DEBUG = True

	# Initialise world.
	world = World(agents, vehicles, waypoints, map_parameters)

	# Display the car loading screen.
	display.connectingToCarsScreen()

	# Initialise car communicator.
	comms = CarCommunicator(vehicles)

	# Event loop.
	print(msgHeader + "Entering main loop.")
	while True:
		# Check if tracker is still connected.
		if not vision.client.isConnected or not display.isDisplaying:
			break
		car_locations = vision.locateCars()
		world.update(car_locations)
		display.update(world.getWorldData())
		for agent in agents:
			agent.update_world_knowledge(world.getWorldData())
	for agent in agents:
		agent.stop()
	print(msgHeader + "Quitting.")