FROM python:latest

WORKDIR /app/data_cleaning/

COPY data_cleaning/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# need libGL.so.1 for cv2
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python3","data_cleaning.py"]
