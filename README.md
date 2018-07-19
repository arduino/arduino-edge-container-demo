# First Iteration

In this tutorial I'll be using [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/ "Download Raspbian"), which is the newest version of Raspbian at the current time, installed on Raspberry Pi 3b+. I choose the Lite version because I don't need the GUI.
It's easier to work on it if you have SSH enabled. To achieve that goal you have to create an empty file (and without extension) named **SSH** and put it in the *boot* partition of the microSD card.

During the first powerup I connected the raspberry pi to my pc using an ethernet cable. I configured my laptop to share the internet connection through the ethernet interface.
In my opinion it was easier to work this way because it's more simple to obtain the ip address of the raspberry. However it's also possible to connect to the internet using wi-fi, but you have to use display and keyboard.

If you know the Raspberry's IP, it's possible to control it (in a bash window) using SSH with the command:
``` bash
$ ssh pi@<ip_address_raspi>
```
The default log-in informations are: user: `pi`, password `raspberry`.

First of all it's mandatory to check if the GPIO libraries for Python are already installed/updated.
``` bash
$ sudo apt-get update
$ sudo apt-get install python-rpi.gpio python3-rpi.gpio
```

Then I wrote two scripts in Python to check the status of a pushbutton (connected to pin 8) and to write a message on the terminal (*pushbutton.py* and *pushbutton_event.py*).
The second script uses the events related to GPIO pins to call a function which prints the button status on the terminal.
This is a more complex way, but the most efficient one.

One easy way to transfer files (or in this case, scripts) to the Raspberry Pi is using *scp*
```bash
$ scp ~/Documents/first_iteration/pushbutton.py pi@<ip_address_raspi>
$ scp ~/Documents/first_iteration/pushbutton_event.py pi@<ip_address_raspi>
```

For all the connection I used this scheme:
![pin raspberry](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Layout-Model-B-Plus-rotated-2700x900.png "Pin Raspberry")
If you want further information on the GPIO pins you can read something useful [here](https://www.raspberrypi.org/documentation/usage/gpio/, "GPIO documentation")

To run the scripts simply run this command:
```bash
$ python3 ~/Documents/first_iteration/pushbutton.py
```
or
```bash
$ python3 ~/Documents/first_iteration/pushbutton_event.py
```

---
# Second Iteration

After installing Raspbian and testing the GPIO pins using Python and a pushbutton, let's add a bit of complexity. Let's add Docker!

Docker will be automatically installed with the Arduino Connector.

If you don't want to use `sudo` when using `docker` you have to create a group *docker* and add your user to the latter:
```bash
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```

For our project we need [Node-RED](https://nodered.org/) which is a flow-based developement tool for wiring together hardware devices, APIs and online services as part of the Internet of Things.

We can use this [Node-RED Docker container](https://hub.docker.com/r/nieleyde/rpi-nodered-gpio/) which is already configured for
 GPIO use.
To install and run the container you can use the following command:

```bash
$ docker run -d -p 1880:1880 -v ~/node-red-data:/data --privileged --name mynodered nieleyde/rpi-nodered-gpio:latest
```
- `run -d nieleyde/rpi-nodered-gpio:latest` This command will download the container from DockerHub (if it's not already been downloaded) and run it in background
- `-p 1880:1880` This option exposes 1880 port outside the container
- `-v ~/node-red-data:/data` This option mounts the host’s *~/node-red-data* directory as the user configuration directory inside the container. It's useful to backup *flows.json* file. This file contains the configuration of all flows created in Node-RED browser editor.
- `--privileged` This option allows the container to access to all devices, in particular to Raspberry's GPIO pins
- `-- name mynodered` This option gives a human readable name to the container

Now we can check the status of the container with `docker ps`, it should be *up*. 
Furthermore we can stop the container with `docker stop mynodered` and start it with `docker start mynodered`

It's also possible to modify the flow and nodes through Node-RED's browser-based web interface, connecting to this URL:
`http://<ip_address_raspi>:1880/`

Finally it's also possible to restore the backup of Node-RED's nodes and flows using scp to copy *flows.json* in the folder *node-red-data* created before.
```bash
$ scp ~/Documents/second_iteration/flows.json pi@<ip_address_raspi>:~/node-red-data/

```
The exemple *flows.json* simply reads the value of a GPIO input pin (pin number 8) and prints in the debug tab its value.

### Second Iteration alternative

At the beginning I started using the [official container of Node-RED](https://hub.docker.com/r/nodered/node-red-docker/), instead of the one used in the second iteration, but I was not able to make it work with GPIO integration.

Finally I succeded. To make it work I used this command:
```bash
docker run -d -p 1880:1880 -v ~/node-red-data:/data --user=root --privileged --name nodered nodered/node-red-docker:0.18.7-rpi-v8

```
It's better to use this container because it's the official one, it's better maintained, and more updated in comparison to the first I used.

I had to run it with `--user=root` because in the [dockerfile](https://github.com/node-red/node-red-docker/blob/master/rpi/Dockerfile) of this container, the developers created the user *node-red* which can not access */dev/mem* (to control the GPIO pins). You can find further information about users [here](https://docs.docker.com/engine/reference/run/#user, "Docker Documentation").


