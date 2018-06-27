FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

COPY . /dashApp
WORKDIR /dashApp

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["application.py"]