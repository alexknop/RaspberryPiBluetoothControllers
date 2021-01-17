import evdev
from evdev import InputDevice, categorize, ecodes, list_devices

#creates object 'gamepad' to store the data
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    #change name to name of your device
    if device.name == "<DEVICE NAME>":
        gamepad = InputDevice(device.path)


for event in gamepad.read_loop():
    #break if you find a button press
    if event.type == ecodes.EV_KEY:
        #change event code to the code of your button
        if event.code == <button code>:
            print("1")
            break
