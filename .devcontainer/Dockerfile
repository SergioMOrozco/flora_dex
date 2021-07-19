FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update

## execution backed for jupyter
RUN pip install ipykernel

RUN apt-get install git -y

## opencv dependency
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install opencv-python
RUN pip install matplotlib
RUN pip install distributed
RUN pip install pandas 

RUN pip install pyinaturalist 
RUN pip install scipy
RUN pip install scikit-learn
