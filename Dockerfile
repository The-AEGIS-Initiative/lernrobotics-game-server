FROM python:3.8.1-alpine3.11

# Install native libraries, required for numpy
RUN apk add --update curl gcc g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY requirements.txt /

#RUN pip install -r /requirements.txt
RUN pip install tornado numpy

COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
