FROM python:latest

WORKDIR /app/test/

COPY test/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3","test.py"]
