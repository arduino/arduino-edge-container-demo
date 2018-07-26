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

Let's make a destination directory to save the scripts
```bash
$ cd ~
mkdir python-data
```

One easy way to transfer files (or in this case, scripts)from your pc to the Raspberry Pi is using *scp*
```bash
$ scp ~/Documents/first_iteration/pushbutton.py ~/Documents/first_iteration/pushbutton_event.py pi@<ip_address_raspi>:~/python-data/
```

If scp is not working (Permission denied) you have to change ownership of the destination folder in the raspi (`chown pi python-data`).

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
Furthermore we can stop the container with `docker stop mynodered` and start it again with `docker start mynodered`

It's also possible to modify the flow and nodes through Node-RED's browser-based web interface, connecting to this URL:
`http://<ip_address_raspi>:1880/`

Finally it's also possible to restore the backup of Node-RED's nodes and flows using scp to copy *flows.json* in the folder *node-red-data* created before.
```bash
$ scp ~/Documents/second_iteration/flows.json pi@<ip_address_raspi>:~/node-red-data/

```
The exemple *flows.json* simply reads the value of a GPIO input pin (pin number 8) and prints in the debug tab its value.

### Second Iteration alternative

At the beginning I started using the [official container of Node-RED](https://hub.docker.com/r/nodered/node-red-docker/), instead of the one used in the [Second Iteration](#second-iteration), but I was not able to make it work with GPIO integration.

Finally I succeded. To make it work I used this command:
```bash
docker run -d -p 1880:1880 -v ~/node-red-data:/data --user=root --privileged --name nodered nodered/node-red-docker:0.18.7-rpi-v8

```
It's better to use this container because it's the official one, it's better maintained, and more updated in comparison to the first I used.

I had to run it with `--user=root` because in the [dockerfile](https://github.com/node-red/node-red-docker/blob/master/rpi/Dockerfile) of this container, the developers created the user *node-red* which can not access */dev/mem* (to control the GPIO pins). You can find further information about users [here](https://docs.docker.com/engine/reference/run/#user, "Docker Documentation").

---
# Third Iteration

Our goal in this iteration is to write an Arduino sketch which reads the value of a pushbutton and notifies Node-RED inside the Docker container. The flow in Node-RED has to rework the value recived from the sketch and to send an email to a specified email-address.

For this step there's no need of configuring anything.
You simply have to import and flash the arduino sketch on the Raspberry Pi using the [Arduino Web Editor](https://create.arduino.cc/editor/, "Arduino Web Editor") and to import the flow in Node-RED.

We can upload it using two different ways:
- download locally the sketch *pushbutton_http_post.ino* and import it in the editor (*Arduino Web Editor > Sketchbook > Import*).
- Take the sketch from [here](https://create.arduino.cc/editor/umbobaldi/37776e35-26e8-428b-962f-ba7f4003f3a7/preview) and open it in the web editor.
Now you can upload the code on your Raspberry Pi.

The sketch simply reads the status of the pushbutton (connected to pin 8) and if it's pressed perform an *HTTP POST* using the bash command `curl`. The request is directed to Node-RED's ip and port.

On Node-RED side we have to import the flow located in *third_iteration* folder.
- You can do that as described in the [Second Iteration](#second-iteration), but coping this new flow:
```bash
$ scp ~/Documents/third_iteration/flows.json pi@<ip_address_raspi>:~/node-red-data/

```
- Or you can use a simpler solution: open the *flows.json* file and copy all its content to the clipboard, then use Node-RED import function (*toast menu > import > clipboard*).

Your flow shoud look like this:

<kbd>
  <img src="docs/flow_email.png">
</kbd>

To make it work you simply have to add the properties inside the e-mail node (Add the recipient, your email address and your password).

<kbd>
  <img src="docs/email_node.png">
</kbd>

I had some problems using my gmail account. To use my email I had to disable *less secure apps* [here](https://myaccount.google.com/lesssecureapps).

Now it's time to deploy the flow and to test it!

---
# Fourth Iteration

In this iteration we are going to test and try [OpenCV](https://opencv.org/), which is a computer vision library written in *C/C++* and it supports *Python*.

The goal, in this iteration, is to install OpenCV and simply to take a photograph and save it using this library.
Since it's not an easy task to install it, we can use a *docker container* already built!
I used [this](https://hub.docker.com/r/sgtwilko/rpi-raspbian-opencv/) one, which comes already compiled for Raspberry Pi and Raspbian Stretch.

To install it I used this command:
```bash
$ docker run -it --privileged -v ~/opencv-data:/data --name opencv sgtwilko/rpi-raspbian-opencv:stretch-latest
```
The various options used in this command are already described in [Second Iteration](#second-iteration).
By the way the option `--privileged` let the container access to all the peripherals connected to our Raspberry, even the webcam/Raspberry Pi Cam.
Personally I used a generic logitech one ([this](http://support.logitech.com/en_us/product/quickcam-communicate-stx-product)).

Furthermore we can stop the container with `docker stop opencv` and start it again with `docker start -i opencv`. (`-i` attach container’s STDIN)

Now you should be in the container's bash!
First of all check if OpenCV is installed by running python interpreter:
``` bash
$ python
Python 2.7.13 (default, Nov 24 2017, 17:33:09) 
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
And then try to import OpenCV library:
```
>>> import cv2
>>> 
```
If you don’t get any errors, you can move on to the next part.
To exit the interpreter simply use `exit()`.

The script I wrote simply take a photo from the webcam and save it in `/data/opencv.png`.

You can copy the script to your raspberry using *scp*
```bash
scp ~/Documents/fourth_iteration/test.py pi@<ip_address_raspi>:~/opencv-data/
```
To run the script simply start the docker container (`docker start -i opencv`),
move to the correct directory (`cd data/`), and finally run the script with `python test.py`.

You can open and see the photo if you copy it to your pc:
```bash
scp pi@<ip_address_raspi>:~/opencv-data/opencv.png ~/Documents/
```
___

# Fifth Iteration

In this iteration we are going to do some **Face Detection**!
If you do not have OpenCV installed on your Raspberry Pi just follow the instruction in the [Fourth Iteration](#fourth-iteration).

Basically Face Detection will detect if a photo contains a face and the position of the face.

Before OpenCV                     | After OpenCV
:--------------------------------:|:----------------------------------:
![Before](docs/test.jpg "Before") | ![After](docs/test_ocv.jpg "After")

OpenCV uses a cascade file (an xml file) which contains data to detect objects, in our case it's used for faces. You only have to initialize it in your code.
OpenCV comes with different cascades built in, for detecting several things such as eyes, hands, legs, animals and so on.
In this tutorial we are going to use Haar Cascade Classifier,
It's a machine learning based approach where a cascade function is trained from a lot of positive (images with face) and negative images (images without face). The algorithm is proposed by Paul Viola and Michael Jones.
Further information [here](https://en.wikipedia.org/wiki/Haar-like_feature)

Next step is to copy the cascade file (`haarcascade_frontalface_alt.xml`) to the Raspberry
```bash
scp ~/Documents/fifth_iteration/haarcascade_frontalface_alt.xml pi@<ip_address_raspi>:~/opencv-data/
```
Then you can copy some test images to the Raspberry
```bash
scp ~/Documents/fifth_iteration/test.jpg pi@<ip_address_raspi>:~/opencv-data/
```
The script I wrote simply opens a photo passed as argument, tries to find faces, and saves the image with faces in the same folder.
You can copy it to the Raspberry with:
```bash
scp ~/Documents/fifth_iteration/face_detection.py pi@<ip_address_raspi>:~/opencv-data/
```

Now everything is configured and you can run the script!
First you have to start the docker container with `docker start -i opencv`,
then you can move to the correct directory (`cd data/`), and finally run the script (`python face_detection.py test.jpg`).

You can open and see the photo with faces if you copy it to your pc:
```bash
scp pi@<ip_address_raspi>:~/opencv-data/test_ocv.jpg ~/Documents/
```

---

# Sixth Iteration

In this iteration we are going to put together all the previous iterations.
The Idea:
- An **Arduino sketch** will run every 15 seconds a shell command to start a docker container.
- A Docker Container which contains **OpenCV** will run a python script on startup. This script will take a photo using a webcam, will draw in the photo a rectangle around a face (if there is one) and save the image in a docker shared volume with the name *opencv.png* if at least one face is found. After all that the container will stop.
- In another Docker Container, a flow in **Node-RED**, will watch the shared volume, waiting for changes in the file *opencv.png*. If the file is changed (the photo is overwritten), the flow composes an email (attaching the photo) and sends it.

<kbd>
  <img src="docs/screenshot_email_ocv.png">
</kbd>

### Arduino sketch

Let's start with the arduino code.
For uploading the sketch to the raspberry you can follow [Third Iteration](#third-iteration).
You can either download it from this repo and import it to [Arduino Web Editor](https://create.arduino.cc/editor/,) or use this [link](https://create-intel.arduino.cc/editor/umbobaldi/2de421c6-dcd8-4327-bdf1-6223e638afd5/preview, "Arduino Start Docker OpenCV")

### Docker container OpenCV

The Docker Container OpenCv part is a bit more complex.
Fist of all you have to create a docker volume to share data between the two containers:
``` bash
docker volume create share
```
To check if everything is ok you can check the list of volumes, you shound also see the newly created volume with `docker volume ls`.

As an experiment I created a docker image, to make the procedure simpler, but if you prefer to build the image by yourself you can read [Docker build OpenCV](#docker-build-opencv) part.
If you have Docker already installed on your Raspberry run this command to download [my image](https://hub.docker.com/r/umbobaldi/opencv_face_detection/):

``` bash
    docker run -it --privileged -v share:/data --name face_detection umbobaldi/opencv_face_detection:1.0
```
- With `-it` you can see a short log and check if everything is ok
- `-v share:/data` mounts the docker volume *share* and binds it with */data* folder inside the container.

The image is already configured to run on startup a python script which uses OpenCV.

The script:
- Take a photo from the webcam
- Does some face detection, likewise described in [Fifth Iteration](#fifth-iteration)
- Saves the photo (*opencv.png*) in the data folder, which is connected to the shared volume, if at least one face is found. Otherwise nothing is saved.
When the script finish the execution the docker container is stopped.

### Docker container Node-Red

In the end you can import *flows.json* as described in [Third iteration](#third-iteration).
Open the file and copy all its content to the clipboard, then use Node-RED import function (*toast menu > import > clipboard*).
To make it work you simply have to add the properties inside the e-mail node (add the recipient, your email address and your password).

Here's the result:

<kbd>
  <img src="docs/screenshot_flow_ocv.png">
</kbd>

This flow:
- Waits for changes in the file *opencv.png* located in the shared volume. When there is a change it means the old file is overwritten by a newer file, so it's time to send an e-mail.
- The *delay node* has to filter the input: when the other container overwrites the file the process in not immediate. So the messages have to be limited to one.
- The *function node* composes the e-mail attaching the photo and writing a proper message.
- In the end the e-mail is sent by the *e-mail node*.

#### Docker build OpenCV

I decided to build my own docker image because I wanted to learn how to do it.
You can find all the files I used in `sixth_iteration/docker_image_files`.

To build the image you have to move in the folder where is located the *Dockerfile* with `cd sixth_iteration/docker_image_files` and run the command:
```bash
docker build -t myopencv:<version> .
```
This command will build your image. To check if everything is ok you can list all docker images with `docker images -a`, if your newly created image is listed you can go on and you can run it, the first time with:
``` bash
docker run -it --privileged -v share:/data --name face_detection myopencv:<version>
```
Or, if it's not the first time, with `docker start -i face_detection`.

The image is modeled after [this one](https://hub.docker.com/r/sgtwilko/rpi-raspbian-opencv/) which has already OpenCV installed.
My Dockerfile creates two folders. One for the code and the other one for sharing the photo. Then mooves *camera.py* and *haarcascade_frontalface_alt.xml* inside the newly created folder inside the container (`/usr/scr/ocv_face_detection`). In the end it starts the python script on startup.




