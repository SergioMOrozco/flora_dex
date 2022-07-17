FROM tensorflow/tensorflow:2.5.0-gpu-jupyter

# https://github.com/NVIDIA/nvidia-docker/issues/1632 workaround for inability to update apt-get
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list

# need libGL.so.1 for cv2
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
