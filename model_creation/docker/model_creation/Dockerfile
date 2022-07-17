FROM jupyter/minimal-notebook

#need root access to run apt-get commands
USER root

# need libGL.so.1 for cv2
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# user configured for jupyter/minimal-notebook
USER jovyan

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
