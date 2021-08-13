# use python container image
FROM python:3.7-stretch

LABEL org.opencontainers.image.authors="damianrene@cs.umd.edu"

COPY . /Flask
WORKDIR /Flask

RUN pip3 install -r requirements.txt
EXPOSE 5000
EXPOSE 3306
CMD ["python3", "run.py"]
