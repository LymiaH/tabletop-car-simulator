
"""
SPAZOUT

Very simple demo strategy.
"""

if self.vehicle.position == (None, None):
    self.vehicle.stop()
elif self.vehicle.position[0] < 400 or self.vehicle.position[0] > 800:
    self.vehicle.left_signal_on()
    self.vehicle.headlights_on()
    self.vehicle.set_angle(40)
    self.vehicle.set_speed(-30)
else:
    self.vehicle.left_signal_off()
    self.vehicle.headlights_off()
    self.vehicle.set_angle(0)
    self.vehicle.set_speed(10)
