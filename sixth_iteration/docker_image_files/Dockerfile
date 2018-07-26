FROM sgtwilko/rpi-raspbian-opencv:stretch-latest

Run mkdir -p /usr/scr/ocv_face_detection
RUN mkdir /data

WORKDIR /usr/src/ocv_face_detection

COPY camera.py /usr/src/ocv_face_detection
COPY haarcascade_frontalface_alt.xml  /usr/src/ocv_face_detection

CMD [ "python", "camera.py" ]
