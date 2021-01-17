# BluetoothControllers
For knock-off controllers that can't automatically re-pair with the Raspberry Pi, this is a script that will poll for the controllers and allow a hotkey to allow polling for the other controllers.

# Background
I have a knock-off PS4 bluetooth controller that I can initially pair up with my Raspberry Pi, but once the controller is turned off, it cannot reconnect to the Pi. I noticed after the controller is a remembered device that I can put the controller in pairing mode and then try to connect to it from the Pi's bluetooth menu and the controller would connect. Manually trying to connect from the Raspberry Pi required another controller, so I sought out to automate the "polling" of the controller so that I could just put the controller in pairing mode and it would connect each time. If your controller is like mine and you can put it in pairing mode, go to the bluetooth menu of the Raspberry Pi, and connect to the remembered controller and they will connect, then this script is for you.


## Set-Up
-You can either edit the files first and then copy to your Raspberry Pi or copy the files and edit on your Raspberry Pi.

-You will need to run "chmod +x \<filename\>" on each file in order to make them executable.
	
First, pair your controllers up so that they are connected.

In the Pi, run the command "hcitool con":

Example:

	pi@pi:~ $ hcitool con
	Connections:
	< ACL 05:80:73:7B:82:C0 handle 14 state 1 lm MASTER AUTH ENCRYPT 
    
In my output, one of my controller MACs is 05:80:73:7B:82:C0.
 
 
Go to controllerPoller and enter your MACs into the fields necessary.
**If using just one controller, then you only need the file controllerPoller_1 Controller and can then go to the Cron Job step. If using 2 controllers, you do not need the controllerPoller_1 Controller file and can continue with these instructions**
 
The first while loop is meant to run while there are no controllers connected. I found that when using 1 controller for a 1-player game, constantly polling the other controller was causing a lot of input lag. The second part of this script is meant to only poll for the second controller when a hotkey is pressed.
 
Next, you are going to want to install the evdev module for python (assuming your raspberry Pi already has Python on it):
 
**sudo pip install evdev**
 
 
I followed these tutorials to get a [list of my devices](https://python-evdev.readthedocs.io/en/latest/tutorial.html#listing-accessible-event-devices) and to be able to [grab the code](https://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events) used for my hotkey.
 
 
Example (copied code into a file called "list"):
 
	pi@pi:~/Scripts $ python list
	('/dev/input/event5', 'Wireless Controller', 'b8:27:eb:ec:b3:2b')
	('/dev/input/event4', 'Wireless Controller Motion Sensors', 'b8:27:eb:ec:b3:2b')
	('/dev/input/event3', 'Wireless Controller Touchpad', 'b8:27:eb:ec:b3:2b')
	('/dev/input/event2', 'Wireless Controller', 'b8:27:eb:ec:b3:2b')
	('/dev/input/event1', 'Wireless Controller Motion Sensors', 'b8:27:eb:ec:b3:2b')
	('/dev/input/event0', 'Wireless Controller Touchpad', 'b8:27:eb:ec:b3:2b')

I am using a knock-off PS4 controller, so it has other devices listed for the touchpad and the motion sensors that are separate from the buttons. I used the touchpad button as my hotkey.

**Remember the name used for your device**

Example (copied code into a file called "presses"):

	pi@pi:~/Scripts $ python presses
	device /dev/input/event3, name "Wireless Controller Touchpad", phys "b8:27:eb:ec:b3:2b"
	key event at 1610909451.333601, 330 (BTN_TOUCH), down
	key event at 1610909451.333601, 325 (BTN_TOOL_FINGER), down
	key event at 1610909452.766071, 272 (['BTN_LEFT', 'BTN_MOUSE']), down
	key event at 1610909452.946221, 272 (['BTN_LEFT', 'BTN_MOUSE']), up
	key event at 1610909453.336032, 272 (['BTN_LEFT', 'BTN_MOUSE']), down
When I press the touchpad, code 272 comes up. 

**Remember the code you will use for your hotkey.**

Go to buttonPress.py and fill out the device name and button code.
This python script will listen for the hotkey and return 1 when it is pressed.

Going back to controllerPoller, fill out the full path of the location of your Python script.

When the hotkey is pressed, 1 is returned, and the 2nd half of the controllerPoller script then allows 3 iterations of polling to the 2nd controller. This usually gives a period of 15 seconds to connect to the other controller.

## Cron Job
The most important part is to be constantly running these scripts. You would want to be able to (re)connect a controller at any time while the Raspberry Pi is on. I have used crontab, which can run the controllerPoller script every minute. When no controllers are connected, the script itself runs for 55 seconds (11 polls at about 5 seconds each). When 1 of the 2 controllers is connected, the python script is triggered and runs forever, but there is logic in the controllerPoller script to kill the previous python script the next time controllerPoller runs. This prevents the python processes from stacking up and draining the resources of your Pi.

Enter **crontab -e** on your Pi. You may have to select a default editor.

On a new line, enter 5 stars with a space between each star and then your full path to your controllerPoller script

Example:
	
	* * * * * /home/pi/Scripts/controllerPoller

Save the cron job file and you are good to go!
