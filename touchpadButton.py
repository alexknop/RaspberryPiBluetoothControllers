import evdev
from evdev import InputDevice, categorize, ecodes, list_devices

#creates object 'gamepad' to store the data
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if device.name == "Wireless Controller Touchpad":
        gamepad = InputDevice(device.path)


for event in gamepad.read_loop():
    #break if you find a touchpad press
    if event.type == ecodes.EV_KEY:
        if event.code == 272:
            print("1")
            break
