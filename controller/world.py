
msgHeader = "[WORLD]: "


class World():
	def __init__(self, agents, vehicles, waypoints, map_params):
		self.worldData = {'agents': agents, 'vehicles': vehicles, 'waypoints': waypoints, 'map_params': map_params}
		print(msgHeader + "Initialisation complete.")

	# Update the world state.
	def update(self, car_locations):
		for known_vehicle in self.worldData['vehicles']:
			updated = False
			for observed_car in car_locations:
				if observed_car['ID'] == known_vehicle.owner.ID:
					known_vehicle.position = observed_car['position']
					known_vehicle.orientation = observed_car['orientation']
					# If car has no current waypoint, assign it to the nearest one.
					if (known_vehicle.owner.worldKnowledge['waypoint_index'] == None):
						dists = [0] * len(self.worldData['waypoints'])
						if (self.worldData['waypoints'] != []):
							closest_wp = 0
							index = 0
							for wp in self.worldData['waypoints']:
								dx = known_vehicle.position[0] - wp[0]
								dy = known_vehicle.position[1] - wp[1]
								dists[index] = dx * dx + dy * dy
								if (dists[index] < dists[closest_wp]):
									closest_wp = index
									index += 1
							known_vehicle.owner.worldKnowledge['waypoint_index'] = closest_wp
						else:
							print("No Waypoints Loaded")
					updated = True
					break
			if not updated:
				known_vehicle.position = (None, None)
				known_vehicle.orientation = None

		#### QUICK ADDITION FOR OPEN DAY
		from controller.vehicle import Car
		from controller.agent import Agent
		for car in car_locations:
			inWorldData = False
			for vehicle in self.worldData['vehicles']:
				if car['ID'] == vehicle.owner.ID:
					inWorldData = True
			if not inWorldData:
				newVehicle = Car(Agent("0"))
				newVehicle.position = car['position']
				newVehicle.orientation = car['orientation']
				self.worldData['vehicles'].append(newVehicle)

	def getWorldData(self):
		return dict(self.worldData)
