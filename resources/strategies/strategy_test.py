"""
TEST
"""

import math, time

def update(self):
	while True:
		if self.stopped or not self.strategy:
			return
		self.strategy.make_decision(self)
		time.sleep(0.25)

def make_decision(self):
	# Give self access to information about other vehicles.
	if "vehicles" not in self.worldKnowledge.keys():
		self.worldKnowledge['vehicles'] = []
		return

	# If we don't know where we are, stop.
	if self.vehicle.position == (None, None) or self.vehicle.orientation == None:
		self.vehicle.stop()
		return

	# Check positions of other cars.
	for vehicle in self.worldKnowledge['vehicles']:
		if vehicle.owner.ID == self.vehicle.owner.ID or vehicle.position == (None, None):
			continue
		# Get vectors to other cars.
		x1 = self.vehicle.position[0]
		y1 = self.vehicle.position[1]
		x2 = vehicle.position[0]
		y2 = vehicle.position[1]
		dist, angle = self.get_vector_between_points(x1, y1, x2, y2)
		cangle = self.vehicle.orientation
		diff = int(math.fabs(angle - cangle))
		if (diff > 180):
			diff = 360 - diff
		# If our nose is too close to another car, stop and complain.
		if dist < 50 and diff < 90:
			self.vehicle.stop()
			self.vehicle.horn_on()
			self.vehicle.headlights_on()
			time.sleep(1)
			self.vehicle.horn_off()
			self.vehicle.headlights_off()
			return

	# Find waypoint vector info
	(wp_dist, wp_angle) = self.get_vector_to_waypoint()
	if wp_dist is None:
		self.vehicle.stop()
		return

	if (wp_dist < 50): # If we are close enough to our waypoint, set our sights on the next one
		while wp_dist < 100:
			self.set_waypoint_index(self.get_waypoint_index() + 1)
			(wp_dist, wp_angle) = self.get_vector_to_waypoint()

	speed = 8
	car_angle = self.vehicle.get_orientation()
	a = int(math.fabs(car_angle - wp_angle))
	if (a > 180):
		a = 360 - a
		if (car_angle < wp_angle):
			da = -a
		else:
			da = a
	else:
		if (car_angle < wp_angle):
			da = a
		else:
			da = -a
	self.vehicle.set_angle(da // 2)
	self.vehicle.set_speed(speed)
