FROM python:latest

WORKDIR /app/data_capture/

COPY data_capture/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3","get_data.py"]
