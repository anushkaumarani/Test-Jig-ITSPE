import board
import digitalio
import storage

# Uncomment the line below if you want to simulate the switch as grounded
simulate_switch_grounded = False  # Change to False to simulate switch open

# Use a GPIO pin for the switch. Here, we use GP6.
switch = digitalio.DigitalInOut(board.GP6)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Simulate the switch being grounded
if simulate_switch_grounded:
    switch_state = False  # Simulate grounded (connected to GND)
else:
    switch_state = switch.value  # Use the actual value from the pin

# Debugging prints to check switch value
print("Simulated switch value:", switch_state)

# If the switch pin is connected to ground, CircuitPython can write to the drive
storage.remount("/", readonly=switch_state)

# Confirm remount status
print("Filesystem is writable" if not switch_state else "Filesystem is read-only")
