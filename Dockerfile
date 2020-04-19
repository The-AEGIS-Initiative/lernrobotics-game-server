FROM kevinkqi/python-numpy-alpine:latest

COPY requirements.txt /

#RUN pip install -r /requirements.txt
RUN pip install tornado

COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
